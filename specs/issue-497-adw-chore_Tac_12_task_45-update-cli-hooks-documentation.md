# Chore: Update CLI Hooks Documentation

## Metadata
issue_number: `497`
adw_id: `chore_Tac_12_task_45`
issue_json: `{"number": 497, "title": "[Task 45/49] [CHORE] Update CLI hooks documentation", "body": "Update CLI hooks documentation with all new TAC-12 hooks."}`

## Chore Description

Enhance hooks.md documentation by adding detailed documentation for the 9 new TAC-12 hooks (send_event, session_start, pre_tool_use, post_tool_use, notification, stop, subagent_stop, pre_compact, user_prompt_submit) while retaining existing content. Add a brief 'Status Line Integration' section documenting how hooks interact with Claude Code's status line feature. Cross-reference utilities.md for the 5 utilities (summarizer, constants, llm/, tts/, and model_extractor).

The task requires:
- Adding documentation for 9 new TAC-12 hooks
- Adding documentation for 5 new utilities (with cross-reference to utilities.md)
- Documenting observability infrastructure
- Adding status line integration documentation

## Relevant Files

### Current Documentation Files
- `tac_bootstrap_cli/docs/hooks.md` - **To be enhanced** with 9 new hook sections and status line integration
- `tac_bootstrap_cli/docs/utilities.md` - **To be enhanced** with 5 new utility sections (already contains LLM/TTS)

### Hook Implementations
The 9 new TAC-12 hooks to document:
- `.claude/hooks/send_event.py` - Core event dispatch for observability
- `.claude/hooks/session_start.py` - Session context initialization
- `.claude/hooks/pre_tool_use.py` - Tool execution validation
- `.claude/hooks/post_tool_use.py` - Post-execution processing
- `.claude/hooks/notification.py` - System notifications
- `.claude/hooks/stop.py` - Session termination and cleanup
- `.claude/hooks/subagent_stop.py` - Subagent completion handling
- `.claude/hooks/pre_compact.py` - Context preservation before compaction
- `.claude/hooks/user_prompt_submit.py` - User prompt handling

### Utility Implementations
The 5 utilities to document:
- `.claude/hooks/utils/constants.py` - Shared configuration and constants
- `.claude/hooks/utils/summarizer.py` - Event and context summarization
- `.claude/hooks/utils/llm/` - LLM providers (already documented in utilities.md)
- `.claude/hooks/utils/tts/` - TTS providers (already documented in utilities.md)
- `.claude/hooks/utils/model_extractor.py` - LLM model extraction utilities

### Status Line Integration
- `.claude/status_lines/status_line_main.py` - Status line integration system

### New Files
No new files required. Only enhancements to existing documentation.

## Step by Step Tasks

### Task 1: Review Current hooks.md Structure
- Read full hooks.md to understand existing organization
- Identify where new hook sections should be inserted
- Note existing documentation patterns and style
- Document hook sections already present: universal_hook_logger, context_bundle_builder, dangerous_command_blocker, pre_tool_use, post_tool_use, stop, notification

**Success Criteria:**
- Understand current documentation structure
- Identify placement for new sections (after existing hooks, before Hook Configuration section)

### Task 2: Read and Analyze New Hook Implementations
- Read first 100 lines of each new hook file to understand purpose and functionality
- Extract key features, triggers, and configuration details
- Note any special dependencies or environment variables
- Document expected inputs/outputs for each hook

**Success Criteria:**
- Have detailed understanding of all 9 hooks
- Identify common patterns and differences
- Ready to create documentation sections

### Task 3: Read Utility Implementations
- Read constants.py to document configuration constants
- Read summarizer.py to document summarization utilities
- Read model_extractor.py to document LLM utilities
- Verify that llm/ and tts/ utilities are already documented in utilities.md

**Success Criteria:**
- Understand 5 utilities and their purposes
- Identify what needs to be added to utilities.md
- Determine what requires cross-reference only

### Task 4: Enhance hooks.md - Add New Hook Sections
- Insert 5 new TAC-12 hook sections after existing hooks
- Add sections for: send_event, session_start, pre_compact, subagent_stop, user_prompt_submit
- Follow existing documentation structure: location, trigger, features, usage/config example, outputs
- Keep examples minimal but concrete (one per hook type)
- Maintain consistent formatting and style with existing sections

**Success Criteria:**
- All 5 new hook sections added with consistent format
- Each section includes: location, trigger timing, features list, basic config example, output locations
- Documentation is complete and accurate

### Task 5: Enhance hooks.md - Add Status Line Integration Section
- Create new "Status Line Integration" section in hooks.md
- Document status_lines/ directory structure
- Explain how hooks can update Claude Code's status line
- Document usage examples: showing agent name, model, branch, custom metrics
- Add cross-reference to utilities.md

**Success Criteria:**
- Status Line Integration section added with clear explanation
- Usage examples provided
- Integration points documented

### Task 6: Enhance utilities.md - Add New Utilities Documentation
- Add "Observability Utilities" section to utilities.md
- Document constants.py with key configuration constants
- Document summarizer.py with summarization interfaces
- Document model_extractor.py with LLM utilities
- Add cross-references back to hooks.md
- Keep LLM and TTS sections as-is (already comprehensive)

**Success Criteria:**
- All 3 new utilities documented in utilities.md
- Cross-references to hooks.md maintained
- Consistent with existing documentation style
- Utilities section updated without disrupting LLM/TTS documentation

### Task 7: Validate Documentation Quality
- Review all new sections for completeness and accuracy
- Check that all 9 hooks have adequate documentation
- Verify cross-references between hooks.md and utilities.md are correct
- Ensure configuration examples are valid JSON
- Check formatting consistency across all new sections

**Success Criteria:**
- All documentation sections complete and internally consistent
- No broken cross-references
- Examples are valid and realistic
- No typos or formatting issues

### Task 8: Run Validation Commands
- Build project and check for errors
- Run any documentation linting (if available)
- Verify files are valid Markdown
- Smoke test the documentation structure

**Success Criteria:**
- All commands pass with no errors
- Documentation is valid Markdown
- No regressions in existing functionality

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check . --select=E,W,F` - Linting check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

- **Retain Existing Content:** Do NOT remove or replace existing documentation sections. Only add new sections and enhance cross-references.
- **Style Consistency:** Match the existing documentation patterns for sections (location, features, usage, outputs)
- **Minimal Configuration Examples:** Show one concrete example per hook type rather than exhaustive examples for all 9 hooks
- **Cross-References:** Link from hooks.md "Utilities" section to utilities.md "Observability Utilities"
- **Acceptance Criteria:** Each hook section should include location, trigger timing, features list, config example, and output locations
- **Status Line Priority:** The status line integration is key observability infrastructure and should be clearly documented as part of the hook output channels

---

**Task Wave:** Wave 8 - Documentation (Task 45 of 6)
**Workflow Metadata:** /chore, /adw_sdlc_zte_iso, /adw_id: chore_Tac_12_task_45
