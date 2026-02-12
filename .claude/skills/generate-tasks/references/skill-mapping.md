# Skill Mapping Rules

Reference for Step 2 (Audit) and Step 6 (Map) of the `generate-tasks` workflow. Defines how ROADMAP steps are matched to installed skills.

---

## Matching Algorithm

Apply rules in **priority order** (first match wins):

1. **Trivial detection** → `skill: none`
2. **File-path pattern** → matched skill name
3. **Description keyword** → matched skill name
4. **Phase-level default** → default skill for that phase
5. **Gap** → `skill: gap:<suggested-name>`

### Recording the Matched Rule

When a step matches, record BOTH the assigned `skill` AND the matched rule as `matched_rule`. This pair is the **grouping key** in Step 6.5.

| Match Source | `matched_rule` Value | Example |
|-------------|----------------------|---------|
| Trivial pattern | `trivial` | `.env` files |
| File-path glob (tables below) | The exact glob string | `**/__init__.py`, `frontend/components/ui/**` |
| Description keyword | `keyword:{first-matched-keyword}` | `keyword:CRUD` |
| Phase-level default | `phase-default` | Infrastructure phase fallback |
| Gap | `gap` | No match |

> **Grouping effect**: Steps sharing the same `skill` AND same file-path glob `matched_rule` are grouped into a single spec in Step 6.5. Only file-path glob matches qualify for grouping — keyword, phase-default, and trivial matches remain standalone.

---

## 1. Trivial Patterns (`skill: none`)

Steps that produce trivial files needing no skill scaffolding:

| Pattern | Examples |
|---------|----------|
| `.env*` files | `.env`, `frontend/.env.local`, `.env.production` |
| Description contains "environment variables" | Environment config files |

These steps get `skill: none` — they are hand-written boilerplate with no reusable pattern.

---

## 2. File-Path Rules

### Infrastructure

| Glob Pattern | Skill | Notes |
|-------------|-------|-------|
| `**/Dockerfile*` | `scaffold-docker-stack` | Backend/frontend Dockerfiles |
| `**/docker-compose*` | `scaffold-docker-stack` | Compose stack definition |
| `infra/**` | `scaffold-docker-stack` | Infrastructure directory |

### Backend

| Glob Pattern | Skill | Notes |
|-------------|-------|-------|
| `**/__init__.py` | `create-init-file` | Python package markers |
| `backend/app/config.*` | `scaffold-backend-service` | App configuration |
| `backend/app/main.*` | `scaffold-backend-service` | FastAPI entrypoint |
| `backend/app/dependencies.*` | `scaffold-backend-service` | DI wiring |
| `backend/app/infrastructure/*.py` (not `__init__.py`) | `scaffold-backend-service` | Data clients, database |
| `backend/app/routers/*.py` (not `__init__.py`) | `scaffold-backend-service` | API endpoints |
| `backend/app/domain/models.*` | `create-crud-entity` | Domain models |
| `backend/app/domain/services.*` | `create-domain-service` | Business logic services |
| `backend/app/domain/events.*` | `create-domain-event` | Domain events |
| `backend/app/domain/value_objects.*` | `create-value-object` | Value objects |
| `backend/tests/test_*` | inherits from tested file | Match the skill of the file being tested |

### Frontend Pages

| Glob Pattern | Skill | Notes |
|-------------|-------|-------|
| `frontend/app/**/page.tsx` | `scaffold-frontend-page` | Next.js App Router pages |
| `frontend/app/**/layout.tsx` | `none` | Layouts are hand-written |
| `frontend/app/globals.css` | `none` | Global styles, hand-written |
| `frontend/lib/utils.*` | `none` | Utility helpers, hand-written |
| `frontend/lib/api.*` | `none` | API client, hand-written |

### Frontend Components

| Glob Pattern | Skill | Notes |
|-------------|-------|-------|
| `frontend/components/ui/**` | `scaffold-ui-component` | Shared UI primitives |
| `frontend/components/charts/**` | `scaffold-chart-component` | Recharts wrappers |
| `frontend/components/domain/**` | `scaffold-ui-component` | Domain-specific components |

### Config Files (all `skill: none`)

| Glob Pattern |
|-------------|
| `**/requirements.txt` |
| `**/package.json` |
| `**/tsconfig.json` |
| `**/tailwind.config.*` |
| `**/next.config.*` |
| `**/*.yml`, `**/*.yaml` (non-docker-compose) |

---

## 3. Description Keyword Fallback

When file-path rules don't match, check the step's Description field:

| Keywords | Skill |
|----------|-------|
| "CRUD", "entity", "model" | `create-crud-entity` |
| "service", "business logic", "orchestrat" | `create-domain-service` |
| "event", "handler", "publish" | `create-domain-event` |
| "value object", "frozen", "immutable" | `create-value-object` |
| "provider", "adapter", "LLM" | `create-provider-adapter` |
| "strategy", "algorithm", "pluggable" | `create-strategy-pattern` |
| "middleware", "decorator", "interceptor" | `create-middleware-decorator` |
| "cache", "LRU", "warmup" | `create-caching-layer` |
| "chart", "graph", "visualiz" | `scaffold-chart-component` |
| "component", "widget", "UI element" | `scaffold-ui-component` |
| "page", "route", "dashboard view" | `scaffold-frontend-page` |
| "endpoint", "router", "API" | `scaffold-backend-service` |
| "Docker", "container", "compose" | `scaffold-docker-stack` |
| "comparison", "evaluation", "ranking" | `create-comparison-analyzer` |

---

## 4. Phase-Level Defaults

When no rule matches at all, apply a phase-level default:

| Phase Category | Default Skill |
|---------------|---------------|
| Infrastructure phases (Docker, config, env) | `scaffold-docker-stack` |
| Backend core / data layer / services | `scaffold-backend-service` |
| Backend API endpoints | `scaffold-backend-service` |
| Frontend foundation | `none` |
| Frontend UI components | `scaffold-ui-component` |
| Frontend domain / chart components | `scaffold-ui-component` |
| Frontend pages | `scaffold-frontend-page` |

These defaults are fallbacks — the file-path and keyword rules should cover most steps.

---

## 5. Gap Detection & Naming

When a step doesn't match any installed skill and no phase default fits:

### Naming Convention
- **Backend gaps**: `create-{domain}` (e.g., `create-notification-handler`)
- **Frontend gaps**: `scaffold-{domain}` (e.g., `scaffold-form-builder`)
- Always kebab-case, max 3 words after prefix

### Grouping Gaps
- If multiple steps map to the same gap, generate **one** skill-creation spec
- Group by: same suggested skill name, or related steps within the same domain

### Inline Creation (Primary)

When gaps are detected, the default path is **inline skill creation** during the `generate-tasks` run:

1. User is prompted with a gap summary table and asked to confirm inline creation.
2. For each gap, `init_skill.py` scaffolds the skill directory, then the generated SKILL.md is edited with synthesized content from ROADMAP, TDD, and STANDARDS context.
3. After creation, a re-audit and re-map cycle confirms the new skills are matched.
4. See `references/inline-skill-context-template.md` for context assembly guidance.

Result: All gaps resolved to `skill: <name>` — no `pending:` references, no chore specs, no Phase 0 prerequisites.

### Chore Spec Fallback (Legacy)

Used when the user declines inline creation or when inline creation fails for a specific gap:

- Filename: `chore-{XXX}-create-skill-{gap-name}.md` (skill-creation specs are numbered first, starting from 001)
- Type: `chore`
- Metadata: `skill: skill-creator`
- Content describes the skill to create, references `skill-creator`, and lists which ROADMAP steps need it
- Gap references become `skill: pending:chore-{XXX}-create-skill-{name}.md`
