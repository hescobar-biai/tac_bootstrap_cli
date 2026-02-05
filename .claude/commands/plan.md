---
allowed-tools: Read, Write, Edit, Glob, Grep, MultiEdit
description: Create implementation plans with simple file exploration workflow
model: claude-opus-4-1-20250805
---

# Simple Planning Command

Create an implementation plan using a streamlined 5-step workflow.

## Variables

issue_number: $1
adw_id: $2
issue_json: $3

## Instructions

- Create a plan to implement a feature in TAC Bootstrap CLI
- CRITICAL: Use RELATIVE path `specs/issue-{issue_number}-adw-{adw_id}-sdlc_planner-{name}.md`
- Follow existing project patterns and conventions
- Keep solutions simple - don't over-engineer

## ⚡ TOKEN OPTIMIZATION RULES (CRITICAL)

**DO NOT repeat issue body/title/description in the plan** - Reference by ID only
**Keep output under 800 tokens** - Use bullets, not prose
**Output ONLY deltas** - Don't re-explain what's already in the issue
**Use structured format** - Follow the plan template exactly, no additional sections
**Be concise** - One line per file, one line per task, short explanations

## Planning Workflow

### Step 1: Understand Requirements

Parse `issue_json` to extract:
- Issue number, title, description
- Key technical requirements
- Acceptance criteria

### Step 2: Read Relevant Files

Use Read, Glob, Grep to explore:
- Glob for file patterns (e.g., `**/*service*.py`)
- Grep for keywords, classes, functions
- Read relevant files to understand patterns

Focus on: architecture patterns, similar features, testing patterns, integration points.

### Step 3: Design Approach

Based on exploration:
- Identify files to modify/create
- Choose patterns aligned with existing code
- Plan implementation sequence

### Step 4: Write Plan

Write structured plan with:
- Metadata, Feature Description, User Story
- Problem/Solution Statement
- Relevant Files (existing + new)
- Implementation Plan (phases)
- Step by Step Tasks
- Testing Strategy
- Validation Commands

### Step 5: Save to specs/

Save to: `specs/issue-{issue_number}-adw-{adw_id}-sdlc_planner-{name}.md`

## Relevant Files

- `PLAN_TAC_BOOTSTRAP.md` - Master plan
- `CLAUDE.md` - Agent guide
- `tac_bootstrap_cli/tac_bootstrap/domain/` - Pydantic models
- `tac_bootstrap_cli/tac_bootstrap/application/` - Services
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/` - Templates
- `tac_bootstrap_cli/tac_bootstrap/interfaces/` - CLI

Read `.claude/commands/conditional_docs.md` for additional docs.

## Plan Format

```md
# Feature: <name>

## Metadata
issue_number: `{issue_number}`
adw_id: `{adw_id}`

## Feature Description
<Purpose and value>

## User Story
As a <user>, I want <action>, so that <benefit>

## Problem Statement
<Problem this addresses>

## Solution Statement
<Approach and how it solves the problem>

## Relevant Files

### Existing Files to Modify
1. **`path/to/file.py`** - Why modification needed

### New Files
2. **`path/to/new_file.py`** - Purpose

## Implementation Plan

### Phase 1: Foundation
<Foundational work>

### Phase 2: Core Implementation
<Main feature>

### Phase 3: Integration
<Integration>

## Step by Step Tasks

### Task 1: <name>
- <detail>

### Task 2: <name>
- <detail>

## Testing Strategy

### Unit Tests
<Tests needed>

### Edge Cases
<Edge cases>

## Acceptance Criteria
1. **Criterion 1** - Description

## Validation Commands
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- `cd tac_bootstrap_cli && uv run ruff check .`
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`

## Notes
<Additional context>
```

## Orchestration Patterns

Para tareas complejas multi-fase, considera usar comandos de orquestación que coordinan múltiples agentes especializados automáticamente:

- [orch_plan_w_scouts_build_review](./orch_plan_w_scouts_build_review.md) - Workflow completo: exploración → planificación → construcción → revisión
- [planner agent](./../agents/planner.md) - Agente especializado en crear planes de implementación estructurados

Usa comandos directos (como este) para tareas de fase única. Usa orquestación para workflows multi-agente coordinados.

## Report

Output ONLY the relative path to the plan file:
```
specs/issue-37-adw-e4dc9574-sdlc_planner-feature-name.md
```

No explanation, no commentary, no markdown formatting. Just the bare path.
