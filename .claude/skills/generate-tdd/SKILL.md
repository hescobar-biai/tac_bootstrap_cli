---
name: generate-tdd
description: Generate a Technical Design Document (TDD) from a PRD, ADRs, and STANDARDS. Produces a complete technical blueprint covering stack, structure, backend, frontend, and verification. Triggers on requests like "generate TDD", "technical design", "create tech spec", "write technical document", or "how should we build this".
---

# Generate TDD

Generate a complete Technical Design Document that specifies HOW to build every component. The TDD is **Phase 2** of the AI-Assisted Development Workflow — it translates architecture decisions (ADRs) into an implementable blueprint.

## Input

Configuration is read from the invoking spec's frontmatter or project context:

| Field | Description | Example |
|-------|-------------|---------|
| `prd_path` | Path to the completed PRD | `docs/plan/PRD.md` |
| `adrs_dir` | Directory containing ADR files | `docs/plan/adr/` |
| `standards_path` | Path to STANDARDS file | `docs/plan/STANDARDS.md` |
| `output_path` | Where to write the TDD | `docs/plan/TDD.md` |

If no spec is provided, look for these files in `<plan-dir>/` by convention.

## Required Inputs

- **PRD** (`<plan-dir>/PRD.md`): Completed product requirements
- **ADRs** (`<plan-dir>/adr/*.md`): All shared + project-specific ADRs
- **STANDARDS** (`<plan-dir>/STANDARDS.md`): Code conventions and patterns

## Output

- A filled `TDD.md` file placed at the configured `output_path`

## Workflow

### Step 1: Read All Inputs

Load and cross-reference:

1. PRD feature map (F-XX IDs) — drives what components are needed
2. All ADRs — drives technology choices and patterns
3. STANDARDS — drives naming conventions, code style, patterns

### Step 2: Fill Template Sections

Use the template from [references/tdd-template.md](references/tdd-template.md) and fill each section:

#### Section 1: Tech Stack & Versions

- Pull technologies from ADRs (framework choices, database, UI libraries, etc.)
- Pin exact versions for reproducibility
- Include ALL dependencies (backend + frontend + database + infra)
- Reference: STANDARDS Section 1 for naming, ADRs for technology choices

#### Section 2: Project Structure

- Complete folder tree showing EVERY file in the project
- Follow naming conventions from STANDARDS (e.g., snake_case backend, kebab-case frontend)
- Every file listed here MUST appear in a ROADMAP phase later
- Include `<plan-dir>/` directory with all documentation files

#### Section 3: Environment Configuration

- List ALL `.env` variables with descriptions
- Describe the config class (fields, types, computed properties) per project framework
- Frontend config: build tool settings, API base URL, path aliases

#### Section 4: Docker Compose Stack

- Number of services, network name, volume configuration
- Table: Service | Image | Port | Depends On | Notes
- Health check details, restart policies, volume mounts

#### Section 5: Backend — Detailed Component Specifications

Fill each subsection with implementation-ready detail:

- **5.1 Data Source Client**: Class name, pattern (singleton, pool, etc.), constructor, core methods with signatures, error handling
- **5.2 Domain Utilities**: Utility/calculation functions with signatures, formulas, constants
- **5.3 Query/Data Access Layer**: Query templates or ORM models, parameterization style, filter strategy
- **5.4 Domain Service**: Class name, pattern, method listing with template used, parameters, return type
- **5.5 Response Models**: All models with key fields (table format)
- **5.6 API Endpoints**: Router prefix, common params, full endpoint table (Method, Path, Response Model, Params, Validation)
- **5.7 App Factory**: App creation with CORS, router registration, startup/shutdown events

#### Section 6: Frontend — Detailed Component Specifications

Fill each subsection:

- **6.1 Shared Utilities**: Function signatures for helpers, formatters, domain-specific functions
- **6.2 API Client**: TypeScript interfaces (mirrors of backend models) + async API functions
- **6.3 Custom Hooks**: Hook signatures, state managed, return values
- **6.4 Base UI Components**: Props interface, variants/sizes, key styling classes, dark mode
- **6.5 Filter Components**: State managed, callback signature, UI behavior, data fetching
- **6.6 Display Components**: Layout components (navbar, summary cards, icons)
- **6.7 Chart Components**: Chart type, data shape, axes, features (per project charting library)
- **6.8 Domain-Specific Components**: Components unique to the project domain
- **6.9 Table Components**: Columns, sort defaults, row interactions

#### Section 7: Frontend Pages — Data Flow & State

For each page:

- **State**: All state variables with types
- **Data Fetching**: Dependencies and API calls
- **Computed**: Derived transformations
- **Sections**: Page layout sections in render order

#### Section 8: Styling & Design System

- Framework, dark mode approach, color palette, fonts, layout, dropdown/loading/error patterns

#### Section 9: Key Architectural Patterns

- List core patterns with one-line explanation of WHY each is used
- Reference ADR numbers for traceability

#### Section 10: Verification Plan

- 8-10 concrete verification steps
- Include: health endpoint, API docs, frontend rendering, domain-specific checks, Docker stack, dark mode

### Step 3: Quality Checks

Before finalizing, verify:

- [ ] Zero `[FILL IN]` placeholders remaining
- [ ] Every section has implementation-ready detail (not just descriptions)
- [ ] Project structure tree shows every file
- [ ] All models listed with fields
- [ ] All API endpoints listed with method, path, response model
- [ ] All frontend components have props interface described
- [ ] All pages have state, data fetching, and layout specified
- [ ] ADR references included where relevant
- [ ] Tech stack versions are pinned (not "latest")
- [ ] Verification plan has concrete curl/browser steps

## Reference Example

A well-written TDD demonstrates these quality indicators:

- **Stack**: 15+ pinned dependencies with exact versions
- **Structure**: 40+ files in complete folder tree
- **Backend**: Data client with methods, query templates, models, API endpoints fully specified
- **Frontend**: Utility functions, TypeScript interfaces, custom hooks, 20+ components
- **Pages**: All pages with full state/effect/computed/layout specifications
- **Verification**: 8-10 concrete steps

See [references/tdd-template.md](references/tdd-template.md) for the full template with all sections.

## File Placement

```
<plan-dir>/
├── TDD.md          <- Output of this skill
```

The TDD feeds into Phase 3 (roadmap generation via `generate-roadmap`).
