# Expertise File Structure Documentation

## Overview

Expertise files are the "mental models" of agent experts - compressed YAML representations that serve as persistent memory across agent executions. They enable the REUSE → ACT → LEARN loop that makes agents self-improving.

**Purpose**: Document system knowledge in a structured, compressed format that agents can:
- **Reuse**: Load at start to avoid re-learning
- **Validate**: Check against current codebase
- **Update**: Self-improve after each task

**File Format**: YAML (preferred) or JSON
**Max Size**: 1000 lines (strictly enforced)
**Naming**: `expertise.yaml` (standard)
**Location**: `.claude/commands/experts/{expert_name}/expertise.yaml`

---

## Complete YAML Schema

### Full Template Structure

```yaml
overview:
  description: "One-sentence description of what this expert covers"
  key_files:
    - "path/to/main/file1.py"
    - "path/to/main/file2.py"
  total_files: 15
  last_updated: "2026-02-03"

core_implementation:
  component_name_1:
    location: "path/to/component.py"
    description: "What this component does"
    key_classes:
      - name: "ClassName"
        line_start: 10
        line_end: 150
        purpose: "Core responsibility"
        key_methods:
          - name: "method_name"
            line_start: 45
            line_end: 78
            signature: "def method_name(self, arg1: str, arg2: int) -> bool"
            logic: "High-level what it does (not line-by-line)"
            dependencies: ["OtherClass", "external_lib"]
    key_functions:
      - name: "standalone_function"
        line_start: 200
        line_end: 250
        signature: "def standalone_function(config: Config) -> Result"
        logic: "What it does and why"

  component_name_2:
    location: "path/to/another_component.py"
    description: "Another component's purpose"
    key_classes:
      - name: "AnotherClass"
        line_start: 20
        line_end: 180
        purpose: "Specific responsibility"
        key_methods:
          - name: "another_method"
            line_start: 55
            line_end: 88
            signature: "def another_method(self, data: dict) -> str"
            logic: "What this method accomplishes"
            dependencies: ["json", "pathlib"]

schema_structure:  # Optional: for database/API experts
  tables:
    - name: "table_name"
      primary_key: "id"
      columns: ["col1", "col2", "col3"]
      relationships:
        - table: "related_table"
          type: "one_to_many"
          foreign_key: "related_id"
  views:
    - name: "view_name"
      query_logic: "Aggregates X from Y"
  migrations:
    - version: "001"
      description: "Initial schema"
      file: "migrations/001_initial.sql"

key_operations:
  operation_category_1:
    description: "What this category handles"
    files:
      - "path/to/file1.py"
      - "path/to/file2.py"
    workflow: |
      1. Step one happens
      2. Step two follows
      3. Final step completes
    patterns:
      - "Pattern A: Use when X"
      - "Pattern B: Use when Y"
    examples:
      - description: "Example use case"
        code_reference: "file.py:100-150"

  operation_category_2:
    description: "Another operational category"
    files: ["path/to/orchestrator.py"]
    workflow: |
      1. Initialization
      2. Processing
      3. Cleanup
    error_handling:
      - scenario: "When X fails"
        action: "Do Y"

integration_points:  # Optional: for systems with external dependencies
  external_services:
    - name: "ServiceName"
      purpose: "What it provides"
      connection: "How we connect (API, SDK, etc)"
      key_operations: ["op1", "op2"]
  internal_dependencies:
    - component: "ComponentName"
      imports: ["import1", "import2"]
      usage: "How this expert uses it"

best_practices:
  dos:
    - "Do X when Y condition"
    - "Always Z before W"
    - "Prefer A over B for performance"
  donts:
    - "Avoid X because Y consequence"
    - "Never Z without W validation"
  patterns:
    - pattern: "Pattern name"
      when: "Use this when..."
      example: "file.py:200-220"

known_issues:
  - issue: "Description of the problem"
    workaround: "Solution or mitigation"
    tracking: "Issue #123 or TODO comment location"
  - issue: "Another known limitation"
    workaround: "Current approach"
    tracking: "file.py:450 comment"

recent_changes:
  - date: "2026-02-03"
    description: "What changed and why"
    files: ["file1.py", "file2.py"]
    impact: "How it affects the system"
  - date: "2026-02-01"
    description: "Previous change"
    files: ["file3.py"]
    impact: "Impact description"
  # Keep only 5 most recent entries

constraints:
  technical:
    - "Must support Python 3.10+"
    - "Max response time: 500ms"
  architectural:
    - "Follow DDD pattern"
    - "No direct database access from domain layer"
  security:
    - "All inputs must be validated"
    - "Use parameterized queries only"
```

---

## Section Descriptions

### 1. Overview (Required)

**Purpose**: High-level system summary for quick context loading

```yaml
overview:
  description: "Concise one-sentence description"
  key_files: ["most", "important", "files.py"]
  total_files: 15  # Approximate count in scope
  last_updated: "2026-02-03"  # Always update on self-improve
```

**Guidelines**:
- `description`: 1 sentence, no jargon, clear scope
- `key_files`: Top 3-5 files, full paths from repo root
- `total_files`: Rough count, helps assess scope
- `last_updated`: ISO date format (YYYY-MM-DD)

### 2. Core Implementation (Required)

**Purpose**: Document main components with precise line numbers

```yaml
core_implementation:
  component_logical_name:
    location: "path/to/file.py"
    description: "What this component does"
    key_classes:
      - name: "ClassName"
        line_start: 10
        line_end: 150
        purpose: "Why this class exists"
        key_methods:
          - name: "method_name"
            line_start: 45
            line_end: 78
            signature: "Full function signature"
            logic: "High-level logic explanation"
            dependencies: ["what", "it", "uses"]
    key_functions:
      - name: "standalone_func"
        line_start: 200
        line_end: 250
        signature: "Full signature"
        logic: "What it does"
```

**Guidelines**:
- Use **logical component names** (not just filenames)
- **Always include line numbers** for quick navigation
- `signature`: Full function/method signature for reference
- `logic`: High-level "what and why", not line-by-line
- `dependencies`: Other classes, modules, external libs

### 3. Schema Structure (Optional)

**Purpose**: Document data structures for database/API experts

```yaml
schema_structure:
  tables:
    - name: "users"
      primary_key: "id"
      columns: ["id", "email", "created_at"]
      relationships:
        - table: "orders"
          type: "one_to_many"
          foreign_key: "user_id"
  views:
    - name: "user_stats"
      query_logic: "Aggregates order counts per user"
  migrations:
    - version: "003"
      description: "Added user_stats view"
      file: "migrations/003_user_stats.sql"
```

**Use for**: Database, API, configuration, data model experts

### 4. Key Operations (Required)

**Purpose**: Document how things work end-to-end

```yaml
key_operations:
  template_registration:
    description: "How templates are registered and rendered"
    files:
      - "scaffold_service.py"
      - "template_loader.py"
    workflow: |
      1. ScaffoldService loads config
      2. _add_templates() registers via plan.add_file()
      3. render_template() processes .j2 files
      4. Output written to target directory
    patterns:
      - "Use skip_if_exists for seed files"
      - "Use create for generated files"
    examples:
      - description: "Expert template registration"
        code_reference: "scaffold_service.py:150-200"
```

**Guidelines**:
- Group related operations logically
- `workflow`: Step-by-step process (numbered)
- `patterns`: Common patterns used
- `examples`: Concrete code references with line numbers

### 5. Integration Points (Optional)

**Purpose**: Document external dependencies and internal coupling

```yaml
integration_points:
  external_services:
    - name: "GitHub API"
      purpose: "Fetch issues and create PRs"
      connection: "REST API via gh CLI"
      key_operations: ["fetch_issue", "create_pr"]
  internal_dependencies:
    - component: "scaffold_service"
      imports: ["ScaffoldService", "ScaffoldPlan"]
      usage: "Used for template registration"
```

**Use for**: Experts covering systems with many dependencies

### 6. Best Practices (Optional but Recommended)

**Purpose**: Capture domain knowledge and conventions

```yaml
best_practices:
  dos:
    - "Use Typer for CLI commands"
    - "Follow DDD: domain → application → infrastructure"
  donts:
    - "Don't hardcode paths (use config variables)"
    - "Never skip template registration validation"
  patterns:
    - pattern: "Template registration"
      when: "Adding new commands or experts"
      example: "scaffold_service.py:200-220"
```

**Guidelines**:
- Keep entries actionable and specific
- Include "why" when not obvious
- Reference code examples with line numbers

### 7. Known Issues (Optional)

**Purpose**: Document limitations and workarounds

```yaml
known_issues:
  - issue: "Template paths must be relative to templates/"
    workaround: "Use pathlib to construct absolute paths"
    tracking: "TODO comment in scaffold_service.py:180"
  - issue: "YAML parsing fails on tabs"
    workaround: "Always use spaces for indentation"
    tracking: "Issue #456"
```

**Use for**: Active problems, edge cases, technical debt

### 8. Recent Changes (Optional but Recommended)

**Purpose**: Track evolution of the system

```yaml
recent_changes:
  - date: "2026-02-03"
    description: "Added TAC-13 expert templates"
    files: ["scaffold_service.py", "templates/claude/commands/experts/"]
    impact: "Enables self-improving agents in generated projects"
  - date: "2026-02-01"
    description: "Refactored template registration"
    files: ["scaffold_service.py"]
    impact: "Simplified addition of new template types"
```

**Guidelines**:
- Keep **only 5 most recent** entries
- Always update on self-improve runs
- Include impact for context

### 9. Constraints (Optional)

**Purpose**: Document hard requirements and limitations

```yaml
constraints:
  technical:
    - "Python 3.10+ required for match statements"
    - "Max file size: 1000 lines for expertise files"
  architectural:
    - "Follow DDD layers: domain/application/infrastructure/interfaces"
    - "Templates must use {{ config.* }} variables"
  security:
    - "Validate all user inputs"
    - "No secrets in templates (use .env)"
```

**Use for**: Non-negotiable requirements, compliance needs

---

## Real-World Examples

### Example 1: CLI Expert

```yaml
overview:
  description: "tac-bootstrap CLI for generating agentic layers"
  key_files:
    - "tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py"
    - "tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py"
  total_files: 8
  last_updated: "2026-02-03"

core_implementation:
  cli_interface:
    location: "tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py"
    description: "Typer CLI commands"
    key_functions:
      - name: "init"
        line_start: 25
        line_end: 45
        signature: "def init(name: str, language: Optional[str] = None)"
        logic: "Creates new project with wizard or options"
      - name: "add_agentic"
        line_start: 50
        line_end: 80
        signature: "def add_agentic(dry_run: bool = False)"
        logic: "Adds agentic layer to existing project"

  scaffold_service:
    location: "tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py"
    description: "Core template rendering and file generation"
    key_classes:
      - name: "ScaffoldService"
        line_start: 15
        line_end: 300
        key_methods:
          - name: "_add_claude_code_commands"
            line_start: 150
            line_end: 200
            logic: "Registers all command templates for rendering"
          - name: "render_template"
            line_start: 220
            line_end: 250
            logic: "Renders Jinja2 template with config variables"

key_operations:
  template_registration:
    description: "How templates are registered and rendered"
    workflow: |
      1. ScaffoldService.__init__ loads config
      2. _add_claude_code_commands() registers templates via plan.add_file()
      3. Each template gets: action, template path, reason
      4. render_template() processes .j2 files with config variables
    files:
      - "scaffold_service.py"
    patterns:
      - "Use skip_if_exists for seed files"
      - "Use create for generated files"

best_practices:
  dos:
    - "Use Typer for CLI command definitions"
    - "Follow DDD architecture layers"
  patterns:
    - pattern: "Template registration"
      when: "Adding new templates"
      example: "scaffold_service.py:150-200"
```

### Example 2: ADW Expert

```yaml
overview:
  description: "AI Developer Workflows for SDLC automation"
  key_files:
    - "adws/adw_sdlc_iso.py"
    - "adws/adw_modules/workflow_ops.py"
    - "adws/adw_modules/state.py"
  total_files: 12

core_implementation:
  state_management:
    location: "adws/adw_modules/state.py"
    key_classes:
      - name: "ADWState"
        line_start: 20
        line_end: 150
        key_methods:
          - name: "save"
            line_start: 80
            logic: "Persists state to .adw_state.json"
          - name: "load"
            line_start: 95
            logic: "Loads state from previous run"

  workflow_orchestration:
    location: "adws/adw_modules/workflow_ops.py"
    key_functions:
      - name: "run_phase"
        line_start: 50
        line_end: 100
        logic: "Executes workflow phase (clarify/plan/build/test/review/ship)"
      - name: "detect_relevant_docs"
        line_start: 200
        line_end: 300
        logic: "TAC-9 integration: auto-detects ai_docs to load"

key_operations:
  sdlc_workflow:
    description: "Full SDLC automation workflow"
    workflow: |
      1. Fetch issue from GitHub
      2. Detect relevant docs (TAC-9)
      3. Clarify requirements
      4. Plan implementation
      5. Build with /build_w_report (TAC-10)
      6. Test
      7. Review
      8. Document
      9. Ship (commit, PR, merge)
    files:
      - "adw_sdlc_iso.py"
      - "adw_sdlc_zte_iso.py"
```

### Example 3: Commands Expert

```yaml
overview:
  description: "Slash command structure and patterns"
  key_files:
    - ".claude/commands/*.md"
  total_files: 25+

core_implementation:
  command_structure:
    description: "Standard slash command file format"
    components:
      yaml_frontmatter:
        required_fields:
          - allowed-tools: "List of tool names"
          - description: "One-line description"
          - argument-hint: "[arg1] [arg2]"
        optional_fields:
          - model: "sonnet|opus|haiku"
      markdown_sections:
        - "## Purpose"
        - "## Variables"
        - "## Instructions"
        - "## Workflow"
        - "## Report"

  variable_injection:
    patterns:
      dynamic_variables:
        - "$1, $2, $3": "Positional arguments"
        - "$ARGUMENTS": "All arguments as string"
      static_variables:
        - "{{ config.project.name }}": "From config.yml"
        - "{{ config.commands.test }}": "Command definitions"

key_operations:
  command_creation:
    workflow: |
      1. Define YAML frontmatter
      2. Document purpose
      3. List variables with defaults
      4. Write workflow steps (numbered)
      5. Define report format
    examples:
      - description: "Simple read-only command"
        code_reference: ".claude/commands/question.md"
      - description: "Build command with subagents"
        code_reference: ".claude/commands/build.md"

best_practices:
  dos:
    - "Use argument-hint to document expected arguments"
    - "Number workflow steps for clarity"
  donts:
    - "Don't use complex Jinja2 logic in command files"
```

---

## Best Practices

### General Guidelines

1. **Compression over Completeness**
   - Max 1000 lines strictly enforced
   - High-level logic, not line-by-line code
   - Reference code, don't duplicate it

2. **Precision Matters**
   - Always include accurate line numbers
   - Update line numbers on every self-improve
   - Invalid line numbers = broken agent context

3. **Structured Over Free-Form**
   - YAML preferred over JSON (more compact)
   - Follow schema structure consistently
   - Use nested structure for organization

4. **Self-Validate**
   - Agents should check against actual code
   - Don't assume expertise is current
   - Update on every significant change

5. **Recent Changes Only**
   - Keep only 5 most recent entries
   - Older history is in git, not expertise

### Writing Logic Descriptions

**Good** (High-level, purpose-driven):
```yaml
logic: "Validates config schema and loads defaults from templates directory"
```

**Bad** (Too detailed, line-by-line):
```yaml
logic: "Reads config file, parses YAML, iterates keys, checks types, loads template files, merges defaults"
```

### Updating Line Numbers

Always update line numbers when code changes:

```yaml
# Before (outdated)
key_methods:
  - name: "render"
    line_start: 150
    line_end: 200

# After code refactor moved it
key_methods:
  - name: "render"
    line_start: 180  # Updated
    line_end: 230    # Updated
```

### Handling Large Systems

For systems with many files, prioritize:

1. **Entry points** (main functions, CLI commands)
2. **Core logic** (business rules, algorithms)
3. **Integration points** (APIs, databases, external services)
4. **Common patterns** (how things are typically done)

Skip:
- Utility functions (unless domain-specific)
- Generated code
- Test files (unless testing patterns are critical)
- Boilerplate

---

## Constraints and Validation

### Hard Constraints (Enforced by Self-Improve)

1. **Max 1000 lines**
   - Self-improve will fail if exceeded
   - Remove oldest `recent_changes` entries first
   - Compress verbose descriptions

2. **Valid YAML**
   - Must parse without errors
   - Use YAML validators before committing
   - Consistent indentation (2 spaces)

3. **Required Sections**
   - `overview` (always required)
   - `core_implementation` (always required)
   - `key_operations` (always required)

4. **Date Format**
   - ISO 8601: `YYYY-MM-DD`
   - Example: `2026-02-03`

### Validation Checklist

Before committing expertise.yaml:

```bash
# 1. Valid YAML
yamllint expertise.yaml

# 2. Line count under 1000
wc -l expertise.yaml

# 3. Has required sections
grep -q "^overview:" expertise.yaml && echo "✓ Has overview"
grep -q "^core_implementation:" expertise.yaml && echo "✓ Has core_implementation"
grep -q "^key_operations:" expertise.yaml && echo "✓ Has key_operations"

# 4. Line numbers reference real code
# (Manual check: open files and verify line_start/line_end)

# 5. Date format correct
grep "last_updated:" expertise.yaml | grep -E "[0-9]{4}-[0-9]{2}-[0-9]{2}"
```

---

## When to Use Each Section

### Always Use
- `overview`: Every expertise file
- `core_implementation`: Every expertise file
- `key_operations`: Every expertise file

### Use When Applicable
- `schema_structure`: Database, API, config experts
- `integration_points`: Systems with many dependencies
- `best_practices`: Experts with domain conventions
- `recent_changes`: All experts (keeps context)

### Optional/Rare
- `known_issues`: Only for active problems
- `constraints`: Only when constraints are critical

---

## Self-Improve Integration

Expertise files are updated automatically through the 7-phase self-improve workflow:

1. **Phase 1**: Git diff analysis (identify changed files)
2. **Phase 2**: Review current expertise
3. **Phase 3**: Validate against codebase
4. **Phase 4**: Detect discrepancies
5. **Phase 5**: Surgical updates (use Edit tool)
6. **Phase 6**: Line limit enforcement (compress if needed)
7. **Phase 7**: Final validation

**Key points**:
- Self-improve **never overwrites** entire file
- Uses **Edit tool** for surgical updates
- **Validates** line numbers against actual code
- **Enforces** 1000 line limit
- **Updates** `last_updated` timestamp

---

## Template for New Experts

Use this minimal template to bootstrap new expertise files:

```yaml
overview:
  description: "[One sentence: what this expert covers]"
  key_files: []
  total_files: 0
  last_updated: "2026-02-03"

core_implementation:
  # To be populated by first self-improve run

key_operations:
  # To be populated by first self-improve run

best_practices:
  # To be populated as patterns emerge

recent_changes:
  - date: "2026-02-03"
    description: "Initial expertise file created"
    files: []
    impact: "Starting point for agent learning"
```

Then run: `/experts:{name}:self-improve false`

---

## Common Patterns

### Pattern 1: Template Registration

```yaml
key_operations:
  template_registration:
    description: "How new templates are registered"
    workflow: |
      1. Create .j2 template in templates/ directory
      2. Add registration in scaffold_service.py
      3. Use plan.add_file(action, template, path, reason)
      4. Test with dry-run mode
    files:
      - "scaffold_service.py"
    patterns:
      - "skip_if_exists: For seed files that shouldn't overwrite"
      - "create: For generated files"
```

### Pattern 2: Workflow Orchestration

```yaml
key_operations:
  phase_execution:
    description: "How workflow phases are executed"
    workflow: |
      1. Load state from previous run
      2. Execute phase-specific operations
      3. Update state with results
      4. Save state for next phase
    files:
      - "workflow_ops.py"
      - "state.py"
    error_handling:
      - scenario: "Phase fails"
        action: "Save error state and exit gracefully"
```

### Pattern 3: Command Structure

```yaml
core_implementation:
  command_format:
    description: "Standard slash command structure"
    components:
      frontmatter:
        - "allowed-tools: [Read, Write, Edit]"
        - "description: One-line purpose"
      sections:
        - "## Purpose: Why this command exists"
        - "## Variables: Inputs and defaults"
        - "## Workflow: Numbered steps"
        - "## Report: Output format"
```

---

## Version History

- **v1.0** (2026-02-03): Initial documentation for TAC-13 Task 2
- Complete YAML schema defined
- Real-world examples from CLI, ADW, Commands experts
- Best practices and constraints documented
- Self-improve integration explained

---

## Related Documentation

- [TAC-13: Agent Experts](Tac-13-agent-experts.md) - Core methodology
- [TAC-13: Implementation Plan](plan_tasks_tac_13.md) - Full 27-task plan
- [TAC-13: Dual Strategy](TAC-13_dual_strategy_summary.md) - Implementation approach
- [TAC-13: Status](TAC-13_implementation_status.md) - Current progress

---

## Quick Reference Card

```yaml
# Minimal viable expertise.yaml
overview:
  description: "What this covers"
  key_files: ["top", "3-5", "files.py"]
  total_files: N
  last_updated: "YYYY-MM-DD"

core_implementation:
  component_name:
    location: "path/to/file.py"
    key_classes:
      - name: "ClassName"
        line_start: N
        line_end: M
        key_methods:
          - name: "method"
            line_start: X
            line_end: Y
            signature: "def method(...)"
            logic: "What it does"

key_operations:
  operation_name:
    description: "What this does"
    workflow: |
      1. Step one
      2. Step two
    files: ["file.py"]

# Optional but recommended
best_practices:
  dos: ["Do X", "Always Y"]
  donts: ["Avoid Z"]

recent_changes:
  - date: "YYYY-MM-DD"
    description: "What changed"
    files: ["file.py"]
```

**Max 1000 lines | Valid YAML | Line numbers accurate | Update on every self-improve**
