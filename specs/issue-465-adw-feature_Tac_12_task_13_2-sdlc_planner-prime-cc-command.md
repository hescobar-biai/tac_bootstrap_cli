# Feature: Create prime_cc Command File and Template

## Metadata
issue_number: `465`
adw_id: `feature_Tac_12_task_13_2`
issue_json: `{"number":465,"title":"[Task 13/49] [FEATURE] Create prime_cc.md command file","body":"## Description\n\nCreate a specialized prime command for Claude Code codebase understanding.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/prime_cc.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2`\n\n## Key Features\n- Specialized for Claude Code projects\n- Deep understanding of CC patterns\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/prime_cc.md`\n\n## Wave 1 - New Commands (Task 13 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_13_2"}`

## Feature Description

The `prime_cc` command is a specialized version of the `/prime` command designed for Claude Code projects. It extends the general project priming with Claude Code-specific context loading including slash commands, automation hooks, output styles, and CLI workflows. This feature is already implemented with both the base command file and Jinja2 template in place, and integrated into the scaffold service. The remaining work is to verify completeness and add comprehensive tests.

## User Story

As a TAC Bootstrap user generating a new project
I want the /prime_cc command to be available in my generated project
So that Claude Code agents can quickly understand both the project structure and the Claude Code-specific setup (commands, hooks, automation)

## Problem Statement

When setting up a new project with Claude Code, agents need to understand not just the project structure and architecture, but also the Claude Code-specific configuration:
- What slash commands are available and what they do
- What automation hooks are configured
- What output styles are defined
- How permissions are configured in settings.json
- What ADW workflows are available

The existing `/prime` command loads general project context, but doesn't specifically focus on Claude Code configuration. Users need a specialized command that gives agents deep understanding of the Claude Code development environment.

## Solution Statement

Create a `/prime_cc` command that:
1. Extends `/prime` by first running it to load general project context
2. Then loads Claude Code-specific configuration files (.claude/commands/, .claude/settings.json, .claude/hooks/, .claude/output-styles/)
3. Provides understanding of available slash commands, automation, and workflows
4. Reports comprehensive context about both project and Claude Code setup

The implementation already exists:
- Base file: `.claude/commands/prime_cc.md` (complete with all sections)
- Template: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2` (with Jinja2 variables)
- Integration: `scaffold_service.py` line 322 includes prime_cc in commands list

The remaining work is to add comprehensive tests following the pattern of existing command template tests.

## Relevant Files

### Existing Files
- `.claude/commands/prime_cc.md` - Base command file with complete implementation
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2` - Jinja2 template with config variables
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:322` - Already includes prime_cc in commands list
- `tac_bootstrap_cli/tests/test_new_tac10_templates.py` - Test patterns to follow

### New Files
- `tac_bootstrap_cli/tests/test_prime_cc_template.py` - New test file for prime_cc command template

## Implementation Plan

### Phase 1: Verification
Verify that the existing implementation is complete and properly integrated:
- Confirm base command file has all required sections (Variables, Instructions, Run, Read, Understand, Examples, Report)
- Verify template uses proper Jinja2 variables from TACConfig model
- Check scaffold_service.py integration (already confirmed at line 322)

### Phase 2: Test Creation
Create comprehensive tests for the prime_cc template following existing patterns:
- Test template renders without errors
- Verify all expected sections are present in generated markdown
- Validate Jinja2 variables are properly substituted
- Ensure conditional blocks work correctly ({% if %} statements)
- Test with different project configurations (with/without ADW, different languages)

### Phase 3: Documentation Verification
Ensure the prime_cc command is properly documented:
- Verify README mentions the command
- Check that CHANGELOG includes this feature
- Confirm conditional_docs.md (if exists) references prime_cc appropriately

## Step by Step Tasks

### Task 1: Verify Existing Implementation
- Read `.claude/commands/prime_cc.md` and confirm all sections are complete
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2` and verify Jinja2 variables
- Confirm variables used match TACConfig model fields
- Verify scaffold_service.py line 322 includes prime_cc (already done in initial read)

### Task 2: Create Test File
- Create `tac_bootstrap_cli/tests/test_prime_cc_template.py`
- Follow patterns from `test_new_tac10_templates.py`
- Create test fixtures (python_config, template_repo)
- Add test class `TestPrimeCCTemplate`

### Task 3: Write Template Rendering Tests
- Test `test_prime_cc_renders_valid_markdown`: Verify template renders without errors
- Test `test_prime_cc_has_required_sections`: Check for Variables, Instructions, Run, Read, Understand, Examples, Report sections
- Test `test_prime_cc_uses_config_variables`: Verify project name, language, architecture, package_manager are substituted
- Test `test_prime_cc_conditional_sections`: Test {% if %} blocks for optional paths (adws_dir, scripts_dir)

### Task 4: Write Content Validation Tests
- Test `test_prime_cc_includes_claude_code_patterns`: Verify key Claude Code guidance is present
- Test `test_prime_cc_includes_tool_preferences`: Check for Read, Edit, Bash, Grep, Glob tool guidance
- Test `test_prime_cc_includes_cli_workflows`: Verify commands section includes project commands
- Test `test_prime_cc_markdown_structure`: Ensure valid markdown (headers, code blocks, lists)

### Task 5: Run Validation Commands
Execute all validation commands to ensure no regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- `cd tac_bootstrap_cli && uv run ruff check .`
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

### Task 6: Documentation Check
- Verify CLAUDE.md mentions prime_cc in commands list
- Check CHANGELOG for entry about prime_cc feature
- Ensure README documents the command if applicable

## Testing Strategy

### Unit Tests

**Template Rendering Tests:**
```python
def test_prime_cc_renders_valid_markdown(template_repo, python_config):
    """prime_cc.md.j2 should render valid markdown with expected sections."""
    content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)
    assert len(content.strip()) > 100
    assert "## Variables" in content
    assert "## Instructions" in content
    assert "## Run" in content
    assert "## Read" in content
    assert "## Understand" in content
    assert "## Examples" in content
    assert "## Report" in content
```

**Config Variable Substitution Tests:**
```python
def test_prime_cc_uses_config_variables(template_repo, python_config):
    """prime_cc.md.j2 should substitute config variables correctly."""
    content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)
    assert "test-python-app" in content  # config.project.name
    assert "Language.PYTHON" in content  # config.project.language
    assert "PackageManager.UV" in content  # config.project.package_manager
```

**Conditional Block Tests:**
```python
def test_prime_cc_conditional_adws_present(template_repo, python_config):
    """prime_cc.md.j2 should include ADW sections when adws_dir is configured."""
    python_config.paths.adws_dir = "adws"
    content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)
    assert "adws/README.md" in content
    assert "AI Developer Workflows" in content

def test_prime_cc_conditional_adws_absent(template_repo, python_config):
    """prime_cc.md.j2 should exclude ADW sections when adws_dir is None."""
    python_config.paths.adws_dir = None
    content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)
    assert "adws/README.md" not in content
```

**Claude Code Patterns Tests:**
```python
def test_prime_cc_includes_tool_preferences(template_repo, python_config):
    """prime_cc.md.j2 should include Claude Code tool preferences."""
    content = template_repo.render("claude/commands/prime_cc.md.j2", python_config)
    assert "Read tool" in content
    assert "Edit tool" in content
    assert "Bash tool" in content
    assert "Grep tool" in content
    assert "Glob tool" in content
```

### Edge Cases

1. **Minimal Config**: Test with minimal TACConfig (only required fields)
2. **Full Config**: Test with all optional paths configured
3. **No ADW**: Test when adws_dir is None or empty
4. **No Scripts**: Test when scripts_dir is None or empty
5. **Different Languages**: Test with Python, TypeScript, Go configurations
6. **Different Package Managers**: Test with uv, npm, pnpm, go, cargo

## Acceptance Criteria

1. **Template Renders Successfully**: The prime_cc.md.j2 template renders without errors for various TACConfig configurations
2. **All Sections Present**: Generated markdown includes all expected sections (Variables, Instructions, Run, Read, Understand, Examples, Report)
3. **Config Variables Substituted**: Jinja2 variables like `{{ config.project.name }}` are properly replaced with actual values
4. **Conditional Blocks Work**: {% if %} blocks correctly include/exclude content based on config
5. **Markdown Valid**: Generated content is valid markdown with proper headers, code blocks, and lists
6. **Claude Code Patterns Included**: Key guidance about tool usage (Read, Edit, Bash, Grep, Glob) is present
7. **Integration Confirmed**: scaffold_service.py includes prime_cc in commands list (already verified at line 322)
8. **All Tests Pass**: New tests pass along with existing test suite
9. **Zero Regressions**: All validation commands succeed (pytest, ruff, mypy, CLI smoke test)
10. **Documentation Complete**: Command is documented in appropriate README/CLAUDE.md files

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios (all tests including new prime_cc tests)
- `cd tac_bootstrap_cli && uv run pytest tests/test_prime_cc_template.py -v` - Run only new tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

**Implementation Status:**
- ✅ Base command file exists at `.claude/commands/prime_cc.md`
- ✅ Template exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2`
- ✅ Integration in scaffold_service.py at line 322
- ⏳ Tests needed for template rendering and validation

**Key Design Decisions:**
1. **Extends /prime**: The command first runs /prime for general context, then adds Claude Code-specific context
2. **Tool Preferences**: Emphasizes using Read, Edit, Bash, Grep, Glob tools over command-line alternatives
3. **Comprehensive Coverage**: Loads commands, hooks, settings, output styles, ADW workflows
4. **Project-Agnostic Static Content**: Claude Code guidance remains the same; only paths/commands are templated
5. **Conditional Sections**: Uses {% if %} for optional features (ADW, scripts) to avoid broken references

**Future Enhancements:**
- Consider adding validation that checks if generated project actually uses Claude Code
- Could add metrics tracking for how often /prime_cc is used vs /prime
- Might add more examples for specific project types (Python/DDD, TypeScript/React, etc.)

**Related Tasks:**
- This is Task 13/49 in the TAC-12 Wave 1 implementation
- Part of the larger effort to add 13 new commands to TAC Bootstrap
- Builds on existing prime.md command foundation
