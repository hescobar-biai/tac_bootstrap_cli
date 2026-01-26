# Feature: Add verbose-bullet-points.md.j2 Output Style Template

## Metadata
- issue_number: `236`
- adw_id: `feature_Tac_9_task_5`
- issue_json: Create Jinja2 template for the "verbose-bullet-points" output style

## Feature Description

Create a Jinja2 template for the "verbose-bullet-points" output style. This style produces detailed, well-structured bullet-point formatted responses that prioritize clarity and comprehensiveness over token efficiency. It complements the existing "concise-*" family of output styles by providing the opposite approach: maximizing information delivery and detailed breakdown of complex topics.

The feature involves creating two files with identical content:
1. **Template file**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/verbose-bullet-points.md.j2`
2. **Rendered file**: `.claude/output-styles/verbose-bullet-points.md`

## User Story

As a **TAC Bootstrap user**
I want to **use the verbose-bullet-points output style for detailed, structured responses**
So that **I can receive comprehensive explanations with clear bullet-point formatting when tackling complex topics requiring detailed breakdown**

## Problem Statement

The TAC Bootstrap project currently provides three output styles (concise-done, concise-ultra, concise-tts) that all prioritize token efficiency and brevity. There is no output style option for users who need detailed, well-structured responses with comprehensive information delivery. The "verbose-bullet-points" style fills this gap by offering an alternative approach optimized for clarity and completeness rather than brevity.

## Solution Statement

Create a new output style template following the established pattern used by existing styles. The verbose-bullet-points style will:
- Provide detailed, comprehensive responses using structured bullet-point formatting
- Emphasize clarity and understanding over token efficiency
- Follow the identical structure and conventions as existing output styles (concise-done, concise-ultra, concise-tts)
- Include response guidelines, use cases, examples, and important notes
- Be deployed as both a Jinja2 template and a rendered markdown file

## Relevant Files

### Existing Reference Files
- `.claude/output-styles/concise-done.md` - Reference for structure and formatting
- `.claude/output-styles/concise-tts.md` - Reference for detailed guidelines section
- `.claude/output-styles/concise-ultra.md` - Reference for consistent pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2` - Reference template
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-tts.md.j2` - Reference template

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/verbose-bullet-points.md.j2` (CREATE)
- `.claude/output-styles/verbose-bullet-points.md` (CREATE)

## Implementation Plan

### Phase 1: Analysis & Planning
Analyze existing output style templates to understand:
- Document structure (heading, guidelines, use cases, examples, notes)
- Formatting conventions (markdown, bullet styles, examples with checkmarks)
- Content patterns and writing style
- Jinja2 template structure (static content with .j2 extension)

### Phase 2: Content Creation
Create the verbose-bullet-points output style content:
- Write response guidelines emphasizing detailed, structured bullet-point approach
- Define when to use this style (complex explanations, multi-step processes, comprehensive analysis)
- Create good/bad example responses showing verbose vs. minimal approaches
- Document important notes about the style's purpose and application

### Phase 3: File Creation & Validation
Create both required files with identical content:
- Generate the Jinja2 template file
- Generate the rendered markdown file
- Verify formatting consistency with existing styles
- Validate markdown syntax

## Step by Step Tasks

### Task 1: Analyze Existing Output Styles
- Read concise-done.md, concise-tts.md, and concise-ultra.md to understand structure
- Identify consistent sections: Response Guidelines, When to Use This Style, Example Responses, Important Notes
- Note formatting conventions: dashes for bullets, bold text, backticks for code, checkmarks for examples
- Document the pattern for replication

**Status:** Ready for implementation

### Task 2: Create verbose-bullet-points.md.j2 Template
- Create file: `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/verbose-bullet-points.md.j2`
- Write heading: "# Verbose Bullet Points Output Style"
- Add introductory statement about the style's purpose
- Create Response Guidelines section with 6-8 bullet points emphasizing:
  - Detailed, comprehensive responses
  - Structured bullet-point formatting
  - Clarity and understanding focus
  - Multi-level hierarchical organization when needed
  - Complete explanations of complex topics
- Maintain static markdown content (no Jinja2 variables)

**Subtasks:**
- Define 5+ use cases for the verbose-bullet-points style
- Write good example responses (marked with ✓) showing detailed bullet-point structure
- Write bad example responses (marked with ✗) showing minimal/insufficient approaches
- Create Important Notes section addressing style application and limitations

### Task 3: Create .claude/output-styles/verbose-bullet-points.md Rendered File
- Copy content from verbose-bullet-points.md.j2 to `.claude/output-styles/verbose-bullet-points.md`
- Verify identical structure and formatting

**Status:** After Task 2 completion

### Task 4: Validate & Verify
- Check markdown syntax is valid
- Verify consistency with existing output style files
- Confirm both files exist and contain identical content
- Run validation commands (linting, type checking)

**Status:** Final validation step

## Testing Strategy

### Unit Tests
- No unit tests required; this is configuration/documentation file
- Structure validation: Ensure markdown syntax is correct

### Edge Cases
- Verify markdown renders correctly in various markdown processors
- Check that bullet-point nesting works as intended
- Validate that example responses are realistic and helpful

### Integration Testing
- Verify files are correctly placed in expected directories
- Confirm `.j2` file would render identically to `.md` file during project generation
- Test that output style can be referenced alongside other styles

## Acceptance Criteria

1. ✓ File `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/verbose-bullet-points.md.j2` created with complete content
2. ✓ File `.claude/output-styles/verbose-bullet-points.md` created with identical content
3. ✓ Document includes all standard sections: heading, Response Guidelines, When to Use This Style, Example Responses, Important Notes
4. ✓ Response Guidelines section contains 6+ bullet points emphasizing detailed, comprehensive, bullet-point-formatted approach
5. ✓ "When to Use This Style" section includes 4+ specific use cases
6. ✓ Example Responses include both good (✓) and bad (✗) examples demonstrating the style
7. ✓ Formatting is consistent with existing output style files (concise-done, concise-tts, concise-ultra)
8. ✓ No Jinja2 variables used; content is static markdown
9. ✓ Markdown syntax is valid and renders correctly
10. ✓ All validation commands pass without errors

## Validation Commands

Execute all commands to validate with zero regressions:

```bash
# Lint check
cd tac_bootstrap_cli && uv run ruff check .

# Type check
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Smoke test - verify CLI still works
cd tac_bootstrap_cli && uv run tac-bootstrap --help

# Verify file existence and content
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/verbose-bullet-points.md.j2 && echo "Template file exists"
test -f .claude/output-styles/verbose-bullet-points.md && echo "Rendered file exists"
```

## Notes

- This feature creates documentation/configuration files, not executable code
- The .j2 extension is a naming convention; files contain static markdown without Jinja2 syntax
- Both files should have identical content (template and rendered versions)
- This complements the existing "concise-*" output style family by providing the verbose alternative
- Future enhancements could include integration with Claude Code output style selection mechanisms
- The style prioritizes information delivery and clarity over token efficiency, making it suitable for complex explanations and documentation use cases
