---
name: scaffold-docker-stack
description: Scaffold a Docker Compose stack following project conventions. Use when setting up infrastructure, creating Docker files, configuring containers, or initializing the development environment. Triggers on requests like "create docker setup", "scaffold infrastructure", "add docker compose", "setup containers", or "scaffold docker".
---

# Scaffold Docker Stack

Generate a Docker Compose stack following project ADRs and conventions.

## Input

Configuration is read from the invoking spec's frontmatter or project context:

| Field | Description | Example |
|-------|-------------|---------|
| `services` | List of services to scaffold | `[postgres, backend, frontend]` |
| `backend_framework` | Backend framework (from ADRs) | `FastAPI`, `Express`, `Spring Boot` |
| `frontend_framework` | Frontend framework (from ADRs) | `Next.js`, `React SPA`, `Vue` |
| `database` | Database choice (from ADRs) | `PostgreSQL`, `MySQL`, `MongoDB` |
| `ports` | Port mappings per service | `{db: 5432, backend: 8000, frontend: 3000}` |

If no spec is provided, detect services from project ADRs or existing code.

## Architecture

```
Database (per project ADR)
    ↑ healthcheck
Backend (per project ADR)
    ↑ depends_on
Frontend (per project ADR)
```

Shared bridge network, named volumes for persistence, health-gated dependencies.

## Quick Start

Copy templates from this skill's `assets/` directory and customize:

1. `docker-compose.template.yml` -> `docker-compose.yml`
2. `backend.Dockerfile.template` -> `<backend-dir>/Dockerfile`
3. `frontend.Dockerfile.template` -> `<frontend-dir>/Dockerfile`
4. `env.example.template` -> `.env`

## Service Configuration

### Database

- Image: Per project ADR (e.g., `postgres:16-alpine`, `mysql:8`, `mongo:7`)
- Healthcheck: Per database type (e.g., `pg_isready`, `mysqladmin ping`)
- Named volume for data persistence
- Ports: Per project config

### Backend

- Base image: Per framework (e.g., `python:3.12-slim`, `node:20-alpine`)
- Non-root user (uid 1000)
- Depends on database with `condition: service_healthy`
- Ports: Per project config
- Command: Per framework (e.g., `uvicorn app.main:app`, `node server.js`)

### Frontend

- Multi-stage build where applicable
  - Stage 1 (deps): Install dependencies
  - Stage 2 (builder): Build application
  - Stage 3 (runner): Copy build output, run as non-root
- Depends on backend
- Ports: Per project config

## Templates

The template files are in [assets/](assets/). Copy and customize for each project:

- **[docker-compose.template.yml](assets/docker-compose.template.yml)** — Full service stack
- **[backend.Dockerfile.template](assets/backend.Dockerfile.template)** — Backend container
- **[frontend.Dockerfile.template](assets/frontend.Dockerfile.template)** — Frontend multi-stage
- **[env.example.template](assets/env.example.template)** — Environment variables

## Key Patterns

### Health-gated dependencies

```yaml
depends_on:
  database:
    condition: service_healthy
```

### Shared bridge network

All services on a single named bridge network for DNS-based service discovery.

### Non-root users

Both backend and frontend Dockerfiles create and switch to non-root users.

### Environment variable forwarding

Use `${VAR:-default}` syntax in docker-compose for host-to-container env passthrough.

## Checklist

1. `docker-compose.yml` with all services on shared network
2. Database with healthcheck and named volume
3. Backend depends on healthy database
4. Frontend depends on backend
5. Both app Dockerfiles use non-root users
6. Frontend uses multi-stage build where applicable
7. `.env` file with all required variables
