# Chore: Add new commands to SLASH_COMMAND_MODEL_MAP in agent.py

## Metadata
issue_number: `494`
adw_id: `chore_Tac_12_task_42`
issue_json: `{"number": 494, "title": "[Task 42/49] [CHORE] Add new commands to SLASH_COMMAND_MODEL_MAP in agent.py", "body": "## Description\n\nAdd model mappings for all new TAC-12 commands.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/agent.py`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2`\n\n## Changes Required\nAdd to SLASH_COMMAND_MODEL_MAP:\n```python\n\"/all_tools\": {\"base\": \"haiku\", \"heavy\": \"haiku\"},\n\"/build\": {\"base\": \"sonnet\", \"heavy\": \"sonnet\"},\n\"/build_in_parallel\": {\"base\": \"sonnet\", \"heavy\": \"opus\"},\n\"/find_and_summarize\": {\"base\": \"sonnet\", \"heavy\": \"sonnet\"},\n\"/load_ai_docs\": {\"base\": \"sonnet\", \"heavy\": \"sonnet\"},\n\"/load_bundle\": {\"base\": \"haiku\", \"heavy\": \"sonnet\"},\n\"/parallel_subagents\": {\"base\": \"sonnet\", \"heavy\": \"opus\"},\n\"/plan\": {\"base\": \"opus\", \"heavy\": \"opus\"},\n\"/plan_w_docs\": {\"base\": \"sonnet\", \"heavy\": \"opus\"},\n\"/plan_w_scouters\": {\"base\": \"sonnet\", \"heavy\": \"opus\"},\n\"/prime_3\": {\"base\": \"sonnet\", \"heavy\": \"sonnet\"},\n\"/prime_cc\": {\"base\": \"sonnet\", \"heavy\": \"sonnet\"},\n\"/scout_plan_build\": {\"base\": \"sonnet\", \"heavy\": \"opus\"},\n```"}`

## Chore Description
This chore requires adding 13 new command mappings to the SLASH_COMMAND_MODEL_MAP dictionary in both the production agent.py file and the template agent.py.j2 file. These mappings define which model (haiku, sonnet, or opus) should be used for each command in both base and heavy model sets.

The new commands include planning, building, exploring, and orchestration utilities that were introduced in TAC-12. The models are pre-specified by the issue and should be accepted as designed without second-guessing.

## Relevant Files
Archivos para completar la chore:

### Core Implementation Files
- **`adws/adw_modules/agent.py:31-73`** - The production SLASH_COMMAND_MODEL_MAP dictionary (lines 31-73). Currently contains ~30 commands, will add 13 new ones.
- **`tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2:31-73`** - The Jinja2 template version of the same file. Must be kept in sync with the production file.
- **`adws/adw_modules/data_types.py:51-75`** - The SlashCommand Literal type definition that validates command names. Will need updating to include the 13 new commands for type safety.

### Background Context
- `PLAN_TAC_BOOTSTRAP.md` - Project plan (reference only, not modified)
- `CLAUDE.md` - Agent guide (reference only)

### No New Files Required
This chore only modifies existing files. No new files need to be created.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Add commands to production agent.py
- Open `adws/adw_modules/agent.py` at lines 31-73 where SLASH_COMMAND_MODEL_MAP is defined
- Insert the 13 new command mappings (as specified in the issue) into the dictionary
- Add appropriate comments to group the new commands logically by category (e.g., "TAC-12: Planning and Orchestration")
- Place them after line 72 (after the existing "/question" entry) but before the closing brace
- Preserve the existing code structure, indentation, and comment style

### Task 2: Add commands to template agent.py.j2
- Open `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2` at lines 31-73
- Add identical command mappings with identical comments (must be exactly the same as production)
- This ensures generated projects will have the same configuration

### Task 3: Update SlashCommand type in data_types.py
- Open `adws/adw_modules/data_types.py` at the SlashCommand Literal definition (lines 51-75)
- Add all 13 new command names to the Literal type:
  - "/all_tools"
  - "/build"
  - "/build_in_parallel"
  - "/find_and_summarize"
  - "/load_ai_docs"
  - "/load_bundle"
  - "/parallel_subagents"
  - "/plan"
  - "/plan_w_docs"
  - "/plan_w_scouters"
  - "/prime_3"
  - "/prime_cc"
  - "/scout_plan_build"
- Group them logically by category with inline comments (e.g., "# TAC-12: Planning and orchestration")
- Maintain alphabetical or logical ordering within each group

### Task 4: Run validation tests
- Execute `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` to run all unit tests
- All tests must pass with zero regressions
- If any failures occur, analyze and fix them before proceeding

### Task 5: Run linting check
- Execute `cd tac_bootstrap_cli && uv run ruff check .` to verify code style
- Address any linting issues that arise

### Task 6: Smoke test the CLI
- Execute `cd tac_bootstrap_cli && uv run tac-bootstrap --help` to ensure the CLI still works
- Verify the help output displays correctly

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The 13 new commands are a TAC-12 feature addition and represent a significant expansion of the command infrastructure
- Model assignments have been pre-decided and are based on computational complexity (haiku for lightweight utilities, sonnet for standard operations, opus for complex reasoning/orchestration)
- No validation or custom error handling is required—the Python type system will catch mismatches
- Both files (production and template) must be kept in sync; there is no automatic synchronization mechanism
- Accept the model specifications as authoritative without second-guessing the design
