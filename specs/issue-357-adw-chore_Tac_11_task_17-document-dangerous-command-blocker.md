# Chore: Document dangerous_command_blocker Security Hook

## Metadata
issue_number: `357`
adw_id: `chore_Tac_11_task_17`
issue_json: `{"number":357,"title":"Update documentation in tac_bootstrap_cli/docs/hooks.md","body":"chore\n/adw_sdlc_iso\n/adw_id: chore_Tac_11_task_17\n\n\nDocument the new dangerous_command_blocker hook.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/docs/hooks.md`\n\n**Implementation details:**\n- Add section for Security Hooks\n- Document dangerous_command_blocker.py functionality\n- Include blocked patterns and safer alternatives\n- Document security_logs directory"}`

## Chore Description
Add comprehensive documentation for the `dangerous_command_blocker.py` security hook to the `tac_bootstrap_cli/docs/hooks.md` file. This hook provides critical protection against accidentally running destructive commands like `rm -rf /`, `dd` to devices, `mkfs`, `chmod 777`, and other operations that could cause data loss or security vulnerabilities.

The documentation needs to:
1. Add a new "Security Hooks" section after "Core Hooks" and before "Hook Configuration"
2. Explain how the hook works (PreToolUse trigger, exit code 2 blocking)
3. List main categories of blocked command patterns with examples
4. Provide 2-3 practical safer alternatives
5. Show configuration example for settings.json
6. Document security_logs location and format
7. Include cross-references to related sections
8. Brief note on customization/disabling for legitimate use cases

## Relevant Files
Files needed to complete this chore:

- `tac_bootstrap_cli/docs/hooks.md` - Main documentation file to be updated (add Security Hooks section after line 27)
- `.claude/hooks/dangerous_command_blocker.py` - Reference implementation to understand blocked patterns and alternatives

## Step by Step Tasks
IMPORTANT: Execute each step in order.

### Task 1: Add Security Hooks Section
- Insert new "## Security Hooks" section header after line 27 (after Core Hooks)
- Add introductory paragraph explaining security hooks protect against destructive operations

### Task 2: Document dangerous_command_blocker Hook
- Add "### Dangerous Command Blocker" subsection
- Add brief description of the hook's purpose and how it works (PreToolUse trigger, exit code 2 blocking)
- Document location: `.claude/hooks/dangerous_command_blocker.py`

### Task 3: List Blocked Command Categories
- Add "**Blocked Operations:**" section
- List main categories with 3-4 examples each:
  - `rm -rf` variants (rm -rf /, rm -rf /etc, rm -rf with variables)
  - `dd` to devices (dd of=/dev/sda, dd of=/dev/nvme0n1)
  - `mkfs` commands (mkfs.ext4, mkfs.xfs)
  - `chmod 777` recursive (chmod -R 777 /, chmod -R 777 /var)
  - `chown` on critical paths (chown -R user:group /)
  - Data destruction tools (shred, wipefs, format)

### Task 4: Document Safer Alternatives
- Add "**Safer Alternatives:**" section
- Include 2-3 practical examples:
  - `rm -rf ./specific_folder` instead of `rm -rf /`
  - `chmod 755` or `chmod 644` instead of `chmod 777`
  - Using specific paths in project directories or /tmp

### Task 5: Add Configuration Example
- Add "**Configuration:**" section
- Show settings.json example with dangerous_command_blocker in PreToolUse hook chain
- Follow existing documentation format

### Task 6: Document Security Logs
- Add "**Security Logs:**" section
- Document location: `agents/security_logs/blocked_commands.jsonl`
- Mention JSONL format for easy parsing
- Brief note on log entry contents (timestamp, command, reason, alternative)

### Task 7: Add Cross-References
- Add "**See Also:**" section
- Cross-reference to Pre-Tool Use Hook section (line 94)
- Cross-reference to Exit Code Strategy table (line 324)

### Task 8: Document Customization Options
- Add "**Customization:**" section
- Brief note on removing from settings.json for temporary disable
- Mention modifying DANGEROUS_PATTERNS in Python file for customization
- Warning about ensuring safety before modifications

### Task 9: Validation
- Run validation commands (final step)
- Verify documentation renders correctly
- Ensure all cross-references are accurate

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `cat tac_bootstrap_cli/docs/hooks.md | grep -A 20 "Security Hooks"` - Verify new section exists

## Notes
- The dangerous_command_blocker.py hook is already fully implemented at `.claude/hooks/dangerous_command_blocker.py`
- Documentation style should match existing hooks.md format (clear headers, code blocks, tables where appropriate)
- Keep it concise but practical - users need to understand what's blocked and why
- Cross-references help users understand how this hook fits into the larger hook system
- Security logs are automatically created in agents/security_logs/ when commands are blocked
- The hook uses exit code 2 for blocking, which is documented in the Exit Code Strategy table
