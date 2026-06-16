# B2B SaaS Platform Backend

A scalable, multi-tenant B2B SaaS platform backend architecture built using FastAPI and PostgreSQL. This platform implements a **schema-per-tenant** isolation strategy to ensure robust data security and separation.

## Key Features

- **Multi-Tenancy**: Data isolation using PostgreSQL schemas and dynamic `search_path` switching.
- **Secure Authentication**: JWT-based authentication with password hashing (bcrypt).
- **Role-Based Access Control (RBAC)**: Support for roles such as `admin`, `staff`, and `member`.
- **Tenant Onboarding**: Automated schema creation for new tenants upon registration.
- **Entity Management**:
  - **Public Schema**: Tenants, Users, Audit Logs, Integration Status.
  - **Tenant Schemas**: Clients, Workflows, Workflow Steps, Communications.
- **Extensible API**: Built with FastAPI for high performance and standard REST conventions.
- **Validation**: Strict data validation using Pydantic schemas.

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Containerization**: [Docker](https://www.docker.com/)
- **Testing**: [Pytest](https://docs.pytest.org/)

## API Endpoints

### Authentication
- `POST /auth/register`: Register a new user.
- `POST /auth/login`: Login and receive a JWT access token.

### Tenant Management
- `POST /tenants/`: Register and onboard a new tenant (requires authentication).

### Tenant-Specific Entities (Requires `X-Tenant-ID` header)
- `GET/POST /clients/`: Manage clients for the specific tenant.
- `GET/POST /workflows/`: Manage workflows and steps for the specific tenant.

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+

### Installation

1. Clone the repository.
2. Copy `.env.example` to `.env` and configure your `DATABASE_URL`.
3. Start the application using Docker:
   ```bash
   docker-compose up --build
   ```

## Development and Testing

To run tests locally:
```bash
PYTHONPATH=. pytest
```

## Security

- **SQL Injection Prevention**: All dynamic schema switching uses `sqlalchemy.sql.quoted_name` for identifier sanitization.
- **Credential Safety**: No hardcoded passwords; all sensitive data is managed via environment variables.
