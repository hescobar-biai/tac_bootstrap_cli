# Chore: Add __init__.py.j2 for LLM utilities package

## Metadata
issue_number: `252`
adw_id: `chore_Tac_9_task_11`
issue_json: `{"number":252,"title":"Add __init__.py.j2 for LLM utilities package","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_9_task_11\n\n**Description:**\nCreate package init file for LLM utilities with exports.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/__init__.py.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/llm/__init__.py` (CREATE - rendered)\n"}`

## Chore Description

Create a minimal `__init__.py.j2` template file for the LLM utilities package that:
- Exports the two stable public functions: `prompt_llm` and `generate_completion_message`
- Uses explicit imports from the three provider modules (oai, ollama, anth)
- Includes a docstring documenting the package purpose using Jinja2 template syntax
- Follows the same pattern as the parent `utils/__init__.py.j2`
- Notes that provider selection happens via direct module imports

This allows users to import functions directly from the llm package: `from llm import prompt_llm, generate_completion_message` while supporting provider-specific imports: `from llm.oai import prompt_llm`.

## Relevant Files

### Existing Files to Reference

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/__init__.py.j2` - Parent package init pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2` - OpenAI provider with `prompt_llm()` and `generate_completion_message()` functions
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2` - Ollama provider with same public functions
- `.claude/hooks/utils/llm/` - Directory where rendered version will be placed

### New Files

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/__init__.py.j2` (CREATE) - Template file
- `.claude/hooks/utils/llm/__init__.py` (CREATE - rendered) - Generated file from template

## Step by Step Tasks

### Task 1: Examine parent package pattern
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/__init__.py.j2`
- Understand the Jinja2 template structure and how it uses `config.project.name`
- Note the docstring format and export pattern

### Task 2: Verify LLM provider modules
- Confirm all three LLM provider modules exist (oai.py.j2, ollama.py.j2, anth.py.j2)
- Verify that each module exports `prompt_llm()` and `generate_completion_message()` functions
- Identify any other public functions that should not be exported (e.g., `main()` is CLI-specific)

### Task 3: Create __init__.py.j2 template
- Create file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/__init__.py.j2`
- Add docstring using Jinja2 template syntax referencing `config.project.name`
- Add explicit imports of the two public functions from all three provider modules:
  ```
  from .oai import prompt_llm, generate_completion_message
  from .ollama import prompt_llm, generate_completion_message
  from .anth import prompt_llm, generate_completion_message
  ```
- Add `__all__` list defining exported API: `["prompt_llm", "generate_completion_message"]`
- Include documentation that provider selection happens via direct module imports

### Task 4: Verify template syntax
- Check that file uses Jinja2 syntax correctly
- Ensure docstring references `{{ config.project.name }}`
- Confirm imports are properly formatted

### Task 5: Run validation commands
- Execute all validation commands listed in the Validation Commands section below

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Verify unit tests pass
- `cd tac_bootstrap_cli && uv run ruff check .` - Verify code style passes linting
- Verify the template file exists at correct location: `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/__init__.py.j2`
- Verify no syntax errors in template file

## Notes

- The anth.py.j2 provider module was not found in the search but is mentioned in the issue. Either it exists in a different location or needs to be created. If the third provider is missing, document this in the plan.
- The imports should use explicit function imports rather than star imports (cleaner API, better IDE support, avoids namespace pollution)
- The `main()` function in each provider is CLI-specific and should NOT be exported as part of the package API
- The docstring should document that this provides a unified interface across multiple LLM providers and reference the available functions
