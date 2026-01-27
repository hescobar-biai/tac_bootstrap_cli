# TAC-12 Integration Task Plan

**Version Target:** 0.7.0
**Date:** 2026-01-27
**Total Tasks:** 56

---

## Wave 1 - New Files to Base Repository (20 tasks)

### 1.1 New Commands

#### Task 1
**[FEATURE] Create all_tools.md command file**

- **Description:** Create a new slash command that lists all available tools for the agent. This is a simple documentation/reference command that outputs the available toolset.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/all_tools.md`
- **Content:** Markdown file with frontmatter (allowed-tools: none, description, model: haiku) that lists all built-in tools available to Claude Code agents.

#### Task 2
**[FEATURE] Create build_in_parallel.md command file**

- **Description:** Create a new slash command for parallel build operations that delegates to multiple build-agent subagents. Uses TAC-12 multi-agent orchestration pattern to parallelize file implementation across multiple agents.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/build_in_parallel.md`
- **Content:** Markdown file with frontmatter (allowed-tools: Task, Read, Write, Edit, Glob, Grep) that orchestrates parallel build agents for faster implementation.

#### Task 3
**[FEATURE] Create build.md command file**

- **Description:** Create a simple build command that implements a single task or file. Simpler than build_in_parallel, used for sequential single-file implementation.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/build.md`
- **Content:** Markdown file with frontmatter for straightforward implementation tasks.

#### Task 4
**[FEATURE] Create find_and_summarize.md command file**

- **Description:** Create a command that searches for files matching criteria and generates AI summaries of their contents. Useful for quick codebase understanding.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/find_and_summarize.md`
- **Content:** Markdown file with frontmatter (allowed-tools: Glob, Grep, Read) for file discovery and summarization.

#### Task 5
**[FEATURE] Create plan_w_docs.md command file**

- **Description:** Create a planning command that explores documentation before creating implementation plans. Uses subagents to fetch and analyze relevant docs.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/plan_w_docs.md`
- **Content:** Markdown file with frontmatter (allowed-tools: Task, Read, Glob, Grep, WebFetch) for documentation-informed planning.

#### Task 6
**[FEATURE] Create plan_w_scouters.md command file**

- **Description:** Create a planning command that uses scout subagents to explore the codebase before planning. Deploys multiple parallel scout agents for comprehensive exploration.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/plan_w_scouters.md`
- **Content:** Markdown file with frontmatter using scout-report-suggest agents for thorough codebase analysis.

#### Task 7
**[FEATURE] Create plan.md command file**

- **Description:** Create a basic planning command for implementation tasks. Simpler than plan_w_scouters, for straightforward planning without extensive exploration.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/plan.md`
- **Content:** Markdown file with frontmatter for basic implementation planning.

#### Task 8
**[FEATURE] Create prime_3.md command file**

- **Description:** Create a prime command with 3 levels of depth for context loading. More thorough than standard prime, explores deeper into codebase structure.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/prime_3.md`
- **Content:** Markdown file with frontmatter for deep context priming with 3 exploration levels.

#### Task 9
**[FEATURE] Create scout_plan_build.md command file**

- **Description:** Create a combined workflow command that executes scout exploration, planning, and building in sequence. End-to-end implementation workflow.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/scout_plan_build.md`
- **Content:** Markdown file with frontmatter orchestrating the complete scout->plan->build pipeline.

---

### 1.2 New Agents

#### Task 10
**[FEATURE] Create build-agent.md agent definition**

- **Description:** Create an agent specialized for implementing individual files as part of parallel build operations. Receives file specifications and implements them following project patterns.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/build-agent.md`
- **Content:** Agent definition with tools (Read, Write, Edit, Glob, Grep) for file implementation.

#### Task 11
**[FEATURE] Create playwright-validator.md agent definition**

- **Description:** Create an agent specialized for browser automation validation using Playwright. Validates UI implementations and runs E2E tests.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/playwright-validator.md`
- **Content:** Agent definition with MCP tools for Playwright browser control and validation.

#### Task 12
**[FEATURE] Create scout-report-suggest.md agent definition**

- **Description:** Create a full scout agent that thoroughly explores the codebase and produces detailed reports with file suggestions. Used by plan_w_scouters.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/scout-report-suggest.md`
- **Content:** Agent definition with exploration tools (Glob, Grep, Read) and structured report format.

#### Task 13
**[FEATURE] Create scout-report-suggest-fast.md agent definition**

- **Description:** Create an optimized fast scout agent that performs quick exploration with reduced depth. Used for parallel scouting where speed matters.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/scout-report-suggest-fast.md`
- **Content:** Agent definition similar to scout-report-suggest but with haiku model and faster patterns.

---

### 1.3 New Hooks

#### Task 14
**[FEATURE] Create send_event.py hook file**

- **Description:** Create a hook that sends events to an observability server. Part of TAC-12 observability infrastructure for tracking agent operations.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/send_event.py`
- **Content:** Python script with HTTP POST to observability endpoint, JSON event payload, graceful failure handling.

#### Task 15
**[FEATURE] Create session_start.py hook file**

- **Description:** Create a SessionStart hook that initializes session context including git branch, model info, and project metadata.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/session_start.py`
- **Content:** Python script that captures session initialization data and writes to session storage.

---

### 1.4 New Hook Utilities

#### Task 16
**[FEATURE] Create summarizer.py hook utility**

- **Description:** Create a utility module that generates AI summaries of events using a small LLM. Used by hooks to create human-readable summaries.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/summarizer.py`
- **Content:** Python module with summarize() function using haiku model for concise event summaries.

#### Task 17
**[FEATURE] Create model_extractor.py hook utility**

- **Description:** Create a utility module that extracts the model name from Claude Code transcripts and session data.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/model_extractor.py`
- **Content:** Python module with extract_model() function parsing JSON transcript files.

---

### 1.5 Status Line

#### Task 18
**[FEATURE] Create status_lines directory and status_line_main.py**

- **Description:** Create the status line infrastructure with a dynamic status line script that displays agent name, model, and git branch in the CLI status bar.
- **Files:**
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/status_lines/` (directory)
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/status_lines/status_line_main.py`
- **Content:** Python script that outputs formatted status line with current agent, model, git branch, and session info.

---

### 1.6 New Data Directories

#### Task 19
**[CHORE] Create .claude/data/sessions directory with .gitkeep**

- **Description:** Create directory for storing session data used by observability hooks.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/data/sessions/.gitkeep`
- **Content:** Empty .gitkeep file to preserve directory in git.

#### Task 20
**[CHORE] Create .claude/data/claude-model-cache directory with .gitkeep**

- **Description:** Create directory for caching model information extracted from transcripts.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/data/claude-model-cache/.gitkeep`
- **Content:** Empty .gitkeep file to preserve directory in git.

---

## Wave 2 - Robustify Existing Commands (2 tasks)

#### Task 21
**[FEATURE] Merge background.md with TAC-12 improvements**

- **Description:** Update the existing background.md command to incorporate TAC-12 improvements including:
  - Use `claude` CLI directly with `--dangerously-skip-permissions`
  - Structured report format (Task Understanding, Progress, Results, Task Completed/Failed)
  - Automatic file renaming to `.complete.md` or `.failed.md` based on result
  - Better timestamp handling
  - Directory structure under `agents/background/`
  - Preserve existing Task tool alternative option
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/background.md`
- **Changes:**
  - Add frontmatter with model specification
  - Add Variables section (USER_PROMPT, MODEL, REPORT_FILE)
  - Add Workflow section with detailed steps
  - Add Report Structure section with append-system-prompt template
  - Add File Renaming section

#### Task 22
**[FEATURE] Merge quick-plan.md with TAC-12 improvements**

- **Description:** Update the existing quick-plan.md command to incorporate TAC-12 improvements including:
  - Scout subagents (3 base @agent-scout-report-suggest + 5 fast @agent-scout-report-suggest-fast) in parallel
  - Enhanced plan format with conditional sections based on task type and complexity
  - Problem Statement (conditional)
  - Solution Approach (conditional)
  - Implementation Phases (for medium/complex tasks)
  - Acceptance Criteria
  - Validation Commands
  - Task type and complexity determination logic
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/quick-plan.md`
- **Changes:**
  - Add scout subagent configuration variables
  - Add parallel scout execution workflow
  - Update plan format with conditional sections
  - Add task type classification (feature, bug, chore)
  - Add complexity classification (simple, medium, complex)

---

## Wave 3 - Templates for New Files (20 tasks)

### 3.1 Command Templates

#### Task 23
**[FEATURE] Create all_tools.md.j2 template**

- **Description:** Create Jinja2 template for all_tools.md command generation.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/all_tools.md.j2`
- **Content:** Template mirroring base file structure with `{{ config }}` variables where applicable.

#### Task 24
**[FEATURE] Create build_in_parallel.md.j2 template**

- **Description:** Create Jinja2 template for build_in_parallel.md command generation.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_in_parallel.md.j2`
- **Content:** Template with build agent delegation and parallel execution logic.

#### Task 25
**[FEATURE] Create find_and_summarize.md.j2 template**

- **Description:** Create Jinja2 template for find_and_summarize.md command generation.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/find_and_summarize.md.j2`
- **Content:** Template for file discovery and summarization.

#### Task 26
**[FEATURE] Create plan_w_docs.md.j2 template**

- **Description:** Create Jinja2 template for plan_w_docs.md command generation.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_docs.md.j2`
- **Content:** Template for documentation-informed planning.

#### Task 27
**[FEATURE] Create plan_w_scouters.md.j2 template**

- **Description:** Create Jinja2 template for plan_w_scouters.md command generation.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2`
- **Content:** Template for scout-based planning.

#### Task 28
**[FEATURE] Create plan.md.j2 template**

- **Description:** Create Jinja2 template for plan.md command generation.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2`
- **Content:** Template for basic planning command.

#### Task 29
**[FEATURE] Create prime_3.md.j2 template**

- **Description:** Create Jinja2 template for prime_3.md command generation.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_3.md.j2`
- **Content:** Template for 3-level deep priming.

#### Task 30
**[FEATURE] Create scout_plan_build.md.j2 template**

- **Description:** Create Jinja2 template for scout_plan_build.md command generation.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout_plan_build.md.j2`
- **Content:** Template for combined scout->plan->build workflow.

---

### 3.2 Agent Templates

#### Task 31
**[FEATURE] Create build-agent.md.j2 template**

- **Description:** Create Jinja2 template for build-agent agent definition.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/build-agent.md.j2`
- **Content:** Template for file implementation agent.

#### Task 32
**[FEATURE] Create playwright-validator.md.j2 template**

- **Description:** Create Jinja2 template for playwright-validator agent definition.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/playwright-validator.md.j2`
- **Content:** Template for browser automation validation agent.

#### Task 33
**[FEATURE] Create scout-report-suggest.md.j2 template**

- **Description:** Create Jinja2 template for scout-report-suggest agent definition.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest.md.j2`
- **Content:** Template for full scout agent.

#### Task 34
**[FEATURE] Create scout-report-suggest-fast.md.j2 template**

- **Description:** Create Jinja2 template for scout-report-suggest-fast agent definition.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest-fast.md.j2`
- **Content:** Template for fast scout agent.

---

### 3.3 Hook Templates

#### Task 35
**[FEATURE] Create send_event.py.j2 template**

- **Description:** Create Jinja2 template for send_event.py hook.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/send_event.py.j2`
- **Content:** Template for observability event sending hook.

#### Task 36
**[FEATURE] Create session_start.py.j2 template**

- **Description:** Create Jinja2 template for session_start.py hook.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/session_start.py.j2`
- **Content:** Template for session initialization hook.

---

### 3.4 Hook Utility Templates

#### Task 37
**[FEATURE] Create summarizer.py.j2 template**

- **Description:** Create Jinja2 template for summarizer.py utility.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/summarizer.py.j2`
- **Content:** Template for AI summarization utility.

#### Task 38
**[FEATURE] Create model_extractor.py.j2 template**

- **Description:** Create Jinja2 template for model_extractor.py utility.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/model_extractor.py.j2`
- **Content:** Template for model extraction utility.

---

### 3.5 Status Line Template

#### Task 39
**[FEATURE] Create status_line_main.py.j2 template**

- **Description:** Create Jinja2 template for status_line_main.py.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/status_lines/status_line_main.py.j2`
- **Content:** Template for dynamic status line script.

---

### 3.6 Data Directory Templates

#### Task 40
**[CHORE] Create sessions .gitkeep template**

- **Description:** Create template for .claude/data/sessions/.gitkeep.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/sessions/.gitkeep.j2`
- **Content:** Empty template for gitkeep.

#### Task 41
**[CHORE] Create claude-model-cache .gitkeep template**

- **Description:** Create template for .claude/data/claude-model-cache/.gitkeep.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/claude-model-cache/.gitkeep.j2`
- **Content:** Empty template for gitkeep.

---

## Wave 4 - Templates for Robustified Commands (2 tasks)

#### Task 42
**[FEATURE] Update background.md.j2 template with TAC-12 improvements**

- **Description:** Update existing background.md.j2 template to match the merged background.md command with all TAC-12 improvements.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2`
- **Changes:** Mirror all changes from Task 21 with Jinja2 templating.

#### Task 43
**[FEATURE] Update quick-plan.md.j2 template with TAC-12 improvements**

- **Description:** Update existing quick-plan.md.j2 template to match the merged quick-plan.md command with all TAC-12 improvements.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2`
- **Changes:** Mirror all changes from Task 22 with Jinja2 templating.

---

## Wave 5 - Configuration Updates (9 tasks)

#### Task 44
**[CHORE] Add new slash commands to data_types.py SlashCommand Literal**

- **Description:** Update the `SlashCommand` Literal type in data_types.py to include all 9 new TAC-12 commands. This enables ADW workflows to use these commands via `execute_template()`.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/data_types.py`
- **Changes:** Add to `SlashCommand` Literal (around line 51-75):
```python
    # TAC-12: Multi-agent orchestration commands
    "/all_tools",
    "/build",
    "/build_in_parallel",
    "/find_and_summarize",
    "/plan",
    "/plan_w_docs",
    "/plan_w_scouters",
    "/prime_3",
    "/scout_plan_build",
    "/quick-plan",
    "/background",
```

#### Task 45
**[CHORE] Add new slash commands to data_types.py.j2 template**

- **Description:** Update the `SlashCommand` Literal type in the data_types.py.j2 template to match the base file changes.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2`
- **Changes:** Mirror the same additions as Task 44.

#### Task 46
**[CHORE] Add statusLine configuration to .claude/settings.json**

- **Description:** Add the statusLine configuration to enable dynamic status line display showing agent name, model, and git branch.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/settings.json`
- **Changes:** Add at root level:
```json
"statusLine": {
  "type": "command",
  "command": "uv run $CLAUDE_PROJECT_DIR/.claude/status_lines/status_line_main.py",
  "padding": 0
}
```

#### Task 47
**[CHORE] Add statusLine configuration to settings.json.j2 template**

- **Description:** Add the statusLine configuration to the settings.json.j2 template for generated projects.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2`
- **Changes:** Add statusLine configuration with templated project directory path.

#### Task 48
**[CHORE] Update scaffold_service.py with new TAC-12 files**

- **Description:** Update the scaffold service to include all new TAC-12 files in the scaffold plan including:
  - 9 new commands
  - 4 new agents
  - 2 new hooks
  - 2 new hook utilities
  - 1 status line script
  - 2 new data directories
  - New agents directory (.claude/agents/)
  - New status_lines directory
  - New data directories
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- **Changes:**
  - Add `.claude/agents/` directory creation
  - Add `.claude/status_lines/` directory creation
  - Add `.claude/data/sessions/` directory creation
  - Add `.claude/data/claude-model-cache/` directory creation
  - Add new commands list entries
  - Add new agents list entries
  - Add new hooks list entries
  - Add hook utilities list entries
  - Add status line file entry

#### Task 49
**[CHORE] Add new commands to SLASH_COMMAND_MODEL_MAP in agent.py**

- **Description:** Add the 9 new TAC-12 commands to the model mapping dictionary.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/agent.py`
- **Changes:** Add to SLASH_COMMAND_MODEL_MAP:
```python
"/all_tools": {"base": "haiku", "heavy": "haiku"},
"/build": {"base": "sonnet", "heavy": "sonnet"},
"/build_in_parallel": {"base": "sonnet", "heavy": "opus"},
"/find_and_summarize": {"base": "sonnet", "heavy": "sonnet"},
"/plan": {"base": "sonnet", "heavy": "opus"},
"/plan_w_docs": {"base": "sonnet", "heavy": "opus"},
"/plan_w_scouters": {"base": "sonnet", "heavy": "opus"},
"/prime_3": {"base": "sonnet", "heavy": "sonnet"},
"/scout_plan_build": {"base": "sonnet", "heavy": "opus"},
```

#### Task 50
**[CHORE] Add new commands to agent.py.j2 template**

- **Description:** Add the 9 new TAC-12 commands to the agent.py.j2 template model mapping.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2`
- **Changes:** Mirror changes from Task 49 in Jinja2 template format.

---

## Wave 6 - Documentation (6 tasks)

#### Task 51
**[CHORE] Update CLI documentation files**

- **Description:** Update the CLI documentation to include all new TAC-12 commands, agents, and hooks.
- **Files:**
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/docs/commands.md`
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/docs/hooks.md`
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/docs/agents.md`
- **Changes:**
  - Add documentation for 9 new commands
  - Add documentation for 4 new agents
  - Add documentation for 2 new hooks and 2 utilities
  - Add status line documentation

#### Task 52
**[CHORE] Update tac_bootstrap_cli README.md**

- **Description:** Update the CLI README with new TAC-12 features overview.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md`
- **Changes:**
  - Add TAC-12 Multi-Agent Orchestration section
  - Add Observability features section
  - Add Status Line documentation
  - Update command reference table

#### Task 53
**[CHORE] Update root README.md with TAC-12 overview**

- **Description:** Update the main repository README with TAC-12 features.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/README.md`
- **Changes:**
  - Add TAC-12 integration section
  - Document new commands and agents
  - Add status line usage

#### Task 54 (OPTIONAL)
**[FEATURE] Add TAC-12 helper functions to workflow_ops.py**

- **Description:** Add optional helper functions to workflow_ops.py for using new TAC-12 commands from ADW workflows. These are convenience wrappers that can be used by future workflows.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/workflow_ops.py`
- **Changes:** Add functions:
  - `scout_codebase()` - Wrapper for /scout command
  - `plan_with_scouts()` - Wrapper for /plan_w_scouters or /quick-plan with scouts
  - `build_in_parallel()` - Wrapper for /build_in_parallel command
  - `find_and_summarize()` - Wrapper for /find_and_summarize command

#### Task 55 (OPTIONAL)
**[FEATURE] Add TAC-12 helper functions to workflow_ops.py.j2 template**

- **Description:** Mirror the helper function additions from Task 54 to the workflow_ops.py.j2 template.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2`
- **Changes:** Same additions as Task 54.

#### Task 56
**[CHORE] Update CHANGELOG.md to version 0.7.0**

- **Description:** Add comprehensive changelog entry for version 0.7.0 documenting all TAC-12 integration changes.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md`
- **Changes:** Add new section at top:

```markdown
## [0.7.0] - 2026-01-XX

### Added

#### Multi-Agent Orchestration (TAC-12)
- Command: `/all_tools` - Lists all available tools
- Command: `/build_in_parallel` - Parallel build with multiple build-agents
- Command: `/build` - Simple single-file build
- Command: `/find_and_summarize` - File search with AI summaries
- Command: `/plan_w_docs` - Planning with documentation exploration
- Command: `/plan_w_scouters` - Planning with scout subagents
- Command: `/plan` - Basic implementation planning
- Command: `/prime_3` - Deep 3-level context priming
- Command: `/scout_plan_build` - Combined scout->plan->build workflow

#### New Agents (TAC-12)
- Agent: `build-agent` - File implementation specialist for parallel builds
- Agent: `playwright-validator` - Browser automation validation
- Agent: `scout-report-suggest` - Full codebase scout with reports
- Agent: `scout-report-suggest-fast` - Optimized fast scout

#### Observability Infrastructure (TAC-12)
- Hook: `send_event.py` - Sends events to observability server
- Hook: `session_start.py` - Session initialization with context
- Utility: `summarizer.py` - AI event summarization
- Utility: `model_extractor.py` - Model name extraction from transcripts
- Status Line: Dynamic status showing agent, model, git branch
- Directory: `.claude/data/sessions/` - Session data storage
- Directory: `.claude/data/claude-model-cache/` - Model info cache

### Changed
- Command: `/background` - Enhanced with CLI delegation, structured reports, automatic file renaming
- Command: `/quick-plan` - Enhanced with parallel scout agents and conditional plan sections
- Configuration: `settings.json` now includes statusLine configuration
- Scaffold: Added new directories, commands, agents, hooks to generation

### Technical Details
TAC-12 features implement the Multi-Agent Orchestration pattern:
- Orchestrator agent pattern for managing agent fleets
- Parallel scout execution for faster codebase exploration
- Observability hooks for real-time monitoring
- Status line for immediate agent/model visibility
- All features include Jinja2 templates for generated projects
```

---

## Execution Order Summary

1. **Tasks 1-9:** Create new command files in `.claude/commands/`
2. **Tasks 10-13:** Create new agent files in `.claude/agents/`
3. **Tasks 14-15:** Create new hook files in `.claude/hooks/`
4. **Tasks 16-17:** Create new utility files in `.claude/hooks/utils/`
5. **Tasks 18-20:** Create status line and data directories
6. **Tasks 21-22:** Merge existing commands with TAC-12 improvements
7. **Tasks 23-41:** Create Jinja2 templates for all new files
8. **Tasks 42-43:** Update templates for merged commands
9. **Tasks 44-50:** Update configuration files (data_types.py, settings.json, scaffold_service.py, agent.py)
10. **Tasks 51-53:** Update documentation
11. **Tasks 54-55 (OPTIONAL):** Add helper functions to workflow_ops.py
12. **Task 56:** Update CHANGELOG (FINAL)

---

## Verification Checklist

After implementation, verify:

- [ ] `uv run pytest` passes all tests
- [ ] All 9 new commands exist in `.claude/commands/`
- [ ] All 4 new agents exist in `.claude/agents/`
- [ ] All hooks and utilities are present
- [ ] Status line works: `uv run .claude/status_lines/status_line_main.py`
- [ ] Background command works: `/background "test task"`
- [ ] Quick-plan command works: `/quick-plan "implement feature X"`
- [ ] data_types.py has new SlashCommand entries
- [ ] agent.py has new SLASH_COMMAND_MODEL_MAP entries
- [ ] CLI generation includes new files: `cd tac_bootstrap_cli && uv run tac-bootstrap init test-project --dry-run`
- [ ] CHANGELOG.md shows version 0.7.0

---

## Parallel Execution Groups

La siguiente tabla muestra cómo agrupar las tareas para ejecución paralela usando la funcionalidad de agentes paralelos. Las tareas dentro de un mismo grupo **NO tienen dependencias entre sí** y pueden ejecutarse simultáneamente.

### Resumen de Grupos Paralelos

| Grupo | Tareas | Cantidad | Dependencia | Descripción |
|-------|--------|----------|-------------|-------------|
| **P1** | 1-9 | 9 | Ninguna | Nuevos comandos (archivos independientes) |
| **P2** | 10-13 | 4 | Ninguna | Nuevos agentes (archivos independientes) |
| **P3** | 14-17 | 4 | Ninguna | Nuevos hooks y utilities |
| **P4** | 18-20 | 3 | Ninguna | Status line y directorios data |
| **P5** | 21-22 | 2 | P2 (agents) | Merge de comandos existentes |
| **P6** | 23-30 | 8 | P1 | Templates de comandos |
| **P7** | 31-34 | 4 | P2 | Templates de agentes |
| **P8** | 35-38 | 4 | P3 | Templates de hooks/utils |
| **P9** | 39-41 | 3 | P4 | Templates de status line y data |
| **P10** | 42-43 | 2 | P5 | Templates de comandos merged |
| **P11** | 44-45 | 2 | Ninguna | data_types.py (base + template) |
| **P12** | 46-47 | 2 | Ninguna | settings.json (base + template) |
| **P13** | 48 | 1 | P6-P10 | scaffold_service.py |
| **P14** | 49-50 | 2 | P11 | agent.py (base + template) |
| **P15** | 51-53 | 3 | P1-P14 | Documentación |
| **P16** | 54-55 | 2 | P14 | workflow_ops.py (OPCIONAL) |
| **SEQ** | 56 | 1 | TODOS | CHANGELOG (FINAL) |

---

### Detalle de Ejecución Paralela por Fase

#### Fase 1: Archivos Base (Sin dependencias) - 20 tareas en 4 grupos paralelos

```
┌─────────────────────────────────────────────────────────────────┐
│                     EJECUCIÓN PARALELA                          │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│ Grupo P1 (9)    │ Grupo P2 (4)    │ Grupo P3 (4)    │ P4 (3)    │
│ Commands        │ Agents          │ Hooks/Utils     │ Status    │
├─────────────────┼─────────────────┼─────────────────┼───────────┤
│ T1: all_tools   │ T10: build-agent│ T14: send_event │ T18: dir  │
│ T2: build_par   │ T11: playwright │ T15: session    │ T19: sess │
│ T3: build       │ T12: scout-rep  │ T16: summarizer │ T20: cache│
│ T4: find_sum    │ T13: scout-fast │ T17: model_ext  │           │
│ T5: plan_docs   │                 │                 │           │
│ T6: plan_scout  │                 │                 │           │
│ T7: plan        │                 │                 │           │
│ T8: prime_3     │                 │                 │           │
│ T9: scout_build │                 │                 │           │
└─────────────────┴─────────────────┴─────────────────┴───────────┘
                    Total: 20 tareas paralelas
```

#### Fase 2: Merge Commands (Depende de P2)

```
┌─────────────────────────────────────────────────────────────────┐
│ Grupo P5 (2) - Merge Commands                                   │
├─────────────────────────────────────────────────────────────────┤
│ T21: background.md    ║    T22: quick-plan.md                   │
│ (usa agents de P2)    ║    (usa agents de P2)                   │
└─────────────────────────────────────────────────────────────────┘
                    Total: 2 tareas paralelas
```

#### Fase 3: Templates (Depende de archivos base)

```
┌─────────────────────────────────────────────────────────────────┐
│                     EJECUCIÓN PARALELA                          │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│ Grupo P6 (8)    │ Grupo P7 (4)    │ Grupo P8 (4)    │ P9 (3)    │
│ Cmd Templates   │ Agent Templates │ Hook Templates  │ Other     │
├─────────────────┼─────────────────┼─────────────────┼───────────┤
│ T23-30          │ T31-34          │ T35-38          │ T39-41    │
│ (Depende P1)    │ (Depende P2)    │ (Depende P3)    │ (Dep P4)  │
└─────────────────┴─────────────────┴─────────────────┴───────────┘
                    Total: 19 tareas paralelas
```

#### Fase 4: Templates Merged + Config Inicial

```
┌─────────────────────────────────────────────────────────────────┐
│                     EJECUCIÓN PARALELA                          │
├─────────────────────┬─────────────────────┬─────────────────────┤
│ Grupo P10 (2)       │ Grupo P11 (2)       │ Grupo P12 (2)       │
│ Merged Templates    │ data_types.py       │ settings.json       │
├─────────────────────┼─────────────────────┼─────────────────────┤
│ T42: background.j2  │ T44: data_types     │ T46: settings       │
│ T43: quick-plan.j2  │ T45: data_types.j2  │ T47: settings.j2    │
│ (Depende P5)        │ (Sin dependencia)   │ (Sin dependencia)   │
└─────────────────────┴─────────────────────┴─────────────────────┘
                    Total: 6 tareas paralelas
```

#### Fase 5: Configuración Final

```
┌─────────────────────────────────────────────────────────────────┐
│ Grupo P13 (1) - SECUENCIAL                                      │
├─────────────────────────────────────────────────────────────────┤
│ T48: scaffold_service.py (Depende de P6-P10 para lista files)   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Grupo P14 (2) - Paralelo (Depende P11)                          │
├─────────────────────────────────────────────────────────────────┤
│ T49: agent.py    ║    T50: agent.py.j2                          │
└─────────────────────────────────────────────────────────────────┘
```

#### Fase 6: Documentación y Finalización

```
┌─────────────────────────────────────────────────────────────────┐
│ Grupo P15 (3) - Documentación Paralela                          │
├─────────────────────────────────────────────────────────────────┤
│ T51: docs/*.md   ║   T52: CLI README  ║   T53: Root README      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Grupo P16 (2) - OPCIONAL                                        │
├─────────────────────────────────────────────────────────────────┤
│ T54: workflow_ops.py   ║   T55: workflow_ops.py.j2              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ SECUENCIAL - FINAL                                              │
├─────────────────────────────────────────────────────────────────┤
│ T56: CHANGELOG.md (Debe ejecutarse ÚLTIMO)                      │
└─────────────────────────────────────────────────────────────────┘
```

---

### Comando de Ejecución Paralela Sugerido

Para cada grupo paralelo, usar el patrón:

```bash
# Ejemplo: Ejecutar Grupo P1 (9 comandos en paralelo)
/parallel_subagents "Tasks: [T1, T2, T3, T4, T5, T6, T7, T8, T9] - Create new command files"
```

### Optimización de Tiempo

| Estrategia | Tareas Secuenciales | Tareas Paralelas | Ahorro Estimado |
|------------|--------------------:|----------------:|-----------------|
| Sin paralelismo | 56 | 0 | 0% |
| Paralelismo máximo | 8 fases | 48 paralelas | ~70% |

**Fases mínimas requeridas:** 8 (debido a dependencias entre waves)
