---
doc_type: feature
adw_id: chore_Tac_12_task_45
date: 2026-02-02
idk:
  - hooks-documentation
  - observability-infrastructure
  - TAC-12-hooks
  - session-management
  - event-tracking
  - status-line-integration
  - hook-configuration
  - utilities-reference
  - security-validation
tags:
  - chore
  - documentation
  - hooks
  - observability
related_code:
  - tac_bootstrap_cli/docs/hooks.md
  - tac_bootstrap_cli/docs/utilities.md
  - .claude/hooks/send_event.py
  - .claude/hooks/session_start.py
  - .claude/hooks/pre_compact.py
  - .claude/hooks/subagent_stop.py
  - .claude/hooks/user_prompt_submit.py
  - .claude/hooks/utils/constants.py
  - .claude/hooks/utils/summarizer.py
  - .claude/status_lines/status_line_main.py
---

# Update CLI Hooks Documentation

**ADW ID:** chore_Tac_12_task_45
**Date:** 2026-02-02
**Specification:** specs/issue-497-adw-chore_Tac_12_task_45-update-cli-hooks-documentation.md

## Overview

Enhanced comprehensive documentation for TAC Bootstrap's hook system and observability utilities by documenting 9 new TAC-12 hooks (send_event, session_start, pre_compact, subagent_stop, user_prompt_submit, and existing pre_tool_use, post_tool_use, notification, stop) and adding status line integration documentation. Cross-referenced observability utilities (constants, summarizer, model_extractor) between hooks.md and utilities.md for seamless infrastructure understanding.

## What Was Built

### Documentation Files Enhanced

- **`tac_bootstrap_cli/docs/hooks.md`** - Comprehensive hook system documentation with:
  - 9 TAC-12 hook sections with trigger timing, features, and configuration examples
  - Status Line Integration section documenting editor status bar display
  - Hook configuration patterns and exit code strategy
  - Custom hook development guidance
  - Hook directory structure

- **`tac_bootstrap_cli/docs/utilities.md`** - Observability utilities documentation with:
  - Configuration Constants (constants.py) for session management
  - Event Summarization (summarizer.py) for AI-powered summaries
  - LLM and TTS provider documentation (already comprehensive)
  - Cross-references to hooks.md for integration patterns

## Technical Implementation

### Key Documentation Sections Added

#### In hooks.md

1. **Hook Types Table** - Overview of all 9 hook triggers and use cases
2. **Additional TAC-12 Hooks Section** - Detailed documentation for:
   - `send_event.py` - Event serialization and remote server transmission
   - `session_start.py` - Session initialization context capture (git, model, project)
   - `pre_compact.py` - Context preservation before compaction
   - `subagent_stop.py` - Subagent completion result aggregation
   - `user_prompt_submit.py` - User prompt validation and logging

3. **Status Line Integration Section** - Documentation for:
   - Status line display format and generation via `status_line_main.py`
   - Environment variables (CLAUDE_AGENT_NAME, CLAUDE_MODEL)
   - Integration with hooks for contributing context
   - Reading session context written by hooks

4. **Hook Configuration Examples** - JSON configuration for all hook types with realistic patterns

#### In utilities.md

1. **Observability Utilities Section** - Documentation for:
   - `constants.py` - Session log directory management functions
   - `summarizer.py` - AI-powered event summarization using Claude Haiku
   - `model_extractor.py` - Planned LLM utility (reference added)

2. **Cross-References** - Links back to [Additional TAC-12 Hooks](hooks.md#additional-tac-12-hooks) section

### Files Modified

- `tac_bootstrap_cli/docs/hooks.md`: Added 5+ sections totaling ~350 lines of new documentation
- `tac_bootstrap_cli/docs/utilities.md`: Added Observability Utilities section with ~150 lines

### Configuration Examples Provided

- Hook chaining patterns (multiple PreToolUse hooks)
- SessionStart hook configuration for context capture
- PreCompact hook setup for context preservation
- SubagentStop hook with transcript capture option
- UserPromptSubmit hook with validation modes
- Status line setup in settings.json

## How to Use

### Using the Hooks Documentation

1. **View all hook types and triggers**: See Hook Types table for quick reference
2. **Configure a specific hook**: Navigate to the relevant hook section in Additional TAC-12 Hooks
3. **Chain multiple hooks**: Use Hook Configuration section examples
4. **Create custom hooks**: Follow Creating Custom Hooks section with exit code strategy

### Using the Utilities Documentation

1. **Session management**: Import `constants.ensure_session_log_dir()` to organize hook logs
2. **Event summarization**: Use `summarizer.generate_event_summary()` for concise audit logs
3. **Provider selection**: Choose LLM/TTS providers based on project requirements
4. **Cross-reference**: Links between hooks.md and utilities.md enable seamless navigation

### Integration Example

```python
# In a custom hook
from utils.constants import ensure_session_log_dir
from utils.summarizer import generate_event_summary
import json

def hook_handler(input_data):
    session_id = input_data.get('session_id')
    log_dir = ensure_session_log_dir(session_id)

    # Summarize event
    event_text = input_data.get('details', '')
    summary = generate_event_summary(event_text)

    # Log with summary
    log_file = log_dir / 'custom_hook.json'
    with open(log_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'summary': summary
        }, f)
```

## Configuration

### Hook Configuration in settings.json

Each hook type is configured with:
- **matcher**: Regex pattern to filter which tools trigger the hook
- **type**: Always "command"
- **command**: Bash command with `|| true` for graceful failure

### Status Line Configuration

```json
{
  "status_lines": [{
    "command": "uv run $CLAUDE_PROJECT_DIR/.claude/status_lines/status_line_main.py"
  }]
}
```

### Environment Variables

- `CLAUDE_HOOKS_LOG_DIR` - Custom directory for hook logs (default: `logs/`)
- `ANTHROPIC_API_KEY` - For summarizer.py LLM calls
- `CLAUDE_AGENT_NAME` - Agent name for status line display
- `CLAUDE_MODEL` - Claude model for status line display

## Testing

### Validate Hook Documentation

```bash
# Check hooks.md for broken references
grep -n "### " tac_bootstrap_cli/docs/hooks.md | head -20
```

### Verify Utilities Cross-References

```bash
# Confirm utilities.md references hooks correctly
grep -n "Additional TAC-12 Hooks" tac_bootstrap_cli/docs/utilities.md
```

### Test Hook Configuration Examples

```bash
# Verify JSON is valid in documentation
cd tac_bootstrap_cli/docs && python3 -c "
import re
import json
with open('hooks.md') as f:
    content = f.read()
    for match in re.finditer(r'\`\`\`json\n(.*?)\n\`\`\`', content, re.DOTALL):
        try:
            json.loads(match.group(1))
            print('✓ Valid JSON found')
        except:
            print('✗ Invalid JSON:', match.group(1)[:50])
"
```

### Manual Verification

```bash
# Check that all 9 hooks are documented
grep "^### " tac_bootstrap_cli/docs/hooks.md | grep -E "send_event|session_start|pre_compact|subagent_stop|user_prompt_submit|pre_tool_use|post_tool_use|notification|stop|dangerous"
```

## Notes

- **Retained Existing Content**: No existing documentation was removed or replaced; all new sections were added
- **Style Consistency**: New hook sections follow the same pattern (Location, Trigger, Features, Configuration, Output Locations)
- **Status Line Priority**: Documented as key observability infrastructure for maintaining editor awareness
- **Cross-References**: Bidirectional links between hooks.md and utilities.md enable seamless navigation
- **Configuration Examples**: Each new hook includes realistic JSON configuration for immediate use
- **Integration Patterns**: Utilities section now clearly shows how constants.py and summarizer.py integrate with hooks

## Related Documentation

- [Hook System Overview](tac_bootstrap_cli/docs/hooks.md) - Complete hook system reference
- [Utilities Reference](tac_bootstrap_cli/docs/utilities.md) - LLM, TTS, and Observability utilities
- [Agents Documentation](tac_bootstrap_cli/docs/agents.md) - Agentic workflow context
- [Expert Hook Development](tac_bootstrap_cli/docs/hooks.md#expert-hook-development) - Advanced hook patterns

## Success Criteria

✓ All 9 TAC-12 hooks documented with location, trigger timing, features, configuration, and outputs
✓ Status Line Integration section added with examples and integration points
✓ Observability utilities (constants, summarizer, model_extractor) documented
✓ Cross-references between hooks.md and utilities.md maintained and validated
✓ Configuration examples are valid JSON and realistic
✓ Documentation maintains consistent formatting and style
✓ No broken internal links or references
