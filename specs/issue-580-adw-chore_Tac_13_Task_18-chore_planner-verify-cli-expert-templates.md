# Chore: Verify CLI Expert Templates (Consolidation)

## Metadata
issue_number: `580`
adw_id: `chore_Tac_13_Task_18`
issue_json: `{"number": 580, "title": "[TAC-13] Task 18: Verify CLI expert templates (consolidation)", "body": "..."}`

## Chore Description

This is a **verification-only** consolidation task. The issue correctly identifies that CLI expert templates were already created in Tasks 4-6 using the dual strategy approach:

- ✅ Task 4: Created `question.md.j2`
- ✅ Task 5: Created `self-improve.md.j2`
- ✅ Task 6: Created `expertise.yaml.j2`

Initial investigation confirms:
- ✅ All 3 template files exist in `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/`
- ✅ Templates use Jinja2 variables (`{{ config.project.name }}`, etc.) correctly
- ✅ All templates registered in `scaffold_service.py` (lines 493, 495, 509-512)

However, registration patterns are inconsistent:
- ⚠️ `question.md` and `self-improve.md` registered in `expert_commands` list (lines 493, 495)
- ✅ `expertise.yaml` properly registered with `plan.add_file()` (lines 509-512)

**Main Task**: Verify all templates are correctly registered and functional. Fix any inconsistencies.

## Relevant Files

### Templates (Already Created)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/question.md.j2` - Question mode prompt (read-only queries)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2` - Self-improve 7-phase workflow
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/expertise.yaml.j2` - Expertise seed template

### Registration
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Template registration service (needs verification)

### Testing
- `tac_bootstrap_cli/tests/` - Unit tests directory

## Step by Step Tasks

### Task 1: Verify Template Files Exist and Quality
Run verification commands to confirm templates are present and well-formed:

```bash
# Check all 3 templates exist
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/question.md.j2 && echo "✓ question.md.j2"
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2 && echo "✓ self-improve.md.j2"
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/expertise.yaml.j2 && echo "✓ expertise.yaml.j2"

# Verify Jinja2 variable usage
grep -c "{{ config\." tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/question.md.j2
grep -c "{{ config\." tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2
grep -c "{{ config\." tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/expertise.yaml.j2

# Check frontmatter in command templates
head -10 tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/question.md.j2
head -10 tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2
```

Expected:
- All 3 files exist
- Multiple `{{ config.* }}` references in question and self-improve
- Valid YAML frontmatter in `.md.j2` files

### Task 2: Verify Template Registration Consistency
Read scaffold_service.py to understand registration patterns and verify CLI expert templates:

```bash
# Read the registration section
cat tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py | sed -n '490,515p'

# Check expert_commands list pattern
grep -A 5 "expert_commands.append" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py | grep "experts/cli"

# Verify how expert_commands list is processed
grep -A 10 "for cmd, reason in expert_commands" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
```

Verify:
- `question.md` and `self-improve.md` are in `expert_commands` list
- `expertise.yaml` is registered via `plan.add_file()`
- Expert commands list is properly processed to call `plan.add_file()`

### Task 3: Test Template Rendering
Verify templates can be rendered with actual config variables:

```bash
# Run CLI help to ensure it builds correctly
cd tac_bootstrap_cli && uv run tac-bootstrap --help

# Test scaffold generation (dry run if possible)
cd tac_bootstrap_cli && uv run python -m tac_bootstrap.interfaces.wizard --help
```

Expected:
- CLI runs without errors
- No Jinja2 template errors

### Task 4: Verify Generated Files Are Valid
If a test project exists, verify generated files:

```bash
# Check if templates generate valid files
# (This would require running scaffold in test mode)
# For now, verify template syntax only

# Validate Jinja2 syntax
python3 << 'EOF'
from jinja2 import Environment, FileSystemLoader
import os

templates_dir = "tac_bootstrap_cli/tac_bootstrap/templates"
env = Environment(loader=FileSystemLoader(templates_dir))

templates = [
    "claude/commands/experts/cli/question.md.j2",
    "claude/commands/experts/cli/self-improve.md.j2",
    "claude/commands/experts/cli/expertise.yaml.j2"
]

for tmpl in templates:
    try:
        env.get_template(tmpl)
        print(f"✓ {tmpl} - valid Jinja2 syntax")
    except Exception as e:
        print(f"✗ {tmpl} - ERROR: {e}")
EOF
```

Expected:
- All templates have valid Jinja2 syntax

### Task 5: Document Findings
Create a brief summary of verification results:

```bash
# Create verification report
cat > /tmp/task-18-verification.md << 'EOF'
# Task 18 Verification Report

## Templates Status
- ✅ question.md.j2: Exists, valid Jinja2, uses config variables
- ✅ self-improve.md.j2: Exists, valid Jinja2, uses config variables
- ✅ expertise.yaml.j2: Exists, valid Jinja2, minimal seed template

## Registration Status
- ✅ question.md: Registered via expert_commands list (line 493)
- ✅ self-improve.md: Registered via expert_commands list (line 495)
- ✅ expertise.yaml: Registered via plan.add_file() (lines 509-512)

## Issues Found
[List any issues discovered]

## Recommendations
[Any recommendations for improvement]
EOF

cat /tmp/task-18-verification.md
```

### Task 6: Run Validation Commands
Execute all validation commands to ensure zero regressions:

```bash
# Run all validation
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Expected:
- All tests pass
- No linting errors
- CLI help displays correctly

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

**Key Insight**: This task was correctly identified as "already completed" by the issue author. The dual strategy applied to Tasks 4-6 created all necessary templates.

**Registration Pattern**:
- Command templates (`.md.j2`) are registered in `expert_commands` list, then processed in a loop that calls `plan.add_file()`
- Seed files (`.yaml.j2`) are registered directly with `plan.add_file()` using `action=FileAction.CREATE`

**No Code Changes Expected**: This is purely verification. Only document findings and ensure consistency.

**Follow-up**: If issues are found, they should be addressed in a separate task/PR, not in this verification chore.
