```mermaid

erDiagram

    %% Relations
    ORGANIZATIONS ||--o{ DEPARTMENTS : has
    USERS ||--o{ DEPARTMENTS_MEMBERSHIP : has
    DEPARTMENTS ||--o{ DEPARTMENTS_MEMBERSHIP: HAS

    %% Tables
    ORGANIZATIONS {
        UUID id PK
        string name
    }

    DEPARTMENTS {
        UUID id PK
        string name
        UUID organization_id FK
    }

    USERS {
        UUID id PK
        string first_name
        string last_name
        string email
        bool is_active
        UUID organization_id FK
        datetime last_login
        datetime created_at
        datetime email_verified_at
        datetime updated_at
    }

    SYSTEM_TYPES {
        UUID id PK
        string name
        string description
    }

    SYSTEMS {
        UUID id PK
        string name
        UUID int_id FK
        string status
        UUID department_owner_id FK
        UUID user_owner_id FK
        UUID organization_id FK
        string tag
        datetime created_at
        datetime updated_at
    }


    %% Memberships
    DEPARTMENTS_MEMBERSHIP {
        UUID id PK
        UUID user_id FK
        UUID department_id FK
        UUID organization_id FK
        string role
        datetime created_at
    }