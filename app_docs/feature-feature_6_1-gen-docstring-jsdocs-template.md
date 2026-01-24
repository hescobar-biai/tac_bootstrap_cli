# LLM-Powered Docstring/JSDoc Generator Template

**ADW ID:** feature_6_1
**Date:** 2026-01-24
**Specification:** /Volumes/MAc1/Celes/tac_bootstrap/trees/feature_6_1/specs/issue-169-adw-feature_6_1-sdlc_planner-gen-docstring-jsdocs.md

## Overview

This feature adds a Jinja2 template that generates an LLM-powered docstring/JSDoc automation script for TAC Bootstrap projects. The generated script automatically enriches Python and TypeScript/JavaScript code with IDK-format (Information Dense Keywords) documentation using configurable AI providers (Ollama local by default, or OpenAI/Anthropic compatible APIs).

## What Was Built

- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/scripts/gen_docstring_jsdocs.py.j2` - A 1003-line template that renders project-specific docstring generation scripts
- **Rendered Script**: `scripts/gen_docstring_jsdocs.py` - A working example generated from the template for the TAC Bootstrap project itself
- **PEP 723 Support**: Inline script dependencies header for seamless execution with `uv run`
- **Multi-language Support**: Python (via AST parsing) and TypeScript/JavaScript (via regex patterns)
- **Multiple Documentation Modes**: `add`, `complement`, and `overwrite` modes with different safety levels
- **Git Integration**: `--changed-only` flag to process only modified files
- **Flexible API Configuration**: Environment variable support for Ollama, OpenAI, and Anthropic APIs

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/scripts/gen_docstring_jsdocs.py.j2`: New Jinja2 template based on reference implementation from `ai_docs/doc/create-crud-entity/generating-fractal-docs/scripts/gen_docstring_jsdocs.py`
- `scripts/gen_docstring_jsdocs.py`: Generated script rendered from the template for TAC Bootstrap project
- `.mcp.json`: Minor configuration update
- `playwright-mcp-config.json`: Minor configuration update
- `specs/issue-169-adw-feature_6_1-sdlc_planner-gen-docstring-jsdocs-checklist.md`: Implementation checklist (104 lines)
- `specs/issue-169-adw-feature_6_1-sdlc_planner-gen-docstring-jsdocs.md`: Feature specification (388 lines)

### Key Changes

1. **Jinja2 Template Variables**:
   - `{{ config.project.name }}` - Injected into script header and generated docstrings for project context
   - `{{ config.project.language }}` - Determines default file extensions to process (python, typescript, etc.)
   - `{{ config.paths.app_root | default("src") }}` - Configures default directory to process with fallback

2. **PEP 723 Inline Dependencies**:
   - Added standardized header for `uv run` support
   - Dependencies: `openai` (OpenAI-compatible API client), `python-dotenv` (environment variable management)

3. **Default API Configuration**:
   - Base URL: `http://localhost:11434/v1/` (Ollama local)
   - Model: `llama3.2` (local open-source LLM)
   - Environment variables: `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, `OPENAI_API_KEY`

4. **IDK Documentation Format**:
   - Structured sections: IDK keywords, Responsibility, Invariants, Inputs, Outputs, Failure Modes
   - 5-12 information-dense keywords in kebab-case format
   - Tag taxonomy support for categorization (expert levels, topics)

5. **CLI Features**:
   - `--mode`: `add` (default, safest), `complement`, `overwrite`
   - `--changed-only`: Process only git-modified files
   - `--no-recursive`: Limit to single directory
   - `--public-only`: Exclude private methods/functions
   - `--dry-run`: Preview changes without modifying files
   - `--exclude`: File pattern exclusion support

6. **Multi-language Processing**:
   - Python: AST parsing for accurate structure detection (classes, functions, methods, async functions)
   - TypeScript/JavaScript: Regex-based parsing for classes, functions, interfaces, arrow functions
   - Support for `.py`, `.ts`, `.tsx`, `.js`, `.jsx` files
   - Automatic TypeScript declaration file (`.d.ts`) exclusion

7. **Error Handling**:
   - Fail fast on API configuration issues
   - Continue processing after individual file parse errors
   - Detailed warning logs for skipped files
   - Success exit code if at least some files processed successfully

## How to Use

### Basic Usage

1. **Generate script for a new project** (TAC Bootstrap CLI will automatically render this template):
   ```bash
   # Template is automatically included in generated projects
   ```

2. **Run the generated script** with default settings (Ollama local):
   ```bash
   cd scripts
   uv run gen_docstring_jsdocs.py --repo /path/to/project --mode add
   ```

3. **Preview changes without modifying files**:
   ```bash
   uv run gen_docstring_jsdocs.py --repo . --dry-run
   ```

4. **Process only git-modified files**:
   ```bash
   uv run gen_docstring_jsdocs.py --repo . --changed-only
   ```

5. **Use with OpenAI or Anthropic**:
   ```bash
   export OPENAI_API_KEY="sk-..."
   uv run gen_docstring_jsdocs.py --repo . \
     --base-url https://api.openai.com/v1/ \
     --model gpt-4
   ```

### Documentation Modes

- **add** (default): Only add docstrings where completely missing - safest option
- **complement**: Add missing sections to partial docstrings without removing existing content
- **overwrite**: Replace all docstrings entirely - commit changes first!

### Advanced Options

```bash
# Process only public functions/methods
uv run gen_docstring_jsdocs.py --repo . --public-only

# Process single directory non-recursively
uv run gen_docstring_jsdocs.py --repo ./src --no-recursive

# Exclude test files
uv run gen_docstring_jsdocs.py --repo . --exclude "test_.*\.py"

# Custom file pattern
uv run gen_docstring_jsdocs.py --repo . --include-glob "src/**/*.py"
```

## Configuration

### Environment Variables

Create a `.env` file or export environment variables:

```bash
# Ollama local (default)
OLLAMA_BASE_URL=http://localhost:11434/v1/
OLLAMA_MODEL=llama3.2
OPENAI_API_KEY=ollama  # dummy key for local

# OpenAI
OPENAI_API_KEY=sk-your-key-here
# Then use: --base-url https://api.openai.com/v1/ --model gpt-4

# Anthropic (via OpenAI-compatible endpoint if available)
OPENAI_API_KEY=your-anthropic-key
# Check Anthropic docs for compatible endpoint
```

### Jinja2 Template Variables (for TAC Bootstrap developers)

When rendering the template, provide these configuration values:

```python
config = ProjectConfig(
    name='my-project',           # Used in generated docstrings
    language='python',            # Determines default file extensions
    paths=PathsConfig(
        app_root='src'            # Default directory to process
    )
)
```

## Testing

### Template Rendering Test

```bash
cd tac_bootstrap_cli && uv run python -c "
from tac_bootstrap.application.template_renderer import TemplateRenderer
from tac_bootstrap.domain.models import ProjectConfig, PathsConfig
from pathlib import Path

config = ProjectConfig(
    name='test-project',
    language='python',
    paths=PathsConfig(app_root='src')
)

renderer = TemplateRenderer(Path('tac_bootstrap/templates'))
rendered = renderer.render_template(
    'scripts/gen_docstring_jsdocs.py.j2',
    {'config': config}
)
print('Template rendered:', len(rendered), 'bytes')
"
```

### Functional Test

```bash
# Test script help
uv run scripts/gen_docstring_jsdocs.py --help

# Create test file
echo "def test_func(): pass" > /tmp/test_sample.py

# Test dry run
uv run scripts/gen_docstring_jsdocs.py --repo /tmp --include-glob "test_sample.py" --mode add --dry-run
```

### Unit Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v -k "gen_docstring"
```

## Notes

### IDK Format Example

Generated docstrings follow this structure:

```python
"""
IDK: llm-integration, docstring-generation, ast-parsing, code-analysis, template-rendering

Responsibility: Automatically generate and update IDK-format docstrings for Python and
TypeScript/JavaScript code using LLM APIs with multiple documentation modes.

Invariants:
- All docstrings must include IDK keywords, Responsibility, Inputs, Outputs, Failure Modes
- IDK keywords must be 5-12 kebab-case technical nouns without verbs or sentences
- File modifications only occur when not in dry-run mode
- Original code structure and logic remain unchanged

Inputs:
- repo: Path - Root directory to process for documentation
- mode: str - Documentation mode (add/complement/overwrite)
- File content as strings from Python/TypeScript/JavaScript source files
- LLM API responses with structured documentation

Outputs:
- Modified source files with added/updated docstrings
- Console output showing processing progress and changes
- Exit code 0 on success, non-zero on critical failures

Failure Modes:
- API authentication failure if credentials invalid (fail fast)
- Individual file parse errors (skip with warning, continue processing)
- Network timeouts on LLM API calls
- Malformed code that cannot be parsed by AST or regex
- Permission errors when writing to files
"""
```

### Performance Considerations

- AST parsing for Python is fast (no external process required)
- LLM API calls are the primary bottleneck (network + generation latency)
- Use `--changed-only` for incremental updates in large codebases
- Use `--include-glob` to limit scope for faster iteration
- Consider local Ollama for faster response times vs cloud APIs

### Safety Best Practices

1. **Always commit changes before using `overwrite` mode**
2. **Use `--dry-run` first** to preview changes
3. **Start with `add` mode** (default) for safest operation
4. **Test on a small subset** using `--include-glob` before full codebase
5. **Review generated docstrings** as LLM output may need refinement
6. **Store API keys in environment variables**, never in command line or code

### Future Enhancements (Out of Scope)

- Configuration file support (`.gen_docstring_config.json`)
- Parallel processing for large codebases
- Pre-commit hook integration
- Additional language support (Go, Rust, Java)
- Interactive review mode
- Progress bar for large repositories
- IDK keyword validation against domain registries
