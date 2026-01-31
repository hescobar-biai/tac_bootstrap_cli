# Feature: Create summarizer.py Hook Utility

## Metadata
- **issue_number:** `481`
- **adw_id:** `feature_Tac_12_task_29`
- **wave:** Hook Utilities (Task 29 of 5)
- **category:** Hook utility implementation

## Feature Description

Create a self-contained hook utility (`summarizer.py`) that generates concise AI-powered summaries of events using the Claude Haiku model. This utility will be used by hooks that need to produce brief, human-readable summaries for logging, notifications, or event tracking.

The summarizer follows existing hook utility patterns in the codebase (e.g., `llm/anth.py`, `tts/` utilities) with:
- Hardcoded model version (claude-haiku-4-5-20251001)
- Silent failure pattern (returns None on errors)
- Environment-based authentication (ANTHROPIC_API_KEY)
- Length validation (max 150 characters)
- One-sentence output format

## User Story

As a hook developer,
I want a reusable summarizer utility that generates event summaries,
So that I can produce concise, consistent summaries across different hooks without duplicating LLM integration code.

## Problem Statement

Currently, there's no dedicated utility for generating AI summaries in hooks. Any hook needing summaries must either:
1. Duplicate Anthropic API integration code
2. Reuse the generic `anth.py` LLM utility without domain-specific prompt engineering

A specialized summarizer utility provides a focused interface for summary generation with appropriate error handling and validation.

## Solution Statement

Create a standalone summarizer utility that:
- Provides a simple `generate_event_summary(event_text: str) -> Optional[str]` function
- Encapsulates Claude API integration (authentication, request/response handling)
- Enforces output constraints (150-char max, single sentence)
- Follows existing hook utility patterns for consistency
- Gracefully degrades on errors (returns None, no exceptions)

The utility will be:
1. Implemented directly in `.claude/hooks/utils/summarizer.py` (no subdirectory)
2. Templated as Jinja2 in `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/summarizer.py.j2`
3. Integrated into `scaffold_service.py` hook utilities list

## Relevant Files

### Existing Files (Reference/Context)
- `.claude/hooks/utils/constants.py` - Pattern for UV script headers and utility structure
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2` - Template pattern with config variables
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Integration point for adding utility to scaffold

### New Files to Create
- `.claude/hooks/utils/summarizer.py` - Base implementation in main repository
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/summarizer.py.j2` - Jinja2 template for CLI generation

### Files to Modify
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Add summarizer.py to `_add_hook_files()` method

## Implementation Plan

### Phase 1: Foundation
- Examine existing hook utility patterns (constants.py, llm utilities)
- Understand UV script header format with embedded dependencies
- Understand how scaffold_service integrates utilities
- Review Jinja2 template structure

### Phase 2: Core Implementation
- Create base summarizer.py in `.claude/hooks/utils/`
- Implement `generate_event_summary()` function with proper error handling
- Add input validation and output length constraints
- Include UV script header with dependencies (anthropic, python-dotenv)

### Phase 3: Template & Integration
- Create Jinja2 template for CLI generation
- Update scaffold_service.py to include summarizer.py in hook utilities
- Verify file placement and naming conventions

### Phase 4: Validation
- Run all validation commands to ensure no regressions
- Verify generated files have correct structure and imports
- Test hook directory scaffold includes summarizer.py

## Step by Step Tasks

### Task 1: Analyze Existing Patterns
- Read `.claude/hooks/utils/constants.py` to understand UV script header
- Examine how `anth.py` (or similar LLM utility) handles API calls
- Review `scaffold_service.py` to see how utilities are registered
- Document expected function signature and return behavior

**Expected Outcome:** Clear understanding of patterns to follow

### Task 2: Create Base Implementation
- Create `.claude/hooks/utils/summarizer.py`
- Implement UV script header with `anthropic` and `python-dotenv` dependencies
- Implement `generate_event_summary(event_text: str) -> Optional[str]` function:
  - Load ANTHROPIC_API_KEY from environment
  - Create Anthropic client
  - Call Claude Haiku with summarization prompt
  - Validate output length (max 150 chars)
  - Return None on any error (silent failure)
- Add docstrings following existing patterns
- Ensure Python 3.8+ compatibility

**Expected Outcome:** Functional summarizer.py in base repo ready for testing

### Task 3: Create Jinja2 Template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/summarizer.py.j2`
- Template should mirror base implementation
- Use Jinja2 variables for project-specific config (if any)
- Keep template close to base implementation (minimal template logic)

**Expected Outcome:** Valid Jinja2 template file

### Task 4: Update ScaffoldService Integration
- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate the `_add_hook_files()` method (or equivalent hook utilities section)
- Add file action for `summarizer.py`:
  ```python
  ".claude/hooks/utils/summarizer.py",
  template="claude/hooks/utils/summarizer.py.j2",
  ```
- Place alongside other hook utilities (e.g., after constants.py)
- Verify file path and template reference are correct

**Expected Outcome:** Scaffold service includes summarizer.py generation

### Task 5: Validation
- Run tests to ensure no regressions
- Verify generated scaffold includes summarizer.py
- Confirm imports and dependencies resolve
- Check file permissions and structure

**Execute all validation commands listed below**

## Testing Strategy

### Unit Tests (if applicable)
- Test `generate_event_summary()` with valid input
- Test return value is <= 150 characters
- Test graceful failure (None return) on API error
- Test environment variable loading (ANTHROPIC_API_KEY)

### Edge Cases
- Empty string input
- Very long input (>5000 chars)
- Missing ANTHROPIC_API_KEY environment variable
- API timeout or rate limiting
- Malformed API response
- Network connectivity issues

### Integration Tests
- Verify scaffold generates summarizer.py correctly
- Verify generated file has correct imports
- Verify template variables render correctly

## Acceptance Criteria

- [ ] `summarizer.py` exists in `.claude/hooks/utils/` with valid Python syntax
- [ ] Function signature: `generate_event_summary(event_text: str) -> Optional[str]`
- [ ] Uses hardcoded model: `claude-haiku-4-5-20251001`
- [ ] Loads API key from `ANTHROPIC_API_KEY` environment variable
- [ ] Returns None on any error (silent failure pattern)
- [ ] Output is validated to be <= 150 characters
- [ ] UV script header includes `anthropic` and `python-dotenv` dependencies
- [ ] Jinja2 template created at correct path
- [ ] `scaffold_service.py` includes summarizer.py in hook utilities
- [ ] All validation commands pass with zero regressions
- [ ] Generated files from template are syntactically correct

## Validation Commands

Ensure zero regressions before completion:

```bash
# Test suite
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test (verify CLI works)
cd tac_bootstrap_cli && uv run tac-bootstrap --help

# Verify hook utilities are included in scaffold
cd tac_bootstrap_cli && uv run pytest -k "test_scaffold" -v
```

## Notes

- **Reference File:** External reference at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/summarizer.py` is for inspiration only; use codebase patterns as authoritative source
- **Placement:** Direct `.claude/hooks/utils/` (not in subdirectory) because summarizer is a specialized utility without multiple implementations (unlike LLM providers or TTS backends)
- **Dependencies:** Both `anthropic` and `python-dotenv` should be included in UV script header with Python 3.8+ requirement
- **Model Version:** Hardcoded to match issue specification; future model updates are standard maintenance
- **Future Enhancements:** Could be extended to support custom prompts or output constraints, but not in scope for this task
