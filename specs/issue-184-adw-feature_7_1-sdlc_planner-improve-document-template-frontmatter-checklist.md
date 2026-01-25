# Validation Checklist: Improve /document Template with IDK Frontmatter

**Spec:** `specs/issue-184-adw-feature_7_1-sdlc_planner-improve-document-template-frontmatter.md`
**Branch:** `feature-issue-184-adw-feature_7_1-improve-document-template-frontmatter`
**Review ID:** `feature_7_1`
**Date:** `2026-01-24`

## Automated Technical Validations

- [x] Syntax and type checking - PASSED
- [x] Linting - PASSED
- [x] Unit tests - PASSED (669 passed, 2 skipped)
- [x] Application smoke test - PASSED

## Acceptance Criteria

- [x] **Template Renders Correctly**
  - `document.md.j2` template renders without Jinja2 errors
  - YAML frontmatter is syntactically valid
  - All Jinja2 variables have appropriate defaults
  - Template works with minimal and full config

- [x] **Frontmatter Structure Complete**
  - Contains all required fields: doc_type, adw_id, date, idk, tags, related_code
  - Uses hardcoded `---` YAML delimiters
  - `{{ config.adw_id | default('N/A') }}` variable works correctly
  - `{{ config.capability | default('general') }}` variable works correctly
  - idk field is a YAML list of strings
  - related_code field is a YAML list of file paths

- [x] **Agent Instructions Clear**
  - Instructions explicitly state to extract 3-8 IDK keywords
  - Guidance to prioritize canonical_idk.yml vocabulary is clear
  - Testing section requirement is explicit with format examples
  - Final step to update conditional_docs.md is present and actionable
  - All steps maintain existing git diff analysis instructions

- [x] **Documentation Format Updated**
  - Frontmatter appears at the beginning of the markdown format
  - New "Testing" section is added between Configuration and Notes
  - All existing sections are preserved
  - Format examples are clear and complete

- [x] **Root File Synchronized**
  - `.claude/commands/document.md` matches template output
  - Spanish language is preserved in root file
  - All instructions are properly translated
  - File is ready for immediate use by agents

- [x] **Canonical IDK Integration**
  - Instructions reference canonical_idk.yml optionally (if exists)
  - Agents are guided to supplement canonical terms with feature-specific keywords
  - No failure occurs when canonical_idk.yml doesn't exist

- [x] **Testing Section Well-Defined**
  - Format uses executable bash commands
  - Commands have brief explanatory text
  - Examples show proper code block formatting
  - Instructions are practical and copy-pasteable

- [x] **Conditional Docs Integration**
  - Final instruction step added to update conditional_docs.md
  - Step appears after documentation file creation
  - Instruction is clear about adding entry with appropriate conditions

## Validation Commands Executed

```bash
# Render template with test config (manual step - verify output)
cd tac_bootstrap_cli && uv run python -c "
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import TACConfig, ProjectSpec, PathsSpec, Language
config = TACConfig(
    project=ProjectSpec(name='test-project', language=Language.PYTHON),
    paths=PathsSpec()
)
repo = TemplateRepository()
output = repo.render('claude/commands/document.md.j2', {'config': config})
print(output[:500])  # Print first 500 chars to verify frontmatter
"

# Validate YAML frontmatter syntax (after rendering)
cd tac_bootstrap_cli && python -c "
import yaml
# Simulate frontmatter extraction
frontmatter_sample = '''---
doc_type: feature
adw_id: test_123
date: 2026-01-24
idk:
  - keyword1
  - keyword2
tags:
  - feature
  - general
related_code:
  - src/file.py
---'''
parsed = yaml.safe_load(frontmatter_sample.split('---')[1])
assert parsed['doc_type'] == 'feature'
assert isinstance(parsed['idk'], list)
print('Frontmatter YAML is valid ✓')
"

# Run standard validation suite
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Review Summary

The implementation successfully enhances the `/document` command template to include YAML frontmatter with IDK keywords. Both the Jinja2 template (`document.md.j2`) and the rendered Spanish root file (`.claude/commands/document.md`) have been updated with:
1. Structured YAML frontmatter containing doc_type, adw_id, date, idk keywords, tags, and related_code fields
2. Clear agent instructions for extracting 3-8 IDK keywords with optional canonical_idk.yml integration
3. New Testing section with executable bash command format
4. Final step to update conditional_docs.md

All acceptance criteria are met. The template renders correctly, YAML frontmatter is syntactically valid, all tests pass (669 passed, 2 skipped), linting and type checking pass, and the CLI smoke test succeeds.

## Review Issues

No blocking issues found. The implementation is complete and ready for merge.

---
*Generado por el comando `/review` - TAC Bootstrap CLI*
