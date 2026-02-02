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

| Command | Description | Tools |
|---------|-------------|-------|
| `/plan <description>` | Basic planning without exploration (legacy variant) | Read, Write, Edit, Glob, Grep, MultiEdit |
| `/feature <description>` | Plan a new feature implementation | (same as feature) |
| `/bug <description>` | Plan a bug fix | (same as bug) |
| `/chore <description>` | Plan a maintenance task | (same as chore) |
| `/patch <description>` | Plan a quick patch | (same as patch) |
| `/plan_w_docs <description>` | Planning with documentation exploration | Task, Read, Glob, Grep, WebFetch |
| `/plan_w_scouters <description>` | Planning with parallel scout-based exploration | Task, Read, Glob, Grep, WebFetch |
| `/quick-plan <description>` | Rapid implementation planning with architect pattern | Task, Read, Write, Edit, Glob, Grep, WebFetch |

### `/plan`

Creates an implementation plan using simple file exploration without parallel scouts.

```
/plan Add validation layer to authentication module
```

**Output:** Structured plan with metadata, requirements analysis, implementation steps, and testing strategy.

### `/plan_w_docs`

Creates a plan by exploring relevant documentation before planning.

```
/plan_w_docs Add WebSocket support to real-time notifications
```

**Approach:**
1. Search local documentation (ai_docs/, app_docs/, specs/)
2. Optionally fetch framework/library documentation
3. Summarize findings
4. Create plan informed by documentation

### `/plan_w_scouters`

Creates a plan using 3 parallel scout agents to comprehensively explore the codebase before planning.

```
/plan_w_scouters 123 "feature_export_config" '{"number":123,"title":"Export configuration","body":"Add command to export project config"}'
```

**Workflow:**
- Base Scout 1: Architectural patterns and domain logic
- Base Scout 2: Infrastructure and integration patterns
- Fast Scout: Surface-level pattern scan

### `/quick-plan`

Creates a concise engineering implementation plan and saves it to the `specs/` directory. Deploys 3 base + 5 fast scout agents in parallel for rapid exploration.

```
/quick-plan Add user authentication with JWT tokens
```

**Output:** `specs/plan-{timestamp}.md` with:
- Requirements analysis
- Implementation steps
- File changes needed
- Testing strategy
- Scout exploration summary

## Implementation Commands

| Command | Description | Tools |
|---------|-------------|-------|
| `/implement <plan>` | Implement from a plan file | (core tools) |
| `/build_in_parallel <plan>` | Parallel file creation delegation to build-agents | Task, Read, Write, Edit, Glob, Grep, MultiEdit |
| `/build_w_report <plan>` | Implement with detailed YAML change report | Read, Write, Edit, Bash |
| `/commit` | Create git commit with conventional format | (git tools) |
| `/pull_request` | Create GitHub pull request | (git tools) |

### `/build_in_parallel`

Implements a plan by delegating individual file creation to specialized build-agents in parallel.

```
/build_in_parallel specs/feature-auth-plan.md
```

**Features:**
- Analyzes plan dependencies
- Launches multiple build-agents in parallel for independent files
- Comprehensive context for each agent
- Batch execution for dependent files
- Final verification step

### `/build_w_report`

Implements a plan and generates a structured YAML report of all changes.

```
/build_w_report specs/feature-auth-plan.md
```

**Output format:**
```yaml
metadata:
  timestamp: "2026-02-02T14:30:22Z"
  branch: "feature/auth"
  plan_file: "specs/feature-auth-plan.md"

work_changes:
  - file: src/auth/service.py
    lines_added: 45
    lines_deleted: 0
    description: Added JWT token generation
  - file: src/auth/routes.py
    lines_added: 30
    lines_deleted: 12
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

| Command | Description | Tools |
|---------|-------------|-------|
| `/document` | Generate feature documentation | (documentation agent) |
| `/find_and_summarize <pattern> [focus]` | Find files matching glob pattern and generate AI summary | Glob, Read |
| `/generate_fractal_docs` | Generate fractal documentation tree | (documentation agent) |
| `/load_ai_docs <topic>` | Load AI documentation via sub-agents | Task, WebFetch |
| `/conditional_docs` | Update conditional documentation | (documentation agent) |

### `/find_and_summarize`

Find files matching a glob pattern and generate an AI-powered summary of their contents.

```
/find_and_summarize "**/*.py" "authentication logic"
/find_and_summarize "src/**/*.service.ts"
/find_and_summarize "docs/**/*.md"
```

**Features:**
- Fast pattern-based file discovery
- Automatic content summarization
- Identifies patterns and relationships
- Lightweight alternative to `/scout`

**Parameters:**
- `<pattern>` (required): Glob pattern (e.g., `**/*.py`, `src/**/service.ts`)
- `[focus]` (optional): Specific aspect to emphasize in summary

**Use when:**
- You know the file pattern to examine
- You need quick overview of a file group
- You want to understand file relationships
- Exploring new codebase areas with known patterns

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

| Command | Description | Tools |
|---------|-------------|-------|
| `/prime_cc` | Claude Code-specific context priming | (Read, Glob, Grep) |
| `/prime_3` | Deep context loading (3-level exploration) | Task, Read, Write, Edit, Glob, Grep, Bash |
| `/load_bundle [bundle]` | Load context from saved bundle | (task delegation) |
| `/tools` | List available built-in tools | (reference) |
| `/all_tools` | List all available tools (comprehensive reference) | (reference) |
| `/question <query>` | Answer questions about project structure using read-only exploration | (Explore agent) |

### `/prime_cc`

Specialized context priming for Claude Code development:
- Loads Claude Code documentation
- Primes for hook development
- Loads settings patterns

```
/prime_cc
```

### `/prime_3`

Load comprehensive codebase context through 3-level progressive exploration:
- **Level 1**: Base context (project basics, documentation)
- **Level 2**: Architectural structure (directory organization, modules)
- **Level 3**: Deep patterns (coding conventions, dependencies, testing)

```
/prime_3
```

**Use when:**
- Before complex multi-file implementations
- You need architectural understanding
- Planning changes across multiple modules

### `/all_tools`

Display comprehensive reference of all available tools including built-in development tools, MCP integrations, and specialized capabilities.

```
/all_tools
```

**Includes:**
- File manipulation tools (Read, Write, Edit, Glob, Grep)
- Task and planning tools
- GitHub and web integration tools
- Browser automation (Playwright)
- Web scraping (Firecrawl)
- Specialized tools

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

| Command | Description | Tools |
|---------|-------------|-------|
| `/background <task>` | Delegate task to background agent | (general-purpose) |
| `/parallel_subagents <task> [count]` | Launch multiple agents in parallel | (task delegation) |
| `/scout <task> [scale]` | Find relevant files using parallel exploration strategies | (Explore agent) |
| `/scout_plan_build <task> [scale] [thoroughness]` | End-to-end scout-plan-build orchestration | Task, Read, Write |

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

### `/scout`

Find files relevant to a specific task using parallel exploration strategies.

```
/scout "add authentication to API endpoints"
/scout "implement caching layer" 6
/scout "fix database connection pooling" 2
```

**Parameters:**
- `<task>` (required): Description of the task or feature to search for
- `[scale]` (optional): Number of parallel search strategies (2-10, default: 4)

**Search Strategies:**
The command launches multiple parallel exploration agents using different approaches:
1. **File Pattern Search**: Glob-based discovery using naming conventions
2. **Content Search**: Grep-based keyword and code search
3. **Architectural Analysis**: Structure understanding through module mapping
4. **Dependency Mapping**: Tracing imports and cross-file references

Higher SCALE values (5-10) add specialized strategies for test files, configuration, type definitions, and documentation.

**Output:**
- Generates detailed report: `agents/scout_files/relevant_files_{timestamp}.md`
- Files grouped by confidence level (high/medium/low)
- Frequency scoring based on how many strategies found each file
- Priority files list and next steps recommendations

**When to Use:**
- Starting work on unfamiliar areas of the codebase
- Understanding scope of changes for a feature or bug fix
- Mapping dependencies before refactoring
- Identifying all potentially affected files

**When NOT to Use:**
- You already know exactly which files to modify
- Single file, trivial changes
- Looking for specific needle queries (use Grep/Glob directly)

### `/scout_plan_build`

End-to-end workflow orchestrating parallel file discovery, implementation planning, and code generation in three sequential phases.

```
/scout_plan_build "Add caching layer to API endpoints" 4
/scout_plan_build "Implement dark mode support" 6 medium
```

**Workflow:**
- **Phase 1 (Scout)**: Parallel exploration to discover relevant files
- **Phase 2 (Plan)**: Create implementation plan informed by scout findings
- **Phase 3 (Build)**: Execute plan sequentially with clear progress tracking

**Parameters:**
- `<task>` (required): Description of what to implement
- `[scale]` (optional): Number of exploration strategies (2-10, default: 4)
- `[thoroughness]` (optional): Plan depth (quick|medium|thorough, default: medium)

**Use when:**
- Starting complete feature implementation from scratch
- You want end-to-end automation from discovery to code
- You have a clear task description
- You need comprehensive file discovery before planning

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

| Command | Description | Tools |
|---------|-------------|-------|
| `/test` | Run test suite | (project-specific) |
| `/test_e2e` | Run end-to-end tests | (project-specific) |
| `/resolve_failed_test <failure_data>` | Analyze and fix failing unit tests | Read, Write, Edit, Bash |
| `/resolve_failed_e2e_test <failure_data>` | Analyze and fix failing E2E tests | (Playwright, analysis) |
| `/track_agentic_kpis <state_json>` | Track agentic development KPIs | Read, Write, Bash |

### `/resolve_failed_test`

Fixes a specific failing unit test using provided failure details.

```
/resolve_failed_test '{"test_name":"test_auth_login","test_path":"tests/test_auth.py","error":"AssertionError: expected True"}'
```

**Workflow:**
1. Analyze test failure and understand purpose
2. Review recent changes and relevant specs
3. Reproduce the failure
4. Fix the issue with minimal changes
5. Validate the fix passes

### `/resolve_failed_e2e_test`

Fixes a specific failing end-to-end test using provided failure details and screenshots.

```
/resolve_failed_e2e_test '{"test_name":"test_user_login_flow","test_path":"tests/e2e/auth_flow.spec.ts","error":"TimeoutError"}'
```

**Workflow:**
1. Analyze E2E test failure (element selectors, timing, layout)
2. Review test file and user story
3. Reproduce the failure in browser
4. Fix element selectors, timing, or logic
5. Validate test passes end-to-end

### `/track_agentic_kpis`

Update ADW performance tracking tables in `app_docs/agentic_kpis.md` with current run metrics.

```
/track_agentic_kpis '{"adw_id":"chore_Tac_12_task_43","issue_number":495,"issue_class":"chore","plan_file":"specs/issue-495.md"}'
```

**Metrics Tracked:**
- Current/longest streak (attempts ≤ 2)
- Plan size statistics
- Diff statistics (lines added/removed)
- Average attempt count

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
