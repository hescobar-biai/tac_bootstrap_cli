---
name: scaffold-project
description: Orchestrate full project scaffolding across all development phases, delegating to specialized scaffold skills. Use when starting a new project from scratch, setting up a complete application, or working through the AI-assisted development workflow. Triggers on requests like "scaffold a new project", "start a new app", "create a full stack project", "set up a new application", or "scaffold project".
---

# Scaffold Project

Orchestrate full-stack project scaffolding by delegating to specialized skills at each phase. Follows the AI-Assisted Development Workflow.

## Input

Configuration is read from the invoking spec's frontmatter or project context:

| Field | Description | Example |
|-------|-------------|---------|
| `project_name` | Human-readable project name | `"Inventory Tracker"` |
| `plan_dir` | Directory for plan documents | `docs/plan/` |
| `backend_dir` | Root directory for backend code | `backend/` |
| `frontend_dir` | Root directory for frontend code | `frontend/` |
| `phases` | Number of build phases | `11` |

If no spec is provided, ask the user for project details and use sensible defaults.

## Phase Overview

| Phase | What | Skill to Delegate To |
|-------|------|---------------------|
| 0 | PRD (product requirements) | `generate-prd` |
| 1 | ADRs (architecture decisions) | `generate-adrs` |
| 2 | TDD (technical design) | `generate-tdd` |
| 3 | Roadmap (implementation phases) | `generate-roadmap` |
| 4 | Infrastructure (Docker + config) | `scaffold-docker-stack` |
| 5 | Backend core (config + data client) | `scaffold-backend-service` (Steps 1-2) |
| 6 | Backend data (models, queries, services) | `scaffold-backend-service` (Steps 3-4) |
| 7 | Backend API (endpoints + app factory) | `scaffold-backend-service` (Steps 5-6) |
| 8 | Frontend foundation (utils, API client, hooks) | Manual (project-specific) |
| 9 | Frontend components (UI + charts) | `scaffold-ui-component` + `scaffold-chart-component` |
| 10 | Frontend pages (integration) | `scaffold-frontend-page` |

Adjust the number of phases to match the project's actual scope. Not all projects need all phases (e.g., API-only projects skip frontend phases, backend-only projects skip phases 8-10).

## Workflow

### Phases 0-3: Documentation

Generate project documentation before writing code by delegating to specialized skills:

1. **Phase 0 — PRD**: Delegate to **`generate-prd`** — gather requirements, fill PRD template, validate completeness
2. **Phase 1 — ADRs**: Delegate to **`generate-adrs`** — evaluate COMMON-DECISIONS catalog against PRD, generate project-specific ADRs
3. **Phase 2 — TDD**: Delegate to **`generate-tdd`** — fill TDD template from PRD + ADRs + STANDARDS
4. **Phase 3 — Roadmap**: Delegate to **`generate-roadmap`** — assign every TDD file to build phases with gates

### Phase 4: Infrastructure

Delegate to **scaffold-docker-stack** to generate:
- `docker-compose.yml` (services per project ADRs)
- Backend and frontend Dockerfiles
- `.env` configuration

### Phases 5-7: Backend

Delegate to **scaffold-backend-service** following its step workflow:
- **Phase 5**: Config + data client
- **Phase 6**: Models + service layer
- **Phase 7**: API endpoints + app factory registration

### Phase 8: Frontend Foundation

Create project-specific foundation files:
- `<frontend-dir>/lib/utils.ts` — formatting helpers (class merging, formatters, etc.)
- `<frontend-dir>/lib/api.ts` — typed API client functions matching backend endpoints
- `<frontend-dir>/hooks/` — custom hooks per project needs

### Phase 9: Frontend Components

Delegate to specialized skills:
- **scaffold-ui-component** for UI primitives (cards, buttons, tables)
- **scaffold-chart-component** for data visualizations (line, bar, pie charts)

### Phase 10: Frontend Pages

Delegate to **scaffold-frontend-page** to generate page components that integrate:
- Filter state management
- API data fetching with parallel calls
- Summary cards, charts, and tables in standard layout

## Detailed Phase Map

For the complete phase-to-skill mapping with TDD sections and workflow references, see [references/phase-map.md](references/phase-map.md).

## Principles

1. **One phase at a time** — Complete and verify each phase before moving to the next
2. **Gate checks** — Each phase has acceptance criteria; confirm before proceeding
3. **Skills are guides, not generators** — Skills provide patterns; adapt to project context
4. **ADRs for "why", skills for "how"** — Reference ADR numbers for traceability
