# Feature: Add anth.py.j2 Anthropic LLM Wrapper Template

## Metadata
issue_number: `239`
adw_id: `feature_Tac_9_task_8`
issue_json: `{"number":239,"title":"Add anth.py.j2 Anthropic LLM wrapper template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_8\n\n**Description:**\nCreate Jinja2 template for Anthropic API wrapper. Provides `prompt_llm()`, `generate_completion_message()`, and `generate_agent_name()` functions using claude-3-5-haiku model.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/llm/anth.py`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/anth.py.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/llm/anth.py` (CREATE - rendered)\n"}`

## Feature Description
This feature creates a Jinja2 template for the Anthropic LLM wrapper utility (`anth.py.j2`). The template preserves the complete functionality of the source implementation, including three functions: `prompt_llm()` for direct LLM prompting, `generate_completion_message()` for AI-friendly task completion messages, and `generate_agent_name()` for generating unique agent names. The template maintains minimal templating (shebang and docstring only) to ensure the wrapper remains a standardized, reusable utility across all generated projects while preserving the standalone executable nature with uv script metadata.

## User Story
As a TAC Bootstrap developer
I want to create a Jinja2 template for the Anthropic LLM wrapper
So that generated projects include a consistent, working utility for interacting with Anthropic's API through hook scripts

## Problem Statement
The TAC Bootstrap CLI needs to template the Anthropic LLM wrapper utility (`anth.py`) for inclusion in generated projects. The source implementation exists at `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/llm/anth.py` but has not yet been converted into a reusable Jinja2 template. Without this template, generated projects will lack a standardized way to interact with the Anthropic API from hook scripts.

## Solution Statement
Create a Jinja2 template (`anth.py.j2`) that:

1. Preserves the exact structure, logic, and all three functions from the source implementation
2. Applies minimal templating only to the shebang line and docstring project name
3. Maintains the executable nature with uv script metadata (`#!/usr/bin/env -S uv run --script` and the `# /// script` block)
4. Hardcodes the model version (`claude-3-5-haiku-20241022`) as a stable interface
5. Keeps all environment variable handling (`ANTHROPIC_API_KEY`, `ENGINEER_NAME`) identical to source
6. Preserves the silent error handling strategy (returns `None` on API errors)
7. Includes all three working functions: `prompt_llm()`, `generate_completion_message()`, and `generate_agent_name()`

The template will be placed in `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/anth.py.j2` and rendered during project generation to `.claude/hooks/utils/llm/anth.py`.

## Relevant Files

### Existing Files (for context)
- `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/llm/anth.py` - Source implementation file with all three functions
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2` - Example template showing minimal Jinja2 usage pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/__init__.py.j2` - Existing template structure
- `config.yml` - Project configuration file

### New Files
1. `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/anth.py.j2` (CREATE) - The Jinja2 template
2. `.claude/hooks/utils/llm/anth.py` (CREATE - rendered output after project generation)

## Implementation Plan

### Phase 1: Foundation
Prepare the directory structure and examine the source implementation to understand the code thoroughly.

**Tasks:**
1. Verify source implementation exists and contains all three functions
2. Create the `utils/llm/` directory structure under templates
3. Review similar template files to understand pattern and conventions

### Phase 2: Core Implementation
Create the Jinja2 template by preserving the source code with minimal templating.

**Tasks:**
1. Create `anth.py.j2` template file in `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/`
2. Copy complete source code from `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/llm/anth.py`
3. Apply templating only to:
   - Shebang line: `#!/usr/bin/env -S uv run --script`
   - Module docstring: Use `{{ config.project.name }}` for project name
4. Verify all three functions are present and unchanged:
   - `prompt_llm(prompt_text)` - Direct LLM prompting
   - `generate_completion_message()` - Task completion messages
   - `generate_agent_name()` - Agent name generation
5. Verify uv script metadata block is preserved exactly

### Phase 3: Integration & Validation
Ensure the template integrates correctly with the project structure.

**Tasks:**
1. Create `__init__.py.j2` file in `utils/llm/` directory if needed
2. Verify template rendering would produce valid Python executable
3. Test template syntax with Jinja2 validation
4. Document the template purpose and usage

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verify Source Implementation
- Read `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/llm/anth.py` completely
- Confirm all three functions exist: `prompt_llm()`, `generate_completion_message()`, `generate_agent_name()`
- Verify shebang line format: `#!/usr/bin/env -S uv run --script`
- Verify uv script metadata block with exact Python version and dependencies
- Document any observations about the implementation

### Task 2: Create Directory Structure
- Create directory `/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/`
- Verify parent directories exist
- Check permissions are appropriate

### Task 3: Create anth.py.j2 Template
- Create file `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/anth.py.j2`
- Copy entire source code from the verified source file
- Replace docstring with: `"""Anthropic LLM wrapper for {{ config.project.name }}.`
- Keep shebang line identical: `#!/usr/bin/env -S uv run --script`
- Keep all code logic identical with NO changes to:
  - `prompt_llm()` function logic and implementation
  - `generate_completion_message()` function logic and implementation
  - `generate_agent_name()` function logic and implementation
  - Model name: `claude-3-5-haiku-20241022`
  - Environment variable handling: `ANTHROPIC_API_KEY`, `ENGINEER_NAME`
  - Error handling: Silent returns of `None`
  - `main()` CLI interface
  - uv script metadata block
- Verify template file has correct permissions (readable by template engine)

### Task 4: Create __init__.py.j2 for utils/llm/
- Create empty `__init__.py.j2` file in the `utils/llm/` directory
- This maintains Python package structure consistency

### Task 5: Validate Template Structure
- Check template syntax is valid Jinja2 (no syntax errors)
- Verify template would render correctly with sample config
- Verify rendered output would be valid Python syntax
- Verify rendered output would be executable

### Task 6: Run Validation Commands
- Run Jinja2 syntax validation on the template
- Run Python syntax check on a rendered sample
- Verify template integration with existing hooks structure
- Run tests (if applicable) to ensure no regressions

## Testing Strategy

### Unit Tests
- Template Jinja2 syntax validation passes without errors
- Template renders with sample `config` object without errors
- Rendered Python file has valid syntax (can be parsed by Python AST)

### Edge Cases
- Template works with project names containing spaces
- Template works with project names containing special characters
- Shebang line is preserved in rendered output
- uv script metadata block is preserved exactly in rendered output
- All three functions are present in rendered output

## Acceptance Criteria
- [ ] Template file created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/anth.py.j2`
- [ ] Template contains all three functions: `prompt_llm()`, `generate_completion_message()`, `generate_agent_name()`
- [ ] Template preserves exact source implementation logic without modifications
- [ ] Only shebang and docstring use Jinja2 templating
- [ ] Model version `claude-3-5-haiku-20241022` is hardcoded
- [ ] uv script metadata block preserved exactly
- [ ] Rendered output is valid executable Python with correct shebang
- [ ] Template passes Jinja2 syntax validation
- [ ] Rendered sample output passes Python syntax validation
- [ ] No test regressions in existing test suite

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && python -m pytest tests/ -v --tb=short` - Run tests to verify no regressions
- `python -c "from jinja2 import Environment, FileSystemLoader; env = Environment(loader=FileSystemLoader('tac_bootstrap_cli/tac_bootstrap/templates')); tmpl = env.get_template('claude/hooks/utils/llm/anth.py.j2'); print('Template syntax OK')"` - Validate Jinja2 syntax
- `python -c "import ast; code = open('tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/anth.py.j2').read(); print('Template file exists')"` - Verify file exists
- `cd tac_bootstrap_cli && uv run ruff check tac_bootstrap/templates/` - Lint template directory
- `ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/` - Verify directory structure

## Notes

### Clarification about generate_agent_name()
The issue description mentioned this function might not exist, but the source implementation DOES contain the `generate_agent_name()` function. The template should include this function as it is part of the validated source implementation.

### Template Variables Philosophy
Only two template variables are used:
- `{{ config.project.name }}` in the module docstring
- The shebang line and all code logic are NOT templated

This follows the pattern of existing templates (constants.py.j2) where utility code is kept generic and configuration-specific values are minimal. The wrapper uses environment variables (`ANTHROPIC_API_KEY`, `ENGINEER_NAME`) at runtime for configuration, not template variables.

### Why Model is Hardcoded
The `claude-3-5-haiku-20241022` model version is intentionally hardcoded because:
- It's part of the stable interface for the utility
- This is the "fastest Anthropic model" as documented in source comments
- It should be consistent across all generated projects
- Runtime model configuration can be added in future iterations if needed

### Executable Script Preservation
The template preserves the uv script metadata block (`# /// script`) because:
- This is essential for running the script as a standalone executable
- The shebang `#!/usr/bin/env -S uv run --script` enables direct execution
- This matches the source implementation's design as a utility script

### Error Handling Strategy
The silent error handling (returning `None` instead of raising exceptions) is intentional:
- Allows graceful degradation in hook contexts
- Permits workflows to continue if API is unavailable
- Caller can handle `None` responses appropriately
- Not configurable - this is part of the design
