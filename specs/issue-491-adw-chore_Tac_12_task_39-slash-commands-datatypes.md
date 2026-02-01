# Chore: Add TAC-12 Commands to SlashCommand Literal

## Metadata
issue_number: `491`
adw_id: `chore_Tac_12_task_39`
issue_json: `{"number": 491, "title": "[Task 39/49] [CHORE] Add new slash commands to data_types.py SlashCommand Literal", "body": "Update SlashCommand Literal type to include all new TAC-12 commands."}`

## Chore Description

Update the SlashCommand Literal type in both `data_types.py` (base) and `data_types.py.j2` (template) to include 15 new TAC-12 multi-agent orchestration commands. This is a type definition update only—no runtime registration or SLASH_COMMAND_MODEL_MAP changes are needed.

The 15 new commands are:
- `/all_tools`, `/build`, `/build_in_parallel`, `/find_and_summarize`, `/load_ai_docs`
- `/load_bundle`, `/parallel_subagents`, `/plan`, `/plan_w_docs`, `/plan_w_scouters`
- `/prime_3`, `/prime_cc`, `/scout_plan_build`, `/quick-plan`, `/background`

## Relevant Files

### Files to Modify
1. **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/data_types.py`
   - Contains the source SlashCommand Literal type definition (lines 51-75)
   - This is the reference implementation

2. **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2`
   - Jinja2 template for generating new projects
   - Must mirror the base file exactly (no template variables needed for static Literal)

### Files NOT to Modify
- `adws/adw_modules/agent.py` — Do NOT add entries to SLASH_COMMAND_MODEL_MAP
- This is a type definition only; runtime registration is handled separately

## Step by Step Tasks

### Task 1: Update Base File (data_types.py)
Update the SlashCommand Literal in the base file:
- Locate the closing bracket of SlashCommand Literal (line 75)
- Insert a new section with comment `# TAC-12: Multi-agent orchestration commands`
- Add all 15 commands in the specified order
- Ensure proper formatting and comma placement

### Task 2: Update Template File (data_types.py.j2)
Apply identical changes to the Jinja2 template file:
- Locate the same SlashCommand Literal section
- Insert the same TAC-12 section with all 15 commands
- Keep the template synchronized with the base file

### Task 3: Verify Changes
Validate that both files are correctly updated:
- Check both files contain all 15 new commands
- Verify commands are grouped with the TAC-12 comment
- Confirm proper Python syntax (trailing commas, string quotes)
- Ensure no duplicate entries

### Task 4: Run Validation Tests
Execute all validation commands to ensure no regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` — Run unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` — Check code style
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` — Smoke test

## Validation Commands

Execute all commands to validate with zero regressions:

```bash
# Unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Code style check
cd tac_bootstrap_cli && uv run ruff check .

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This is a pure type definition update—no logic changes or runtime registration required
- Both files must be kept in sync for consistency
- The SlashCommand Literal acts as a contract/whitelist of available commands
- Commands should be grouped by category with descriptive comments for maintainability
- The order of entries in a Python Literal is unordered at runtime, but logical grouping aids readability
