"""
IDK: documentation-templates, mermaid-diagrams, adr-templates, doc-formats
Responsibility: Provides template strings for documentation generation including
                Mermaid diagrams, ADR format, API docs, and architecture descriptions
Invariants: Templates use simple string.format() substitution, all templates are
            static class methods for stateless access
"""

from typing import Dict, List, Optional

# ============================================================================
# DOCUMENTATION TEMPLATES
# ============================================================================


class DocsTemplates:
    """
    IDK: doc-template-provider, mermaid-templates, adr-format, api-doc-format
    Responsibility: Provides pre-built documentation templates for various
                    documentation types (ADR, API, architecture, deployment, contributing)
    Invariants: All templates are stateless class methods, templates use named
                placeholders for string formatting
    """

    @staticmethod
    def adr_template(
        number: int,
        title: str,
        status: str = "Accepted",
        context: str = "",
        decision: str = "",
        consequences: str = "",
        date: str = "",
    ) -> str:
        """
        Generate an Architecture Decision Record (ADR).

        Args:
            number: ADR number
            title: Decision title
            status: Status (Proposed, Accepted, Deprecated, Superseded)
            context: Context and problem statement
            decision: The decision made
            consequences: Consequences of the decision
            date: Date of the decision

        Returns:
            Formatted ADR markdown string
        """
        return f"""# ADR-{number:04d}: {title}

## Status

{status}

## Date

{date}

## Context

{context}

## Decision

{decision}

## Consequences

### Positive

{consequences}

### Negative

- (None identified yet)

### Neutral

- This decision will need to be revisited as the project evolves.

## References

- (Add relevant links, documents, or discussions)
"""

    @staticmethod
    def api_docs_template(
        project_name: str,
        base_url: str = "http://localhost:8000",
        endpoints: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        Generate API documentation template.

        Args:
            project_name: Name of the project
            base_url: API base URL
            endpoints: Optional list of endpoint definitions

        Returns:
            API documentation markdown string
        """
        endpoint_docs = ""
        if endpoints:
            for ep in endpoints:
                method = ep.get("method", "GET")
                path = ep.get("path", "/")
                desc = ep.get("description", "")
                endpoint_docs += f"\n### {method} {path}\n\n{desc}\n"
        else:
            endpoint_docs = """
### GET /api/v1/health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### GET /api/v1/resources

List all resources.

### POST /api/v1/resources

Create a new resource.

### GET /api/v1/resources/{id}

Get a specific resource by ID.

### PUT /api/v1/resources/{id}

Update a specific resource.

### DELETE /api/v1/resources/{id}

Delete a specific resource.
"""

        return f"""# {project_name} API Documentation

## Base URL

```
{base_url}
```

## Authentication

> Configure authentication as needed for your project.

## Endpoints
{endpoint_docs}

## Error Handling

All errors follow this format:

```json
{{
  "detail": "Error message",
  "status_code": 400
}}
```

## Rate Limiting

> Configure rate limiting as needed.

## Versioning

API versioning is handled via URL path prefix (`/api/v1/`).
"""

    @staticmethod
    def architecture_docs_template(
        project_name: str,
        architecture: str = "simple",
        language: str = "python",
        framework: str = "none",
    ) -> str:
        """
        Generate architecture documentation.

        Args:
            project_name: Project name
            architecture: Architecture pattern
            language: Programming language
            framework: Framework used

        Returns:
            Architecture documentation markdown string
        """
        return f"""# {project_name} Architecture

## Overview

This document describes the software architecture of {project_name}.

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | {language} |
| Framework | {framework} |
| Architecture | {architecture} |

## Architecture Pattern: {architecture.title()}

### Directory Structure

```
{project_name}/
├── src/                    # Application source code
│   ├── domain/            # Business logic and entities
│   ├── application/       # Use cases and services
│   ├── infrastructure/    # External integrations
│   └── interfaces/        # API and UI layers
├── tests/                 # Test suites
├── docs/                  # Documentation
├── config.yml             # Project configuration
└── .claude/               # Agentic layer
```

## Design Principles

1. **Separation of Concerns** - Each layer has a specific responsibility
2. **Dependency Inversion** - Dependencies point inward
3. **Single Responsibility** - Each module does one thing well
4. **Open/Closed** - Open for extension, closed for modification

## Data Flow

See the component diagram below for the data flow architecture.

## Security Considerations

- Authentication and authorization at API boundary
- Input validation at all entry points
- Secrets managed via environment variables
- Logging of security-relevant events

## Deployment

See `docs/deployment.md` for deployment instructions.
"""

    @staticmethod
    def component_diagram(
        project_name: str,
        components: Optional[List[str]] = None,
    ) -> str:
        """
        Generate a Mermaid component diagram.

        Args:
            project_name: Project name
            components: Optional list of component names

        Returns:
            Mermaid diagram string
        """
        if components:
            component_nodes = "\n".join(
                f"    {c.replace(' ', '_')}[{c}]" for c in components
            )
        else:
            component_nodes = """    CLI[CLI Interface]
    API[API Layer]
    Service[Application Service]
    Domain[Domain Logic]
    Repo[Repository]
    DB[(Database)]"""

        return f"""```mermaid
graph TB
    subgraph {project_name}
{component_nodes}
    end

    CLI --> API
    API --> Service
    Service --> Domain
    Service --> Repo
    Repo --> DB
```"""

    @staticmethod
    def data_flow_diagram(
        project_name: str,
    ) -> str:
        """
        Generate a Mermaid data flow diagram.

        Args:
            project_name: Project name

        Returns:
            Mermaid diagram string
        """
        return """```mermaid
flowchart LR
    User([User]) --> |Request| API[API Gateway]
    API --> |Validate| Auth[Auth Middleware]
    Auth --> |Authorized| Handler[Request Handler]
    Handler --> |Execute| Service[Application Service]
    Service --> |Query/Command| Repository[Repository]
    Repository --> |CRUD| DB[(Database)]
    DB --> |Result| Repository
    Repository --> |Domain Object| Service
    Service --> |Response DTO| Handler
    Handler --> |Response| API
    API --> |JSON| User
```"""

    @staticmethod
    def architecture_diagram(
        architecture: str = "simple",
    ) -> str:
        """
        Generate a Mermaid architecture diagram based on pattern.

        Args:
            architecture: Architecture pattern name

        Returns:
            Mermaid diagram string
        """
        if architecture == "ddd":
            return """```mermaid
graph TB
    subgraph Interface Layer
        API[REST API]
        CLI[CLI]
    end

    subgraph Application Layer
        UC1[Use Case 1]
        UC2[Use Case 2]
        AppService[Application Service]
    end

    subgraph Domain Layer
        Entity[Entities]
        VO[Value Objects]
        DomainService[Domain Service]
        Event[Domain Events]
    end

    subgraph Infrastructure Layer
        Repo[Repository Implementation]
        External[External Services]
        DB[(Database)]
    end

    API --> UC1
    CLI --> UC2
    UC1 --> AppService
    UC2 --> AppService
    AppService --> Entity
    AppService --> DomainService
    DomainService --> VO
    Entity --> Event
    AppService --> Repo
    Repo --> DB
    AppService --> External
```"""
        elif architecture == "hexagonal":
            return """```mermaid
graph TB
    subgraph Driving Adapters
        REST[REST API]
        CLI[CLI]
        Events[Event Consumer]
    end

    subgraph Application Core
        Port1[Input Port]
        UseCase[Use Case]
        Port2[Output Port]
        Domain[Domain Model]
    end

    subgraph Driven Adapters
        DBAdapter[DB Adapter]
        APIAdapter[API Adapter]
        MsgAdapter[Message Adapter]
    end

    REST --> Port1
    CLI --> Port1
    Events --> Port1
    Port1 --> UseCase
    UseCase --> Domain
    UseCase --> Port2
    Port2 --> DBAdapter
    Port2 --> APIAdapter
    Port2 --> MsgAdapter
```"""
        else:
            return """```mermaid
graph TB
    subgraph Presentation
        UI[User Interface]
    end

    subgraph Application
        Service[Service Layer]
    end

    subgraph Domain
        Model[Domain Model]
    end

    subgraph Data
        DB[(Database)]
    end

    UI --> Service
    Service --> Model
    Service --> DB
```"""

    @staticmethod
    def deployment_guide(
        project_name: str,
        language: str = "python",
    ) -> str:
        """
        Generate deployment documentation.

        Args:
            project_name: Project name
            language: Programming language

        Returns:
            Deployment guide markdown string
        """
        return f"""# {project_name} Deployment Guide

## Prerequisites

- Docker and Docker Compose
- Access to deployment environment
- Environment variables configured

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | Database connection string | Yes | - |
| `SECRET_KEY` | Application secret key | Yes | - |
| `LOG_LEVEL` | Logging level | No | INFO |
| `PORT` | Application port | No | 8000 |

## Local Development

```bash
# Install dependencies
# (use your package manager)

# Set up environment
cp .env.example .env
# Edit .env with your values

# Run development server
# (use your start command)
```

## Docker Deployment

```dockerfile
# Build image
docker build -t {project_name} .

# Run container
docker run -p 8000:8000 --env-file .env {project_name}
```

## Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: {project_name}
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${{DB_PASSWORD}}
    volumes:
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
```

## Health Check

```bash
curl http://localhost:8000/api/v1/health
```

## Monitoring

- Application logs: `docker logs {project_name}`
- Health endpoint: `/api/v1/health`
- Metrics: Configure Prometheus/Grafana as needed
"""

    @staticmethod
    def contributing_guide(
        project_name: str,
    ) -> str:
        """
        Generate contributing documentation.

        Args:
            project_name: Project name

        Returns:
            Contributing guide markdown string
        """
        return f"""# Contributing to {project_name}

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Submit a pull request

## Development Setup

```bash
# Clone the repository
git clone <your-fork-url>
cd {project_name}

# Install dependencies
# (use your package manager)

# Run tests
# (use your test command)
```

## Code Standards

- Follow the existing code style
- Write tests for new features
- Update documentation as needed
- Keep commits focused and descriptive

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Ensure all tests pass
3. Update the documentation
4. The PR will be merged once reviewed and approved

## Reporting Issues

- Use GitHub Issues for bug reports and feature requests
- Include reproduction steps for bugs
- Provide system information when relevant

## Code of Conduct

- Be respectful and constructive
- Focus on the code, not the person
- Welcome newcomers and help them learn
"""
