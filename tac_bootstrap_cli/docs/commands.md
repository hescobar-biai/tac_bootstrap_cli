# Slash Commands

Complete reference for all slash commands available in TAC Bootstrap projects.

## Core Development Commands

| Command | Description |
|---------|-------------|
| `/prime` | Load project context and prepare Claude for development |
| `/start` | Start the application |
| `/test` | Run test suite |
| `/test_e2e` | Run end-to-end tests |
| `/lint` | Run code linter |
| `/build` | Build the project |

## Planning Commands

| Command | Description |
|---------|-------------|
| `/feature <description>` | Plan a new feature implementation |
| `/bug <description>` | Plan a bug fix |
| `/chore <description>` | Plan a maintenance task |
| `/patch <description>` | Plan a quick patch |
| `/quick-plan <description>` | Rapid implementation planning with architect pattern |

### `/quick-plan`

Creates a concise engineering implementation plan and saves it to the `specs/` directory.

```
/quick-plan Add user authentication with JWT tokens
```

**Output:** `specs/plan-{timestamp}.md` with:
- Requirements analysis
- Implementation steps
- File changes needed
- Testing strategy

## Implementation Commands

| Command | Description |
|---------|-------------|
| `/implement <plan>` | Implement from a plan file |
| `/build_w_report <plan>` | Implement with detailed YAML change report |
| `/commit` | Create git commit with conventional format |
| `/pull_request` | Create GitHub pull request |

### `/build_w_report`

Implements a plan and generates a structured YAML report of all changes.

```
/build_w_report specs/feature-auth-plan.md
```

**Output format:**
```yaml
work_changes:
  - file: src/auth/service.py
    lines_changed: 45
    description: Added JWT token generation
  - file: src/auth/routes.py
    lines_changed: 30
    description: Added login/logout endpoints
```

## Review & Quality Commands

| Command | Description |
|---------|-------------|
| `/review <plan>` | Review implementation against specification |
| `/in_loop_review` | Quick review during development |
| `/health_check` | Validate project health and dependencies |
| `/github_check` | Check GitHub CI/CD status |

## Documentation Commands

| Command | Description |
|---------|-------------|
| `/document` | Generate feature documentation |
| `/generate_fractal_docs` | Generate fractal documentation tree |
| `/load_ai_docs <topic>` | Load AI documentation via sub-agents |
| `/conditional_docs` | Update conditional documentation |

### `/load_ai_docs`

Fetches and integrates external documentation into project context.

```
/load_ai_docs FastAPI authentication
/load_ai_docs React hooks best practices
```

Uses the `docs-scraper` and `research-docs-fetcher` agents to:
1. Search for official documentation
2. Fetch and process content
3. Save to `ai_docs/` directory

## Context Management Commands

| Command | Description |
|---------|-------------|
| `/prime_cc` | Claude Code-specific context priming |
| `/load_bundle [bundle]` | Load context from saved bundle |
| `/tools` | List available built-in tools |

### `/prime_cc`

Specialized context priming for Claude Code development:
- Loads Claude Code documentation
- Primes for hook development
- Loads settings patterns

```
/prime_cc
```

### `/load_bundle`

Recovers context from previously saved session bundles.

```
/load_bundle                           # Load latest bundle
/load_bundle agents/context_bundles/session-123.jsonl
```

**Use cases:**
- Resume interrupted sessions
- Share context between sessions
- Recover from context compaction

## Agent Delegation Commands

| Command | Description |
|---------|-------------|
| `/background <task>` | Delegate task to background agent |
| `/parallel_subagents <task> [count]` | Launch multiple agents in parallel |

### `/background`

Delegates tasks to out-of-loop background agents for autonomous execution.

```
/background Run all tests and fix any failures
/background Refactor the authentication module
```

**Features:**
- Non-blocking execution
- Progress tracking
- Result aggregation

### `/parallel_subagents`

Launches multiple specialized agents in parallel for complex tasks.

```
/parallel_subagents "Analyze codebase security" 3
/parallel_subagents "Research best practices for caching"
```

**Workflow:**
1. Parse input and determine agent count
2. Design specialized prompts for each agent
3. Launch agents in parallel
4. Collect and summarize results

## Meta & Generation Commands

| Command | Description |
|---------|-------------|
| `/t_metaprompt_workflow <description>` | Generate new slash command prompts |
| `/generate_branch_name` | Generate descriptive git branch name |

### `/t_metaprompt_workflow`

Meta-prompt (Level 6) that generates new slash commands following TAC format.

```
/t_metaprompt_workflow Create a command for database migrations
```

**Generates:**
- Frontmatter with metadata
- Variables section
- Workflow steps
- Report format

## Expert Commands

Expert commands implement the Plan-Build-Improve cycle for specialized domains.

### Claude Code Hook Expert

| Command | Description |
|---------|-------------|
| `/experts:cc_hook_expert:cc_hook_expert_plan <requirements>` | Plan hook implementation |
| `/experts:cc_hook_expert:cc_hook_expert_build [plan]` | Build hook from plan |
| `/experts:cc_hook_expert:cc_hook_expert_improve` | Self-improvement from recent changes |

**Workflow:**
```
1. /experts:cc_hook_expert:cc_hook_expert_plan "PreToolUse hook for security validation"
2. /experts:cc_hook_expert:cc_hook_expert_build specs/hook-security-plan.md
3. /experts:cc_hook_expert:cc_hook_expert_improve
```

## Workflow Commands

| Command | Description |
|---------|-------------|
| `/classify_adw` | Classify issue for ADW workflow |
| `/classify_issue` | Classify GitHub issue type |
| `/install` | Install project dependencies |
| `/install_worktree` | Set up isolated worktree |
| `/cleanup_worktrees` | Clean up ADW worktrees |
| `/prepare_app` | Prepare application for deployment |

## Test Commands

| Command | Description |
|---------|-------------|
| `/resolve_failed_test` | Analyze and fix failing tests |
| `/resolve_failed_e2e_test` | Analyze and fix failing E2E tests |
| `/track_agentic_kpis` | Track agentic development KPIs |

## Command Anatomy

All commands follow a consistent structure:

```markdown
---
description: Brief description for delegation
allowed-tools: Tool1, Tool2, Tool3
argument-hint: <required-arg> [optional-arg]
model: sonnet | opus | haiku
---

# Purpose
What this command accomplishes.

## Variables
VARIABLE_NAME: $ARGUMENTS or $1, $2, etc.

## Instructions
Step-by-step workflow.

## Report
Expected output format.
```

## Creating Custom Commands

Add new commands to `.claude/commands/`:

```bash
.claude/commands/
├── my-command.md      # /my-command
└── category/
    └── sub-command.md # /category:sub-command
```

See [Meta-Prompt Workflow](#t_metaprompt_workflow) for automated command generation.
