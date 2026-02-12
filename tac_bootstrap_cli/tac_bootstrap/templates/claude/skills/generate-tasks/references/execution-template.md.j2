# EXECUTION.md Template

Use this template when generating `project/tasks/EXECUTION.md` in Step 8.

---

## Template

```md
# Execution Plan

> Auto-generated from `project/plan/ROADMAP.md` by the `generate-tasks` skill.
> Specs located in `project/tasks/`. Each spec follows the `product-issues` template for its type.

## Summary

| Phase | Name | Specs | Parallel Groups | Skill Gaps |
|-------|------|-------|-----------------|------------|
<for each phase (skipping Phase 0), add a row:>
| <phase-number> | <phase-name> | <spec-count> | <group-count> | <gap-count> |

**Total specs**: <total>

---

<if skills were created inline during Step 6b:>

## Inline-Created Skills

> The following skills were created inline during task generation to resolve skill gaps.
> These are starter-quality skills and may benefit from iteration after the first implementation pass.

| Skill | Path | ROADMAP Steps | Description |
|-------|------|---------------|-------------|
| <skill-name> | `.claude/skills/<skill-name>/` | <step numbers> | <brief description> |

---

<end if>

<if legacy fallback produced skill-creation specs:>

## Skill Prerequisites

> **Legacy fallback** — The following skills must be created before their dependent specs can be implemented.
> Each uses the `skill-creator` skill. Complete these before starting Phase 1.

| Spec | Skill to Create | Needed By | Steps |
|------|----------------|-----------|-------|
| <spec-filename> | <gap-skill-name> | <list of dependent spec filenames> | <step numbers> |

---

<end if>

<for each phase (skipping Phase 0):>

## Phase <N>: <Name>

**Gate**: <gate criteria from ROADMAP>

### Group 1 (no intra-phase dependencies)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| <spec-filename> | <type> | <roadmap-file-path or "N files (pattern)"> | <dependency-spec-filenames or "—"> | <skill-name or "none"> |

### Group 2 (depends on Group 1)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| <spec-filename> | <type> | <roadmap-file-path or "N files (pattern)"> | <dependency-spec-filenames> | <skill-name or "none"> |

<continue groups as needed>

---

<end for each phase>

## Dependency Graph

<text-based overview showing which phases depend on which, e.g.:>

Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
                                            ↓
Phase 1 → Phase 6 → Phase 7 → Phase 8 → Phase 9
```

---

## Worked Example

Below is a worked example using the celes-support ROADMAP to illustrate the expected output. This example demonstrates **Step 6.5 grouping** — 43 original ROADMAP steps are consolidated into **28 specs** (22 standalone + 6 grouped).

### Grouping Applied

| Group | Original Specs | Grouped Spec | Phase |
|-------|---------------|--------------|-------|
| 5 `__init__.py` files | 010, 013, 015, 017, 024 | `chore-010-python-init-files.md` | 2 |
| 4 infra services | 016, 020, 021, 022 | `feature-016-infrastructure-services.md` | 3 |
| 3 API routers | 025, 026, 027 | `feature-025-api-routers.md` | 5 |
| 4 UI base components | 033, 034, 035, 036 | `feature-033-base-ui-components.md` | 7 |
| 3 domain components | 037, 040, 041 | `feature-037-domain-ui-components.md` | 8 |
| 2 chart components | 038, 039 | `feature-038-chart-components.md` | 8 |

### Key Dependency Redirections

- Any spec that depended on `chore-010-app-init.md`, `chore-013-tests-init.md`, `chore-015-infrastructure-init.md`, `chore-017-domain-init.md`, or `chore-024-routers-init.md` → now depends on `chore-010-python-init-files.md`
- Any spec that depended on `feature-020-slack-client.md`, `feature-021-storage-client.md`, or `feature-022-llm-client.md` → now depends on `feature-016-infrastructure-services.md`
- Any spec that depended on `feature-025-ingestion.md`, `feature-026-dashboard.md`, or `feature-027-api.md` → now depends on `feature-025-api-routers.md`
- Any spec that depended on `feature-033-button.md`, `feature-034-card.md`, `feature-035-input.md`, or `feature-036-table.md` → now depends on `feature-033-base-ui-components.md`
- Any spec that depended on `feature-037-metric-card.md`, `feature-040-case-table.md`, or `feature-041-solution-editor.md` → now depends on `feature-037-domain-ui-components.md`
- Any spec that depended on `feature-038-sla-chart.md` or `feature-039-category-pie-chart.md` → now depends on `feature-038-chart-components.md`

```md
# Execution Plan

> Auto-generated from `project/plan/ROADMAP.md` by the `generate-tasks` skill.
> Specs located in `project/tasks/`. Each spec follows the `product-issues` template for its type.

## Summary

| Phase | Name | Specs | Parallel Groups | Skill Gaps |
|-------|------|-------|-----------------|------------|
| 1 | Infrastructure & Config | 9 | 3 | 0 |
| 2 | Backend Core | 4 | 3 | 0 |
| 3 | Backend Data Layer | 3 | 2 | 0 |
| 4 | Backend Services & Infrastructure | 1 | 1 | 0 |
| 5 | Backend API Endpoints | 1 | 1 | 0 |
| 6 | Frontend Foundation | 5 | 2 | 0 |
| 7 | Frontend UI Components | 1 | 1 | 0 |
| 8 | Frontend Domain Components | 2 | 1 | 0 |
| 9 | Frontend Pages | 2 | 1 | 0 |

**Total specs**: 28

---

## Phase 1: Infrastructure & Config

**Gate**: `docker compose build` succeeds without errors.

### Group 1 (no intra-phase dependencies)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| `chore-001-env.md` | chore | `.env` | — | none |
| `chore-002-frontend-env-local.md` | chore | `frontend/.env.local` | — | none |
| `chore-003-requirements-txt.md` | chore | `backend/requirements.txt` | — | none |
| `chore-005-package-json.md` | chore | `frontend/package.json` | — | none |

### Group 2 (depends on Group 1)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| `chore-004-backend-dockerfile.md` | chore | `backend/Dockerfile` | `chore-003-requirements-txt.md` | scaffold-docker-stack |
| `chore-007-tsconfig-json.md` | chore | `frontend/tsconfig.json` | `chore-005-package-json.md` | none |
| `chore-008-tailwind-config.md` | chore | `frontend/tailwind.config.ts` | `chore-005-package-json.md` | none |
| `chore-009-next-config.md` | chore | `frontend/next.config.mjs` | `chore-005-package-json.md` | none |

### Group 3 (depends on Group 2)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| `chore-006-docker-compose.md` | chore | `infra/docker-compose.yml` | `chore-004-backend-dockerfile.md`, `chore-005-package-json.md` | scaffold-docker-stack |

---

## Phase 2: Backend Core

**Gate**: `docker compose up backend` starts successfully and responds to `/health`.

### Group 1 (no intra-phase dependencies)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| `chore-010-python-init-files.md` | chore | 5 files (`**/__init__.py`) | — | create-init-file |

> Grouped spec — covers steps 2.1, 2.4, 3.1, 3.3, 5.1 (`backend/app/__init__.py`, `backend/tests/__init__.py`, `backend/app/infrastructure/__init__.py`, `backend/app/domain/__init__.py`, `backend/app/routers/__init__.py`). Cross-phase group assigned to earliest phase (2).

### Group 2 (depends on Group 1)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| `feature-011-config.md` | feature | `backend/app/config.py` | `chore-001-env.md` | scaffold-backend-service |

### Group 3 (depends on Group 2)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| `feature-012-main.md` | feature | `backend/app/main.py` | `feature-011-config.md` | scaffold-backend-service |
| `feature-014-test-main.md` | feature | `backend/tests/test_main.py` | `feature-012-main.md` | scaffold-backend-service |

---

## Phase 3: Backend Data Layer

**Gate**: Backend starts and connects to Postgres (logs show successful connection).

### Group 1 (no intra-phase dependencies)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| `feature-016-infrastructure-services.md` | feature | 4 files (`backend/app/infrastructure/*.py`) | `feature-011-config.md` | scaffold-backend-service |

> Grouped spec — covers steps 3.2, 4.1, 4.2, 4.3 (`backend/app/infrastructure/database.py`, `backend/app/infrastructure/slack_client.py`, `backend/app/infrastructure/storage_client.py`, `backend/app/infrastructure/llm_client.py`). Cross-phase group assigned to earliest phase (3). Internal dep on `feature-011-config.md` is external (Phase 2).

### Group 2 (depends on Group 1)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| `feature-018-domain-models.md` | feature | `backend/app/domain/models.py` | `feature-016-infrastructure-services.md` | create-crud-entity |
| `feature-019-dependencies.md` | feature | `backend/app/dependencies.py` | `feature-016-infrastructure-services.md` | scaffold-backend-service |

---

## Phase 4: Backend Services & Infrastructure

**Gate**: Unit tests pass for client wrappers (using mocks).

### Group 1 (no intra-phase dependencies)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| `feature-023-services.md` | feature | `backend/app/domain/services.py` | `feature-018-domain-models.md`, `feature-016-infrastructure-services.md` | create-domain-service |

---

## Phase 5: Backend API Endpoints

**Gate**: Swagger UI at `/docs` shows all endpoints. `curl` to ingestion endpoint triggers pipeline (mocked).

### Group 1 (no intra-phase dependencies)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| `feature-025-api-routers.md` | feature | 3 files (`backend/app/routers/*.py`) | `feature-023-services.md` | scaffold-backend-service |

> Grouped spec — covers steps 5.2, 5.3, 5.4 (`backend/app/routers/ingestion.py`, `backend/app/routers/dashboard.py`, `backend/app/routers/api.py`). Internal dep between `api.py` → `ingestion.py`/`dashboard.py` removed. External dep on `feature-023-services.md` preserved.

---

## Phase 6: Frontend Foundation

**Gate**: `npm run dev` serves the application at `http://localhost:3000`.

### Group 1 (no intra-phase dependencies)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| `feature-028-layout.md` | feature | `frontend/app/layout.tsx` | `chore-005-package-json.md` | none |
| `feature-029-globals-css.md` | feature | `frontend/app/globals.css` | `chore-008-tailwind-config.md` | none |
| `feature-030-utils.md` | feature | `frontend/lib/utils.ts` | `chore-005-package-json.md` | none |

### Group 2 (depends on Group 1)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| `feature-031-api-client.md` | feature | `frontend/lib/api.ts` | `feature-025-api-routers.md` | none |
| `feature-032-home-page.md` | feature | `frontend/app/page.tsx` | `feature-028-layout.md` | scaffold-frontend-page |

---

## Phase 7: Frontend UI Components

**Gate**: Components render correctly in a test page or Storybook (if used).

### Group 1 (no intra-phase dependencies)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| `feature-033-base-ui-components.md` | feature | 4 files (`frontend/components/ui/**`) | `feature-030-utils.md` | scaffold-ui-component |

> Grouped spec — covers steps 7.1, 7.2, 7.3, 7.4 (`frontend/components/ui/button.tsx`, `frontend/components/ui/card.tsx`, `frontend/components/ui/input.tsx`, `frontend/components/ui/table.tsx`).

---

## Phase 8: Frontend Domain Components

**Gate**: Components render with mock data.

### Group 1 (no intra-phase dependencies)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| `feature-037-domain-ui-components.md` | feature | 3 files (`frontend/components/domain/**`) | `feature-033-base-ui-components.md` | scaffold-ui-component |
| `feature-038-chart-components.md` | feature | 2 files (`frontend/components/charts/**`) | `chore-005-package-json.md` | scaffold-chart-component |

> `feature-037-domain-ui-components.md` — covers steps 8.2, 8.4, 8.5 (`MetricCard.tsx`, `CaseTable.tsx`, `SolutionEditor.tsx`). Internal deps between domain components removed. External dep on `feature-033-base-ui-components.md` preserved.
> `feature-038-chart-components.md` — covers steps 8.1, 8.3 (`SLAChart.tsx`, `CategoryPieChart.tsx`).

---

## Phase 9: Frontend Pages

**Gate**: Full E2E flow. Dashboard loads data from backend, charts render, table populates.

### Group 1 (no intra-phase dependencies)

| Spec | Type | File(s) | Depends On | Skill |
|------|------|---------|------------|-------|
| `feature-042-dashboard-page.md` | feature | `frontend/app/dashboard/page.tsx` | `feature-037-domain-ui-components.md`, `feature-038-chart-components.md` | scaffold-frontend-page |
| `feature-043-solutions-page.md` | feature | `frontend/app/dashboard/solutions/page.tsx` | `feature-037-domain-ui-components.md` | scaffold-frontend-page |

---

## Dependency Graph

Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
                                            ↓
Phase 1 → Phase 6 → Phase 7 → Phase 8 → Phase 9
```

---

## Notes

- **Parallel groups** within a phase indicate which specs can be worked on simultaneously.
- **Cross-phase dependencies** are implicit: all specs in Phase N must complete before Phase N+1 begins.
- **Intra-phase dependencies** are explicit: Group 2 specs depend on Group 1 specs within the same phase.
- The `Depends On` column shows spec filenames for traceability back to individual specs.
- The `Skill` column indicates which installed skill to invoke for implementation:
  - A skill name (e.g., `scaffold-backend-service`) means invoke that skill.
  - A skill name with `(created-inline)` suffix means the skill was created during this task generation run (see Inline-Created Skills section).
  - `none` means the file is trivial boilerplate or hand-written — no skill needed.
  - `pending:<spec-filename>` means a skill must be created first (legacy fallback only — see Skill Prerequisites section).
- The `Skill Gaps` column in the summary shows how many steps in each phase require a skill that doesn't exist yet:
  - When inline creation succeeded, this is `0` for all phases.
  - When legacy fallback was used, gaps count the `pending:` references. A **Skill Prerequisites** section appears before Phase 1.
  - When mixed (partial inline success), both sections may appear.
