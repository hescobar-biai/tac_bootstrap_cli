# TAC Bootstrap Plugin

Claude Code plugin providing the complete Celes stack for supply chain development.

## Installation

Add to your project's `.claude/settings.json`:

```json
{
  "plugins": ["path/to/tac-bootstrap-plugin"]
}
```

## Skills (33)

### Infrastructure & Cloud
| Skill | Command | Description |
|-------|---------|-------------|
| BigQuery Ops | `/bigquery-ops` | Manage BigQuery datasets, tables, and queries |
| GCP Infra | `/gcp-infra` | Manage GCP resources with Terraform |
| AWS Ops | `/aws-ops` | Manage AWS resources with Terraform |
| Data Pipeline | `/data-pipeline` | Design ETL/ELT pipelines with BigQuery + dbt |

### Data & ML
| Skill | Command | Description |
|-------|---------|-------------|
| dbt Workflow | `/dbt-workflow` | Create dbt models with dual-target support |
| ML Forecast | `/ml-forecast` | Build demand forecasting pipelines |

### Backend Architecture
| Skill | Command | Description |
|-------|---------|-------------|
| FastAPI DDD | `/fastapi-ddd` | Generate vertical slice DDD components |
| CRUD Entity | `/create-crud-entity` | Generate complete CRUD entities |
| Domain Service | `/create-domain-service` | Generate application-layer services |
| Value Object | `/create-value-object` | Generate frozen Pydantic value objects |
| Domain Event | `/create-domain-event` | Generate domain event classes |
| Provider Adapter | `/create-provider-adapter` | Generate LLM provider implementations |
| Strategy Pattern | `/create-strategy-pattern` | Generate Strategy ABC implementations |
| Caching Layer | `/create-caching-layer` | Generate thread-safe LRU cache |
| Middleware | `/create-middleware-decorator` | Generate FastAPI middleware |
| Comparison Analyzer | `/create-comparison-analyzer` | Generate evaluation analyzers |

### Frontend
| Skill | Command | Description |
|-------|---------|-------------|
| React Frontend | `/react-frontend` | Generate React 19 components and pages |
| UI Component | `/scaffold-ui-component` | Scaffold UI components |
| Chart Component | `/scaffold-chart-component` | Scaffold chart components |
| Frontend Page | `/scaffold-frontend-page` | Scaffold frontend pages |

### Development Tools
| Skill | Command | Description |
|-------|---------|-------------|
| PRD Generator | `/generate-prd` | Generate Product Requirements Documents |
| ADR Generator | `/generate-adrs` | Generate Architecture Decision Records |
| TDD Generator | `/generate-tdd` | Generate Technical Design Documents |
| Roadmap Generator | `/generate-roadmap` | Generate implementation roadmaps |
| Task Generator | `/generate-tasks` | Generate tasks from roadmaps |
| Fractal Docs | `/generating-fractal-docs` | Generate fractal documentation |
| Product Issues | `/product-issues` | Classify and template product issues |

### Project Scaffolding
| Skill | Command | Description |
|-------|---------|-------------|
| Scaffold Project | `/scaffold-project` | Full project scaffolding |
| Backend Service | `/scaffold-backend-service` | Scaffold backend services |
| Docker Stack | `/scaffold-docker-stack` | Scaffold Docker Compose stacks |

### Specialized
| Skill | Command | Description |
|-------|---------|-------------|
| Meta Skill | `/meta-skill` | Create new Agent Skills |
| Skill Creator | `/skill-creator` | Guide for creating skills |
| Start Orchestrator | `/start-orchestrator` | Start orchestrator services |

## Agents (12)

| Agent | Model | Specialization |
|-------|-------|---------------|
| build-agent | opus | File implementation specialist |
| data-engineer | opus | dbt, BigQuery, data pipelines |
| docs-scraper | opus | Documentation scraping |
| frontend-engineer | opus | React 19, TanStack Query, MUI X |
| infra-ops | sonnet | GCP/AWS infrastructure, Terraform |
| meta-agent | opus | Generate new agent definitions |
| ml-engineer | opus | Demand forecasting, multi-framework ML |
| planner | opus | Implementation planning |
| playwright-validator | opus | Browser automation validation |
| research-docs-fetcher | opus | Research documentation retrieval |
| scout-report-suggest-fast | haiku | Fast codebase scouting |
| scout-report-suggest | opus | Comprehensive codebase analysis |

## Hooks (3)

| Hook | Type | Description |
|------|------|-------------|
| dangerous_command_blocker.py | Security | Blocks dangerous Bash commands |
| universal_hook_logger.py | Audit | Logs all tool executions |
| context_bundle_builder.py | Context | Tracks file operations for session recovery |
