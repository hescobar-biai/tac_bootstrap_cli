# Chore: Update SLASH_COMMAND_MODEL_MAP in agent.py with TAC-11 commands

## Metadata
issue_number: `332`
adw_id: `chore_Tac_11_task_14`
issue_json: `{"number":332,"title":"Update SLASH_COMMAND_MODEL_MAP in agent.py with TAC-11 commands","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_11_task_14\n\nAdd the new TAC-11 slash commands to the model map in the base repository.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/agent.py`\n\n**Implementation details:**\n- Add `/scout`: {\"base\": \"sonnet\", \"heavy\": \"sonnet\"}\n- Add `/question`: {\"base\": \"sonnet\", \"heavy\": \"sonnet\"}\n- Both are lightweight commands that don't need opus"}`

## Chore Description
This chore updates the `SLASH_COMMAND_MODEL_MAP` dictionary in `adws/adw_modules/agent.py` to include two new TAC-11 slash commands: `/scout` and `/question`. Both commands are lightweight and should use the "sonnet" model for both base and heavy model sets.

The `SLASH_COMMAND_MODEL_MAP` is a critical configuration that determines which AI model (opus, sonnet, or haiku) to use for each slash command in different model set contexts (base vs heavy). This mapping is used by the `get_model_for_slash_command()` function to select the appropriate model during agent execution.

## Relevant Files
Files required to complete this chore:

1. **adws/adw_modules/agent.py** (lines 28-69)
   - Contains the `SLASH_COMMAND_MODEL_MAP` dictionary
   - Need to add entries for `/scout` and `/question`
   - Map is organized by command categories (classification, implementation, testing, etc.)
   - Both new commands should use sonnet for base and heavy model sets

### New Files
No new files required. This is a simple configuration update to an existing file.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Add `/scout` to SLASH_COMMAND_MODEL_MAP
- Locate the appropriate section in `SLASH_COMMAND_MODEL_MAP` (likely in the classification/lightweight section near the top)
- Add entry: `"/scout": {"base": "sonnet", "heavy": "sonnet"},`
- Add inline comment to explain the command's purpose (e.g., "# TAC-11: Scout command for exploration")

### Task 2: Add `/question` to SLASH_COMMAND_MODEL_MAP
- Add entry below `/scout`: `"/question": {"base": "sonnet", "heavy": "sonnet"},`
- Add inline comment to explain the command's purpose (e.g., "# TAC-11: Question command for clarification")

### Task 3: Validate the changes
- Verify the dictionary syntax is correct (proper commas, quotes, braces)
- Ensure the new entries are in a logical position (with other lightweight commands)
- Check that the comments follow the existing comment style in the file
- Run validation commands to ensure no regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The `/scout` and `/question` commands are part of the TAC-11 integration
- Both commands are lightweight analysis/clarification tools that don't require the heavyweight opus model
- These commands should be positioned logically in the map, potentially in a new "TAC-11" section or near other classification/analysis commands
- The file already contains examples of TAC-9 and TAC-10 commands with comments, so follow that pattern
- This is a low-risk change since it only adds new entries without modifying existing ones
