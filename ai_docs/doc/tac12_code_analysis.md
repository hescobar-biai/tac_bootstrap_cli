# TAC-12 Code Analysis: Real Implementation vs Current Plan

**Date:** 2026-01-29
**Source:** `/Volumes/MAc1/Celes/TAC/tac-12`
**Target:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap`

## Executive Summary

El plan actual (`plan_tasks_Tac_12.md`) se basó en la documentación del curso TAC-12, pero NO en el código real implementado. Este análisis compara el código real del TAC-12 con nuestro proyecto base para identificar:

1. **Comandos faltantes**
2. **Mejoras en comandos existentes**
3. **Agentes adicionales**
4. **Hooks y utilities completos**
5. **Configuración de settings.json**

---

## 1. Comandos en TAC-12 Real

### Comandos que TAC-12 tiene (19 comandos):

```
1. all_tools.md              ✅ En plan (Task 1)
2. background.md             ⚠️  Tenemos pero necesita mejoras (Task 21)
3. build_in_parallel.md      ✅ En plan (Task 2)
4. build.md                  ⚠️  Tenemos versión básica (Task 3)
5. find_and_summarize.md     ✅ En plan (Task 4)
6. load_ai_docs.md           ❌ NO en plan - FALTA
7. load_bundle.md            ❌ NO en plan - FALTA
8. parallel_subagents.md     ❌ NO en plan - FALTA
9. plan_w_docs.md            ✅ En plan (Task 5)
10. plan_w_scouters.md       ✅ En plan (Task 6)
11. plan.md                  ✅ En plan (Task 7) - Pero código real es DIFERENTE
12. prime_3.md               ✅ En plan (Task 8)
13. prime_cc.md              ❌ NO en plan - FALTA
14. prime.md                 ✅ Ya lo tenemos
15. question.md              ✅ Ya lo tenemos
16. quick-plan.md            ⚠️  Tenemos pero necesita mejoras (Task 22)
17. scout_plan_build.md      ✅ En plan (Task 9)
18. scout.md                 ✅ Ya lo tenemos
19. (otros comandos nuestros no están en TAC-12)
```

### Comandos que FALTAN en el plan actual:

#### NEW Task: Create load_ai_docs.md
- **File:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/load_ai_docs.md`
- **Purpose:** Loads AI documentation files into context for planning
- **Tools:** Read, Glob, Grep

#### NEW Task: Create load_bundle.md
- **File:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/load_bundle.md`
- **Purpose:** Loads context bundles (pre-packaged sets of files) into context
- **Tools:** Read, Glob

#### NEW Task: Create parallel_subagents.md
- **File:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/parallel_subagents.md`
- **Purpose:** Orchestrates multiple subagents in parallel for divide-and-conquer tasks
- **Tools:** Task

#### NEW Task: Create prime_cc.md
- **File:** `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/prime_cc.md`
- **Purpose:** Prime specifically for Claude Code codebase understanding
- **Tools:** Read, Glob, Grep

---

## 2. Agentes en TAC-12 Real

### Agentes que TAC-12 tiene (6 agentes):

```
1. build-agent.md                ✅ En plan (Task 10)
2. docs-scraper.md               ❌ NO en plan - FALTA
3. meta-agent.md                 ❌ NO en plan - FALTA
4. playwright-validator.md       ✅ En plan (Task 11)
5. scout-report-suggest-fast.md  ✅ En plan (Task 13)
6. scout-report-suggest.md       ✅ En plan (Task 12)
```

### Agentes que FALTAN en el plan actual:

#### NEW Task: Create docs-scraper.md agent
- **Purpose:** Specialized agent for scraping and extracting documentation from web sources
- **Tools:** WebFetch, WebSearch, Read, Write

#### NEW Task: Create meta-agent.md agent
- **Purpose:** Meta-agent that creates OTHER agents based on specifications
- **Tools:** Read, Write, Edit, Glob, Grep

---

## 3. Hooks en TAC-12 Real

### Hooks que TAC-12 tiene (10 hooks):

```
1. notification.py          ❌ NO en plan - FALTA
2. post_tool_use.py         ❌ NO en plan - FALTA
3. pre_compact.py           ❌ NO en plan - FALTA
4. pre_tool_use.py          ❌ NO en plan - FALTA
5. send_event.py            ✅ En plan (Task 14)
6. session_start.py         ✅ En plan (Task 15)
7. stop.py                  ❌ NO en plan - FALTA
8. subagent_stop.py         ❌ NO en plan - FALTA
9. user_prompt_submit.py    ❌ NO en plan - FALTA
```

### Hook Utils que TAC-12 tiene (5+ utilities):

```
hooks/utils/
├── constants.py              ❌ NO en plan - FALTA
├── llm/                      ❌ NO en plan - FALTA (subdirectory)
├── model_extractor.py        ✅ En plan (Task 17)
├── summarizer.py             ✅ En plan (Task 16)
└── tts/                      ❌ NO en plan - FALTA (subdirectory)
```

### Hooks que FALTAN en el plan actual:

#### NEW Task: Create pre_tool_use.py hook
- **Purpose:** Hook that runs BEFORE every tool use
- **Integration:** Calls send_event.py with --event-type PreToolUse

#### NEW Task: Create post_tool_use.py hook
- **Purpose:** Hook that runs AFTER every tool use
- **Integration:** Calls send_event.py with --event-type PostToolUse

#### NEW Task: Create notification.py hook
- **Purpose:** Hook for system notifications
- **Integration:** Calls send_event.py with --event-type Notification

#### NEW Task: Create stop.py hook
- **Purpose:** Hook that runs when session stops
- **Integration:** Calls send_event.py with --event-type Stop --add-chat

#### NEW Task: Create subagent_stop.py hook
- **Purpose:** Hook that runs when a subagent stops
- **Integration:** Calls send_event.py with --event-type SubagentStop

#### NEW Task: Create pre_compact.py hook
- **Purpose:** Hook that runs before context compaction
- **Integration:** Calls send_event.py with --event-type PreCompact

#### NEW Task: Create user_prompt_submit.py hook
- **Purpose:** Hook that runs when user submits a prompt
- **Flags:** `--log-only --store-last-prompt --name-agent`
- **Integration:** Calls send_event.py with --event-type UserPromptSubmit

#### NEW Task: Create constants.py utility
- **Purpose:** Shared constants for hooks

#### NEW Task: Create llm/ utilities subdirectory
- **Purpose:** LLM-related utilities for hooks

#### NEW Task: Create tts/ utilities subdirectory
- **Purpose:** Text-to-speech utilities for hooks

---

## 4. Settings.json Configuration

### TAC-12 Real settings.json estructura:

```json
{
  "statusLine": {
    "type": "command",
    "command": "uv run $CLAUDE_PROJECT_DIR/.claude/status_lines/status_line_main.py",
    "padding": 0
  },
  "hooks": {
    "PreToolUse": [...],      // ✅ En plan pero incompleto
    "PostToolUse": [...],      // ✅ En plan pero incompleto
    "Notification": [...],     // ❌ NO en plan - FALTA
    "Stop": [...],            // ❌ NO en plan - FALTA
    "SubagentStop": [...],    // ❌ NO en plan - FALTA
    "PreCompact": [...],      // ❌ NO en plan - FALTA
    "UserPromptSubmit": [...] // ❌ NO en plan - FALTA
  }
}
```

**IMPORTANTE:** Cada hook event type tiene DOS hooks:
1. El hook específico (e.g., `pre_tool_use.py`)
2. El hook de observability (`send_event.py` con --summarize)

---

## 5. Mejoras en Comandos Existentes

### background.md Improvements (Task 21)

**Current Plan:** Menciona mejoras pero sin detalles completos

**Real TAC-12 Implementation:**
```markdown
- Uses `claude` CLI directly with --dangerously-skip-permissions
- Structured report format with sections:
  - Task Understanding
  - Progress (updated continuously)
  - Results
  - Task Completed / Task Failed
- Auto-rename to .complete.md or .failed.md
- Timestamp captured ONCE for consistency
- Directory structure: agents/background/
- append-system-prompt with full workflow instructions
```

**Key Code Pattern:**
```bash
claude \
  --model "${MODEL}" \
  --output-format text \
  --dangerously-skip-permissions \
  --append-system-prompt "..." \
  --print "${USER_PROMPT}"
```

### quick-plan.md Improvements (Task 22)

**Current Plan:** Tiene mejoras pero falta detalle de scouts

**Real TAC-12 Implementation:**
```markdown
Variables:
- TOTAL_BASE_SCOUT_SUBAGENTS: 3
- TOTAL_FAST_SCOUT_SUBAGENTS: 5

Workflow Step 2 (Explore Codebase):
1. Run 3 @agent-scout-report-suggest in parallel
2. Run 5 @agent-scout-report-suggest-fast in parallel
3. Consolidate results
4. MANUAL validation of files needed

Plan Format:
- Conditional sections based on task_type and complexity
- Problem Statement (if feature or medium/complex)
- Solution Approach (if feature or medium/complex)
- Implementation Phases (if medium/complex)
- Testing Strategy (if feature or medium/complex)
```

### plan.md Real Implementation

**Real TAC-12 `/plan.md`:**
```markdown
---
description: Creates a concise engineering implementation plan based on user requirements and saves it to specs directory
argument-hint: [user prompt]
model: claude-opus-4-1-20250805
---

# Quick Plan

Variables:
- USER_PROMPT: $ARGUMENTS
- PLAN_OUTPUT_DIRECTORY: specs/

Workflow:
1. Analyze Requirements - THINK HARD
2. Design Solution - Technical approach
3. Document Plan - Comprehensive markdown
4. Generate Filename - Kebab-case
5. Save & Report - Write to specs/
```

**DIFERENCIA:** El `/plan.md` del TAC-12 es SIMPLE (sin scouts), mientras que `/quick-plan.md` usa scouts.

---

## 6. Build Commands Analysis

### build.md Real Implementation

**Real TAC-12 `/build.md`:**
```markdown
---
description: Build the codebase based on the plan
argument-hint: [path-to-plan]
---

Variables:
- PATH_TO_PLAN: $ARGUMENTS

Workflow:
- Read plan at PATH_TO_PLAN
- Ultrathink and IMPLEMENT top to bottom
- Complete every step before stopping
- Validate work with validation commands

Report:
- Summarize work in bullet points
- git diff --stat
```

**IMPORTANTE:** Simple, secuencial, NO usa subagents.

### build_in_parallel.md Real Implementation

**Real TAC-12 `/build_in_parallel.md`:**
```markdown
---
model: claude-sonnet-4-5-20250929
description: Build the codebase in parallel by delegating to build-agents
---

Uses: .claude/agents/build-agent.md

Workflow:
1. Read and Analyze Plan
2. Gather Context for Specs
3. Create Detailed File Specs (with full template)
4. Identify Parallel vs Sequential Work (Batches)
5. Launch Build Agents in Parallel (single message, multiple Task calls)
6. Monitor and Collect Results
7. Handle Issues
8. Final Verification

Key Pattern:
- One file per build-agent
- Comprehensive specs with:
  - Purpose, Requirements, Related Files
  - Code Style & Patterns, Dependencies
  - Example Code, Integration Points
  - Verification steps
```

**IMPORTANTE:** Usa multi-agent orchestration pattern con build-agent specialized subagents.

---

## 7. Other Directories

### TAC-12 tiene:

```
.claude/
├── agents/
├── commands/
├── hooks/
│   └── utils/
│       ├── llm/
│       └── tts/
├── output-styles/      ❌ NO en plan - FALTA
├── settings.json
├── skills/             ❌ NO en plan - FALTA
└── status_lines/
```

### output-styles/ Directory

**Purpose:** Custom output styles for Claude Code responses

**Contents:** (need to explore further)

### skills/ Directory

**Purpose:** Custom skills (similar to commands but different mechanism)

**Contents:** (need to explore further)

---

## 8. Data Directories

**Current Plan:**
- Task 19: .claude/data/sessions/
- Task 20: .claude/data/claude-model-cache/

**TAC-12 Real:**
- ❌ NO tiene `.claude/data/` directory visible
- Session data y cache probablemente se manejan diferente

**ACTION:** Verificar si realmente necesitamos estos directorios o si TAC-12 usa otro enfoque.

---

## 9. Agents Detailed Analysis

### build-agent.md

**Key Features:**
- Specialist for ONE file implementation
- Requires verbose, detailed specs
- Production-quality code with error handling
- Type annotations and comprehensive docs
- Verification with tests/linters
- Structured report format

**Workflow:**
1. Read & analyze spec
2. Gather context from referenced files
3. Understand codebase conventions
4. Implement file
5. Verify implementation
6. Report completion

### scout-report-suggest.md

**Key Features:**
- READ-ONLY analysis
- Identifies exact locations (file paths + line numbers)
- Root cause analysis
- Structured SCOUT REPORT format

**Report Sections:**
- Problem Statement
- Search Scope & Files Analyzed
- Executive Summary
- Findings (with file paths and line numbers)
- Detailed Analysis (with code snippets)
- Suggested Resolution (step-by-step)
- Additional Context

---

## 10. Summary of Missing Items

### Commands (4 missing):
1. load_ai_docs.md
2. load_bundle.md
3. parallel_subagents.md
4. prime_cc.md

### Agents (2 missing):
1. docs-scraper.md
2. meta-agent.md

### Hooks (7 missing):
1. pre_tool_use.py
2. post_tool_use.py
3. notification.py
4. stop.py
5. subagent_stop.py
6. pre_compact.py
7. user_prompt_submit.py

### Hook Utils (3+ missing):
1. constants.py
2. llm/ subdirectory
3. tts/ subdirectory

### Directories (2 missing):
1. output-styles/
2. skills/

### Settings.json (5 hook types missing):
1. Notification hooks
2. Stop hooks
3. SubagentStop hooks
4. PreCompact hooks
5. UserPromptSubmit hooks

---

## 11. Recommendations

### Priority 1 (Critical for TAC-12 Integration):
1. ✅ Add missing commands (load_ai_docs, load_bundle, parallel_subagents, prime_cc)
2. ✅ Add missing hooks (all 7 hooks for full observability)
3. ✅ Update settings.json with ALL hook types
4. ✅ Improve background.md and quick-plan.md with real implementations

### Priority 2 (Important for Completeness):
1. ✅ Add missing agents (docs-scraper, meta-agent)
2. ✅ Add missing hook utilities (constants, llm/, tts/)
3. ✅ Create templates for all new files

### Priority 3 (Future Enhancement):
1. ⚠️  Explore output-styles/ directory
2. ⚠️  Explore skills/ directory
3. ⚠️  Verify data directories approach

---

## 12. Action Plan

### Update Existing Plan (plan_tasks_Tac_12.md):

1. **Wave 1 - Add 4 new command tasks:**
   - Task 1a: Create load_ai_docs.md
   - Task 1b: Create load_bundle.md
   - Task 1c: Create parallel_subagents.md
   - Task 1d: Create prime_cc.md

2. **Wave 1 - Add 2 new agent tasks:**
   - Task 10a: Create docs-scraper.md
   - Task 10b: Create meta-agent.md

3. **Wave 1 - Add 7 new hook tasks:**
   - Task 14a: Create pre_tool_use.py
   - Task 14b: Create post_tool_use.py
   - Task 14c: Create notification.py
   - Task 14d: Create stop.py
   - Task 14e: Create subagent_stop.py
   - Task 14f: Create pre_compact.py
   - Task 14g: Create user_prompt_submit.py

4. **Wave 1 - Add 3 new utility tasks:**
   - Task 17a: Create constants.py
   - Task 17b: Create llm/ subdirectory with utilities
   - Task 17c: Create tts/ subdirectory with utilities

5. **Wave 2 - Update Task 21 (background.md) with complete implementation details**

6. **Wave 2 - Update Task 22 (quick-plan.md) with scout details**

7. **Wave 3 - Add templates for all new files**

8. **Wave 5 - Update Task 46-47 (settings.json) with ALL 7 hook types**

---

## Conclusion

El plan actual es un buen punto de partida, pero necesita **16+ tareas adicionales** para reflejar completamente el código real del TAC-12. Las diferencias principales son:

1. **Comandos faltantes:** 4 comandos adicionales
2. **Agentes faltantes:** 2 agentes adicionales
3. **Hooks faltantes:** 7 hooks adicionales para observabilidad completa
4. **Utils faltantes:** 3+ utilities adicionales
5. **Settings.json incompleto:** Falta configuración de 5 tipos de hooks
6. **Detalles de implementación:** Los comandos existentes necesitan actualizaciones con patrones del código real

**Total nuevo de tareas:** ~72 tareas (56 originales + 16 nuevas)
