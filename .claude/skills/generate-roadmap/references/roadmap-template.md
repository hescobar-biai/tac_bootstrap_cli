# Roadmap Template

> Source: `projects/plan/documentation-framework/templates/ROADMAP.template.md`

Use this template as the starting point. Replace all `[FILL IN]` markers with project-specific content. Every file from TDD Section 2 must appear in exactly one phase.

---

# Implementation Roadmap — [PROJECT NAME]

> **Version**: 1.0
> **Last Updated**: [YYYY-MM-DD]
> **Audience**: Development Team, Project Manager
> **Purpose**: Execution order with dependencies

---

## Phase 0: Documentation (DO FIRST)

```
[ ] PRD.md            -> Feature map, requirements, personas
[ ] ADR/*.md          -> Architecture decision records
[ ] TDD.md            -> Full technical blueprint
[ ] STANDARDS.md      -> Code conventions and patterns
[ ] ROADMAP.md        -> This file
```

> Never skip Phase 0. Documentation drives every subsequent phase.
> Copy `shared/STANDARDS.md` and shared ADRs from the documentation framework.
> Fill in `templates/PRD.template.md` first, then generate project-specific ADRs, then TDD.

## Phase 1: Infrastructure & Config

```
Step  File                              Depends On  Description
1.1   docker-compose.yml                -           [FILL IN]-service stack definition
1.2   .env + .env.example               -           All environment variables
1.3   backend/Dockerfile                -           Python 3.12 slim image
1.4   frontend/Dockerfile               -           Node 20 alpine multi-stage
1.5   [FILL IN: setup/init scripts]     -           [FILL IN: Description]
```

**Gate**: `docker compose build` succeeds

## Phase 2: Backend Core Layer

```
Step  File                                      Depends On  Description
2.1   backend/requirements.txt                  -           All Python deps
2.2   backend/app/__init__.py                   -           Package init
2.3   backend/app/core/__init__.py              -           Package init
2.4   backend/app/core/config.py                2.1         Pydantic Settings
2.5   backend/app/core/[FILL IN]_client.py      2.4         [FILL IN: Data source client]
2.6   backend/app/services/__init__.py          -           Package init
2.7   backend/app/services/[FILL IN].py         -           [FILL IN: Utility functions]
```

**Gate**: `python -c "from app.core.config import settings; print(settings.APP_NAME)"` works

## Phase 3: Backend Data Layer

```
Step  File                                      Depends On  Description
3.1   backend/app/models/__init__.py            -           Package init
3.2   backend/app/models/schemas.py             -           [FILL IN: N] Pydantic response models
3.3   backend/app/services/[FILL IN].py         -           [FILL IN: Queries/ORM layer]
3.4   backend/app/services/[FILL IN]_service.py 2.5, 3.2    [FILL IN: Domain service]
```

**Gate**: Unit tests for query builders and utilities pass

## Phase 4: Backend API Layer

```
Step  File                                              Depends On  Description
4.1   backend/app/api/__init__.py                       -           Package init
4.2   backend/app/api/v1/__init__.py                    -           Package init
4.3   backend/app/api/v1/endpoints/__init__.py          -           Package init
4.4   backend/app/api/v1/endpoints/health.py            2.5         Health + root endpoints
4.5   backend/app/api/v1/endpoints/[FILL IN].py         3.4, 3.2    [FILL IN: Domain endpoints]
4.6   backend/app/main.py                               4.4, 4.5    App factory (CORS, routers)
4.7   backend/run.py                                    4.6         Dev server entry point
```

**Gate**: `curl localhost:8000/api/v1/health` returns healthy. Swagger at `/docs` shows all endpoints.

## Phase 5: Frontend Foundation

```
Step  File                          Depends On  Description
5.1   frontend/package.json         -           All npm dependencies
5.2   frontend/tsconfig.json        -           TypeScript config (strict, path alias)
5.3   frontend/next.config.ts       -           Standalone output mode
5.4   frontend/eslint.config.mjs    -           ESLint flat config
5.5   frontend/postcss.config.mjs   -           Tailwind plugin
5.6   frontend/app/globals.css      -           Tailwind imports + CSS variables
5.7   frontend/app/layout.tsx       5.6         Root layout (fonts, metadata)
```

**Gate**: `npm run dev` serves empty page at localhost:3000

## Phase 6: Frontend Shared Code

```
Step  File                          Depends On  Description
6.1   frontend/lib/utils.ts         -           [FILL IN: N] utility/formatting functions
6.2   frontend/lib/api.ts           -           [FILL IN: N] interfaces + [FILL IN: N] API functions
6.3   frontend/hooks/[FILL IN].tsx  -           [FILL IN: Custom hooks]
```

**Gate**: TypeScript compiles with no errors

## Phase 7: Frontend Base Components

```
Step  File                                      Depends On  Description
7.1   frontend/components/ui/button.tsx          6.1         3 variants, 3 sizes
7.2   frontend/components/ui/card.tsx            6.1         Compound Card component
7.3   frontend/components/ui/sort-indicator.tsx  -           Chevron icons for sort state
7.4   frontend/components/ui/sortable-table.tsx  6.1, 6.3    Generic sortable table
7.5   frontend/components/[FILL IN].tsx          -           [FILL IN: Display components]
7.6   frontend/components/[FILL IN].tsx          7.2         [FILL IN: Card variants]
7.7   frontend/components/navbar.tsx             -           Navigation bar with active state
```

**Gate**: Visual check — render each component in isolation

## Phase 8: Frontend Filter Components

```
Step  File                                          Depends On  Description
8.1   frontend/components/date-range-picker.tsx      7.1         Presets + custom + dropdown
8.2   frontend/components/[FILL IN]-picker.tsx       7.1         [FILL IN: Filter description]
8.3   frontend/components/[FILL IN]-picker.tsx       7.1, 6.2    [FILL IN: Dynamic filter]
8.4   frontend/components/[FILL IN]-picker.tsx       7.1         [FILL IN: Filter description]
```

**Gate**: All pickers render, toggle, and emit callback values

## Phase 9: Frontend Visualization Components

```
Step  File                                                  Depends On  Description
9.1   frontend/components/charts/[FILL IN]-chart.tsx        -           [FILL IN: Chart type]
9.2   frontend/components/charts/[FILL IN]-chart.tsx        -           [FILL IN: Chart type]
[FILL IN: Add rows for domain-specific visualization components]
[FILL IN: Add rows for domain-specific table components]
```

**Gate**: Components render with mock data

## Phase 10: Frontend Pages (Integration)

```
Step  File                              Depends On      Description
10.1  frontend/app/[FILL IN]/page.tsx   6.2, 8.*, 9.*  [FILL IN: Page description]
10.2  frontend/app/[FILL IN]/page.tsx   6.2, 8.*, 9.*  [FILL IN: Page description]
10.3  frontend/app/[FILL IN]/page.tsx   6.2, 8.*, 9.*  [FILL IN: Page description]
10.4  frontend/app/page.tsx             -               Redirect to default page
```

**Gate**: Full end-to-end — open localhost:3000, all pages load data from backend, filters work, charts render, tables sort

---

## Execution Checklist

```
[ ] 1. Create projects/plan/ directory and write PRD.md
[ ] 2. Create projects/plan/adr/ and write all ADR files
[ ] 3. Write projects/plan/TDD.md (full technical blueprint)
[ ] 4. Write projects/plan/STANDARDS.md (conventions)
[ ] 5. Write projects/plan/ROADMAP.md (this execution plan)
[ ] 6. Execute Phase 1 - Infrastructure
[ ] 7. Execute Phase 2 - Backend Core
[ ] 8. Execute Phase 3 - Backend Data Layer
[ ] 9. Execute Phase 4 - Backend API (Gate: health check passes)
[ ] 10. Execute Phase 5 - Frontend Foundation
[ ] 11. Execute Phase 6 - Frontend Shared Code
[ ] 12. Execute Phase 7 - Frontend Base Components
[ ] 13. Execute Phase 8 - Frontend Filter Components
[ ] 14. Execute Phase 9 - Frontend Visualizations
[ ] 15. Execute Phase 10 - Frontend Pages (Gate: E2E works)
[ ] 16. Docker Compose full stack validation
```

---

## Example: Celes Cost Roadmap (Key Phases)

Below are key phases from the completed celes-cost ROADMAP to illustrate the expected quality:

### Phase 0 (example)

```
[x] PRD.md            -> Feature map, requirements, personas
[x] ADR/*.md          -> 9 architecture decision records
[x] TDD.md            -> Full technical blueprint
[x] STANDARDS.md      -> Code conventions and patterns
[x] ROADMAP.md        -> This file
```

### Phase 1 (example)

```
Step  File                              Depends On  Description
1.1   docker-compose.yml                -           3-service stack definition
1.2   .env + .env.example               -           All environment variables
1.3   backend/Dockerfile                -           Python 3.12 slim image
1.4   frontend/Dockerfile               -           Node 20 alpine multi-stage
1.5   scripts/setup_bq_sa.sh            -           GCP service account setup
```

**Gate**: `docker compose build` succeeds

### Phase 2 (example)

```
Step  File                                      Depends On  Description
2.1   backend/requirements.txt                  -           All Python deps
2.4   backend/app/core/config.py                2.1         Pydantic Settings (env vars, computed props)
2.5   backend/app/core/bigquery_client.py       2.4         Singleton BQ wrapper (auth, execute, test)
2.7   backend/app/services/cost_calculator.py   -           Cost/slot/format utilities
```

**Gate**: `python -c "from app.core.config import settings; print(settings.APP_NAME)"` works
