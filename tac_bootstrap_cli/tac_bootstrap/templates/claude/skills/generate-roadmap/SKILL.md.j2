---
name: generate-roadmap
description: Generate an implementation roadmap from a completed TDD. Assigns every file to a build phase with dependency tracking and gate criteria. Triggers on requests like "generate roadmap", "implementation plan", "create phases", "build order", or "what should we build first".
---

# Generate Roadmap

Generate a phased implementation roadmap that assigns every file from the TDD to a build phase with dependency tracking. The roadmap is **Phase 3** of the AI-Assisted Development Workflow — it defines the execution order for code generation.

## Input

Configuration is read from the invoking spec's frontmatter or project context:

| Field | Description | Example |
|-------|-------------|---------|
| `tdd_path` | Path to the completed TDD | `docs/plan/TDD.md` |
| `output_path` | Where to write the ROADMAP | `docs/plan/ROADMAP.md` |

If no spec is provided, look for the TDD in `<plan-dir>/TDD.md` by convention.

## Required Inputs

- **TDD** (`<plan-dir>/TDD.md`): Completed technical design with project structure and all component specs

## Output

- A filled `ROADMAP.md` file placed at the configured `output_path`

## Workflow

### Step 1: Extract File Inventory

Read the TDD Section 2 (Project Structure) and build a complete inventory of every file:

1. List all files from the folder tree
2. Note which TDD section specifies each file's implementation detail
3. Flag any files in the tree that lack a TDD specification

### Step 2: Assign Files to Phases

Follow the phased structure from the template in [references/roadmap-template.md](references/roadmap-template.md). The number of phases depends on the project scope; a typical project uses 8-12 phases:

| Phase | Name | What Goes Here |
|-------|------|----------------|
| 0 | Documentation | PRD, ADRs, TDD, STANDARDS, ROADMAP |
| 1 | Infrastructure & Config | docker-compose.yml, Dockerfiles, .env, setup scripts |
| 2 | Backend Core | dependency files, init files, config, data client |
| 3 | Backend Data | schemas/models, query layer, service layer |
| 4 | Backend API | endpoint modules, app factory, entrypoint |
| 5 | Frontend Foundation | package config, build config, global styles, layout |
| 6 | Frontend Shared Code | utilities, API client, custom hooks |
| 7 | Frontend Base Components | UI primitives (buttons, cards, tables), navigation |
| 8 | Frontend Filter Components | Date pickers, dropdowns, filter controls |
| 9 | Frontend Visualizations | Chart components, domain-specific visualizations, table components |
| 10 | Frontend Pages | Page components integrating filters, charts, tables |

Adjust the number of phases and their groupings to match the project's actual scope. Not all projects need all phases (e.g., API-only projects skip frontend phases).

### Step 3: Establish Dependencies

For each file, determine what it depends on:

- Init/marker files: no dependencies (listed as `-`)
- Config files: depend on dependency manifests
- Clients: depend on config
- Services: depend on client + models
- Endpoints: depend on service + models
- Frontend components: depend on utils + hooks
- Pages: depend on API client + all components used

**Rules**:
- No forward dependencies (Phase N cannot depend on Phase N+1)
- Within a phase, steps are numbered (1.1, 1.2, etc.) and can depend on earlier steps
- Cross-phase dependencies are implicit (Phase 3 depends on Phase 2 completing)

### Step 4: Define Gate Criteria

Each phase ends with a **Gate** — a concrete check that must pass before proceeding:

| Phase | Gate Pattern |
|-------|-------------|
| 0 | All documentation files exist and have no `[FILL IN]` markers |
| 1 | Container build succeeds |
| 2 | Config module can be imported/loaded |
| 3 | Unit tests for query builders and utilities pass |
| 4 | Health endpoint returns healthy; API docs show all endpoints |
| 5 | Dev server serves page at expected port |
| 6 | Type checking / compilation passes with no errors |
| 7 | Visual check — render each component in isolation |
| 8 | All interactive controls render and emit callback values |
| 9 | Components render with mock data |
| 10 | Full E2E — pages load data from backend, filters work, charts render, tables sort |

### Step 5: Write Roadmap File

Use the template format. For each phase:

```
## Phase N: [Name]

` ` `
Step  File                              Depends On  Description
N.1   path/to/file.ext                  -           Brief description
N.2   path/to/other.ext                 N.1         Brief description
` ` `

**Gate**: [Concrete verification command or check]
```

End with an **Execution Checklist** summarizing all phases as checkbox items.

### Step 6: Quality Checks

Before finalizing, verify:

- [ ] Every file from TDD Section 2 appears in exactly one phase
- [ ] No forward dependencies (file in Phase N doesn't depend on Phase N+1 file)
- [ ] Each phase has a gate with a concrete verification step
- [ ] Step dependencies within a phase are correct
- [ ] Phase 0 includes all documentation files
- [ ] Execution checklist covers all phases
- [ ] No `[FILL IN]` placeholders remaining
- [ ] File paths match TDD project structure exactly

## Reference Example

A well-written ROADMAP demonstrates these quality indicators:

- **Phase 0**: Documentation files (PRD, ADRs, TDD, STANDARDS, ROADMAP)
- **Phase 1**: Infrastructure files (docker-compose, .env, Dockerfiles, setup scripts)
- **Phase 2+**: Backend and frontend phases following dependency order
- **Gates**: Concrete commands (container build, module import, health check, dev server, E2E check)
- **No forward dependencies**: Each phase only depends on prior phases

See [references/roadmap-template.md](references/roadmap-template.md) for the full template with all phases.

## File Placement

```
<plan-dir>/
├── ROADMAP.md          <- Output of this skill
```

The ROADMAP feeds into Phase 4+ (code generation via `scaffold-docker-stack`, `scaffold-backend-service`, etc.).
