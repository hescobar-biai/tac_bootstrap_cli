# Phase-to-Skill Mapping

Derived from `guides/AI-WORKFLOW.md`.

## Complete Phase Map

| Phase | Name | TDD Sections | Skill | Skill Steps | ADRs |
|-------|------|-------------|-------|-------------|------|
| 0 | Planning | — | `generate-prd` | Gather requirements, fill PRD template | — |
| 1 | Architecture | — | `generate-adrs` | Evaluate COMMON-DECISIONS, generate ADRs | — |
| 2 | Technical Design | — | `generate-tdd` | Fill TDD template from PRD + ADRs | — |
| 3 | Roadmap | — | `generate-roadmap` | Assign files to phases with gates | — |
| 4 | Infrastructure | 3-4 | `scaffold-docker-stack` | Copy templates, customize | 001, 002, 009 |
| 5 | Backend Core | 5.1-5.2 | `scaffold-backend-service` | Steps 1-2 (config + client) | 001, 005 |
| 6 | Backend Data | 5.3-5.5 | `scaffold-backend-service` | Steps 3-4 (models + service) | 001, 005 |
| 7 | Backend API | 5.6-5.7 | `scaffold-backend-service` | Steps 5-6 (endpoints + main) | 001, 005 |
| 8 | Frontend Foundation | 6.1-6.3 | Manual | Utils, API client, hooks | 002, 006 |
| 9 | Frontend Components | 6.4-6.9 | `scaffold-ui-component` + `scaffold-chart-component` | Full workflows | 003, 007 |
| 10 | Frontend Pages | 7 | `scaffold-frontend-page` | Steps 1-7 | 002, 006 |

## ADR Coverage

| ADR | Title | Consumed By |
|-----|-------|------------|
| 001 | FastAPI Backend | scaffold-backend-service, scaffold-docker-stack |
| 002 | Next.js App Router | scaffold-frontend-page, scaffold-docker-stack |
| 003 | Custom Tailwind | scaffold-ui-component, scaffold-chart-component |
| 004 | Multi-env UNION ALL | Not mapped (project-specific query pattern) |
| 005 | Singleton Pattern | scaffold-backend-service |
| 006 | React Hooks State | scaffold-frontend-page |
| 007 | Recharts | scaffold-chart-component |
| 008 | No Auth | Not mapped (anti-decision) |
| 009 | PostgreSQL | scaffold-docker-stack |

## AI-WORKFLOW Context per Phase

### Phase 0 (Planning)
- Feed to AI: User requirements or project idea
- Skill: `generate-prd`
- Output: `projects/plan/PRD.md`

### Phase 1 (Architecture)
- Feed to AI: PRD + STANDARDS + COMMON-DECISIONS catalog
- Skill: `generate-adrs`
- Output: `projects/plan/adr/*.md` (project-specific ADRs)

### Phase 2 (Technical Design)
- Feed to AI: PRD + all ADRs + STANDARDS
- Skill: `generate-tdd`
- Output: `projects/plan/TDD.md`

### Phase 3 (Roadmap)
- Feed to AI: Completed TDD
- Skill: `generate-roadmap`
- Output: `projects/plan/ROADMAP.md`

### Phase 4 (Infrastructure)
- Feed to AI: TDD sections 3-4, ROADMAP Phase 1
- Output: docker-compose.yml, Dockerfiles, .env

### Phases 5-7 (Backend)
- Feed to AI: TDD sections 5.1-5.7 (incrementally), STANDARDS section 2
- Output: config.py, client.py, schemas.py, service.py, endpoints.py, main.py

### Phases 8-9 (Frontend Foundation + Components)
- Feed to AI: TDD sections 6.1-6.9, STANDARDS section 3
- Output: utils.ts, api.ts, hooks, UI components, chart components

### Phase 10 (Frontend Pages)
- Feed to AI: TDD section 7, STANDARDS section 3
- Output: page.tsx files with full state management and layout
