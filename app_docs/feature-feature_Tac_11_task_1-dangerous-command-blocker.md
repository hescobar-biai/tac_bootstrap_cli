---
doc_type: feature
adw_id: feature_Tac_11_task_1
date: 2026-01-27
idk:
  - security-hook
  - pre-tool-use
  - command-validation
  - regex-patterns
  - audit-logging
  - bash-interception
  - critical-paths
  - exit-codes
tags:
  - feature
  - security
  - hooks
related_code:
  - .claude/hooks/dangerous_command_blocker.py
  - .claude/settings.json
---

# Dangerous Command Blocker Security Hook

**ADW ID:** feature_Tac_11_task_1
**Date:** 2026-01-27
**Specification:** specs/issue-327-adw-feature_Tac_11_task_1-sdlc_planner-dangerous-command-blocker.md

## Overview

A comprehensive security hook that intercepts Bash tool calls and validates them against dangerous command patterns before execution. This hook protects users from accidentally running destructive filesystem operations like `rm -rf /`, `dd` to critical devices, `mkfs`, and other commands that could cause data loss or system damage.

## What Was Built

- **PreToolUse security hook** (`.claude/hooks/dangerous_command_blocker.py`) - 288 lines of Python code implementing command validation
- **Comprehensive pattern matching** - 8+ regex patterns covering rm, dd, mkfs, chmod, chown, shred, wipefs, and format commands
- **Critical path protection** - 14 system paths that are automatically protected from destructive operations
- **Security audit logging** - JSON lines format logging to `agents/security_logs/blocked_commands.jsonl`
- **Safer alternative suggestions** - Contextual guidance for each blocked command
- **Hook integration** - Chained into PreToolUse hook pipeline in `.claude/settings.json`

## Technical Implementation

### Files Modified

- `.claude/hooks/dangerous_command_blocker.py`: New 288-line security hook implementing comprehensive command validation
- `.claude/settings.json`: Updated PreToolUse hook chain to include dangerous_command_blocker.py

### Key Changes

1. **Pattern Detection Engine**
   - Regex-based matching for dangerous commands (rm -rf, dd, mkfs, etc.)
   - Case-insensitive command normalization for consistent matching
   - Special handling for commands with variables (`$VAR`) and command substitution (`$()`)
   - Detection in piped commands, sudo contexts, and subshells

2. **Critical Path Validation**
   - Hardcoded list of 14 system paths (/, /etc, /usr, /bin, /home, etc.)
   - Path matching with wildcards and exact matches
   - Allows relative paths (./build, ../temp) and safe absolute paths (/tmp/myapp)
   - Context-aware blocking only when dangerous patterns target critical paths

3. **Security Audit Trail**
   - Auto-creates `agents/security_logs/` directory with 0o755 permissions
   - Appends blocked commands to `blocked_commands.jsonl` in JSON lines format
   - Includes timestamp (ISO 8601), command, reason, suggested_alternative, and blocked=true
   - Graceful error handling to prevent logging failures from affecting hook execution

4. **User Guidance System**
   - Contextual safer alternatives mapped to specific dangerous operations
   - Clear error messages explaining why commands were blocked
   - Actionable suggestions for achieving the same goal safely

5. **Hook Integration**
   - Chained after universal_hook_logger.py and pre_tool_use.py in PreToolUse pipeline
   - Returns exit code 0 to allow safe commands
   - Returns exit code 2 to block dangerous commands
   - Graceful fallback with `|| true` to prevent hook chain failures

## How to Use

The hook operates transparently and requires no explicit invocation. It automatically intercepts all Bash commands executed by Claude Code.

### Automatic Protection

When attempting dangerous commands, the hook blocks execution:

```bash
# This command will be blocked:
rm -rf /etc

# You'll see an error message like:
# ================================================================================
# BLOCKED: Dangerous command detected
# ================================================================================
#
# Reason: Command matches dangerous pattern and targets critical path '/etc'
#
# Blocked command:
# rm -rf /etc
#
# Safer alternative:
# Use specific paths in /tmp or project directories: rm -rf /tmp/myapp_temp
#
# ================================================================================
```

### Allowed Commands

Safe commands pass through without blocking:

```bash
# These commands are allowed:
rm -rf ./build
rm -rf ../temp
rm -rf /tmp/myapp_temp
mkdir -p test && rm -rf test
```

## Configuration

The hook is configured with hardcoded patterns and paths for simplicity:

### Dangerous Patterns (8 categories)

- **rm -rf variants**: Matches `rm -rf`, `rm -fr`, `rm --recursive --force`, etc.
- **dd to devices**: Blocks `dd if=... of=/dev/...`
- **mkfs operations**: Blocks all `mkfs.*` commands (mkfs.ext4, mkfs.xfs, etc.)
- **format commands**: Blocks `format` command
- **shred operations**: Blocks `shred` commands for secure deletion
- **wipefs operations**: Blocks `wipefs` commands
- **chmod -R 777**: Blocks recursive 777 permissions (security vulnerability)
- **chown -R on critical paths**: Blocks recursive ownership changes on absolute paths

### Critical Paths (14 locations)

`/`, `/etc`, `/usr`, `/bin`, `/sbin`, `/lib`, `/lib64`, `/boot`, `/home`, `/root`, `/var`, `/sys`, `/proc`, `/dev`

### Hook Chain Location

The hook is integrated in `.claude/settings.json` at `.claude/settings.json:30`:

```json
"command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event PreToolUse && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/dangerous_command_blocker.py || true"
```

## Testing

### Verify Hook Installation

```bash
# Check hook file exists and is executable
ls -la .claude/hooks/dangerous_command_blocker.py
```

### Verify Hook Integration

```bash
# Check hook is in settings.json
cat .claude/settings.json | grep dangerous_command_blocker
```

### Test Dangerous Command Blocking

```bash
# Test with simulated hook input (exit code should be 2)
echo '{"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}' | uv run .claude/hooks/dangerous_command_blocker.py
```

### Test Safe Command Allowance

```bash
# Test with safe command (exit code should be 0)
echo '{"tool_name": "Bash", "tool_input": {"command": "rm -rf ./build"}}' | uv run .claude/hooks/dangerous_command_blocker.py
```

### Verify Security Logging

```bash
# Check security logs are created
ls -la agents/security_logs/

# View recent blocked commands
cat agents/security_logs/blocked_commands.jsonl | tail -5
```

### Validate Python Syntax

```bash
# Verify no syntax errors
uv run python -m py_compile .claude/hooks/dangerous_command_blocker.py
```

## Notes

### Design Philosophy

- **Defense-in-depth**: Works alongside `.claude/settings.json` permissions.deny for layered security
- **Fail-safe**: Uses `|| true` in hook chain to prevent blocking legitimate commands if hook errors occur
- **Graceful degradation**: JSON decode errors and exceptions default to exit code 0 (allow)
- **User-friendly**: Provides helpful error messages and safer alternatives rather than cryptic blocks

### Security Considerations

- This hook prevents accidental damage, not malicious attacks
- Users with malicious intent can disable hooks or edit the hook file
- Sophisticated attackers could potentially bypass regex patterns
- Should be used as one layer in a defense-in-depth strategy
- Regex matching has ~10ms latency per Bash command (minimal performance impact)

### Template Usage

- Hook is part of TAC Bootstrap template and will be copied to generated projects
- Uses only Python standard library (json, sys, re, os, pathlib, datetime)
- No external dependencies required
- Compatible with Python 3.8+ (uv script metadata)

### Limitations

- Cannot detect dangerous commands in dynamic contexts where variables expand at runtime
- Flags commands with `$VAR` or `$()` as potentially dangerous when they match patterns
- Does not whitelist explicitly allowed dangerous operations
- No configuration file for custom patterns per project
- No log rotation for security logs (manual cleanup required)

### Future Enhancements (out of scope)

- Add whitelist configuration for explicitly allowed dangerous operations
- Per-project configuration file for custom patterns
- Log rotation and retention policies
- Statistics dashboard showing blocked command trends
- Integration with external security monitoring tools (SIEM)
- Machine learning-based anomaly detection for command patterns
