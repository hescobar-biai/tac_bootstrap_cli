# Feature: Update background.md with TAC-12 improvements

## Metadata
issue_number: `489`
adw_id: `feature_Tac_12_task_37`
issue_title: `[Task 37/49] [FEATURE] Update background.md with TAC-12 improvements`

## Feature Description

Replace the current Task Tool delegation documentation in `background.md` with a complete TAC-12 implementation using the `claude` CLI directly. This transformation moves from abstract Task tool concepts to concrete bash-based command execution with structured reporting, file auto-renaming, and proper error handling.

The new implementation enables users to execute user prompts in the background with:
- Direct `claude` CLI invocation with `--dangerously-skip-permissions` flag
- Structured report generation with timestamps
- Automatic file renaming to `.complete.md` or `.failed.md`
- Clear security warnings and usage guidelines
- Project-specific template parameterization via Jinja2

## User Story

As a developer using TAC Bootstrap,
I want to execute prompts in background with structured reporting,
So that I can delegate long-running analysis tasks without blocking my workflow and have automatic status tracking.

## Problem Statement

The current `background.md` documentation focuses on abstract Task tool delegation using the Claude Code SDK. This approach doesn't align with TAC-12's emphasis on direct `claude` CLI usage and structured automation. Users need a concrete, documented way to:

1. Execute user-provided prompts via `claude` CLI in the background
2. Capture structured reports with proper formatting
3. Automatically track execution status (completion or failure)
4. Understand security implications of bypassing permission checks
5. Know where output files are saved and how to monitor them

## Solution Statement

Create comprehensive markdown documentation that teaches the background command workflow using bash scripting with the `claude` CLI. The solution includes:

- **Base file** (`.claude/commands/background.md`): Uses runtime variables ($1, $2, $3) for flexibility
- **Template file** (`tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2`): Uses Jinja2 for project-level configuration
- **Complete implementation**: Variables, instructions, bash code blocks, examples, and security warnings
- **Structured reporting**: Timestamped reports with status-based file renaming
- **Error handling**: Fallback mechanisms for rename failures
- **Directory structure**: Documents the `agents/background/` directory prerequisite

## Relevant Files

### Existing Files to Modify

1. **Base file**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/background.md`
   - Currently contains Task Tool documentation
   - Must be replaced with bash-based claude CLI implementation
   - Uses shell variables ($1, $2, $3) for runtime flexibility

2. **Template file**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2`
   - Must match base file structure and content
   - Uses Jinja2 for project-specific configuration
   - Parameterizes directory paths and configuration examples

### Reference Implementation

- External reference: `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/background.md` (not directly accessible, use issue specifications)

### Related Files for Context

- `.claude/commands/` - Other command documentation files (for pattern reference)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/` - Template directory structure
- `CLAUDE.md` - Project guidelines (Jinja2 variable conventions, DDD patterns)

### New Files

None - only updates to existing files

## Implementation Plan

### Phase 1: Analysis and Design
- Understand current background.md limitations
- Review issue specifications for complete requirements
- Identify key differences from Task Tool approach
- Design variable mapping ($1, $2, $3) and Jinja2 parameterization strategy
- Plan documentation structure for clarity and security

### Phase 2: Base File Implementation
- Replace current Task Tool documentation with new bash-based approach
- Implement Variables section with clear descriptions
- Add comprehensive Instructions section
- Create bash code block with claude CLI invocation
- Document structured report format
- Add security warnings for --dangerously-skip-permissions
- Include examples showing common use cases
- Document directory structure prerequisites

### Phase 3: Template File Implementation
- Update template file to match base file structure
- Apply Jinja2 parameterization for project-specific values
- Ensure directory paths use template variables
- Verify configuration examples work in rendered template context

### Phase 4: Validation and Testing
- Verify both files are identical in structure and instructions
- Confirm all Key Changes from issue are present
- Test bash code blocks for syntax correctness
- Validate Jinja2 template rendering (if possible)
- Run acceptance criteria checks

## Step by Step Tasks

### Task 1: Analyze Current State and Issue Requirements
- Read current background.md to understand existing content
- Extract all Key Changes specifications from issue
- Identify all required variables: USER_PROMPT ($1), MODEL ($2), REPORT_FILE ($3)
- Understand auto-rename behavior (.complete.md, .failed.md)
- Note timestamp handling: TIMESTAMP=$(date +%a_%H_%M_%S)
- Document directory structure requirement: agents/background/

### Task 2: Design File Content Structure
- Create outline of new background.md structure
- Map issue requirements to documentation sections
- Plan Variable descriptions for $1, $2, $3 with defaults
- Design Instructions section with security implications
- Plan bash script structure with proper error handling
- Design Examples showing different use cases
- Create security warnings section
- Plan Report section expectations

### Task 3: Implement Base File Content
- Replace complete content of `.claude/commands/background.md`
- Write Variables section with clear explanations
- Write Instructions section covering:
  - When to use background execution
  - Security implications of --dangerously-skip-permissions
  - Directory structure requirements
  - Output file behavior and auto-renaming
- Implement bash code block with:
  - Proper variable handling ($1, $2, $3)
  - Timestamp capture: TIMESTAMP=$(date +%a_%H_%M_%S)
  - Claude CLI invocation with --dangerously-skip-permissions
  - Structured report format
  - Auto-rename logic with error handling (.complete.md/.failed.md)
  - Fallback mechanisms if rename fails
- Add 2-3 practical Examples
- Write Report section with expected outcomes

### Task 4: Implement Template File
- Update `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2`
- Copy base file structure to template
- Add Jinja2 variables for:
  - Directory paths (agents/background/)
  - Project-specific configuration references
  - Example adaptations for templated projects
- Ensure runtime variables ($1, $2, $3) remain as bash variables (NOT templated)
- Verify clean separation: Jinja2 for template-time, bash variables for runtime

### Task 5: Verify Content Consistency
- Compare base file and template file structures
- Confirm identical documentation and approach
- Verify all Key Changes are present in both files
- Check that template file would render correctly
- Validate bash script syntax in both files
- Confirm Jinja2 syntax is correct in template

### Task 6: Documentation and Security Review
- Add clear security warnings about --dangerously-skip-permissions
- Document when directory should be created
- Verify all use cases are covered by Examples
- Check that error handling is properly documented
- Ensure Report section expectations are clear
- Add notes about file output location and monitoring

### Task 7: Run Validation Commands
- Verify file format (valid markdown)
- Check bash script syntax with shellcheck if available
- Validate Jinja2 syntax for template file
- Confirm directory structure documentation is complete
- Run final acceptance criteria checks

## Testing Strategy

### Content Validation
- Verify markdown syntax is valid in both files
- Check that all code blocks are properly formatted
- Confirm variable references ($1, $2, $3) are consistent
- Validate Jinja2 template syntax in .j2 file

### Bash Script Validation
- Review bash script for proper variable handling
- Check error handling logic (rename failure fallback)
- Verify timestamp format matches specification
- Confirm claude CLI invocation is correct
- Test that report file renaming works as expected

### Documentation Completeness
- Verify all issue Key Changes are addressed
- Confirm security warnings are clear and prominent
- Check that Examples cover common scenarios
- Validate Report section expectations

### Edge Cases
- Missing agents/background/ directory
- Report file rename failure
- Malformed USER_PROMPT input
- Model parameter with invalid value
- REPORT_FILE path doesn't exist or isn't writable

## Acceptance Criteria

1. **Base file updated**: `.claude/commands/background.md` completely replaced with bash-based claude CLI implementation
2. **Template file updated**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2` with Jinja2 parameterization
3. **All Key Changes present**:
   - Variables: USER_PROMPT ($1), MODEL ($2, defaults 'sonnet'), REPORT_FILE ($3)
   - Uses `claude` CLI directly with --dangerously-skip-permissions
   - Structured report format with append-system-prompt
   - Auto-rename to .complete.md or .failed.md based on exit code
   - Timestamp: TIMESTAMP=$(date +%a_%H_%M_%S)
   - Directory: agents/background/ documented
4. **Files are identical in structure**: Base and template have same documentation approach, differ only in variable syntax
5. **Security warnings included**: Clear documentation of --dangerously-skip-permissions implications
6. **Error handling documented**: Fallback behavior when rename fails, directory doesn't exist, etc.
7. **Examples provided**: 2-3 realistic use cases showing command execution
8. **Valid markdown and bash syntax**: Files pass validation checks

## Validation Commands

Run these commands to validate implementation with zero regressions:

```bash
# Verify base file exists and is valid markdown
head -20 .claude/commands/background.md

# Verify template file exists and is valid markdown
head -20 tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2

# Check bash syntax in base file (if shellcheck available)
shellcheck -s bash .claude/commands/background.md

# Verify files contain all required elements (spot checks)
grep -q "USER_PROMPT" .claude/commands/background.md && echo "✓ USER_PROMPT variable documented"
grep -q "MODEL" .claude/commands/background.md && echo "✓ MODEL variable documented"
grep -q "REPORT_FILE" .claude/commands/background.md && echo "✓ REPORT_FILE variable documented"
grep -q "dangerously-skip-permissions" .claude/commands/background.md && echo "✓ Security flag documented"
grep -q ".complete.md" .claude/commands/background.md && echo "✓ Complete status renaming documented"
grep -q ".failed.md" .claude/commands/background.md && echo "✓ Failed status renaming documented"
grep -q "agents/background" .claude/commands/background.md && echo "✓ Directory structure documented"

# Verify template file has Jinja2 variables (examples)
grep -q "{{" tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2 && echo "✓ Template has Jinja2 variables"
```

## Notes

- The issue reference file at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/background.md` is not directly accessible, so implementation uses detailed specifications from the issue itself
- Both base and template files should be updated identically in structure and approach
- Runtime variables ($1, $2, $3) are NOT templated with Jinja2 - they remain as bash shell variables
- Jinja2 parameterization should be limited to: directory paths, configuration references, and template-time customizations
- Security implications of --dangerously-skip-permissions are significant and should be documented prominently
- The auto-rename behavior (.complete.md/.failed.md) is critical for workflow status tracking
- Directory `agents/background/` should be created during project initialization; documentation should note this prerequisite
- Future consideration: Add monitoring utilities or dashboard for tracking background task statuses
