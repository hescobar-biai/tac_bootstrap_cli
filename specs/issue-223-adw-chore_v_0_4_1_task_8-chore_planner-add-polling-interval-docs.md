# Chore: Add polling interval documentation to tac_bootstrap_cli README

## Metadata
issue_number: `223`
adw_id: `chore_v_0_4_1_task_8`
issue_json: `{"number":223,"title":"Add polling interval documentation to tac_bootstrap_cli README","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_v_0_4_1_task_8\n\n\n**Description:**\nAdd a dedicated section documenting recommended polling intervals and GitHub API rate limiting considerations for the trigger systems.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md`\n\n**Content to add after \"Issue Chain Trigger Setup\" section:**\n\n```markdown\n#### Trigger Polling Configuration\n\n| Trigger | Default Interval | Recommended Range | Notes |\n|---------|------------------|-------------------|-------|\n| `trigger_cron.py` | 20s | 15s - 60s | Lower intervals increase API usage |\n| `trigger_issue_chain.py` | 20s | 20s - 120s | Sequential processing, less frequent OK |\n\n**GitHub API Rate Limiting:**\n- Authenticated requests: 5,000/hour\n- Each polling cycle makes 1-3 API calls per open issue\n- For repos with many open issues, use longer intervals (30s+)\n- Monitor rate limits: `gh api rate_limit`"}`

## Chore Description

Add documentation section to the tac_bootstrap_cli README.md file explaining recommended polling intervals for the trigger systems (`trigger_cron.py` and `trigger_issue_chain.py`) and GitHub API rate limiting considerations. This will help users configure their trigger systems appropriately based on their repository's needs.

## Relevant Files

### Existing Files
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md` - Main README file where the documentation section needs to be added. The content should be inserted after the "Issue Chain Trigger Setup" section (around line 636).

### New Files
None - this is a documentation update to an existing file.

## Step by Step Tasks

### Task 1: Locate insertion point in README.md
- Read the README.md file to confirm the exact location of the "Issue Chain Trigger Setup" section
- Verify the section ends around line 636
- Identify the proper insertion point (after the Issue Chain Trigger Setup section, before "### Key Concepts" section)

### Task 2: Add polling interval documentation section
- Insert the new "#### Trigger Polling Configuration" section with the table showing default intervals, recommended ranges, and notes for each trigger type
- Add the "**GitHub API Rate Limiting:**" subsection with bullet points explaining rate limits and monitoring commands
- Ensure proper markdown formatting and indentation consistency with the rest of the document

### Task 3: Validate changes
- Review the updated README.md to ensure formatting is correct
- Verify the new section flows naturally with surrounding content
- Check that all markdown syntax is valid (table formatting, bold text, code blocks)
- Run validation commands to ensure no regressions

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

- This is a documentation-only change and should not affect any code functionality
- The polling intervals mentioned (20s default, 15-60s for cron, 20-120s for issue chain) are based on the existing trigger implementations
- The GitHub API rate limit information (5,000/hour for authenticated requests) is accurate as of the current GitHub API documentation
- The insertion point should be after line 636 (end of Issue Chain Trigger Setup) and before the "### Key Concepts" section
