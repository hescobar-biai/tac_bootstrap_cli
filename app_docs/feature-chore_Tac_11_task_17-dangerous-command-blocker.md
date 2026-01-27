---
doc_type: feature
adw_id: chore_Tac_11_task_17
date: 2026-01-27
idk:
  - security-hooks
  - pre-tool-use
  - command-validation
  - dangerous-patterns
  - exit-code-blocking
  - audit-trail
  - jsonl-logging
tags:
  - feature
  - security
  - hooks
related_code:
  - .claude/hooks/dangerous_command_blocker.py
  - tac_bootstrap_cli/docs/hooks.md
---

# Dangerous Command Blocker Security Hook

**ADW ID:** chore_Tac_11_task_17
**Date:** 2026-01-27
**Specification:** specs/issue-357-adw-chore_Tac_11_task_17-document-dangerous-command-blocker.md

## Overview

The Dangerous Command Blocker is a security hook that intercepts and validates bash commands before execution, protecting users from accidentally running destructive operations like `rm -rf /`, `dd` to critical devices, `mkfs`, `chmod -R 777`, and other commands that could cause data loss, system damage, or security vulnerabilities. It provides real-time validation with informative error messages, safer alternatives, and maintains a comprehensive security audit trail.

## What Was Built

- **Security Hook Documentation**: Comprehensive documentation added to `tac_bootstrap_cli/docs/hooks.md` covering the dangerous command blocker hook
- **Security Hooks Section**: New section in hooks documentation explaining security validation and pre-execution blocking
- **Command Pattern Documentation**: Detailed tables listing all blocked operation categories (recursive rm, device writes, filesystem creation, insecure permissions, ownership changes, data destruction tools)
- **Configuration Examples**: Multiple examples showing how to integrate the hook into `.claude/settings.json` with proper hook chaining
- **Security Logs Documentation**: Complete documentation of the JSONL audit trail format and location
- **Safer Alternatives Guide**: Practical examples of safer command alternatives for each blocked operation category
- **Cross-References**: Links to related hook system documentation sections
- **Customization Guide**: Instructions for disabling or customizing the hook for legitimate use cases

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/docs/hooks.md`: Added comprehensive Security Hooks section (140 new lines) covering:
  - Hook purpose and features
  - Blocked operations table with risk levels
  - Protected critical paths list
  - Safer alternatives with examples
  - Configuration examples for single and multiple hooks
  - Security logs format and location
  - Customization options with warnings
  - Cross-references to related sections

### Key Changes

- **New Security Hooks Section**: Added after Core Hooks section (line 94+) with complete documentation of the dangerous command blocker hook
- **Blocked Operations Table**: Created structured table showing 6 categories of dangerous patterns with examples and risk descriptions
- **Critical Paths Protection**: Documented 14 system paths that receive extra protection (/, /etc, /usr, /bin, etc.)
- **Configuration Examples**: Provided both standalone and chained hook configurations with proper JSON syntax
- **Security Audit Trail**: Documented JSONL logging format with complete example log entry including timestamp, command, reason, alternative, and blocked flag
- **File Structure Update**: Added `security_logs/` directory to the project structure diagram
- **Cross-References**: Linked to Pre-Tool Use Hook, Exit Code Strategy, and Hook Configuration sections

## How to Use

### Reading the Documentation

1. Open the hooks documentation:
   ```bash
   cat tac_bootstrap_cli/docs/hooks.md
   ```

2. Navigate to the Security Hooks section (starts around line 94):
   ```bash
   cat tac_bootstrap_cli/docs/hooks.md | grep -A 150 "## Security Hooks"
   ```

3. Review blocked operations and safer alternatives:
   ```bash
   cat tac_bootstrap_cli/docs/hooks.md | grep -A 30 "Blocked Operations:"
   ```

### Understanding Protection Levels

The documentation organizes dangerous commands into 6 categories:
- **Recursive rm**: Commands that could delete entire filesystems
- **Device writes**: Direct writes to disk devices that could wipe data
- **Filesystem creation**: Commands that destroy existing filesystem data
- **Insecure permissions**: Operations that create security vulnerabilities
- **Ownership changes**: Commands that could break system access
- **Data destruction**: Tools designed for permanent data erasure

### Viewing Security Logs

When commands are blocked, check the audit trail:
```bash
cat agents/security_logs/blocked_commands.jsonl
```

Parse the JSONL format to find specific blocked commands:
```bash
cat agents/security_logs/blocked_commands.jsonl | jq 'select(.command | contains("rm"))'
```

## Configuration

The hook is already configured in `.claude/settings.json` but the documentation provides examples for:

**Single Hook Configuration:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/dangerous_command_blocker.py || true"
          }
        ]
      }
    ]
  }
}
```

**Chained Hook Configuration:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event PreToolUse && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/dangerous_command_blocker.py && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py || true"
          }
        ]
      }
    ]
  }
}
```

## Testing

Verify the documentation was added correctly:

```bash
cat tac_bootstrap_cli/docs/hooks.md | grep -A 20 "Security Hooks"
```

Check that all sections are present:

```bash
grep -E "^(###|##) " tac_bootstrap_cli/docs/hooks.md | grep -A 10 "Security Hooks"
```

Validate the file structure diagram was updated:

```bash
cat tac_bootstrap_cli/docs/hooks.md | grep -A 3 "security_logs"
```

Ensure cross-references are correct:

```bash
cat tac_bootstrap_cli/docs/hooks.md | grep "See Also" -A 5
```

## Notes

- The dangerous command blocker hook itself (`.claude/hooks/dangerous_command_blocker.py`) was already fully implemented - this task focused on documenting it comprehensively
- The documentation follows the existing hooks.md format with clear headers, code blocks, and tables
- Security logs are automatically created in `agents/security_logs/` when commands are blocked (directory is created automatically)
- The hook uses exit code 2 for blocking, which is documented in the Exit Code Strategy table
- Documentation includes practical examples and real-world use cases rather than just technical specifications
- Cross-references help users understand how this hook fits into the larger hook system architecture
- The documentation emphasizes safety while also providing customization options for advanced users who understand the risks
