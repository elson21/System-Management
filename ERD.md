```mermaid

erDiagram

    %%===============
    %%== Relations ==
    %%===============
    ORGANIZATIONS ||--o{ DEPARTMENTS : has
    ORGANIZATIONS ||--o{ SYSTEMS: has
    USERS ||--o{ DEPARTMENTS_MEMBERSHIP : has
    DEPARTMENTS ||--o{ DEPARTMENTS_MEMBERSHIP: HAS
    SYSTEMS }o--|| SYSTEM_TYPES: includes

    %%================
    %%==== Tables ====
    %%================
    ORGANIZATIONS {
        UUID id PK
        string name
        datetime created_at
    }

    DEPARTMENTS {
        UUID id PK
        string name
        UUID organization_id FK
        datetime created_at
    }

    USERS {
        UUID id PK
        string first_name
        string last_name
        string email
        string password_hash
        UUID organization_id FK
        bool is_active
        string avatar_url
        datetime last_login
        datetime created_at
        datetime updated_at
        datetime email_verified_at
    }

    SYSTEM_TYPES {
        UUID id PK
        string name
        string description
        datetime created_at
    }

    SYSTEMS {
        UUID id PK
        string name
        UUID organization_id FK
        string status
        UUID department_id FK
        UUID user_owner_id FK
        string tag
        datetime created_at
        datetime updated_at
    }

    %%=======================
    %%== Ownership History ==
    %%=======================
    SYSTEM_CLAIMS {
        UUID id PK
        UUID organization_id FK
        UUID system_id FK
        UUID claimed_by_user_id FK
        datetime claimed_at
        datetime released_at
        string notes
    }

    %%=================
    %%== Memberships ==
    %%=================
    DEPARTMENTS_MEMBERSHIP {
        UUID id PK
        UUID user_id FK
        UUID department_id FK
        UUID organization_id FK
        string role
        datetime created_at
    }