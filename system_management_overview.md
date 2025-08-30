# System Management Web Application – Architecture & Decisions

This document captures the core architectural choices and recommendations for building the System Management web application with **Python**, **FastAPI**, and **Postgres**.

---

## 1. App Style
- **Framework:** FastAPI (async-first, strongly typed)
- **ORM:** SQLAlchemy 2.0 (async engine) 
- **Validation/DTOs:** Pydantic v2
- **Database:** PostgreSQL
- **Caching / async jobs:** Redis + Celery (or Dramatiq)  
  - FastAPI `BackgroundTasks` only for very short tasks
- **Auth:** Cookie-based sessions for web + optional JWT for API clients  
  - Password hashing: argon2 (via `passlib`)  
  - CSRF protection for HTMX forms  
  - Cookies: `httponly`, `secure`

---

## 2. Multi-User & Isolation
- **RBAC:** role-based access control (`owner`, `admin`, `member`, `viewer`)
- **Multi-tenancy isolation:** Row-Level Security (RLS) in Postgres  
  - Each row has `org_id`  
  - `SET app.current_tenant` per request + Postgres `POLICY` rules
- Alternatives: logical separation by schema or separate DBs

---

## 3. UI Layout
- **Left feed panel:**  
  - Shows short messages (global, department, or system-specific).  
  - Collapsible/hidden via HTMX toggle.  
  - Infinite scroll with `hx-get` + `hx-trigger="revealed"`.  
  - Future: optional websocket/SSE for realtime updates.

- **Top navbar (sticky):**  
  - Always visible.  
  - Will contain: button for **overview of systems**, navigation links.  
  - Right side: user avatar + dropdown menu (profile, settings, change user, logout).

- **Main content (center):**  
  - Grid of **system cards**.  
  - Clicking a card flips it (CSS transform).  
  - Back side shows **system owner avatar** (fun visual).  
  - Cards can show system status, type, and quick actions.  

---

## 4. Services & Packaging
- Docker + docker-compose for local dev
- Celery worker container + beat scheduler
- Email: Postmark/SES (`fastapi-mail`)
- Object storage: S3/MinIO

---

## 5. Observability & Security
- **Logging:** structlog or JSON logs
- **Metrics:** Prometheus (`prometheus-fastapi-instrumentator`)
- **Tracing:** OpenTelemetry
- **Security:** 
  - Strict CORS  
  - Content-Security-Policy (nonce for HTMX)  
  - Rate limit sensitive endpoints  
  - Dependency-injected permission checks  
  - Regular dependency updates (pip-tools or uv)

---

## 6. Data Model (starter)

### Organizations & Departments
- **organizations**  
  - id (PK)  
  - name  
  - created_at  

- **departments**  
  - id (PK)  
  - org_id (FK → organizations)  
  - name  
  - created_at  
  - UNIQUE(org_id, name)

### Users & Memberships
- **users**  
  - id (PK)  
  - org_id (FK → organizations)  
  - email (unique, case-insensitive)  
  - password_hash  
  - first_name  
  - last_name  
  - avatar_url  
  - is_active  
  - created_at  
  - updated_at  
  - last_login_at  
  - email_verified_at  

- **department_memberships**  
  - id (PK)  
  - org_id (FK → organizations)  
  - department_id (FK → departments)  
  - user_id (FK → users)  
  - role ENUM['lead','member','viewer']  
  - created_at  
  - UNIQUE(department_id, user_id)

> **Memberships** represent the many-to-many link between users and departments, with a role attached. A user can belong to multiple departments, and departments can have multiple users.

### Systems
- **system_types** (optional helper table)  
  - id (PK)  
  - org_id (FK → organizations)  
  - name  
  - description  
  - UNIQUE(org_id, name)

- **systems**  
  - id (PK)  
  - org_id (FK → organizations)  
  - department_id (FK → departments, nullable)  
  - name  
  - type_id (FK → system_types, nullable)  
  - status ENUM['active','commissioning','maintenance','decommissioned'] DEFAULT 'active'  
  - owner_user_id (FK → users, nullable)  
  - metadata JSONB (for PLC type, transformer type, etc)  
  - tags TEXT[]  
  - created_at  
  - updated_at  

### Ownership history
- **system_claims**  
  - id (PK)  
  - org_id (FK → organizations)  
  - system_id (FK → systems)  
  - claimed_by_user_id (FK → users)  
  - claimed_at  
  - released_at (nullable)  
  - notes  

### Feed messages
- **feed_messages**  
  - id (PK)  
  - org_id (FK → organizations)  
  - author_user_id (FK → users)  
  - department_id (FK → departments, nullable)  
  - system_id (FK → systems, nullable)  
  - body TEXT  
  - created_at  
  - edited_at (nullable)  
  - deleted_at (nullable)

### Events (audit log)
- **events**  
  - id (PK)  
  - org_id (FK → organizations)  
  - actor_user_id (FK → users)  
  - action TEXT  
  - target_type TEXT  
  - target_id UUID  
  - data JSONB  
  - created_at  

### Secret references
- **credential_refs**  
  - id (PK)  
  - org_id (FK → organizations)  
  - system_id (FK → systems)  
  - provider ENUM['vault','aws','gcp','azure','other']  
  - ref_path TEXT (reference to external secret manager, not the secret itself)  
  - purpose TEXT  
  - created_at  

---

## 7. Timestamps
- **created_at** → when the row was first inserted (immutable).  
- **updated_at** → when the row was last modified.  
- **last_login_at** → for users, last login timestamp.  
- Keep `created_at` and `updated_at` on most tables for auditing and sorting.

---

## 8. Project Structure
```text
app/
  main.py
  api/
    routers/
      auth.py
      systems.py
      claims.py
  core/
    config.py
    security.py
    dependencies.py
  db/
    session.py
    models/
      __init__.py
      user.py
      department.py
      system.py
      claim.py
    migrations/  # alembic
  repositories/
    users.py
    systems.py
    claims.py
  services/
    auth.py
    claims.py
  schemas/
    auth.py
    user.py
    system.py
    claim.py
  web/           # Jinja2 templates + HTMX partials + static
    templates/
      base.html
      index.html
      auth/
        login.html
        register.html
      systems/
        list.html
        _row.html
    static/
tests/
  test_claims.py

```

---

## 9. Implementation Notes
- Use **async SQLAlchemy** + **asyncpg** driver.
- Middleware sets `app.current_tenant` **after authentication** for RLS.
- **Cookie session auth** for browsers; use **JWT** only if you need external API clients.
- Postgres **RLS** ensures tenant isolation:
  ```sql
  ALTER TABLE systems ENABLE ROW LEVEL SECURITY;
  CREATE POLICY tenant_isolation ON systems
    USING (org_id = current_setting('app.current_tenant')::uuid);
  ```
- Celery handles long jobs (reports, integrations).
- Store **only references to secrets**, not plaintext credentials (use a secret manager).

---

## 10. Dev Workflow
```bash
# Start services
docker compose up -d db redis

# Install dependencies
uv pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start dev server
uvicorn app.main:app --reload

# Start worker
celery -A app.workers.tasks worker -l info
```

---

## 11. Decisions (recommended)
1. Auth for browser users: **Cookie sessions** ✅  
2. Isolation: **Postgres RLS** ✅  
3. Async jobs: **Celery + Redis** ✅  
4. UI: **FastAPI + Jinja + HTMX + Tailwind** ✅  
5. RBAC: org-level roles + **memberships per department** ✅  
6. Secrets: **pydantic-settings + env vars**, external secret manager ✅  
7. Observability: **Prometheus + JSON logs** ✅  

---

## 12. Next Steps
Generate:
1. Starter project layout (FastAPI, SQLAlchemy async, Alembic)  
2. Initial models/schemas (Users, Orgs, Departments, Memberships, Systems)  
3. Auth routes (register/login/logout, cookie sessions, CSRF)  
4. RLS migrations + middleware  
5. Simple HTMX page for feed + system cards  
6. `docker-compose.yml` and sample `.env`
