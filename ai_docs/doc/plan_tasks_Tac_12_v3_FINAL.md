# TAC-12 Integration Task Plan v3 (FINAL)

**Version Target:** 0.7.0
**Date:** 2026-01-29
**Based On:** Real TAC-12 code analysis from `/Volumes/MAc1/Celes/TAC/tac-12`
**Total Tasks:** 89

**IMPORTANT:**
- Each file is created/modified TWICE: once in base project, once in CLI templates
- Each task includes workflow metadata for ADW execution
- scaffold_service.py is updated for each new file added

---

## Wave 1 - New Commands to Base Repository (13 tasks)

### 1.1 Command Files

#### Task 1
**[CHORE] Create all_tools.md command file**

/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_12_task_1

- **Description:** Create a new slash command that lists all available tools for the agent.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/all_tools.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/all_tools.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` commands list
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

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_2

- **Description:** Create a slash command for parallel build operations using build-agent subagents. Based on real TAC-12 implementation with detailed file specifications.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/build_in_parallel.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_in_parallel.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` commands list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/build_in_parallel.md`
- **Key Features:**
  - Uses `.claude/agents/build-agent.md` subagent
  - Model: claude-sonnet-4-5-20250929
  - 8-step workflow with detailed file specifications
  - Parallel batch execution pattern
  - Comprehensive reporting format

#### Task 3
**[FEATURE] Create build.md command file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_3

- **Description:** Create a simple sequential build command that implements a plan top-to-bottom without parallelization.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/build.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` commands list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/build.md`
- **Key Features:**
  - Simple sequential implementation
  - Reads plan from PATH_TO_PLAN
  - Ultrathink and implement
  - Validation with git diff --stat

#### Task 4
**[FEATURE] Create find_and_summarize.md command file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_4

- **Description:** Create a command that searches for files and generates AI summaries.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/find_and_summarize.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/find_and_summarize.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` commands list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/find_and_summarize.md`
- **Key Features:**
  - allowed-tools: Glob, Grep, Read
  - File discovery with patterns
  - AI-powered summarization

#### Task 5
**[FEATURE] Create plan_w_docs.md command file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_5

- **Description:** Create a planning command that explores documentation before creating plans.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/plan_w_docs.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_docs.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` commands list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan_w_docs.md`
- **Key Features:**
  - allowed-tools: Task, Read, Glob, Grep, WebFetch
  - Documentation exploration with subagents
  - Enhanced planning with doc context

#### Task 6
**[FEATURE] Create plan_w_scouters.md command file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_6

- **Description:** Create a planning command that uses scout subagents for codebase exploration.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/plan_w_scouters.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` commands list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan_w_scouters.md`
- **Key Features:**
  - Multiple parallel scout agents
  - Both base and fast scouts
  - Comprehensive codebase analysis

#### Task 7
**[FEATURE] Create plan.md command file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_7

- **Description:** Create a simple planning command without scout agents. SIMPLER than plan_w_scouters.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/plan.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` commands list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan.md`
- **Key Features:**
  - Model: claude-opus-4-1-20250805
  - allowed-tools: Read, Write, Edit, Glob, Grep, MultiEdit
  - Simple 5-step workflow (no scouts)
  - Saves to specs/ directory

#### Task 8
**[FEATURE] Create prime_3.md command file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_8

- **Description:** Create a deep priming command with 3 levels of exploration.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/prime_3.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_3.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` commands list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/prime_3.md`
- **Key Features:**
  - 3-level deep context loading
  - Comprehensive codebase understanding

#### Task 9
**[FEATURE] Create scout_plan_build.md command file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_9

- **Description:** Create an end-to-end workflow command: scout -> plan -> build.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/scout_plan_build.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout_plan_build.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` commands list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/scout_plan_build.md`
- **Key Features:**
  - Complete implementation pipeline
  - Orchestrates multiple phases

#### Task 10
**[FEATURE] Create load_ai_docs.md command file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_10

- **Description:** Create a command that loads AI documentation files into context.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/load_ai_docs.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` commands list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/load_ai_docs.md`
- **Key Features:**
  - Loads documentation from ai_docs/ or similar
  - Context preparation for planning
  - allowed-tools: Read, Glob, Grep

#### Task 11
**[FEATURE] Create load_bundle.md command file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_11

- **Description:** Create a command that loads context bundles (pre-packaged file sets).
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/load_bundle.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` commands list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/load_bundle.md`
- **Key Features:**
  - Pre-packaged context loading
  - Bundle definitions
  - allowed-tools: Read, Glob

#### Task 12
**[FEATURE] Create parallel_subagents.md command file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_12

- **Description:** Create a command that orchestrates multiple subagents in parallel for divide-and-conquer tasks.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/parallel_subagents.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` commands list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/parallel_subagents.md`
- **Key Features:**
  - Multi-agent orchestration
  - Parallel execution pattern
  - Task delegation
  - allowed-tools: Task

#### Task 13
**[FEATURE] Create prime_cc.md command file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_13

- **Description:** Create a specialized prime command for Claude Code codebase understanding.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/prime_cc.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` commands list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/prime_cc.md`
- **Key Features:**
  - Specialized for Claude Code projects
  - Deep understanding of CC patterns

---

## Wave 2 - New Agents to Base Repository (6 tasks)

#### Task 14
**[FEATURE] Create build-agent.md agent definition**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_14

- **Description:** Create a specialized agent for implementing individual files in parallel builds.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/build-agent.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/build-agent.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` agents list and ensure `.claude/agents/` directory is created
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

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_15

- **Description:** Create an agent for browser automation and E2E validation.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/playwright-validator.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/playwright-validator.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` agents list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/playwright-validator.md`
- **Key Features:**
  - Browser automation with Playwright
  - E2E test execution
  - UI validation

#### Task 16
**[FEATURE] Create scout-report-suggest.md agent definition**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_16

- **Description:** Create a full scout agent for codebase exploration with detailed reports.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/scout-report-suggest.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` agents list
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

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_17

- **Description:** Create a fast scout agent optimized for quick exploration.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/scout-report-suggest-fast.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest-fast.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` agents list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/scout-report-suggest-fast.md`
- **Key Features:**
  - Optimized for speed
  - model: haiku (faster)
  - Similar structure to scout-report-suggest

#### Task 18
**[FEATURE] Create docs-scraper.md agent definition**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_18

- **Description:** Create a specialized agent for scraping and extracting documentation from web sources.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/docs-scraper.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` agents list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/docs-scraper.md`
- **Key Features:**
  - Web documentation scraping
  - Content extraction
  - tools: WebFetch, WebSearch, Read, Write

#### Task 19
**[FEATURE] Create meta-agent.md agent definition**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_19

- **Description:** Create a meta-agent that generates OTHER agents based on specifications.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/meta-agent.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2`
- **Scaffold Update:** Add to `scaffold_service.py` agents list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/meta-agent.md`
- **Key Features:**
  - Agent generation
  - Template-based agent creation
  - tools: Read, Write, Edit, Glob, Grep

---

## Wave 3 - New Hooks to Base Repository (9 tasks)

#### Task 20
**[FEATURE] Create send_event.py hook file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_20

- **Description:** Create the observability hook that sends events to server.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/send_event.py`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/send_event.py.j2`
- **Scaffold Update:** Add to `scaffold_service.py` hooks list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/send_event.py`
- **Key Features:**
  - HTTP POST to observability endpoint
  - Arguments: --source-app, --event-type, --server-url, --add-chat, --summarize
  - Integrates with summarizer.py and model_extractor.py
  - Always exits with 0 (non-blocking)

#### Task 21
**[FEATURE] Create session_start.py hook file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_21

- **Description:** Create the SessionStart hook for initializing session context.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/session_start.py`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/session_start.py.j2`
- **Scaffold Update:** Add to `scaffold_service.py` hooks list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/session_start.py`
- **Key Features:**
  - Captures git branch, model, project metadata
  - Writes to session storage

#### Task 22
**[FEATURE] Create pre_tool_use.py hook file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_22

- **Description:** Create a hook that runs BEFORE every tool use.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/pre_tool_use.py`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_tool_use.py.j2`
- **Scaffold Update:** Add to `scaffold_service.py` hooks list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/pre_tool_use.py`
- **Key Features:**
  - Pre-tool use logging
  - Integration point for observability
  - Called before every tool invocation

#### Task 23
**[FEATURE] Create post_tool_use.py hook file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_23

- **Description:** Create a hook that runs AFTER every tool use.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/post_tool_use.py`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/post_tool_use.py.j2`
- **Scaffold Update:** Add to `scaffold_service.py` hooks list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/post_tool_use.py`
- **Key Features:**
  - Post-tool use logging
  - Result capture
  - Performance tracking

#### Task 24
**[FEATURE] Create notification.py hook file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_24

- **Description:** Create a hook for system notifications.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/notification.py`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/notification.py.j2`
- **Scaffold Update:** Add to `scaffold_service.py` hooks list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/notification.py`
- **Key Features:**
  - System notification handling
  - Event logging

#### Task 25
**[FEATURE] Create stop.py hook file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_25

- **Description:** Create a hook that runs when the session stops.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/stop.py`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/stop.py.j2`
- **Scaffold Update:** Add to `scaffold_service.py` hooks list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/stop.py`
- **Key Features:**
  - Session cleanup
  - Final logging
  - Chat transcript capture

#### Task 26
**[FEATURE] Create subagent_stop.py hook file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_26

- **Description:** Create a hook that runs when a subagent stops.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/subagent_stop.py`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/subagent_stop.py.j2`
- **Scaffold Update:** Add to `scaffold_service.py` hooks list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/subagent_stop.py`
- **Key Features:**
  - Subagent lifecycle tracking
  - Result aggregation

#### Task 27
**[FEATURE] Create pre_compact.py hook file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_27

- **Description:** Create a hook that runs before context compaction.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/pre_compact.py`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_compact.py.j2`
- **Scaffold Update:** Add to `scaffold_service.py` hooks list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/pre_compact.py`
- **Key Features:**
  - Pre-compaction logging
  - Context size tracking

#### Task 28
**[FEATURE] Create user_prompt_submit.py hook file**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_28

- **Description:** Create a hook that runs when user submits a prompt.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/user_prompt_submit.py`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/user_prompt_submit.py.j2`
- **Scaffold Update:** Add to `scaffold_service.py` hooks list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/user_prompt_submit.py`
- **Key Features:**
  - Prompt logging
  - Flags: --log-only, --store-last-prompt, --name-agent
  - User interaction tracking

---

## Wave 4 - New Hook Utilities to Base Repository (5 tasks)

#### Task 29
**[FEATURE] Create summarizer.py hook utility**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_29

- **Description:** Create a utility that generates AI summaries using haiku model.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/summarizer.py`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/summarizer.py.j2`
- **Scaffold Update:** Add to `scaffold_service.py` hook utilities list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/summarizer.py`
- **Key Features:**
  - generate_event_summary() function
  - Uses claude-haiku-4-5-20251001
  - Concise one-sentence summaries
  - Graceful error handling

#### Task 30
**[FEATURE] Create model_extractor.py hook utility**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_30

- **Description:** Create a utility that extracts model name from transcripts with caching.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/model_extractor.py`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/model_extractor.py.j2`
- **Scaffold Update:** Add to `scaffold_service.py` hook utilities list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/model_extractor.py`
- **Key Features:**
  - get_model_from_transcript() function
  - Cache in .claude/data/claude-model-cache/
  - Parses JSONL transcript files

#### Task 31
**[FEATURE] Create constants.py hook utility**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_31

- **Description:** Create a utility with shared constants for hooks.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/constants.py`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2`
- **Scaffold Update:** Add to `scaffold_service.py` hook utilities list
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/constants.py`
- **Key Features:**
  - Shared constant definitions
  - API endpoints
  - Default values

#### Task 32
**[FEATURE] Create llm/ utilities subdirectory**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_32

- **Description:** Create LLM-related utilities for hooks.
- **Base Directory:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/llm/`
- **Template Directory:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/`
- **Scaffold Update:** Add directory creation and files to `scaffold_service.py`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/llm/`
- **Key Features:**
  - LLM helper functions
  - API wrappers
  - (Read TAC-12 contents for specifics)

#### Task 33
**[FEATURE] Create tts/ utilities subdirectory**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_33

- **Description:** Create text-to-speech utilities for hooks.
- **Base Directory:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/tts/`
- **Template Directory:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/`
- **Scaffold Update:** Add directory creation and files to `scaffold_service.py`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/tts/`
- **Key Features:**
  - TTS integration
  - Audio notification support
  - (Read TAC-12 contents for specifics)

---

## Wave 5 - Status Line and Data Directories (3 tasks)

#### Task 34
**[FEATURE] Create status_lines directory and status_line_main.py**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_34

- **Description:** Create the dynamic status line script.
- **Base Files:**
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/status_lines/` (directory)
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/status_lines/status_line_main.py`
- **Template Files:**
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/status_lines/` (directory)
  - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/status_lines/status_line_main.py.j2`
- **Scaffold Update:** Add directory creation and status line file to `scaffold_service.py`
- **Content:** Python script that outputs formatted status line with agent name, model, git branch

#### Task 35
**[CHORE] Create .claude/data/sessions directory with .gitkeep**

/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_12_task_35

- **Description:** Create directory for session data.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/data/sessions/.gitkeep`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/sessions/.gitkeep.j2`
- **Scaffold Update:** Add directory creation to `scaffold_service.py`
- **Note:** Verify if needed based on TAC-12 actual usage

#### Task 36
**[CHORE] Create .claude/data/claude-model-cache directory with .gitkeep**

/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_12_task_36

- **Description:** Create directory for model info cache.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/data/claude-model-cache/.gitkeep`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/claude-model-cache/.gitkeep.j2`
- **Scaffold Update:** Add directory creation to `scaffold_service.py`
- **Note:** Used by model_extractor.py for caching

---

## Wave 6 - Robustify Existing Commands (2 tasks)

#### Task 37
**[FEATURE] Update background.md with TAC-12 improvements**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_37

- **Description:** Update background.md command with COMPLETE TAC-12 implementation.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/background.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2`
- **Scaffold Update:** File already in scaffold, verify content matches
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/background.md`
- **Key Changes:**
  - Variables: USER_PROMPT ($1), MODEL ($2, defaults 'sonnet'), REPORT_FILE ($3)
  - Uses `claude` CLI directly with --dangerously-skip-permissions
  - Structured report format in append-system-prompt
  - Auto-rename to .complete.md or .failed.md
  - Timestamp captured ONCE: `TIMESTAMP=$(date +%a_%H_%M_%S)`
  - Directory: `agents/background/`

#### Task 38
**[FEATURE] Update quick-plan.md with TAC-12 improvements**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_38

- **Description:** Update quick-plan.md command with COMPLETE TAC-12 implementation including scouts.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/quick-plan.md`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2`
- **Scaffold Update:** File already in scaffold, verify content matches
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan_w_scouters.md` (Note: TAC-12 quick-plan is SIMPLER)
- **Key Changes:**
  - Variables: TOTAL_BASE_SCOUT_SUBAGENTS: 3, TOTAL_FAST_SCOUT_SUBAGENTS: 5
  - Workflow Step 2: Deploy 3 base scouts + 5 fast scouts in PARALLEL
  - Task type: chore|feature|refactor|fix|enhancement
  - Complexity: simple|medium|complex
  - Conditional Plan Format sections

---

## Wave 7 - Configuration Updates (7 tasks)

#### Task 39
**[CHORE] Add new slash commands to data_types.py SlashCommand Literal**

/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_12_task_39

- **Description:** Update the SlashCommand Literal type to include all new TAC-12 commands.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/data_types.py`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2`
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

#### Task 40
**[CHORE] Add statusLine and ALL hooks to .claude/settings.json**

/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_12_task_40

- **Description:** Add statusLine configuration and ALL 7 hook types to settings.json.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/settings.json`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2`
- **Reference:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/settings.json`
- **Key Changes:**
  - Add statusLine configuration
  - Add PreToolUse hooks (pre_tool_use.py + send_event.py)
  - Add PostToolUse hooks (post_tool_use.py + send_event.py)
  - Add Notification hooks (notification.py + send_event.py)
  - Add Stop hooks (stop.py + send_event.py with --add-chat)
  - Add SubagentStop hooks (subagent_stop.py + send_event.py)
  - Add PreCompact hooks (send_event.py only)
  - Add UserPromptSubmit hooks (user_prompt_submit.py with flags + send_event.py)

#### Task 41
**[CHORE] Update scaffold_service.py with new TAC-12 files**

/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_12_task_41

- **Description:** Update scaffold service to include ALL new TAC-12 files in generation.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- **Changes:**
  - Add `.claude/agents/` directory creation
  - Add `.claude/status_lines/` directory creation
  - Add `.claude/data/sessions/` directory creation
  - Add `.claude/data/claude-model-cache/` directory creation
  - Add `.claude/hooks/utils/llm/` directory creation
  - Add `.claude/hooks/utils/tts/` directory creation
  - Add 13 new commands (Tasks 1-13)
  - Add 6 new agents (Tasks 14-19)
  - Add 9 new hooks (Tasks 20-28)
  - Add 5 new hook utilities (Tasks 29-33)
  - Add status line file
  - Add data directory .gitkeep files

#### Task 42
**[CHORE] Add new commands to SLASH_COMMAND_MODEL_MAP in agent.py**

/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_12_task_42

- **Description:** Add model mappings for all new TAC-12 commands.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/agent.py`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2`
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

---

## Wave 8 - Documentation (6 tasks)

#### Task 43
**[CHORE] Update CLI commands documentation**

/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_12_task_43

- **Description:** Update CLI commands documentation with all new TAC-12 commands.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/docs/commands.md`
- **Changes:**
  - Add documentation for 13 new commands
  - Include usage examples
  - Document allowed-tools and models

#### Task 44
**[CHORE] Update CLI agents documentation**

/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_12_task_44

- **Description:** Update CLI agents documentation with all new TAC-12 agents.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/docs/agents.md`
- **Changes:**
  - Add documentation for 6 new agents
  - Include agent capabilities
  - Document tools and models

#### Task 45
**[CHORE] Update CLI hooks documentation**

/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_12_task_45

- **Description:** Update CLI hooks documentation with all new TAC-12 hooks.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/docs/hooks.md`
- **Changes:**
  - Add documentation for 9 new hooks
  - Add documentation for 5 new utilities
  - Document observability infrastructure
  - Add status line documentation

#### Task 46
**[CHORE] Update tac_bootstrap_cli README.md**

/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_12_task_46

- **Description:** Update CLI README with TAC-12 features overview.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md`
- **Changes:**
  - Add TAC-12 Multi-Agent Orchestration section
  - Add Observability features section
  - Update command reference table

#### Task 47
**[CHORE] Update root README.md with TAC-12 overview**

/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_12_task_47

- **Description:** Update main repository README with TAC-12 features.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/README.md`
- **Changes:**
  - Add TAC-12 integration section
  - Document new commands and agents

#### Task 48
**[CHORE] Update CHANGELOG.md to version 0.7.0**

/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_12_task_48

- **Description:** Add comprehensive changelog entry for version 0.7.0.
- **File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md`
- **Changes:** Add complete 0.7.0 entry documenting:
  - 13 new commands with descriptions
  - 6 new agents with descriptions
  - 9 new hooks with descriptions
  - 5 new utilities
  - Observability infrastructure
  - Status line
  - background.md and quick-plan.md improvements
  - Technical implementation details

---

## Wave 9 - Optional Enhancements (2 tasks)

#### Task 49 (OPTIONAL)
**[FEATURE] Add TAC-12 helper functions to workflow_ops.py**

/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_12_task_49

- **Description:** Add optional helper functions for using new TAC-12 commands from ADW workflows.
- **Base File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/workflow_ops.py`
- **Template File:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2`
- **Changes:** Add functions:
  - scout_codebase() - Wrapper for /scout
  - plan_with_scouts() - Wrapper for /plan_w_scouters
  - build_in_parallel() - Wrapper for /build_in_parallel
  - find_and_summarize() - Wrapper for /find_and_summarize

---

## Execution Summary

### Total Tasks: 49 (47 main + 2 optional)

### File Creation Pattern:
Each task creates TWO files:
1. **Base file** in project root (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`)
2. **Template file** in CLI templates (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`)
3. **Scaffold update** in `scaffold_service.py` to include the file in generation

### Parallel Execution Groups:

**Wave 1: Commands (13 parallel)**
- Tasks 1-13 can run in parallel

**Wave 2: Agents (6 parallel)**
- Tasks 14-19 can run in parallel

**Wave 3: Hooks (9 parallel)**
- Tasks 20-28 can run in parallel

**Wave 4: Utilities (5 parallel)**
- Tasks 29-33 can run in parallel

**Wave 5: Status & Dirs (3 parallel)**
- Tasks 34-36 can run in parallel

**Wave 6: Updates (2 parallel)**
- Tasks 37-38 can run in parallel

**Wave 7: Config (sequential)**
- Tasks 39-42 (Task 41 depends on all previous, others can be parallel)

**Wave 8: Docs (6 parallel)**
- Tasks 43-48 can run in parallel (except 48 should be last)

**Wave 9: Optional (2 parallel)**
- Tasks 49 (optional)

### Minimum Phases: 9 waves
### Parallelizable Tasks: ~43 of 49 tasks

---

## Verification Checklist

After implementation, verify:

- [ ] All 13 new commands exist in `.claude/commands/` and templates
- [ ] All 6 new agents exist in `.claude/agents/` and templates
- [ ] All 9 hooks exist in `.claude/hooks/` and templates
- [ ] All 5 utilities exist in `.claude/hooks/utils/` and templates
- [ ] Status line script exists and works
- [ ] settings.json has ALL 7 hook types configured
- [ ] background.md matches TAC-12 implementation
- [ ] quick-plan.md has scout agents configuration
- [ ] data_types.py has all 15 new slash commands
- [ ] agent.py has all 13 new model mappings
- [ ] scaffold_service.py generates all new files correctly
- [ ] CLI generation test passes: `cd tac_bootstrap_cli && uv run tac-bootstrap init test-project --dry-run`
- [ ] All tests pass: `uv run pytest`
- [ ] CHANGELOG shows version 0.7.0 with complete details
- [ ] All documentation updated

---

## Reference Files

**Original Plan v1:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/plan_tasks_Tac_12.md`
**Code Analysis:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/tac12_code_analysis.md`
**Plan v2:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/plan_tasks_Tac_12_v2_UPDATED.md`
**This Plan (v3):** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/plan_tasks_Tac_12_v3_FINAL.md`

**TAC-12 Source:** `/Volumes/MAc1/Celes/TAC/tac-12`
**Course Docs:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/Tac-12_1.md`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/Tac-12_2.md`
