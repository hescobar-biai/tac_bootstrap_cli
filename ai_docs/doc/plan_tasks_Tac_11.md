# TAC-11 Integration Task Plan

## Overview

Integration of TAC-11 (Custom Agents & Claude Code SDK) features into tac_bootstrap. This plan covers security hooks, new slash commands, and enhanced hook configuration.

**Version Target:** 0.6.0

---

## Task 1

**[FEATURE] Create dangerous_command_blocker.py security hook in base repository**

Create a new security hook that blocks dangerous shell commands like `rm -rf /` and other destructive patterns. The hook intercepts Bash tool calls and validates commands against dangerous patterns before execution.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/dangerous_command_blocker.py`

**Implementation details:**
- Define DANGEROUS_PATTERNS regex list for rm -rf variants
- Define CRITICAL_PATHS list (/, /etc, /usr, /bin, /home, etc.)
- Implement `is_dangerous_command()` function returning (bool, reason)
- Implement `suggest_safer_alternative()` for user guidance
- Implement `log_blocked_command()` for security audit to `agents/security_logs/`
- Read hook input from stdin as JSON
- Only process Bash tool calls
- Exit with code 2 to block dangerous commands
- Exit with code 0 to allow safe commands

---

## Task 2

**[FEATURE] Create dangerous_command_blocker.py.j2 template**

Create the Jinja2 template version of the dangerous command blocker hook for generated projects.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/dangerous_command_blocker.py.j2`

**Implementation details:**
- Mirror the implementation from Task 1
- Use `{{ config.project.package_manager.value }}` where applicable
- Ensure template renders correctly for uv, pip, and other package managers

---

## Task 3

**[FEATURE] Create /scout slash command in base repository**

Create a new slash command that performs parallel multi-model codebase search using external AI tools (gemini, opencode, codex, claude).

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/scout.md`

**Implementation details:**
- Purpose: Search codebase for files needed to complete a task
- Variables: USER_PROMPT ($1), SCALE ($2, defaults to 4)
- Output directory: `agents/scout_files/`
- Workflow:
  - Launch SCALE number of Task agents in parallel
  - Each agent calls Bash to run: gemini, opencode, codex, claude CLI tools
  - Collect outputs as structured file lists with offset/limit
  - Run `git diff --stat` to verify no changes, reset if needed
  - Write results to `agents/scout_files/relevant_files_<unique-id>.md`
- Use model: claude-sonnet-4-5-20250929

---

## Task 4

**[FEATURE] Create scout.md.j2 template**

Create the Jinja2 template version of the /scout command for generated projects.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout.md.j2`

**Implementation details:**
- Mirror the implementation from Task 3
- Add template variables for customization if needed

---

## Task 5

**[FEATURE] Create /question slash command in base repository**

Create a read-only Q&A command for answering questions about project structure without making code changes.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/question.md`

**Implementation details:**
- Allowed tools: Bash(git ls-files:*), Read only
- Purpose: Answer questions about project structure and documentation
- Variables: QUESTION ($ARGUMENTS)
- Workflow:
  - Use `git ls-files` to understand project structure
  - Read README.md for project overview
- Response format:
  - Direct answer to question
  - Supporting evidence from project structure
  - References to relevant documentation
  - Conceptual explanations where applicable
- IMPORTANT: No code changes allowed

---

## Task 6

**[FEATURE] Create question.md.j2 template**

Create the Jinja2 template version of the /question command for generated projects.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/question.md.j2`

**Implementation details:**
- Mirror the implementation from Task 5
- Use read-only tool restrictions

---

## Task 7

**[CHORE] Update settings.json to include dangerous_command_blocker hook in base repository**

Add the dangerous_command_blocker hook to PreToolUse for Bash commands with a specific matcher.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/settings.json`

**Implementation details:**
- Add new PreToolUse entry with matcher "Bash"
- Hook command: `uv run $CLAUDE_PROJECT_DIR/.claude/hooks/dangerous_command_blocker.py`
- Set timeout: 5 seconds
- Place before the universal logger hook
- Ensure the hook blocks dangerous commands before they reach other hooks

---

## Task 8

**[CHORE] Update settings.json.j2 template with dangerous_command_blocker hook**

Update the settings.json.j2 template to include the dangerous command blocker for generated projects.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2`

**Implementation details:**
- Add new PreToolUse entry with matcher "Bash"
- Hook command using package manager variable
- Set timeout: 5 seconds
- Maintain existing hook structure

---

## Task 9

**[CHORE] Create security_logs directory structure in base repository**

Create the directory structure for security audit logs from the dangerous_command_blocker hook.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/agents/security_logs/.gitkeep`

**Implementation details:**
- Create `agents/security_logs/` directory
- Add `.gitkeep` file to preserve directory in git
- This directory will store blocked command audit logs

---

## Task 10

**[CHORE] Create security_logs directory template**

Create the template for security_logs directory in generated projects.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/security_logs/.gitkeep.j2`

**Implementation details:**
- Create empty .gitkeep.j2 template
- Ensures security_logs directory is created in generated projects

---

## Task 11

**[CHORE] Create scout_files directory structure in base repository**

Create the directory structure for scout command output files.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/agents/scout_files/.gitkeep`

**Implementation details:**
- Create `agents/scout_files/` directory
- Add `.gitkeep` file to preserve directory in git
- This directory will store relevant file lists from /scout command

---

## Task 12

**[CHORE] Create scout_files directory template**

Create the template for scout_files directory in generated projects.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/scout_files/.gitkeep.j2`

**Implementation details:**
- Create empty .gitkeep.j2 template
- Ensures scout_files directory is created in generated projects

---

## Task 13

**[CHORE] Update scaffold_service.py to render new templates**

Update the scaffold service to include the new templates in the rendering process.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`

**Implementation details:**
- Add `dangerous_command_blocker.py.j2` to hooks rendering
- Add `scout.md.j2` to commands rendering
- Add `question.md.j2` to commands rendering
- Add `security_logs/.gitkeep.j2` to structure rendering
- Add `scout_files/.gitkeep.j2` to structure rendering
- Verify template paths are correct

---

## Task 14

**[CHORE] Update SLASH_COMMAND_MODEL_MAP in agent.py with TAC-11 commands**

Add the new TAC-11 slash commands to the model map in the base repository.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/agent.py`

**Implementation details:**
- Add `/scout`: {"base": "sonnet", "heavy": "sonnet"}
- Add `/question`: {"base": "sonnet", "heavy": "sonnet"}
- Both are lightweight commands that don't need opus

---

## Task 15

**[CHORE] Update SLASH_COMMAND_MODEL_MAP in agent.py.j2 template**

Add the new TAC-11 slash commands to the model map template.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2`

**Implementation details:**
- Mirror changes from Task 14
- Add `/scout` and `/question` to SLASH_COMMAND_MODEL_MAP

---

## Task 16

**[CHORE] Update documentation in tac_bootstrap_cli/docs/commands.md**

Document the new /scout and /question commands.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/docs/commands.md`

**Implementation details:**
- Add /scout command documentation under "Agent Orchestration Commands"
- Add /question command documentation under "Research Commands" or new section
- Include usage examples and options

---

## Task 17

**[CHORE] Update documentation in tac_bootstrap_cli/docs/hooks.md**

Document the new dangerous_command_blocker hook.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/docs/hooks.md`

**Implementation details:**
- Add section for Security Hooks
- Document dangerous_command_blocker.py functionality
- Include blocked patterns and safer alternatives
- Document security_logs directory

---

## Task 18

**[CHORE] Update CHANGELOG.md and increment version to 0.6.0**

Update the changelog with all TAC-11 integration changes and increment version.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md`

**Implementation details:**
- Increment version from 0.5.1 to 0.6.0
- Add section for v0.6.0 with date
- Document new features:
  - Security hook: dangerous_command_blocker.py
  - New command: /scout (multi-model parallel search)
  - New command: /question (read-only Q&A)
  - New directories: agents/security_logs/, agents/scout_files/
- Document template additions
- Reference TAC-11 as source

---

## Execution Checklist

- [ ] Task 1: Create dangerous_command_blocker.py in base
- [ ] Task 2: Create dangerous_command_blocker.py.j2 template
- [ ] Task 3: Create /scout command in base
- [ ] Task 4: Create scout.md.j2 template
- [ ] Task 5: Create /question command in base
- [ ] Task 6: Create question.md.j2 template
- [ ] Task 7: Update settings.json in base
- [ ] Task 8: Update settings.json.j2 template
- [ ] Task 9: Create security_logs directory in base
- [ ] Task 10: Create security_logs template
- [ ] Task 11: Create scout_files directory in base
- [ ] Task 12: Create scout_files template
- [ ] Task 13: Update scaffold_service.py
- [ ] Task 14: Update agent.py in base
- [ ] Task 15: Update agent.py.j2 template
- [ ] Task 16: Update commands.md documentation
- [ ] Task 17: Update hooks.md documentation
- [ ] Task 18: Update CHANGELOG.md to v0.6.0

---

## Parallel Execution Groups

Tasks grouped by dependencies for maximum parallel execution:

### Wave 1 - No Dependencies (Run All in Parallel)

| Task | Description |
|------|-------------|
| 1 | Create dangerous_command_blocker.py in base |
| 3 | Create /scout command in base |
| 5 | Create /question command in base |
| 9 | Create security_logs directory in base |
| 11 | Create scout_files directory in base |
| 14 | Update agent.py in base |

**6 tasks can run simultaneously**

---

### Wave 2 - Depends on Wave 1 (Run All in Parallel)

| Task | Depends On | Description |
|------|------------|-------------|
| 2 | 1 | Create dangerous_command_blocker.py.j2 template |
| 4 | 3 | Create scout.md.j2 template |
| 6 | 5 | Create question.md.j2 template |
| 7 | 1 | Update settings.json in base |
| 10 | 9 | Create security_logs template |
| 12 | 11 | Create scout_files template |
| 15 | 14 | Update agent.py.j2 template |
| 16 | 3, 5 | Update commands.md documentation |
| 17 | 1 | Update hooks.md documentation |

**9 tasks can run simultaneously**

---

### Wave 3 - Depends on Wave 2 (Run All in Parallel)

| Task | Depends On | Description |
|------|------------|-------------|
| 8 | 7 | Update settings.json.j2 template |
| 13 | 2, 4, 6, 10, 12 | Update scaffold_service.py |

**2 tasks can run simultaneously**

---

### Wave 4 - Final (Sequential)

| Task | Depends On | Description |
|------|------------|-------------|
| 18 | All | Update CHANGELOG.md to v0.6.0 |

**Must run last after all tasks complete**

---

## Visual Dependency Graph

```
Wave 1 (Parallel):     [1] [3] [5] [9] [11] [14]
                        │   │   │   │    │    │
                        ▼   ▼   ▼   ▼    ▼    ▼
Wave 2 (Parallel):     [2] [4] [6] [10] [12] [15]
                       [7]     [16]     [17]
                        │       │
                        ▼       │
Wave 3 (Parallel):     [8]    [13] ◄────────────┘
                        │       │
                        ▼       ▼
Wave 4 (Final):            [18]
```

**Total execution time: 4 waves instead of 18 sequential tasks**
