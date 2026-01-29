# TAC-12 Integration Task Plan v2 (UPDATED FROM REAL CODE)

**Version Target:** 0.7.0
**Date:** 2026-01-29
**Based On:** Real TAC-12 code analysis from `/Volumes/MAc1/Celes/TAC/tac-12`
**Total Tasks:** 72 (56 original + 16 new from code analysis)

**IMPORTANT:** This plan is based on the REAL TAC-12 code implementation, not just documentation.

---

## Changes from v1

### New Tasks Added:
- **4 new commands:** load_ai_docs, load_bundle, parallel_subagents, prime_cc
- **2 new agents:** docs-scraper, meta-agent
- **7 new hooks:** pre_tool_use, post_tool_use, notification, stop, subagent_stop, pre_compact, user_prompt_submit
- **3 new utilities:** constants.py, llm/ subdirectory, tts/ subdirectory
- **Updated implementations:** background.md and quick-plan.md with full details from real code

---

## Wave 1 - New Files to Base Repository (33 tasks)

### 1.1 New Commands (13 tasks)

#### Task 1
**[FEATURE] Create all_tools.md command file**

- **Description:** Create a new slash command that lists all available tools for the agent.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/all_tools.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/all_tools.md`
- **Content:**
```markdown
---
description: Lists all available tools for Claude Code agents
allowed-tools: none
model: haiku
---

# All Tools

Lists all built-in tools available to Claude Code agents including:
- File operations (Read, Write, Edit, Glob, Grep, MultiEdit)
- Execution tools (Bash, Task, TaskOutput)
- Web tools (WebFetch, WebSearch)
- Agent tools (EnterPlanMode, ExitPlanMode, AskUserQuestion, Skill)
- Other tools (NotebookEdit, mcp__)
```

#### Task 2
**[FEATURE] Create build_in_parallel.md command file**

- **Description:** Create a slash command for parallel build operations using build-agent subagents. Based on real TAC-12 implementation with detailed file specifications.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/build_in_parallel.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/build_in_parallel.md`
- **Key Features:**
  - Uses `.claude/agents/build-agent.md` subagent
  - Model: claude-sonnet-4-5-20250929
  - 8-step workflow with detailed file specifications
  - Parallel batch execution pattern
  - Comprehensive reporting format

#### Task 3
**[FEATURE] Create build.md command file**

- **Description:** Create a simple sequential build command that implements a plan top-to-bottom without parallelization.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/build.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/build.md`
- **Key Features:**
  - Simple sequential implementation
  - Reads plan from PATH_TO_PLAN
  - Ultrathink and implement
  - Validation with git diff --stat

#### Task 4
**[FEATURE] Create find_and_summarize.md command file**

- **Description:** Create a command that searches for files and generates AI summaries.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/find_and_summarize.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/find_and_summarize.md`
- **Key Features:**
  - allowed-tools: Glob, Grep, Read
  - File discovery with patterns
  - AI-powered summarization

#### Task 5
**[FEATURE] Create plan_w_docs.md command file**

- **Description:** Create a planning command that explores documentation before creating plans.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/plan_w_docs.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan_w_docs.md`
- **Key Features:**
  - allowed-tools: Task, Read, Glob, Grep, WebFetch
  - Documentation exploration with subagents
  - Enhanced planning with doc context

#### Task 6
**[FEATURE] Create plan_w_scouters.md command file**

- **Description:** Create a planning command that uses scout subagents for codebase exploration.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/plan_w_scouters.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan_w_scouters.md`
- **Key Features:**
  - Multiple parallel scout agents
  - Both base and fast scouts
  - Comprehensive codebase analysis

#### Task 7
**[FEATURE] Create plan.md command file**

- **Description:** Create a simple planning command without scout agents. SIMPLER than plan_w_scouters.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/plan.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan.md`
- **Key Features:**
  - Model: claude-opus-4-1-20250805
  - allowed-tools: Read, Write, Edit, Glob, Grep, MultiEdit
  - Simple 5-step workflow (no scouts)
  - Saves to specs/ directory

#### Task 8
**[FEATURE] Create prime_3.md command file**

- **Description:** Create a deep priming command with 3 levels of exploration.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/prime_3.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/prime_3.md`
- **Key Features:**
  - 3-level deep context loading
  - Comprehensive codebase understanding

#### Task 9
**[FEATURE] Create scout_plan_build.md command file**

- **Description:** Create an end-to-end workflow command: scout -> plan -> build.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/scout_plan_build.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/scout_plan_build.md`
- **Key Features:**
  - Complete implementation pipeline
  - Orchestrates multiple phases

#### Task 10 (NEW)
**[FEATURE] Create load_ai_docs.md command file**

- **Description:** Create a command that loads AI documentation files into context.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/load_ai_docs.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/load_ai_docs.md`
- **Key Features:**
  - Loads documentation from ai_docs/ or similar
  - Context preparation for planning
  - allowed-tools: Read, Glob, Grep

#### Task 11 (NEW)
**[FEATURE] Create load_bundle.md command file**

- **Description:** Create a command that loads context bundles (pre-packaged file sets).
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/load_bundle.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/load_bundle.md`
- **Key Features:**
  - Pre-packaged context loading
  - Bundle definitions
  - allowed-tools: Read, Glob

#### Task 12 (NEW)
**[FEATURE] Create parallel_subagents.md command file**

- **Description:** Create a command that orchestrates multiple subagents in parallel for divide-and-conquer tasks.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/parallel_subagents.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/parallel_subagents.md`
- **Key Features:**
  - Multi-agent orchestration
  - Parallel execution pattern
  - Task delegation
  - allowed-tools: Task

#### Task 13 (NEW)
**[FEATURE] Create prime_cc.md command file**

- **Description:** Create a specialized prime command for Claude Code codebase understanding.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/prime_cc.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/prime_cc.md`
- **Key Features:**
  - Specialized for Claude Code projects
  - Deep understanding of CC patterns

---

### 1.2 New Agents (6 tasks)

#### Task 14
**[FEATURE] Create build-agent.md agent definition**

- **Description:** Create a specialized agent for implementing individual files in parallel builds.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/build-agent.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/build-agent.md`
- **Key Features:**
  - name: build-agent
  - tools: Write, Read, Edit, Grep, Glob, Bash, TodoWrite
  - model: sonnet
  - color: blue
  - Specialized for ONE file implementation
  - 6-step workflow with verification
  - Structured report format

#### Task 15
**[FEATURE] Create playwright-validator.md agent definition**

- **Description:** Create an agent for browser automation and E2E validation.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/playwright-validator.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/playwright-validator.md`
- **Key Features:**
  - Browser automation with Playwright
  - E2E test execution
  - UI validation

#### Task 16
**[FEATURE] Create scout-report-suggest.md agent definition**

- **Description:** Create a full scout agent for codebase exploration with detailed reports.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/scout-report-suggest.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/scout-report-suggest.md`
- **Key Features:**
  - name: scout-report-suggest
  - tools: Read, Glob, Grep
  - model: sonnet
  - color: blue
  - READ-ONLY analysis
  - Structured SCOUT REPORT format
  - Root cause analysis

#### Task 17
**[FEATURE] Create scout-report-suggest-fast.md agent definition**

- **Description:** Create a fast scout agent optimized for quick exploration.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/scout-report-suggest-fast.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/scout-report-suggest-fast.md`
- **Key Features:**
  - Optimized for speed
  - model: haiku (faster)
  - Similar structure to scout-report-suggest

#### Task 18 (NEW)
**[FEATURE] Create docs-scraper.md agent definition**

- **Description:** Create a specialized agent for scraping and extracting documentation from web sources.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/docs-scraper.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/docs-scraper.md`
- **Key Features:**
  - Web documentation scraping
  - Content extraction
  - tools: WebFetch, WebSearch, Read, Write

#### Task 19 (NEW)
**[FEATURE] Create meta-agent.md agent definition**

- **Description:** Create a meta-agent that generates OTHER agents based on specifications.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/meta-agent.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/meta-agent.md`
- **Key Features:**
  - Agent generation
  - Template-based agent creation
  - tools: Read, Write, Edit, Glob, Grep

---

### 1.3 New Hooks (9 tasks)

#### Task 20
**[FEATURE] Create send_event.py hook file**

- **Description:** Create the observability hook that sends events to server.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/send_event.py`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/send_event.py`
- **Key Features:**
  - HTTP POST to observability endpoint
  - Arguments: --source-app, --event-type, --server-url, --add-chat, --summarize
  - Integrates with summarizer.py and model_extractor.py
  - Always exits with 0 (non-blocking)

#### Task 21
**[FEATURE] Create session_start.py hook file**

- **Description:** Create the SessionStart hook for initializing session context.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/session_start.py`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/session_start.py`
- **Key Features:**
  - Captures git branch, model, project metadata
  - Writes to session storage

#### Task 22 (NEW)
**[FEATURE] Create pre_tool_use.py hook file**

- **Description:** Create a hook that runs BEFORE every tool use.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/pre_tool_use.py`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/pre_tool_use.py`
- **Key Features:**
  - Pre-tool use logging
  - Integration point for observability
  - Called before every tool invocation

#### Task 23 (NEW)
**[FEATURE] Create post_tool_use.py hook file**

- **Description:** Create a hook that runs AFTER every tool use.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/post_tool_use.py`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/post_tool_use.py`
- **Key Features:**
  - Post-tool use logging
  - Result capture
  - Performance tracking

#### Task 24 (NEW)
**[FEATURE] Create notification.py hook file**

- **Description:** Create a hook for system notifications.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/notification.py`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/notification.py`
- **Key Features:**
  - System notification handling
  - Event logging

#### Task 25 (NEW)
**[FEATURE] Create stop.py hook file**

- **Description:** Create a hook that runs when the session stops.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/stop.py`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/stop.py`
- **Key Features:**
  - Session cleanup
  - Final logging
  - Chat transcript capture

#### Task 26 (NEW)
**[FEATURE] Create subagent_stop.py hook file**

- **Description:** Create a hook that runs when a subagent stops.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/subagent_stop.py`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/subagent_stop.py`
- **Key Features:**
  - Subagent lifecycle tracking
  - Result aggregation

#### Task 27 (NEW)
**[FEATURE] Create pre_compact.py hook file**

- **Description:** Create a hook that runs before context compaction.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/pre_compact.py`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/pre_compact.py`
- **Key Features:**
  - Pre-compaction logging
  - Context size tracking

#### Task 28 (NEW)
**[FEATURE] Create user_prompt_submit.py hook file**

- **Description:** Create a hook that runs when user submits a prompt.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/user_prompt_submit.py`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/user_prompt_submit.py`
- **Key Features:**
  - Prompt logging
  - Flags: --log-only, --store-last-prompt, --name-agent
  - User interaction tracking

---

### 1.4 New Hook Utilities (5 tasks)

#### Task 29
**[FEATURE] Create summarizer.py hook utility**

- **Description:** Create a utility that generates AI summaries using haiku model.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/summarizer.py`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/summarizer.py`
- **Key Features:**
  - generate_event_summary() function
  - Uses claude-haiku-4-5-20251001
  - Concise one-sentence summaries
  - Graceful error handling

#### Task 30
**[FEATURE] Create model_extractor.py hook utility**

- **Description:** Create a utility that extracts model name from transcripts with caching.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/model_extractor.py`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/model_extractor.py`
- **Key Features:**
  - get_model_from_transcript() function
  - Cache in .claude/data/claude-model-cache/
  - Parses JSONL transcript files

#### Task 31 (NEW)
**[FEATURE] Create constants.py hook utility**

- **Description:** Create a utility with shared constants for hooks.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/constants.py`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/constants.py`
- **Key Features:**
  - Shared constant definitions
  - API endpoints
  - Default values

#### Task 32 (NEW)
**[FEATURE] Create llm/ utilities subdirectory**

- **Description:** Create LLM-related utilities for hooks.
- **Directory:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/llm/`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/llm/`
- **Key Features:**
  - LLM helper functions
  - API wrappers
  - (Explore TAC-12 contents for specifics)

#### Task 33 (NEW)
**[FEATURE] Create tts/ utilities subdirectory**

- **Description:** Create text-to-speech utilities for hooks.
- **Directory:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/tts/`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/tts/`
- **Key Features:**
  - TTS integration
  - Audio notification support
  - (Explore TAC-12 contents for specifics)

---

### 1.5 Status Line (1 task)

#### Task 34
**[FEATURE] Create status_lines directory and status_line_main.py**

- **Description:** Create the dynamic status line script.
- **Files:**
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/status_lines/` (directory)
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/status_lines/status_line_main.py`
- **Content:** Python script that outputs formatted status line with agent name, model, git branch.

---

### 1.6 New Data Directories (2 tasks)

#### Task 35
**[CHORE] Create .claude/data/sessions directory with .gitkeep**

- **Description:** Create directory for session data.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/data/sessions/.gitkeep`
- **Note:** Verify if TAC-12 actually uses this approach (analysis shows no visible .claude/data/ dir)

#### Task 36
**[CHORE] Create .claude/data/claude-model-cache directory with .gitkeep**

- **Description:** Create directory for model info cache.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/data/claude-model-cache/.gitkeep`
- **Note:** Used by model_extractor.py for caching

---

## Wave 2 - Robustify Existing Commands (2 tasks)

#### Task 37
**[FEATURE] Merge background.md with TAC-12 improvements**

- **Description:** Update background.md command with COMPLETE TAC-12 implementation.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/background.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/background.md`
- **Key Changes:**
  - Variables: USER_PROMPT ($1), MODEL ($2, defaults 'sonnet'), REPORT_FILE ($3)
  - Uses `claude` CLI directly with --dangerously-skip-permissions
  - Structured report format in append-system-prompt:
    - Task Understanding (numbered list)
    - Progress (updated iteratively)
    - Results (concrete outcomes)
    - Task Completed / Task Failed
  - Auto-rename to .complete.md or .failed.md
  - Timestamp captured ONCE: `TIMESTAMP=$(date +%a_%H_%M_%S)`
  - Directory: `agents/background/`
  - Command pattern:
```bash
claude \
  --model "${MODEL}" \
  --output-format text \
  --dangerously-skip-permissions \
  --append-system-prompt "IMPORTANT: You are running as a background agent..." \
  --print "${USER_PROMPT}"
```

#### Task 38
**[FEATURE] Merge quick-plan.md with TAC-12 improvements**

- **Description:** Update quick-plan.md command with COMPLETE TAC-12 implementation including scouts.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/quick-plan.md`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan_w_scouters.md` (Note: TAC-12 quick-plan is SIMPLER)
- **Key Changes:**
  - Variables:
    - USER_PROMPT: $1
    - PLAN_OUTPUT_DIRECTORY: specs/
    - TOTAL_BASE_SCOUT_SUBAGENTS: 3
    - TOTAL_FAST_SCOUT_SUBAGENTS: 5
  - Workflow Step 2 - Explore Codebase:
    1. Deploy 3 @agent-scout-report-suggest in PARALLEL
    2. Deploy 5 @agent-scout-report-suggest-fast in PARALLEL
    3. Consolidate results
    4. MANUAL validation
  - Task type determination: chore|feature|refactor|fix|enhancement
  - Complexity determination: simple|medium|complex
  - Conditional Plan Format sections:
    - Problem Statement (if feature or medium/complex)
    - Solution Approach (if feature or medium/complex)
    - Implementation Phases (if medium/complex)
    - Testing Strategy (if feature or medium/complex)

---

## Wave 3 - Templates for New Files (33 tasks)

### 3.1 Command Templates (13 tasks)

#### Task 39-51
**[FEATURE] Create command templates**

Create Jinja2 templates for all 13 new commands:
- Task 39: all_tools.md.j2
- Task 40: build_in_parallel.md.j2
- Task 41: build.md.j2
- Task 42: find_and_summarize.md.j2
- Task 43: plan_w_docs.md.j2
- Task 44: plan_w_scouters.md.j2
- Task 45: plan.md.j2
- Task 46: prime_3.md.j2
- Task 47: scout_plan_build.md.j2
- Task 48: load_ai_docs.md.j2
- Task 49: load_bundle.md.j2
- Task 50: parallel_subagents.md.j2
- Task 51: prime_cc.md.j2

**Directory:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/`
**Content:** Jinja2 templates with {{ config }} variables where applicable

---

### 3.2 Agent Templates (6 tasks)

#### Task 52-57
**[FEATURE] Create agent templates**

Create Jinja2 templates for all 6 new agents:
- Task 52: build-agent.md.j2
- Task 53: playwright-validator.md.j2
- Task 54: scout-report-suggest.md.j2
- Task 55: scout-report-suggest-fast.md.j2
- Task 56: docs-scraper.md.j2
- Task 57: meta-agent.md.j2

**Directory:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/`

---

### 3.3 Hook Templates (9 tasks)

#### Task 58-66
**[FEATURE] Create hook templates**

Create Jinja2 templates for all 9 hooks:
- Task 58: send_event.py.j2
- Task 59: session_start.py.j2
- Task 60: pre_tool_use.py.j2
- Task 61: post_tool_use.py.j2
- Task 62: notification.py.j2
- Task 63: stop.py.j2
- Task 64: subagent_stop.py.j2
- Task 65: pre_compact.py.j2
- Task 66: user_prompt_submit.py.j2

**Directory:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/`

---

### 3.4 Hook Utility Templates (5 tasks)

#### Task 67-71
**[FEATURE] Create hook utility templates**

Create Jinja2 templates for all 5 utilities:
- Task 67: summarizer.py.j2
- Task 68: model_extractor.py.j2
- Task 69: constants.py.j2
- Task 70: llm/ subdirectory templates (multiple files)
- Task 71: tts/ subdirectory templates (multiple files)

**Directory:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/`

---

### 3.5 Status Line Template (1 task)

#### Task 72
**[FEATURE] Create status_line_main.py.j2 template**

- **Description:** Create Jinja2 template for status line script.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/status_lines/status_line_main.py.j2`

---

### 3.6 Data Directory Templates (2 tasks)

#### Task 73-74
**[CHORE] Create data directory .gitkeep templates**

- Task 73: sessions/.gitkeep.j2
- Task 74: claude-model-cache/.gitkeep.j2

**Directory:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/`

---

## Wave 4 - Templates for Robustified Commands (2 tasks)

#### Task 75
**[FEATURE] Update background.md.j2 template with TAC-12 improvements**

- **Description:** Update template to match merged background.md.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2`
- **Changes:** Mirror all changes from Task 37

#### Task 76
**[FEATURE] Update quick-plan.md.j2 template with TAC-12 improvements**

- **Description:** Update template to match merged quick-plan.md.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2`
- **Changes:** Mirror all changes from Task 38

---

## Wave 5 - Configuration Updates (9 tasks)

#### Task 77
**[CHORE] Add new slash commands to data_types.py SlashCommand Literal**

- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/data_types.py`
- **Changes:** Add to SlashCommand Literal (around line 51-75):
```python
# TAC-12: Multi-agent orchestration commands
"/all_tools",
"/build",
"/build_in_parallel",
"/find_and_summarize",
"/load_ai_docs",
"/load_bundle",
"/parallel_subagents",
"/plan",
"/plan_w_docs",
"/plan_w_scouters",
"/prime_3",
"/prime_cc",
"/scout_plan_build",
"/quick-plan",
"/background",
```

#### Task 78
**[CHORE] Add new slash commands to data_types.py.j2 template**

- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2`
- **Changes:** Mirror Task 77

#### Task 79
**[CHORE] Add statusLine and ALL hooks to .claude/settings.json**

- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/settings.json`
- **Changes:** Add statusLine and configure ALL 7 hook types:
```json
{
  "statusLine": {
    "type": "command",
    "command": "uv run $CLAUDE_PROJECT_DIR/.claude/status_lines/status_line_main.py",
    "padding": 0
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py"
          },
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/send_event.py --source-app multi-agent-orchestration --event-type PreToolUse --summarize"
          }
        ]
      }
    ],
    "PostToolUse": [...],      // Similar structure
    "Notification": [...],     // Similar structure
    "Stop": [...],            // Similar structure with --add-chat
    "SubagentStop": [...],    // Similar structure
    "PreCompact": [...],      // Similar structure
    "UserPromptSubmit": [...]  // --log-only --store-last-prompt --name-agent
  }
}
```

#### Task 80
**[CHORE] Add statusLine and hooks to settings.json.j2 template**

- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2`
- **Changes:** Mirror Task 79 with Jinja2 templating

#### Task 81
**[CHORE] Update scaffold_service.py with new TAC-12 files**

- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- **Changes:**
  - Add `.claude/agents/` directory creation
  - Add `.claude/status_lines/` directory creation
  - Add `.claude/data/sessions/` directory creation
  - Add `.claude/data/claude-model-cache/` directory creation
  - Add 13 new commands (Tasks 1-13)
  - Add 6 new agents (Tasks 14-19)
  - Add 9 new hooks (Tasks 20-28)
  - Add 5 new hook utilities (Tasks 29-33)
  - Add status line file

#### Task 82
**[CHORE] Add new commands to SLASH_COMMAND_MODEL_MAP in agent.py**

- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/agent.py`
- **Changes:** Add to SLASH_COMMAND_MODEL_MAP:
```python
"/all_tools": {"base": "haiku", "heavy": "haiku"},
"/build": {"base": "sonnet", "heavy": "sonnet"},
"/build_in_parallel": {"base": "sonnet", "heavy": "opus"},
"/find_and_summarize": {"base": "sonnet", "heavy": "sonnet"},
"/load_ai_docs": {"base": "sonnet", "heavy": "sonnet"},
"/load_bundle": {"base": "haiku", "heavy": "sonnet"},
"/parallel_subagents": {"base": "sonnet", "heavy": "opus"},
"/plan": {"base": "opus", "heavy": "opus"},
"/plan_w_docs": {"base": "sonnet", "heavy": "opus"},
"/plan_w_scouters": {"base": "sonnet", "heavy": "opus"},
"/prime_3": {"base": "sonnet", "heavy": "sonnet"},
"/prime_cc": {"base": "sonnet", "heavy": "sonnet"},
"/scout_plan_build": {"base": "sonnet", "heavy": "opus"},
```

#### Task 83
**[CHORE] Add new commands to agent.py.j2 template**

- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2`
- **Changes:** Mirror Task 82

---

## Wave 6 - Documentation (6 tasks)

#### Task 84
**[CHORE] Update CLI documentation files**

- **Files:**
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/docs/commands.md`
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/docs/hooks.md`
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/docs/agents.md`
- **Changes:**
  - Add documentation for 13 new commands
  - Add documentation for 6 new agents
  - Add documentation for 9 new hooks
  - Add status line documentation

#### Task 85
**[CHORE] Update tac_bootstrap_cli README.md**

- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md`
- **Changes:**
  - Add TAC-12 Multi-Agent Orchestration section
  - Add Observability features section
  - Update command reference table

#### Task 86
**[CHORE] Update root README.md with TAC-12 overview**

- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/README.md`
- **Changes:**
  - Add TAC-12 integration section
  - Document new commands and agents

#### Task 87 (OPTIONAL)
**[FEATURE] Add TAC-12 helper functions to workflow_ops.py**

- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/workflow_ops.py`
- **Changes:** Add functions:
  - scout_codebase()
  - plan_with_scouts()
  - build_in_parallel()
  - find_and_summarize()

#### Task 88 (OPTIONAL)
**[FEATURE] Add TAC-12 helper functions to workflow_ops.py.j2 template**

- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2`
- **Changes:** Mirror Task 87

#### Task 89
**[CHORE] Update CHANGELOG.md to version 0.7.0**

- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md`
- **Changes:** Add comprehensive 0.7.0 entry with:
  - 13 new commands
  - 6 new agents
  - 9 new hooks
  - Observability infrastructure
  - Status line
  - background.md and quick-plan.md improvements

---

## Execution Order Summary

### Phase 1: Base Files (33 tasks)
- Tasks 1-13: Commands (13)
- Tasks 14-19: Agents (6)
- Tasks 20-28: Hooks (9)
- Tasks 29-33: Utilities (5)
- Tasks 34-36: Status line and data dirs (3)

### Phase 2: Merge Existing (2 tasks)
- Tasks 37-38: background.md and quick-plan.md

### Phase 3: Templates for New Files (33 tasks)
- Tasks 39-51: Command templates (13)
- Tasks 52-57: Agent templates (6)
- Tasks 58-66: Hook templates (9)
- Tasks 67-71: Utility templates (5)
- Tasks 72-74: Status line and data templates (3)

### Phase 4: Templates for Merged (2 tasks)
- Tasks 75-76: background.md.j2 and quick-plan.md.j2

### Phase 5: Configuration (7 tasks)
- Tasks 77-83: data_types, settings.json, scaffold_service, agent.py

### Phase 6: Documentation (6 tasks)
- Tasks 84-89: Docs, README, CHANGELOG

**Total: 89 tasks (72 main + 2 optional)**

---

## Verification Checklist

- [ ] All 13 new commands exist in `.claude/commands/`
- [ ] All 6 new agents exist in `.claude/agents/`
- [ ] All 9 hooks exist in `.claude/hooks/`
- [ ] All 5 utilities exist in `.claude/hooks/utils/`
- [ ] Status line works
- [ ] settings.json has ALL 7 hook types configured
- [ ] background.md matches TAC-12 implementation
- [ ] quick-plan.md has scout agents
- [ ] data_types.py has all new slash commands
- [ ] agent.py has all new model mappings
- [ ] scaffold_service.py generates all new files
- [ ] CLI generation test passes: `cd tac_bootstrap_cli && uv run tac-bootstrap init test-project --dry-run`
- [ ] All tests pass: `uv run pytest`
- [ ] CHANGELOG shows version 0.7.0

---

## Parallel Execution Groups

*(Same as v1 but adjusted for new task count)*

### Phase 1: Base Files - Can run 33 tasks in 4 parallel groups

**Group P1A (13 commands):** Tasks 1-13 in parallel
**Group P1B (6 agents):** Tasks 14-19 in parallel
**Group P1C (9 hooks):** Tasks 20-28 in parallel
**Group P1D (5 utils + status + dirs):** Tasks 29-36 in parallel

### Phase 2: Merge - Can run 2 tasks in parallel

**Group P2:** Tasks 37-38 in parallel

### Phase 3: Templates - Can run 33 tasks in 4 parallel groups

**Group P3A (13 cmd templates):** Tasks 39-51 in parallel
**Group P3B (6 agent templates):** Tasks 52-57 in parallel
**Group P3C (9 hook templates):** Tasks 58-66 in parallel
**Group P3D (5 util templates):** Tasks 67-74 in parallel

### Phase 4: Template Merges - Can run 2 tasks in parallel

**Group P4:** Tasks 75-76 in parallel

### Phase 5: Configuration - Mix of parallel and sequential

**Group P5A (2 tasks):** Tasks 77-78 in parallel (data_types)
**Group P5B (2 tasks):** Tasks 79-80 in parallel (settings.json)
**Sequential:** Task 81 (scaffold_service) - depends on all previous
**Group P5C (2 tasks):** Tasks 82-83 in parallel (agent.py)

### Phase 6: Documentation - Can run in parallel

**Group P6A (3 tasks):** Tasks 84-86 in parallel (docs)
**Group P6B (2 tasks):** Tasks 87-88 in parallel (OPTIONAL)
**Sequential:** Task 89 (CHANGELOG) - FINAL

**Total minimum phases:** 10
**Total parallelizable tasks:** ~79 of 89 tasks

---

## Reference

**Original Plan:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/plan_tasks_Tac_12.md`
**Code Analysis:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/tac12_code_analysis.md`
**TAC-12 Source:** `/Volumes/MAc1/Celes/TAC/tac-12`
**Course Docs:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/Tac-12_1.md`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/Tac-12_2.md`
