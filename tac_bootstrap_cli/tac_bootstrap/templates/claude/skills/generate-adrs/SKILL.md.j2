---
name: generate-adrs
description: Generate Architecture Decision Records (ADRs) from a PRD and STANDARDS. Evaluates shared vs project-specific decisions using the COMMON-DECISIONS catalog. Triggers on requests like "generate ADRs", "architecture decisions", "evaluate tech choices", "create ADRs", or "what tech stack should we use".
---

# Generate ADRs

Generate project-specific Architecture Decision Records by evaluating the COMMON-DECISIONS catalog against the project's PRD. This is **Phase 1** of the AI-Assisted Development Workflow — it bridges WHAT (PRD) to HOW (TDD).

## Input

Configuration is read from the invoking spec's frontmatter or project context:

| Field | Description | Example |
|-------|-------------|---------|
| `prd_path` | Path to the completed PRD | `docs/plan/PRD.md` |
| `standards_path` | Path to STANDARDS file | `docs/plan/STANDARDS.md` |
| `shared_dir` | Path to shared documentation framework | `docs/plan/documentation-framework/shared/` |
| `output_dir` | Directory for ADR output files | `docs/plan/adr/` |

If no spec is provided, look for these files in `<plan-dir>/` by convention.

## Required Inputs

- **PRD** (`<plan-dir>/PRD.md`): Must exist with completed feature map and requirements
- **STANDARDS** (`<plan-dir>/STANDARDS.md`): Copy from shared documentation framework if not present
- **COMMON-DECISIONS catalog**: Bundled in [references/common-decisions.md](references/common-decisions.md)

## Output

- ADR files in `<output_dir>/` directory (e.g., `004-*.md`, `008-*.md`, `009-*.md`)

## Workflow

### Step 1: Copy Shared Assets

If not already present:

1. Copy `<shared_dir>/STANDARDS.md` to `<plan-dir>/STANDARDS.md`
2. Copy shared ADRs from `<shared_dir>/adr/` to `<output_dir>/`

### Step 2: Read PRD and Identify Decision Points

Read the project PRD and extract:

- Deployment model (self-hosted, cloud, SaaS)
- Data sources (API, database, data warehouse, files)
- User authentication needs (from NFRs and features)
- Performance requirements (from NFRs)
- Feature complexity (from feature map)

### Step 3: Evaluate Shared ADRs

The shared ADRs cover standard stack decisions. For each, confirm whether the project uses the standard stack or needs to override:

| Shared ADR | Decision | Override If... |
|------------|----------|----------------|
| Backend framework | Default backend framework | Using different framework or language |
| Frontend framework | Default frontend framework | Using different UI framework or SPA |
| UI styling | Default styling approach | Adopting a different component library |
| Dependency injection | Default DI pattern | Using different DI pattern |
| State management | Default state management | Using different state library |
| Visualization library | Default charting library | Using different charting approach |

If all shared ADRs apply as-is, note "Using shared ADR-00X" and move on. Only create override ADRs if deviating.

### Step 4: Evaluate Project-Specific Decision Categories

For each category in the COMMON-DECISIONS catalog, make a decision based on PRD requirements:

#### Authentication Strategy

- Match to PRD security requirements and deployment model
- Options: No auth (network-level), JWT, OAuth2/SSO, API keys, Session-based

#### Database Choice

- Match to PRD data requirements and features
- Options: No database, PostgreSQL (active), PostgreSQL (provisioned), SQLite, Redis

#### Primary Data Source

- Match to PRD product vision and data flow
- Options: External API, Data warehouse, Own database, File system, Message queue

#### Caching Strategy

- Match to PRD performance requirements
- Options: No caching, Data source native, Application-level, CDN/browser, Stale-while-revalidate

#### Deployment Model

- Match to PRD deployment requirements
- Options: Docker Compose, Kubernetes, Serverless, Platform (Vercel/Railway)

#### Error Handling Approach

- Match to PRD reliability requirements
- Options: HTTPException + logging, Structured error codes, Sentry, Custom middleware

#### Multi-Tenancy / Multi-Environment

- Match to PRD feature requirements for multi-user or multi-env support
- Options: Single tenant, Multi-tenant (shared DB), Multi-environment (UNION), Config-driven

### Step 5: Write ADR Files

For each project-specific decision, create an ADR using the Nygard format:

```markdown
# ADR-[NNN]: [Decision Title]

**Status**: Accepted

**Date**: [YYYY-MM-DD]

## Context
[WHY this decision is needed — tie to PRD requirements]

## Decision
[WHAT was decided — specific technology/pattern/approach]

## Consequences

### Positive
- [Benefit tied to project goals]

### Negative
- [Trade-off with mitigation if applicable]
```

**Numbering rules**:
- Shared ADRs occupy the lower numbers (already exist)
- Project-specific ADRs fill remaining slots
- File naming: `NNN-short-kebab-description.md` (e.g., `004-multi-environment-union-all.md`)

### Step 6: Quality Checks

Before finalizing, verify:

- [ ] Every decision category from COMMON-DECISIONS has been evaluated
- [ ] Shared ADRs confirmed or overridden
- [ ] Each ADR has Status, Date, Context, Decision, Consequences sections
- [ ] Context ties back to PRD requirements (reference F-XX or NFR-XX)
- [ ] No `[FILL IN]` placeholders remaining
- [ ] ADR numbers don't conflict with shared ADRs
- [ ] Negative consequences are honest (every decision has trade-offs)

## Reference Example

A well-written ADR set demonstrates these quality indicators:

- **Project-specific ADRs**: 2-4 decisions tailored to the project's unique requirements
- **Context sections**: Reference specific project constraints (data structure, deployment environment, access patterns)
- **Decisions**: Concrete choices (not "we might use X" but "use UNION ALL with template system")
- **Negative consequences**: Honest trade-offs with mitigations where applicable

See [references/common-decisions.md](references/common-decisions.md) for the full decision catalog and ADR template format.

## File Placement

```
<plan-dir>/
├── STANDARDS.md           <- Copied from shared/
├── adr/
│   ├── 0XX-*.md          <- Shared (copied)
│   └── 0XX-*.md          <- Project-specific (generated)
```

The ADRs feed into Phase 2 (TDD generation via `generate-tdd`).
