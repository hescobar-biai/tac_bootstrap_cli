# Feature: Dangerous Command Blocker Security Hook

## Metadata
issue_number: `327`
adw_id: `feature_Tac_11_task_1`
issue_json: `{"number":327,"title":"Create dangerous_command_blocker.py security hook in base repository","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_11_task_1\n\nreate a new security hook that blocks dangerous shell commands like `rm -rf /` and other destructive patterns. The hook intercepts Bash tool calls and validates commands against dangerous patterns before execution.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/dangerous_command_blocker.py`\n\n**Implementation details:**\n- Define DANGEROUS_PATTERNS regex list for rm -rf variants\n- Define CRITICAL_PATHS list (/, /etc, /usr, /bin, /home, etc.)\n- Implement `is_dangerous_command()` function returning (bool, reason)\n- Implement `suggest_safer_alternative()` for user guidance\n- Implement `log_blocked_command()` for security audit to `agents/security_logs/`\n- Read hook input from stdin as JSON\n- Only process Bash tool calls\n- Exit with code 2 to block dangerous commands\n- Exit with code 0 to allow safe commands"}`

## Feature Description

Create a comprehensive security hook that intercepts Bash tool calls and validates them against dangerous command patterns before execution. This hook will protect users from accidentally running destructive filesystem operations like `rm -rf /`, `dd` to critical devices, `mkfs`, and other commands that could cause data loss or system damage.

The hook will operate in pre-execution blocking mode, analyzing the full command string (including piped commands, sudo, and subshells) and blocking dangerous operations with informative error messages that include safer alternatives. All blocked commands will be logged to a security audit trail in JSON lines format.

## User Story

As a developer using TAC Bootstrap CLI with AI assistance
I want dangerous shell commands to be automatically blocked before execution
So that I can prevent accidental data loss or system damage from destructive operations

## Problem Statement

AI agents can inadvertently generate or execute dangerous shell commands that could cause:
- Irreversible data loss (rm -rf on critical paths)
- System instability (mkfs on wrong devices, dd to critical devices)
- Security vulnerabilities (chmod -R 777 on system directories)

While `.claude/settings.json` has basic deny patterns for `rm -rf`, it lacks:
- Comprehensive pattern coverage for all destructive operations
- Helpful error messages with safer alternatives
- Security audit logging for compliance and debugging
- Detection of dangerous patterns in piped/sudo/subshell contexts
- Validation of commands with environment variables or command substitution

## Solution Statement

Implement a dedicated `dangerous_command_blocker.py` hook that:
1. Reads PreToolUse hook input from stdin as JSON
2. Filters for Bash tool calls only
3. Validates commands against hardcoded DANGEROUS_PATTERNS (regex list) and CRITICAL_PATHS
4. Blocks dangerous commands with exit code 2 and writes informative messages to stderr
5. Logs all blocked attempts to `agents/security_logs/` in JSON lines format
6. Suggests safer alternatives for common dangerous operations
7. Handles edge cases like piped commands, sudo, subshells, and dynamic content ($VAR, $())

This approach provides defense-in-depth beyond permissions.deny, with better user guidance and auditability.

## Relevant Files

Existing files to reference for patterns:

- `.claude/hooks/pre_tool_use.py` - Current PreToolUse hook that already blocks some rm commands and .env access. Shows hook input/output patterns, exit codes, and JSON structure.
- `.claude/settings.json` - Hook configuration showing PreToolUse matcher and command structure
- `.claude/hooks/utils/constants.py` - Utility functions for directory creation and path handling

### New Files

- `.claude/hooks/dangerous_command_blocker.py` - New security hook implementing comprehensive command validation
- `agents/security_logs/` - Directory for security audit logs (auto-created with 0o755 permissions)

## Implementation Plan

### Phase 1: Foundation
1. Study existing `pre_tool_use.py` hook to understand:
   - JSON input schema from stdin
   - Exit code conventions (0=allow, 2=block)
   - Error message format to stderr
   - Tool name filtering for Bash

2. Define comprehensive security rules:
   - DANGEROUS_PATTERNS regex list (rm -rf variants, dd, mkfs, format, shred, wipefs, chmod/chown on critical paths)
   - CRITICAL_PATHS list (/, /etc, /usr, /bin, /sbin, /lib, /lib64, /boot, /home, /root, /var, /sys, /proc, /dev)
   - SAFER_ALTERNATIVES mapping for common dangerous operations

### Phase 2: Core Implementation
1. Implement `is_dangerous_command(command: str) -> tuple[bool, str]`:
   - Return (True, reason) if dangerous pattern detected
   - Return (False, "") if safe
   - Check full command string for patterns (handles piped/sudo/subshell)
   - Flag commands with $VAR or $() if they match dangerous patterns

2. Implement `suggest_safer_alternative(command: str, reason: str) -> str`:
   - Return specific alternative for known dangerous operations
   - Return generic safety guidance if no specific alternative

3. Implement `log_blocked_command(command: str, reason: str, alternative: str)`:
   - Create `agents/security_logs/` if missing (0o755)
   - Append JSON line with: timestamp, command, reason, suggested_alternative, blocked=true
   - Handle file I/O errors gracefully

4. Implement main hook logic:
   - Read JSON from stdin
   - Filter for tool_name == 'Bash'
   - Extract command from tool_input
   - Call is_dangerous_command()
   - If dangerous: log, write error to stderr with alternative, exit 2
   - If safe: exit 0

### Phase 3: Integration
1. Update `.claude/settings.json` to call dangerous_command_blocker.py in PreToolUse hook:
   - Add to existing PreToolUse command chain (after pre_tool_use.py)
   - Use `|| true` to handle errors gracefully

2. Test hook with various dangerous and safe commands

3. Verify security logs are created and populated correctly

## Step by Step Tasks

### Task 1: Study existing hook patterns
- Read `.claude/hooks/pre_tool_use.py` to understand JSON input schema
- Read `.claude/hooks/utils/constants.py` for utility functions
- Read `.claude/settings.json` to understand hook integration
- Document JSON input structure and expected output

### Task 2: Create dangerous_command_blocker.py skeleton
- Create `.claude/hooks/dangerous_command_blocker.py` with shebang and script metadata
- Define DANGEROUS_PATTERNS list with comprehensive regex patterns:
  - `r'\brm\s+.*-[rf].*[rf]'` - rm -rf variants
  - `r'\bdd\s+if=.*of=/dev/'` - dd to devices
  - `r'\bmkfs\.'` - mkfs operations
  - `r'\bformat\s+'` - format operations
  - `r'\bshred\s+'` - shred operations
  - `r'\bwipefs\s+'` - wipefs operations
  - `r'\bchmod\s+.*-R.*777'` - recursive 777
  - `r'\bchown\s+.*-R.*/(?:etc|usr|bin|home|root)'` - recursive chown on critical paths
- Define CRITICAL_PATHS list: ['/', '/etc', '/usr', '/bin', '/sbin', '/lib', '/lib64', '/boot', '/home', '/root', '/var', '/sys', '/proc', '/dev']
- Define SAFER_ALTERNATIVES dict with helpful messages

### Task 3: Implement is_dangerous_command() function
- Accept command string parameter
- Return tuple[bool, str] (is_dangerous, reason)
- Iterate through DANGEROUS_PATTERNS and check for matches
- Check for CRITICAL_PATHS in command when dangerous patterns found
- Allow relative paths (./build, ../temp) and non-critical absolute paths
- Flag commands with $VAR or $() if they contain dangerous patterns
- Return detailed reason string explaining why command is dangerous

### Task 4: Implement suggest_safer_alternative() function
- Accept command string and reason as parameters
- Return helpful alternative suggestion string
- Match against common patterns (rm -rf, dd, mkfs, etc.)
- Return specific alternatives for known operations
- Return generic safety message if no specific alternative exists
- Keep suggestions concise and actionable

### Task 5: Implement log_blocked_command() function
- Accept command, reason, and alternative as parameters
- Create `agents/security_logs/` directory if it doesn't exist (mode 0o755)
- Append JSON line to `agents/security_logs/blocked_commands.jsonl`
- Include fields: timestamp (ISO 8601), command, reason, suggested_alternative, blocked=true
- Handle file I/O errors gracefully (log to stderr but don't fail)

### Task 6: Implement main() hook logic
- Read JSON input from stdin using json.load(sys.stdin)
- Extract tool_name and tool_input from input_data
- Return early with exit(0) if tool_name != 'Bash'
- Extract command from tool_input.get('command', '')
- Call is_dangerous_command(command)
- If dangerous:
  - Generate safer alternative with suggest_safer_alternative()
  - Log with log_blocked_command()
  - Write error message to stderr with reason and alternative
  - Exit with code 2 to block
- If safe: exit with code 0 to allow
- Wrap in try/except to handle JSON errors gracefully

### Task 7: Integrate hook into settings.json
- Read current `.claude/settings.json`
- Update PreToolUse hook command to chain dangerous_command_blocker.py
- Add after universal_hook_logger.py and pre_tool_use.py
- Use format: `uv run $CLAUDE_PROJECT_DIR/.claude/hooks/dangerous_command_blocker.py || true`
- Ensure proper && chaining so all hooks run in sequence

### Task 8: Test hook with various commands
- Test dangerous commands that should be blocked:
  - `rm -rf /`
  - `rm -rf /etc`
  - `dd if=/dev/zero of=/dev/sda`
  - `mkfs.ext4 /dev/sda1`
  - `chmod -R 777 /etc`
- Test safe commands that should be allowed:
  - `rm -rf ./build`
  - `rm -rf ../temp`
  - `mkdir -p test && rm -rf test`
- Verify error messages include reason and safer alternative
- Verify blocked commands are logged to `agents/security_logs/blocked_commands.jsonl`

### Task 9: Final validation and documentation
- Run validation commands to ensure no regressions
- Verify hook is properly integrated in settings.json
- Confirm security logs directory is auto-created
- Verify JSON lines format is valid and parseable
- Update CLAUDE.md if needed to document new hook

## Testing Strategy

### Unit Tests
Since this is a hook script (not part of tac_bootstrap_cli package), testing will be manual and integration-based rather than pytest unit tests.

### Manual Testing
1. **Dangerous command blocking:**
   - Verify `rm -rf /` is blocked with helpful message
   - Verify `dd if=/dev/zero of=/dev/sda` is blocked
   - Verify `mkfs.ext4 /dev/sda` is blocked
   - Verify `chmod -R 777 /etc` is blocked

2. **Safe command allowance:**
   - Verify `rm -rf ./build` is allowed
   - Verify `rm -rf /tmp/myapp_temp` is allowed
   - Verify `mkdir test && rm -rf test` is allowed

3. **Edge cases:**
   - Piped commands: `cat file | rm -rf /`
   - Sudo commands: `sudo rm -rf /etc`
   - Subshells: `$(rm -rf /)`
   - Environment variables: `rm -rf $DANGEROUS_PATH`

4. **Security logging:**
   - Verify `agents/security_logs/` is created automatically
   - Verify blocked commands are logged in JSON lines format
   - Verify log entries include timestamp, command, reason, alternative

### Integration Testing
1. Trigger PreToolUse hook by attempting Bash command in Claude Code session
2. Verify hook chain executes in correct order
3. Verify exit code 2 blocks command execution
4. Verify error message appears in Claude Code interface

## Acceptance Criteria

1. **Hook Implementation:**
   - [ ] `.claude/hooks/dangerous_command_blocker.py` exists with proper shebang and script metadata
   - [ ] DANGEROUS_PATTERNS list includes at least 8 comprehensive regex patterns
   - [ ] CRITICAL_PATHS list includes at least 10 system directories
   - [ ] is_dangerous_command() returns (bool, str) tuple correctly
   - [ ] suggest_safer_alternative() provides helpful guidance for all dangerous patterns
   - [ ] log_blocked_command() writes JSON lines to agents/security_logs/

2. **Hook Integration:**
   - [ ] PreToolUse hook in settings.json calls dangerous_command_blocker.py
   - [ ] Hook chain uses proper && and || true syntax
   - [ ] Hook only processes Bash tool calls

3. **Security Validation:**
   - [ ] Blocks rm -rf on critical paths (/, /etc, /usr, etc.)
   - [ ] Blocks dd to critical devices (/dev/sda, etc.)
   - [ ] Blocks mkfs, format, shred, wipefs operations
   - [ ] Blocks chmod -R 777 and chown -R on critical paths
   - [ ] Allows relative paths (./build, ../temp)
   - [ ] Allows non-critical absolute paths (/tmp/myapp)

4. **User Experience:**
   - [ ] Error messages are clear and include reason for blocking
   - [ ] Error messages include safer alternative suggestions
   - [ ] Exit code 2 properly blocks command execution
   - [ ] Exit code 0 allows safe commands through

5. **Audit Trail:**
   - [ ] agents/security_logs/ directory is auto-created with 0o755
   - [ ] Blocked commands logged in JSON lines format
   - [ ] Log entries include: timestamp, command, reason, suggested_alternative, blocked=true
   - [ ] Logs are append-only (don't overwrite previous entries)

6. **Edge Case Handling:**
   - [ ] Detects dangerous patterns in piped commands
   - [ ] Detects dangerous patterns with sudo prefix
   - [ ] Flags commands with $VAR or $() when they match dangerous patterns
   - [ ] Handles JSON decode errors gracefully (exit 0)

## Validation Commands

Since this is a hook rather than CLI code, validation focuses on integration:

```bash
# Verify hook file exists and is executable
ls -la .claude/hooks/dangerous_command_blocker.py

# Verify hook is integrated in settings.json
cat .claude/settings.json | grep dangerous_command_blocker

# Verify Python syntax is valid
uv run python -m py_compile .claude/hooks/dangerous_command_blocker.py

# Test hook manually with sample input (simulate PreToolUse event)
echo '{"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}' | uv run .claude/hooks/dangerous_command_blocker.py
# Expected: Exit code 2, error message to stderr

echo '{"tool_name": "Bash", "tool_input": {"command": "rm -rf ./build"}}' | uv run .claude/hooks/dangerous_command_blocker.py
# Expected: Exit code 0, no error

# Verify security logs are created
ls -la agents/security_logs/
cat agents/security_logs/blocked_commands.jsonl | head -5

# Standard project validation (should have no impact since this is a hook)
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

1. **Hook vs Permission System:**
   - This hook provides defense-in-depth beyond `.claude/settings.json` permissions.deny
   - Permissions deny patterns are simple string matches; this hook uses comprehensive regex
   - Hook can provide helpful error messages and logging that permissions cannot

2. **Template Usage:**
   - This hook is part of the TAC Bootstrap template and will be copied to generated projects
   - Keep implementation simple and self-contained (no external dependencies beyond stdlib)
   - Hardcode patterns rather than using config files for simplicity

3. **Future Enhancements (out of scope):**
   - Add whitelist for explicitly allowed dangerous operations
   - Configuration file for custom patterns per project
   - Log rotation for security logs
   - Statistics dashboard for blocked commands
   - Integration with external security monitoring tools

4. **Security Considerations:**
   - This hook is not foolproof - sophisticated attackers could potentially bypass it
   - It's designed to prevent accidental damage, not malicious actors
   - Should be used as one layer in a defense-in-depth strategy
   - Users with malicious intent can disable hooks or edit the hook file

5. **Performance:**
   - Hook adds minimal latency (< 10ms) per Bash command
   - Regex matching on command strings is fast
   - Logging is append-only (no file parsing required)

6. **Dependencies:**
   - Uses only Python standard library (json, sys, re, os, pathlib, datetime)
   - No external packages required
   - Compatible with Python 3.8+ (uv script metadata requires-python)
