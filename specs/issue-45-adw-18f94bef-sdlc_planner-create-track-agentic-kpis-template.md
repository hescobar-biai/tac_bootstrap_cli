# Feature: Create track_agentic_kpis.md.j2 Template

## Metadata
issue_number: `45`
adw_id: `18f94bef`
issue_json: `{"number":45,"title":"TAREA 4: Crear Template `track_agentic_kpis.md.j2`","body":"**Archivo a crear:** `tac_bootstrap/templates/claude/commands/track_agentic_kpis.md.j2`\n\n**Prompt:**\n```\nCrea el template Jinja2 para el comando slash /track_agentic_kpis.\n\nEste comando trackea los KPIs de Tactical Agentic Coding:\n1. SIZE: Trabajo delegable a agentes por ejecución\n2. ATTEMPTS: Iteraciones requeridas post-ejecución\n3. STREAK: Ejecuciones one-shot exitosas consecutivas\n4. PRESENCE: Tiempo humano requerido durante ejecución\n\nEl comando debe:\n1. Leer logs de ejecuciones anteriores en {{ config.paths.logs_dir }}\n2. Calcular métricas agregadas\n3. Mostrar tendencias (mejorando/empeorando)\n4. Sugerir acciones para mejorar KPIs\n\nUsa como referencia:\n- El comando existente en ../../.claude/commands/track_agentic_kpis.md\n- Documentación TAC en ai_docs/doc/\n\nOutput en formato tabla con Rich.\n```\n\n**Criterios de aceptación:**\n- [ ] Template renderiza sin errores\n- [ ] Define los 4 KPIs claramente\n- [ ] Incluye cálculo y visualización"}`

## Feature Description
This task involves creating a Jinja2 template for the `/track_agentic_kpis` slash command that will be generated when TAC Bootstrap creates an agentic layer for new projects. The template will provide a sophisticated command for tracking and analyzing the four core KPIs of Tactical Agentic Coding.

The track_agentic_kpis command template should:
- Track SIZE: Amount of delegable work per agent execution
- Track ATTEMPTS: Number of iterations required after execution
- Track STREAK: Consecutive successful one-shot executions
- Track PRESENCE: Human time required during execution
- Read execution logs from the configured logs directory
- Calculate aggregate metrics across all executions
- Display trends (improving/degrading performance)
- Suggest actionable improvements for KPI optimization
- Output results in formatted tables

This command is critical for helping teams measure and improve their agentic engineering practices over time.

## User Story
As a TAC Bootstrap user
I want a `/track_agentic_kpis` command template that tracks my agentic coding performance
So that generated agentic layers can help me measure and improve my use of agents over time

## Problem Statement
Tactical Agentic Coding (TAC) is built on measurable improvement through four key performance indicators. Without systematic tracking of these KPIs, teams cannot:
- Measure if their agentic practices are improving
- Identify bottlenecks in their agent workflows
- Benchmark their performance against best practices
- Demonstrate ROI from agentic engineering investments

The `/track_agentic_kpis` command needs to automate the collection, calculation, and visualization of these metrics from ADW (AI Developer Workflow) execution logs, making it effortless for teams to monitor their agentic performance.

## Solution Statement
Create a new Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/track_agentic_kpis.md.j2` that renders a comprehensive KPI tracking command. The template will:
- Parse ADW state JSON from execution logs
- Calculate the four core TAC KPIs with clear formulas
- Maintain both summary metrics (Agentic KPIs) and detailed metrics (ADW KPIs)
- Use Python for all numeric calculations to ensure accuracy
- Generate or update the `app_docs/agentic_kpis.md` file
- Display results in markdown tables
- Follow the exact structure and logic of the reference implementation in `.claude/commands/track_agentic_kpis.md`
- Use configuration variables from the `config` object for paths and settings

## Relevant Files
Files necessary for implementing the feature:

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/track_agentic_kpis.md.j2` - **New file to create**
- `.claude/commands/track_agentic_kpis.md` - **Reference implementation** (lines 1-125) - The existing command that defines the full logic
- `ai_docs/doc/Tac-8_1.md` - TAC course documentation on the agentic layer and KPIs
- `ai_docs/doc/Tac-8_2.md` - TAC course documentation on primitives and workflows
- `config.yml` - Shows the structure of config variables, particularly `paths.logs_dir` (line 21)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prepare_app.md.j2` - Reference for complex multi-step command patterns
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/install.md.j2` - Reference for structured command templates

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/track_agentic_kpis.md.j2` - The new template file

## Implementation Plan

### Phase 1: Template Foundation
Create the basic template structure with proper Jinja2 syntax and configuration variable references.

### Phase 2: KPI Logic Implementation
Implement the complete logic for parsing state data, calculating metrics, and updating the KPI tracking file.

### Phase 3: Validation & Testing
Verify template rendering and ensure all calculations follow the reference implementation.

## Step by Step Tasks
IMPORTANT: Execute each step in order.

### Task 1: Create track_agentic_kpis.md.j2 template file
- Create new file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/track_agentic_kpis.md.j2`
- Add header: `# Track Agentic KPIs`
- Add description explaining the four TAC KPIs:
  - SIZE: Work delegable to agents per execution
  - ATTEMPTS: Iterations required post-execution
  - STREAK: Consecutive one-shot successes
  - PRESENCE: Human time during execution
- Include reference to `app_docs/agentic_kpis.md` as the output file

### Task 2: Implement Variables section
- Define `state_json: $ARGUMENTS` to receive ADW state data
- Define `attempts_incrementing_adws: [adw_plan_iso, adw_patch_iso]` for workflows that increment attempt counters
- Use Jinja2 list syntax, not Python list syntax

### Task 3: Implement Instructions - Parse State Data
- Add section: "### 1. Parse State Data"
- Parse from state_json:
  - `adw_id`
  - `issue_number`
  - `issue_class`
  - `plan_file` path
  - `all_adws` list (contains workflow names run)

### Task 4: Implement Instructions - Calculate Metrics
- Add section: "### 2. Calculate Metrics"
- Add subsections:
  - Get current date/time using `date` command
  - Calculate Attempts: Count occurrences of attempts_incrementing_adws in all_adws using Python
  - Calculate Plan Size: Count lines in plan_file using `wc -l`, default to 0 if missing
  - Calculate Diff Statistics: Parse `git diff origin/main --shortstat` for files/lines changed
  - Format diff as "Added/Removed/Files" (e.g., "150/25/8")
- Emphasize: "IMPORTANT: Use Python to calculate the exact count value" with example command

### Task 5: Implement Instructions - Read Existing File
- Add section: "### 3. Read Existing File"
- Check if `app_docs/agentic_kpis.md` exists
- If exists: read and parse existing tables
- If not: prepare to create new file with both tables

### Task 6: Implement Instructions - Update ADW KPIs Table
- Add section: "### 4. Update ADW KPIs Table"
- Check if current adw_id exists in table
- If exists: update that row with new values
- If not: append new row at bottom
- Set Created date on new rows, Updated date on existing rows
- Use `date` command for timestamps

### Task 7: Implement Instructions - Calculate Agentic KPIs
- Add section: "### 5. Calculate Agentic KPIs"
- Include: "IMPORTANT: All calculations must be done using Python expressions. Use `python -c "print(expression)"` for every numeric calculation."
- Define calculations with Python examples:
  - Current Streak: Count consecutive rows from bottom where Attempts ≤ 2
  - Longest Streak: Find longest consecutive sequence where Attempts ≤ 2
  - Total Plan Size: Sum all plan sizes
  - Largest Plan Size: Maximum plan size
  - Total Diff Size: Sum all diff statistics (added + removed)
  - Largest Diff Size: Maximum diff (added + removed)
  - Average Presence: Average of all attempts, rounded to 2 decimals

### Task 8: Implement Instructions - Write Updated File
- Add section: "### 6. Write Updated File"
- Create/update `app_docs/agentic_kpis.md`
- Ensure proper markdown table formatting
- Include "Last Updated" timestamp using `date` command

### Task 9: Implement File Structure section
- Add section: "## File Structure"
- Provide complete markdown template for the output file:
  - Header: "# Agentic KPIs"
  - Description: "Performance metrics for the AI Developer Workflow (ADW) system."
  - Agentic KPIs table with 7 metrics
  - ADW KPIs table with detailed per-workflow metrics
- Use exact table structure from reference implementation

### Task 10: Implement Report section
- Add section: "## Report"
- Define output: 'Return only: "Updated app_docs/agentic_kpis.md"'

### Task 11: Validate template rendering
- Test template renders without Jinja2 syntax errors
- Verify all config variables are correctly referenced
- Ensure Python calculation examples are properly formatted
- Check table structures match the reference implementation
- Run validation commands

### Task 12: Run validation commands
- Execute: `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Execute: `cd tac_bootstrap_cli && uv run ruff check .`
- Execute: `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Execute: `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests
No specific unit tests needed for template files, but should verify:
- Template syntax is valid Jinja2
- Template renders with sample config data
- Rendered output contains all required sections
- Python calculation commands are syntactically correct

### Edge Cases
- Empty logs directory (no previous ADW executions)
- Missing plan_file in state_json
- ADW KPIs table doesn't exist yet (first run)
- Git diff returns no changes
- Division by zero in Average Presence calculation
- Config without `paths.logs_dir` defined

## Acceptance Criteria
- [ ] Template file created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/track_agentic_kpis.md.j2`
- [ ] Template renders without Jinja2 syntax errors
- [ ] All four TAC KPIs are clearly defined in the description
- [ ] Variables section includes state_json and attempts_incrementing_adws
- [ ] Instructions section has all 6 subsections (Parse, Calculate, Read, Update ADW, Calculate Agentic, Write)
- [ ] All calculations use Python commands as specified in reference implementation
- [ ] File Structure section provides complete markdown template for output
- [ ] Report section specifies exact output message
- [ ] Template uses `{{ config.paths.logs_dir }}` for log directory reference
- [ ] Template follows same structural pattern as reference implementation
- [ ] All validation commands pass without errors

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type checking
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The track_agentic_kpis command is one of the most complex slash commands in the agentic layer
- It implements a critical TAC pattern: measuring and improving agentic performance
- The reference implementation in `.claude/commands/track_agentic_kpis.md` should be followed exactly for the logic
- The template should be flexible enough to work with any project that has ADW execution logs
- This command helps teams move from "coding with agents" to "systematic agentic engineering"
- Future enhancement: Consider adding visualization with charts or graphs for trend analysis
- The KPI definitions come from Lesson 8 of the TAC course, which emphasizes prioritizing the agentic layer
- Consider this a "meta" command - it helps measure the effectiveness of the agentic layer itself
