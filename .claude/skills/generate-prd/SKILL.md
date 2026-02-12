---
name: generate-prd
description: Generate a Product Requirements Document (PRD) from user requirements or a project idea. Use when defining product scope, writing requirements, or creating a product spec. Triggers on requests like "write a PRD", "define requirements", "create product spec", "generate PRD", or "what should the product do".
---

# Generate PRD

Generate a complete Product Requirements Document following the documentation framework template. The PRD is **Phase 0** of the AI-Assisted Development Workflow — it defines WHAT the product is before any architecture or code decisions.

## Input

Configuration is read from the invoking spec's frontmatter or project context:

| Field | Description | Example |
|-------|-------------|---------|
| `output_path` | Where to write the PRD | `docs/plan/PRD.md` |
| `project_name` | Human-readable project name | `"Inventory Tracker"` |

If no spec is provided, ask the user for the output path or default to `<plan-dir>/PRD.md`.

## Required Inputs

- **User requirements or project idea**: A description of the product to build (can be brief — the skill guides you to expand it)

## Output

- A filled `PRD.md` file placed at the configured `output_path`

## Workflow

### Step 1: Gather Requirements

Ask the user for (if not already provided):

1. **Problem**: What pain points exist? What can users NOT do today?
2. **Product type**: Dashboard, API, tool, SaaS, CLI?
3. **Deployment model**: Self-hosted, cloud, SaaS?
4. **Primary data source**: External API, database, data warehouse, file system?
5. **Target users**: Who will use this? (roles, not names)
6. **Key features**: What are the must-have capabilities?

If the user provides a brief idea (e.g., "a real-time inventory tracker for warehouses"), expand it into full requirements by asking clarifying questions.

### Step 2: Fill Template Sections

Use the template from [references/prd-template.md](references/prd-template.md) and fill each section:

#### Section 1: Problem Statement

- 3-5 bullet points describing specific gaps or pain points
- Focus on what users CANNOT do today
- Be concrete: "cannot track cost trends" not "lacks visibility"

#### Section 2: Product Vision

- One paragraph describing what the product IS
- Include: deployment model, core capability, data source, key differentiator
- Example: "A self-hosted web dashboard that connects to warehouse inventory APIs across multiple locations and provides real-time stock analytics with filtering, charting, and drill-down capabilities."

#### Section 3: User Personas

- Table with 3-5 personas
- Each has: Persona Name, Role/Job Title, Primary Goal
- Personas should cover the range of users (operator, analyst, engineer, manager)

#### Section 4: Feature Map

- Every feature gets an `F-XX` ID (F-01, F-02, etc.)
- Features need a short name, description, and priority
- **Priority key**: P0 = Must-have (v1), P1 = Should-have (v1 if time), P2 = Nice-to-have (v2+)
- Aim for 8-15 features for a typical project
- F-XX IDs are used throughout the project for traceability (branches, ADRs, roadmap)

#### Section 5: Functional Requirements

- Group as FR-01, FR-02, etc.
- Each requirement uses MUST/SHOULD/MAY language
- Include constraints, formats, defaults, limits, edge cases
- Each FR maps to one or more features from Section 4

#### Section 6: Non-Functional Requirements

- Table with NFR-01 through NFR-07 (adjust as needed)
- Cover: performance, load time, concurrency, browser support, deployment, security, availability
- Each has a measurable target

#### Section 7: Out of Scope

- 4-6 items explicitly excluded from v1
- Include features that seem related but are NOT being built
- Include integrations deferred to future versions

### Step 3: Quality Checks

Before finalizing, verify:

- [ ] No `[FILL IN]` placeholders remaining
- [ ] Every feature has an F-XX ID
- [ ] Every feature has a priority assigned (P0/P1/P2)
- [ ] Functional requirements use MUST/SHOULD/MAY language
- [ ] Non-functional requirements have measurable targets
- [ ] Out of scope section has 4+ items
- [ ] Problem statement has 3+ specific bullet points
- [ ] Product vision is a single clear paragraph

## Reference Example

A well-written PRD demonstrates these quality indicators:

- **Problem**: 4+ specific bullet points about concrete gaps in current capabilities
- **Vision**: One paragraph covering deployment model, core capability, data source, differentiator
- **Personas**: 4+ personas spanning the user spectrum (operators, analysts, engineers, managers)
- **Features**: 10-15 features with F-XX IDs and P0/P1/P2 priorities
- **FRs**: 5-7 functional requirements with specific constraints (formats, formulas, behaviors)
- **NFRs**: 5-7 non-functional requirements with measurable targets (< Xs API, < Ys load, N+ concurrent)
- **Out of Scope**: 5+ items clearly excluded from v1

See [references/prd-template.md](references/prd-template.md) for the full template with all sections.

## File Placement

```
<plan-dir>/
├── PRD.md          <- Output of this skill
```

The PRD feeds into Phase 1 (ADR generation via `generate-adrs`).
