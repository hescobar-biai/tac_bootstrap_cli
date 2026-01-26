# Feature: Add oai.py.j2 OpenAI LLM Wrapper Template

## Metadata
issue_number: `240`
adw_id: `feature_Tac_9_task_9`
issue_json: `{"number":240,"title":"Add oai.py.j2 OpenAI LLM wrapper template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_9\n\n**Description:**\nCreate Jinja2 template for OpenAI API wrapper. Mirrors Anthropic interface using gpt-4.1-nano model.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/llm/oai.py`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/llm/oai.py` (CREATE - rendered)"}`

## Feature Description
This feature creates a Jinja2 template for the OpenAI LLM wrapper utility (`oai.py.j2`). The template preserves the complete functionality of the source implementation, providing two core functions: `prompt_llm()` for direct LLM prompting and `generate_completion_message()` for AI-friendly task completion messages. The template maintains minimal templating (shebang and docstring only) to ensure the wrapper remains a standardized, reusable utility across all generated projects while preserving the standalone executable nature with uv script metadata. The template uses `gpt-4o-mini` as the model (OpenAI's fastest and cheapest current option as of 2025) instead of the non-existent 'gpt-4.1-nano' referenced in the source.

## User Story
As a TAC Bootstrap developer
I want to create a Jinja2 template for the OpenAI LLM wrapper
So that generated projects include a consistent, working utility for interacting with OpenAI's API through hook scripts

## Problem Statement
The TAC Bootstrap CLI needs to template the OpenAI LLM wrapper utility (`oai.py`) for inclusion in generated projects. The source implementation exists at `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/llm/oai.py` but has not yet been converted into a reusable Jinja2 template. Without this template, generated projects will lack a standardized way to interact with the OpenAI API from hook scripts. Additionally, the current source uses 'gpt-4.1-nano' which is not a valid OpenAI model and needs correction to 'gpt-4o-mini'.

## Solution Statement
Create a Jinja2 template (`oai.py.j2`) that:

1. Preserves the exact structure, logic, and both functions from the source implementation
2. Applies minimal templating only to the shebang line and docstring project name
3. Maintains the executable nature with uv script metadata (`#!/usr/bin/env -S uv run --script` and the `# /// script` block)
4. Uses the valid model version `gpt-4o-mini` (OpenAI's fastest and cheapest current model) instead of the non-existent 'gpt-4.1-nano'
5. Keeps all environment variable handling (`OPENAI_API_KEY`, `ENGINEER_NAME`) identical to source
6. Preserves the silent error handling strategy (returns `None` on API errors)
7. Includes both working functions: `prompt_llm()` and `generate_completion_message()`
8. Mirrors the Anthropic template structure exactly for consistency

The template will be placed in `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2` and rendered during project generation to `.claude/hooks/utils/llm/oai.py`.

## Relevant Files

### Existing Files (for context)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/llm/oai.py` - Source implementation file with both functions
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/llm/anth.py` - Parallel Anthropic implementation for reference
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/anth.py.j2` - Parallel Anthropic template (once created)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2` - Example template showing minimal Jinja2 usage pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/__init__.py.j2` - Existing template structure
- `config.yml` - Project configuration file

### New Files
1. `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2` (CREATE) - The Jinja2 template
2. `.claude/hooks/utils/llm/oai.py` (CREATE - rendered output after project generation)

## Implementation Plan

### Phase 1: Foundation
Prepare the directory structure and examine the source implementation to understand the code thoroughly.

**Tasks:**
1. Verify source implementation exists and contains both functions
2. Confirm directory structure `/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/` exists
3. Review the Anthropic template (`anth.py.j2`) to understand the exact pattern and conventions to follow

### Phase 2: Core Implementation
Create the Jinja2 template by preserving the source code with minimal templating and correcting the model name.

**Tasks:**
1. Create `oai.py.j2` template file in `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/`
2. Copy complete source code from `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/llm/oai.py`
3. Replace model name from `gpt-4.1-nano` to `gpt-4o-mini`
4. Apply templating only to:
   - Shebang line: `#!/usr/bin/env -S uv run --script`
   - Module docstring: Use `{{ config.project.name }}` for project name
5. Verify both functions are present and unchanged:
   - `prompt_llm(prompt_text)` - Direct LLM prompting
   - `generate_completion_message()` - Task completion messages
6. Verify uv script metadata block is preserved exactly

### Phase 3: Integration & Validation
Ensure the template integrates correctly with the project structure.

**Tasks:**
1. Verify template rendering would produce valid Python executable
2. Test template syntax with Jinja2 validation
3. Verify consistency with the Anthropic template structure
4. Run tests to ensure no regressions

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verify Source Implementation
- Read `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/llm/oai.py` completely
- Confirm both functions exist: `prompt_llm()`, `generate_completion_message()`
- Verify shebang line format: `#!/usr/bin/env -S uv run --script`
- Verify uv script metadata block with exact Python version and dependencies
- Note the model name (`gpt-4.1-nano`) that needs to be corrected
- Document any observations about the implementation

### Task 2: Verify Directory Structure
- Confirm directory `/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/` exists
- Check if `__init__.py.j2` exists in that directory
- Verify parent directories exist and have appropriate permissions

### Task 3: Review Anthropic Template Pattern
- Read the Anthropic template file to understand the exact templating pattern
- Identify the specific lines that use Jinja2 templating
- Note the structure for how docstrings are templated with `{{ config.project.name }}`
- Understand how the shebang and uv script metadata are preserved

### Task 4: Create oai.py.j2 Template
- Create file `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2`
- Copy entire source code from the verified source file
- Replace model name: change `"gpt-4.1-nano"` to `"gpt-4o-mini"`
- Replace docstring with: `"""Base OpenAI LLM prompting method using fastest model for {{ config.project.name }}.`
- Keep shebang line identical: `#!/usr/bin/env -S uv run --script`
- Keep all code logic identical with NO changes to:
  - `prompt_llm()` function logic and implementation
  - `generate_completion_message()` function logic and implementation
  - Environment variable handling: `OPENAI_API_KEY`, `ENGINEER_NAME`
  - Error handling: Silent returns of `None`
  - `main()` CLI interface
  - uv script metadata block
- Verify template file has correct permissions (readable by template engine)

### Task 5: Validate Template Structure
- Check template syntax is valid Jinja2 (no syntax errors)
- Verify template would render correctly with sample config
- Verify rendered output would be valid Python syntax
- Verify rendered output would be executable

### Task 6: Verify Consistency with Anthropic Template
- Compare line-by-line structure of both templates
- Ensure both templates follow identical patterns for:
  - Shebang line
  - Docstring with `{{ config.project.name }}`
  - uv script metadata block
  - Function signatures and error handling
- Document any intentional differences (e.g., model name, imports)

### Task 7: Run Validation Commands
- Run Jinja2 syntax validation on the template
- Run Python syntax check on a rendered sample
- Verify template integration with existing hooks structure
- Run tests to ensure no regressions

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
- Both functions are present in rendered output
- Model name is correctly set to `gpt-4o-mini` in rendered output

## Acceptance Criteria
- [ ] Template file created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2`
- [ ] Template contains both functions: `prompt_llm()`, `generate_completion_message()`
- [ ] Template preserves exact source implementation logic without modifications
- [ ] Model name corrected from `gpt-4.1-nano` to `gpt-4o-mini`
- [ ] Only shebang and docstring use Jinja2 templating
- [ ] uv script metadata block preserved exactly
- [ ] Rendered output is valid executable Python with correct shebang
- [ ] Template passes Jinja2 syntax validation
- [ ] Rendered sample output passes Python syntax validation
- [ ] Template structure mirrors Anthropic template exactly
- [ ] No test regressions in existing test suite

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/feature_Tac_9_task_9 && python -m pytest tests/ -v --tb=short` - Run tests to verify no regressions
- `python -c "from jinja2 import Environment, FileSystemLoader; env = Environment(loader=FileSystemLoader('tac_bootstrap_cli/tac_bootstrap/templates')); tmpl = env.get_template('claude/hooks/utils/llm/oai.py.j2'); print('Template syntax OK')"` - Validate Jinja2 syntax
- `python -c "import ast; code = open('tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2').read(); print('Template file exists')"` - Verify file exists
- `cd tac_bootstrap_cli && uv run ruff check tac_bootstrap/templates/` - Lint template directory
- `ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/` - Verify directory structure

## Notes

### Model Name Selection
The source implementation references 'gpt-4.1-nano' which is not a valid OpenAI model. The correction to 'gpt-4o-mini' is deliberate:
- `gpt-4o-mini` is OpenAI's fastest and cheapest current model as of 2025
- It provides excellent speed and low cost for completion message generation
- It mirrors the philosophy of using the fastest model (like `claude-3-5-haiku` for Anthropic)
- This maintains parity between OpenAI and Anthropic implementations

### Template Variables Philosophy
Only two template variables are used:
- `{{ config.project.name }}` in the module docstring
- The shebang line and all code logic are NOT templated

This follows the pattern of the Anthropic template where utility code is kept generic and configuration-specific values are minimal. The wrapper uses environment variables (`OPENAI_API_KEY`, `ENGINEER_NAME`) at runtime for configuration, not template variables.

### Parallel Implementation with Anthropic
This OpenAI template is designed to mirror the Anthropic template (`anth.py.j2`) exactly in structure:
- Identical function signatures
- Identical error handling (silent returns of `None`)
- Identical Jinja2 templating patterns
- Only the model name and API client library differ

This consistency makes it easy for developers to understand both implementations and switch between them.

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
