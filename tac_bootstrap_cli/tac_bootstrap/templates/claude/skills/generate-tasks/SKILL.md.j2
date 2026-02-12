---
name: generate-tasks
description: |
  Generates task files from a project ROADMAP using product-issues templates.
  Triggers: "generate tasks", "create tasks from roadmap", "plan to tasks", "roadmap to tasks"
user-invocable: true
---

# Generate Tasks from ROADMAP

Bulk-generate product specification files from the phased steps in a project ROADMAP, then produce a dependency-aware EXECUTION plan. Each spec is mapped to an installed skill (or flags a gap requiring skill creation first).

## Input

Configuration is read from the invoking spec's frontmatter or project context:

| Field | Description | Example |
|-------|-------------|---------|
| `roadmap_path` | Path to the ROADMAP file | `docs/plan/ROADMAP.md` |
| `output_dir` | Directory for generated spec files | `project/tasks/` |
| `plan_dir` | Directory containing plan documents | `docs/plan/` |

If no spec is provided, look for the ROADMAP in `<plan-dir>/ROADMAP.md` and output to `<tasks-dir>/` by convention.

## Quick Overview

| | |
|---|---|
| **Input** | `<plan-dir>/ROADMAP.md` + context docs (PRD, TDD, STANDARDS, ADRs) |
| **Output** | One spec per task (steps grouped by skill + file-path pattern where applicable) in `<output-dir>/`, plus `<output-dir>/EXECUTION.md` |
| **Templates** | Delegates to `product-issues` skill's 5 reference templates |
| **Naming** | `{type}-{XXX}-{name}.md` |
| **Skips** | Phase 0 by default (documentation phase — those files are inputs, not deliverables) |
| **Skill Mapping** | Each spec includes a `skill:` field indicating which skill implements it |

## Workflow

Follow these 8 steps in order. Do not skip any step.

### Step 1: Discover Spec Templates

1. Read `.claude/skills/product-issues/SKILL.md` to load the classification decision table and template references.
2. Verify the 5 reference templates exist:
   - `.claude/skills/product-issues/reference/feature.md`
   - `.claude/skills/product-issues/reference/bug.md`
   - `.claude/skills/product-issues/reference/chore.md`
   - `.claude/skills/product-issues/reference/refactor.md`
   - `.claude/skills/product-issues/reference/perf.md`
3. Read each template so you have their full structure available for Step 7.
4. **Fallback**: If `product-issues` skill is not found, check for `<output-dir>/README.md` for project-specific spec format guidance. If neither exists, use a minimal format: Title, Summary, Acceptance Criteria (Gherkin), Dependencies, Out of Scope.

### Step 2: Audit Installed Skills

Build an inventory of installed skills so Step 6 can map ROADMAP steps to them.

1. Glob `.claude/skills/*/SKILL.md` to discover all installed skills.
2. Read the frontmatter (YAML between `---` markers) of each skill to extract `name` and `description`.
3. Group skills into categories:

   | Category | Skills |
   |----------|--------|
   | **Scaffolding** | `scaffold-*` skills (docker-stack, backend-service, frontend-page, ui-component, chart-component, project) |
   | **Domain Patterns** | `create-*` skills (crud-entity, domain-service, domain-event, value-object, provider-adapter, strategy-pattern, middleware-decorator, caching-layer, comparison-analyzer) |
   | **Meta / Utilities** | `skill-creator`, `product-issues`, `generating-fractal-docs`, `meta-skill` |

4. Load mapping rules from `references/skill-mapping.md`.
5. **Fallback**: If no skills are found (empty glob), log a warning and skip Steps 2 and 6 entirely — all specs will get `skill: none`.

### Step 3: Read Plan Documents

Load the following files. Warn if any are missing but continue with what exists:

| File | Role | Required? |
|------|------|-----------|
| `<plan-dir>/ROADMAP.md` | Primary input — phases, steps, dependencies | **Yes** (abort if missing) |
| `<plan-dir>/PRD.md` | Product requirements context | No |
| `<plan-dir>/TDD.md` | Technical design context | No |
| `<plan-dir>/STANDARDS.md` | Coding standards context | No |
| `<plan-dir>/COMMON-DECISIONS.md` | Cross-cutting decisions | No |
| `<plan-dir>/adr/*.md` | Architecture Decision Records | No |

Additionally, scan every loaded document for `reference_file` directives. These appear as blockquote lines matching the pattern:

```
> **Best Practices**: `reference_file = <path>`
```

Build a **reference file registry** keyed by source location:
- **ROADMAP phases**: Associate the `reference_file` with the phase number it appears under (between `## Phase N:` header and the step table).
- **ADR files**: Associate the `reference_file` with the ADR filename.
- **TDD / STANDARDS sections**: Associate the `reference_file` with the section heading it appears under.

A single phase or document may contain multiple `reference_file` directives.

### Step 4: Parse ROADMAP Structure

Extract the ROADMAP into a structured representation:

#### Phase Format
```
## Phase N: Name
```

#### Step Table Format (inside code blocks)
```text
Step  File                          Depends On  Description
N.M   path/to/file.ext              ...         What this step does
```

#### Columns
| Column | Content |
|--------|---------|
| `Step` | `{phase}.{step}` number (e.g., `1.4`, `5.2`) |
| `File` | Target file path |
| `Depends On` | Dependency notation (see below) |
| `Description` | Human-readable description |

#### Dependency Notation
| Notation | Meaning | Example |
|----------|---------|---------|
| `-` | No dependencies | Step can start immediately |
| `N.M` | Single dependency | Depends on step N.M |
| `N.M,N.K` | Multiple dependencies | Depends on steps N.M and N.K |
| `N.M-N.K` | Range of dependencies | `0.3-0.7` expands to `0.3, 0.4, 0.5, 0.6, 0.7` |
| `N.M,N.K-N.J` | Mixed | Combine individual and range |

#### Gate Criteria
The line after each code block starting with `**Gate**:` contains the phase completion criteria. Capture this for each phase.

#### Phase-Level Reference Files
If the text between a `## Phase N:` header and its step table contains one or more `reference_file` directives (from the registry built in Step 3), record them as `reference_files` for that phase. Every step in the phase inherits these references.

### Step 5: Classify Each Step

Use the `product-issues` 5-type classification system. Apply signal words first, then file-path heuristics as tiebreaker.

#### Signal Words (check Description field)

| Type | Signal Words |
|------|-------------|
| `feature` | "add", "create", "new", "implement", "build" |
| `bug` | "error", "fail", "broken", "fix", "patch" |
| `chore` | "update", "configure", "migrate", "dependencies", "upgrade" |
| `refactor` | "clean", "reorganize", "improve code", "restructure" |
| `perf` | "slow", "optimize", "performance", "speed up" |

#### File-Path Heuristics (check File field)

| Pattern | Likely Type |
|---------|-------------|
| Page / route files (e.g., `page.tsx`, `page.ts`) | `feature` |
| API endpoints, UI components, domain models, service clients | `feature` |
| `__init__.py`, package markers | `chore` |
| `.env`, `.env.local`, `.env.*` | `chore` |
| `Dockerfile`, `docker-compose.*` | `chore` |
| Dependency manifests (`requirements.txt`, `package.json`, `go.mod`) | `chore` |
| Build/tool config (`tsconfig.json`, `tailwind.config.*`, etc.) | `chore` |
| Config files (`.yml`, `.yaml`, `.toml`, `.json` in root/infra) | `chore` |

#### Fallback Rules
- If no signal words or heuristics match clearly:
  - Infrastructure / config / setup files → `chore`
  - Everything else → `feature`

### Step 6: Map Steps to Skills

Using the skill inventory from Step 2 and the mapping rules from `references/skill-mapping.md`, assign a skill to each ROADMAP step.

#### Mapping Process

For each step parsed in Step 4, apply the matching algorithm (first match wins):

1. **Trivial detection**: Check if the file matches trivial patterns (`.env*`, "environment variables" descriptions). If so → `skill: none`. For `__init__.py` files → `skill: create-init-file`.
2. **File-path pattern**: Match the step's File column against the file-path rule tables. If a rule matches → use that skill name.
3. **Description keyword**: Check the Description column against the keyword fallback table. If keywords match → use that skill name.
4. **Phase-level default**: Apply the phase category default for the step's phase.
5. **Gap**: If nothing matches → `skill: gap:<suggested-name>`.

#### Recording Results

For each step, record one of:
- `skill: <skill-name>` — a matching installed skill exists
- `skill: none` — trivial file, no skill needed
- `skill: gap:<suggested-name>` — no matching skill, needs creation

Additionally, record the **matched file-path rule** for each step (see `references/skill-mapping.md` "Recording the Matched Rule"). This serves as a grouping key in Step 6.5.

#### Gap Resolution: Inline Skill Creation

After mapping all steps, collect all gaps and resolve them inline:

1. **Group gaps by similarity**: If multiple steps suggest the same gap skill, they share one creation action (same as before).
2. **Present gap summary to user** — display a table:

   | # | Gap Skill | Affected Steps | Description |
   |---|-----------|----------------|-------------|
   | 1 | `create-notification-handler` | 4.3, 4.5 | Handles notification dispatch |

   Ask: **"N skill gap(s) detected. Create these skills inline? (Yes/No)"**
   - **Yes** → proceed to Step 6b (inline creation)
   - **No** → fall back to Legacy Gap Handling (see subsection below)

3. **Step 6b: Create each missing skill inline** — For each gap:
   a. **Assemble context**: Gather purpose from ROADMAP step descriptions, architectural patterns from TDD, conventions from STANDARDS, and identify the closest existing skill as a structural reference.
   b. **Read** `references/inline-skill-context-template.md` for structure guidance (line targets, naming patterns, cleanup checklist).
   c. **Run** `python3 .claude/skills/skill-creator/scripts/init_skill.py {gap-name} --path .claude/skills` to scaffold the skill directory.
   d. **Edit the generated SKILL.md**: Replace TODO frontmatter with synthesized `name` and `description`. Write a workflow-based body following the inline-skill-context-template (Overview, Input, Workflow steps, Conventions). Target under 80 lines — starter quality.
   e. **Delete unneeded example files**: Remove `scripts/example.py`, `references/api_reference.md`, `assets/example_asset.txt`. Delete empty `scripts/`, `references/`, `assets/` directories if the skill needs none.
   f. **Log**: Record each created skill (name, path, associated ROADMAP steps) for Step 8 reporting.

4. **Step 6c: Re-audit** — Perform a lightweight re-glob of `.claude/skills/*/SKILL.md`. Read only the frontmatter of newly created skills. Merge them into the skill inventory from Step 2.

5. **Step 6d: Re-map** — Re-process only the former `gap:<name>` entries through the matching algorithm. If the mapping algorithm doesn't match (unlikely since the skill was purpose-built), force-assign by name: if the gap was `gap:create-foo` and `.claude/skills/create-foo/SKILL.md` now exists, assign `skill: create-foo`.

6. **Step 6e: Verify zero gaps** — Confirm all former gaps now have `skill: <name>` assignments. If any remain, apply per-gap fallback (see Edge Cases).

#### Legacy Gap Handling (Fallback)

Preserved for when the user declines inline creation or as per-gap fallback when inline creation fails:

1. **Generate skill-creation specs** with:
   - Filename: `chore-{XXX}-create-skill-{gap-name}.md` (skill-creation specs are numbered first, starting from 001)
   - Type: `chore` (use the product-issues chore template)
   - Metadata: `skill: skill-creator`
   - Content: describe the skill to create, reference the `skill-creator` skill, list which ROADMAP steps need this skill
2. **Update gap references**: Change all `skill: gap:<name>` entries to `skill: pending:chore-{XXX}-create-skill-{name}.md` so specs reference the prerequisite.

#### Skip Conditions
- If Step 2 was skipped (no skills found), skip this step — all specs get `skill: none`.
- If all steps are covered (no gaps), skip skill-creation spec generation.

### Step 6.5: Group Steps by Skill + File-Path Pattern

After all steps are mapped and gaps resolved, group steps sharing the **same skill AND same matched file-path rule** into batches. Each qualifying batch becomes a single grouped spec file.

#### Grouping Algorithm

1. **Build grouping key** for each step: `{skill}:{matched_rule}`.
   - `create-init-file:**/__init__.py`
   - `scaffold-ui-component:frontend/components/ui/**`
   - `scaffold-ui-component:frontend/components/domain/**` (different key — different pattern)
   - `scaffold-backend-service:backend/app/infrastructure/*.py`
   - `scaffold-backend-service:backend/app/routers/*.py` (different key)

2. **Exclude from grouping** (remain standalone):
   - Steps with `skill: none`
   - Steps where `matched_rule` is `keyword:*`, `phase-default`, `trivial`, or `none`
   - Singleton groups (only 1 step with that key)

3. **For each group with 2+ members**, create a group record:

   | Field | Value |
   |-------|-------|
   | `skill` | Shared skill name |
   | `matched_rule` | Shared file-path glob |
   | `steps` | All step numbers, sorted (e.g., `[2.1, 2.4, 3.1, 3.3, 5.1]`) |
   | `files` | All file paths, in step order |
   | `phase` | **Earliest** phase number among group members |
   | `type` | Majority type; if tied, use first member's type |
   | `depends_on` | Union of external dependencies (see below) |

4. **Cross-phase grouping allowed**: Steps from different phases may share a group. Assigned to earliest phase.

#### Dependency Resolution for Groups

1. **Collect** all `depends_on` from every group member.
2. **Remove internal deps**: If steps A and B are both in the group and A depends on B, drop it.
3. **Deduplicate** remaining external dependencies.
4. **Redirect incoming deps**: Any step outside this group that depended on a member step redirects to the grouped spec filename.

#### Group Naming

Derive a descriptive plural name from the common pattern:

| Skill + Pattern | Group Name |
|-----------------|-----------|
| `create-init-file:**/__init__.py` | `python-init-files` |
| `scaffold-ui-component:frontend/components/ui/**` | `base-ui-components` |
| `scaffold-chart-component:frontend/components/charts/**` | `chart-components` |
| `scaffold-ui-component:frontend/components/domain/**` | `domain-ui-components` |
| `scaffold-backend-service:backend/app/infrastructure/*.py` | `infrastructure-services` |
| `scaffold-backend-service:backend/app/routers/*.py` | `api-routers` |

Rules: kebab-case, plural form, derive from directory/pattern. If name collides with standalone spec, append `-group`.

#### Numbering

Grouped spec takes the **lowest original spec number** among its members. Numbering gaps are acceptable.

#### Output

After this step, the generation list is a mix of **grouped specs** and **standalone specs**. Both feed into Step 7.

### Step 7: Generate Spec Files in `<output-dir>/`

#### Pre-flight
1. Create `<output-dir>/` directory if it doesn't exist.
2. If spec files already exist in `<output-dir>/`, list them and **ask the user** before overwriting. Options:
   - Overwrite all
   - Skip existing
   - Abort

#### Generation Order
1. **If inline creation succeeded** (zero remaining gaps): Skip skill-creation specs entirely. Generate Phase 1+ specs directly.
2. **If legacy fallback was used** (gaps produced chore specs): Skill-creation specs first (Phase 0 prerequisites), then Phase 1+ specs in phase/step order.

#### Naming Convention
```
{type}-{XXX}-{name}.md
```

- `{type}` = `feature`, `bug`, `chore`, `refactor`, `perf`
- `{XXX}` = zero-padded 3-digit sequential number, globally unique (001–999)
- `{name}` = kebab-case, only lowercase `a-z`, `0-9`, hyphens

**Numbering order**:
1. **If inline creation succeeded**: Numbering starts at 001 with Phase 1 specs directly (no skill-creation spec prefix).
2. **If legacy fallback was used**: Skill-creation specs first (lowest numbers, starting from 001), then Phase 1+ specs in phase/step order after skill-creation specs.

**Deriving `{name}`**: Take the filename from the File column (without extension and directory), convert to kebab-case.
- `<backend-dir>/Dockerfile` → `backend-dockerfile`
- `<backend-dir>/routers/ingestion.py` → `ingestion`
- `<frontend-dir>/dashboard/page.tsx` → `dashboard-page`
- `<frontend-dir>/components/ui/button.tsx` → `button`
- `<frontend-dir>/components/domain/MetricCard.tsx` → `metric-card`
- `<frontend-dir>/components/charts/SLAChart.tsx` → `sla-chart`
- `infra/docker-compose.yml` → `docker-compose`
- `<backend-dir>/domain/models.py` → `domain-models`
- `<backend-dir>/infrastructure/database.py` → `database`
- `<backend-dir>/config.py` → `config`

For ambiguous names (e.g., multiple `__init__.py` files), include the parent directory for disambiguation:
- `<backend-dir>/app/__init__.py` → `app-init`
- `<backend-dir>/tests/__init__.py` → `tests-init`
- `<backend-dir>/app/infrastructure/__init__.py` → `infrastructure-init`
- `<backend-dir>/app/domain/__init__.py` → `domain-init`
- `<backend-dir>/app/routers/__init__.py` → `routers-init`

**Examples**:
- `chore-001-env.md`
- `chore-004-backend-dockerfile.md`
- `feature-025-ingestion.md`
- `feature-042-dashboard-page.md`
- `chore-010-app-init.md`
- `chore-001-create-skill-notification-handler.md` (skill-creation spec)

**Grouped spec naming**: For grouped specs (from Step 6.5):
- `{type}-{XXX}-{group-name}.md` where `{XXX}` is the lowest member's spec number.
- Examples: `chore-010-python-init-files.md`, `feature-033-base-ui-components.md`, `feature-016-infrastructure-services.md`

#### Content Generation

For each step (skipping Phase 0, except skill-creation specs):

1. **Select template**: Based on the type from Step 5, read the corresponding `product-issues` reference template.

2. **Fill template placeholders** using context from plan documents:

| Template Section | Source |
|-----------------|--------|
| Summary / User Story | ROADMAP step Description + PRD feature requirements |
| Context & Motivation | PRD problem statement, business context |
| Functional Requirements | PRD feature details, ROADMAP step Description |
| Acceptance Criteria (Gherkin) | Derive from ROADMAP gate criteria + step description |
| UI/UX Requirements | PRD UI requirements (for frontend features) |
| Success Metrics | PRD success metrics (if applicable) |
| Out of Scope | Other steps in the same phase that are NOT this step |
| Dependencies | ROADMAP `Depends On` column — list dependent spec filenames |
| Skill Reference | Step 6 mapping — which skill to use for implementation |
| Open Questions | Flag anything unclear from the plan docs |

3. **Content rules**:
   - Follow the `product-issues` convention: focus on WHAT and WHY, not HOW
   - Do NOT include technical implementation details, file paths in the spec body, or code architecture decisions
   - Acceptance criteria must be in Gherkin format
   - Dependencies section should reference other spec filenames (e.g., "Depends on: `chore-003-requirements-txt.md`")
   - Each spec should be self-contained — a reader should understand the task without reading other specs
   - **Skill note in Summary**: If mapped to a skill, include: "Implementation uses the `{skill-name}` skill."
   - **Inline-created skill note in Summary**: If mapped to a skill that was created inline during this run, include: "Implementation uses the `{skill-name}` skill (created inline during task generation)."
   - **Reference file note in Summary**: If the spec has `reference_files`, include: "Best practices reference: `<path>` — follow patterns defined in this document."  For multiple references, list each on its own line.
   - **Gap note in Summary** (legacy fallback only): If mapped to a gap, include: "Requires creating the `{gap-name}` skill first (see `chore-{XXX}-create-skill-{gap-name}.md`)."

5. **Grouped spec content rules**:
   - **Summary**: Describe the batch purpose, not individual files.
   - **File listing**: Include a bullet list of all files with ROADMAP step references.
   - **Acceptance Criteria**: Cover the batch as a whole.
   - **Dependencies**: Only external deps (union, internal removed).
   - **Out of Scope**: Steps NOT in this group, even if same skill but different pattern.

4. **Add a metadata header** at the top of each spec file:

   **Standalone spec** (unchanged):
   ```md
   ---
   spec: {XXX}
   type: {type}
   phase: {phase-number}
   step: {step-number}
   file: {file-path-from-roadmap}
   depends_on: [{comma-separated-step-numbers}]
   skill: {skill-name|none|pending:chore-{XXX}-create-skill-{name}.md}
   reference_files: [{comma-separated-paths}]
   ---
   ```

   **Grouped spec** (plural keys):
   ```md
   ---
   spec: {XXX}
   type: {type}
   phase: {phase-number}
   steps: [{comma-separated-step-numbers}]
   files: [{comma-separated-file-paths}]
   depends_on: [{external-only-step-numbers}]
   skill: {skill-name}
   reference_files: [{comma-separated-paths}]
   ---
   ```

   Note: `steps` (was `step`) and `files` (was `file`). Grouped `depends_on` excludes internal dependencies.

   - **`reference_files`**: If the step's phase has associated `reference_file` entries (from Step 4), include them as a list. Omit the field entirely if no references apply.

> **Note**: When inline skill creation succeeds, no `pending:` values appear — all former gaps become direct `skill: <name>` references. The `pending:` format only appears when using the legacy fallback path.

### Step 8: Generate `<output-dir>/EXECUTION.md`

Generate `<output-dir>/EXECUTION.md` using the template at `references/execution-template.md`.

#### Parallel Grouping Algorithm

For each phase (starting from Phase 1):

1. **Group 1**: Steps with no unresolved intra-phase dependencies (either no dependencies, or all dependencies are in prior phases).
2. **Group 2**: Steps whose intra-phase dependencies are all in Group 1.
3. **Group 3**: Steps whose intra-phase dependencies are all in Groups 1-2.
4. Continue until all steps in the phase are placed.

"Intra-phase dependency" = a dependency on another step within the same phase. Cross-phase dependencies are always resolved (prior phases complete before the next begins).

#### Content
- Summary table with phase name, spec count (post-grouping), number of parallel groups, and **skill gaps count** (`0` when inline creation succeeded)
- **Inline-Created Skills section** (if skills were created inline in Step 6b): Table documenting each created skill — name, path, associated ROADMAP steps, and quality note ("starter quality — may benefit from iteration")
- **Skill Prerequisites section** (legacy fallback only — if gaps produced chore specs): table of skill-creation specs as a prerequisite block before Phase 1
- Per-phase sections with parallel group tables **including a Skill column**
  - Column header: `File(s)` (not `File`)
  - For grouped specs: show `N files (pattern)` in the File(s) column (e.g., `5 files (**/__init__.py)`)
  - For standalone specs: show the single file path as before
- Gate criteria per phase (from ROADMAP)
- Dependency graph overview (which phases depend on which)
- A grouped spec spanning multiple phases is placed in the earliest phase for parallel-group analysis

## Edge Cases

### Missing Files
- **ROADMAP missing**: Abort with clear error message. This file is required.
- **PRD/TDD/STANDARDS missing**: Warn and continue. Fill template sections with `[Context not available — to be filled manually]`.
- **ADR files missing**: Continue without ADR references.
- **product-issues skill missing**: Fall back to `<output-dir>/README.md`, then to minimal spec format.

### Existing Specs
- If `<output-dir>/` already contains `.md` files, **always ask before overwriting**.
- Offer three options: overwrite all, skip existing, abort.
- Never silently overwrite existing work.

### Ambiguous Classification
- If a step could reasonably be classified as two types, prefer the type that better matches the `product-issues` signal words.
- `__init__.py` files are always `chore` regardless of description.
- Package markers, config files, and environment files are always `chore`.

### Phase 0 Handling
- Skip Phase 0 by default — these are documentation steps that serve as inputs to this skill.
- If the user explicitly requests Phase 0 specs, generate them as `chore` type.
- **When inline creation succeeded**: No skill-creation specs exist — numbering starts at 001 with Phase 1.
- **When legacy fallback was used**: Skill-creation specs are numbered sequentially starting from 001 (before Phase 1+ specs) and are **not** skipped — they are prerequisites.

### Empty Phases
- If a phase has no steps after filtering, skip it in EXECUTION.md.

### Dependency Validation
- If a step references a dependency that doesn't exist in the ROADMAP, warn but continue.
- Include a note in that spec's Dependencies section: `[Warning: Step X.Y referenced but not found in ROADMAP]`.

### No Installed Skills
- If the glob in Step 2 returns no skill files, skip Steps 2 and 6 entirely.
- All specs get `skill: none` in their metadata.
- EXECUTION.md omits the Skill column and Skill Prerequisites section.

### All Steps Covered
- If every step maps to an installed skill or `none`, no skill-creation specs are generated and no inline creation is needed.
- The user prompt in Step 6 is skipped entirely.
- EXECUTION.md summary shows `Skill Gaps: 0` for all phases.

### Multiple Steps Share One Gap
- If multiple ROADMAP steps map to the same gap skill, they share **one** inline creation action (or one skill-creation spec in legacy mode).
- All those steps reference the same skill after creation.

### Inline Creation Failure
- If `init_skill.py` fails or SKILL.md editing fails for a specific gap, fall back to chore-spec for **that gap only**.
- Other successfully created skills are preserved and mapped normally.
- EXECUTION.md includes both the "Inline-Created Skills" section (for successes) and the "Skill Prerequisites" section (for the failed gap's chore spec).

### Re-audit No Match
- If the re-audit in Step 6c finds the new skill but the re-map in Step 6d doesn't match it through the normal algorithm, **force-assign by name**: if the gap was `gap:create-foo` and `.claude/skills/create-foo/SKILL.md` exists, assign `skill: create-foo`.
- This is expected since inline-created skills are purpose-built for specific gaps.

### User Declines Inline Creation
- If the user answers "No" to the inline creation prompt, fall back entirely to legacy gap handling.
- Behavior is identical to the original workflow: chore specs are generated, numbering starts with skill-creation specs, EXECUTION.md includes "Skill Prerequisites" section.

### Mixed Results (Partial Inline Success)
- If some gaps are created inline successfully and others fail, both paths coexist:
  - Successfully created skills get `skill: <name>` assignments.
  - Failed gaps get `skill: pending:chore-{XXX}-create-skill-{name}.md` assignments.
  - Numbering: chore specs for failed gaps get the lowest numbers (starting from 001), followed by Phase 1+ specs.
  - EXECUTION.md includes both "Inline-Created Skills" and "Skill Prerequisites" sections.

### Grouped Spec Dependencies
- External step depending on ANY group member → redirect to grouped spec filename.
- Cross-group dependencies preserved between grouped spec filenames.

### Mixed Types in a Group
- Majority type wins. If tied, earliest member's type.

### Group Name Collisions
- Append `-group` suffix if name collides with standalone spec.

### Single-Member Groups
- Not grouped. Remain standalone with singular frontmatter.

### Cross-Phase Group Placement
- Assigned to earliest phase. Other phases may lose specs or become empty (existing "Empty Phases" edge case applies).

## References

- **Execution template**: `references/execution-template.md`
- **Skill mapping rules**: `references/skill-mapping.md`
- **Inline skill context template**: `references/inline-skill-context-template.md`
- **Spec templates**: `.claude/skills/product-issues/reference/{type}.md`
- **Classification logic**: `.claude/skills/product-issues/SKILL.md`
- **Skill creator script**: `.claude/skills/skill-creator/scripts/init_skill.py`
- **Skill creator guide**: `.claude/skills/skill-creator/SKILL.md`
- **Plan documents**: `<plan-dir>/` directory
