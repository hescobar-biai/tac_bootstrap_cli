# Chore: Update AI docs keyword mappings for TAC-13

## Metadata
issue_number: `588`
adw_id: `chore_Tac_13_Task_26`
issue_json: `{"number": 588, "title": "[TAC-13] Task 26: Update AI docs keyword mappings", "body": "**Workflow Metadata:**\n```\n/chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_13_Task_26\n```\n\n**Description:**\nAdd TAC-13 documentation topics to the auto-detection keyword mappings.\n\n**Technical Steps:**\n1. Open `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/workflow_ops.py`\n2. In the `detect_relevant_docs()` function, add new keyword mappings:\n   ```python\n   \"Tac-13-agent-experts\": [\"agent expert\", \"expertise file\", \"self-improving\", \"mental model\", \"act learn reuse\"],\n   \"expertise-file-structure\": [\"expertise yaml\", \"expertise structure\", \"expertise schema\"],\n   \"meta-skill-pattern\": [\"meta-skill\", \"progressive disclosure\", \"skill levels\"],\n   ```\n3. Sync to template: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2`\n\n**Acceptance Criteria:**\n- Keywords trigger auto-loading of TAC-13 docs\n- Dynamic scanning still works for custom docs\n- Template is synchronized\n\n**Impacted Paths:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/workflow_ops.py`\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2`"}`

## Chore Description
Add TAC-13 documentation topics to the auto-detection keyword mappings in the `detect_relevant_docs()` function. This enables automatic loading of TAC-13 related documentation when issues contain relevant keywords like "agent expert", "expertise file", "self-improving", "mental model", etc.

The chore follows the dual strategy pattern: update both the live implementation file and synchronize changes to the Jinja2 template for the CLI generator.

## Relevant Files
Files required to complete the chore:

- `adws/adw_modules/workflow_ops.py` - Contains the `detect_relevant_docs()` function with the `doc_keywords` dictionary that needs new TAC-13 mappings (lines 631-683)
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2` - Jinja2 template that must be synchronized with the same keyword additions

### New Files
No new files required.

## Step by Step Tasks

### Task 1: Update workflow_ops.py with TAC-13 keyword mappings
- Open `adws/adw_modules/workflow_ops.py`
- Locate the `detect_relevant_docs()` function (around line 631)
- Find the `doc_keywords` dictionary (around lines 663-683)
- Add three new keyword mappings for TAC-13 topics:
  ```python
  "Tac-13-agent-experts": ["agent expert", "expertise file", "self-improving", "mental model", "act learn reuse"],
  "expertise-file-structure": ["expertise yaml", "expertise structure", "expertise schema"],
  "meta-skill-pattern": ["meta-skill", "progressive disclosure", "skill levels"],
  ```
- Place these new entries in a logical section (suggest adding a new "# TAC-13 - Agent Experts" comment section after the "# AI & SDK" section)
- Verify the syntax is correct (proper commas, matching quotes)

### Task 2: Synchronize template with keyword mappings
- Open `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2`
- Locate the same `doc_keywords` dictionary in the template
- Add the exact same three keyword mappings in the same location
- Ensure Jinja2 syntax is preserved (the template should match the source file exactly in this section)
- Verify template variable placeholders like `{% raw %}` and `{% endraw %}` are correctly positioned around JSON/dict structures if present

### Task 3: Execute Validation Commands
- Run `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` to verify no regressions in tests
- Run `cd tac_bootstrap_cli && uv run ruff check .` to ensure code quality standards
- Run `cd tac_bootstrap_cli && uv run tac-bootstrap --help` to verify CLI still functions
- Manually verify the changes:
  - Check that both files have identical keyword mappings
  - Verify that the new keywords are properly formatted as Python lists of strings
  - Confirm no syntax errors or missing commas

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The `detect_relevant_docs()` function uses keyword matching to automatically load relevant documentation during ADW workflows
- TAC-13 introduces the Agent Experts pattern, expertise files, and meta-skills, so these keywords enable automatic context loading
- The dual strategy pattern requires both the live implementation and template to stay synchronized
- The template file uses Jinja2 syntax but for this dictionary section, it should be identical to the source
- Keywords are case-insensitive when matched (the function lowercases the issue title/body)
- Maximum 8 topics can be loaded (MAX_TOPICS = 8), so these additions should not exceed reasonable limits
