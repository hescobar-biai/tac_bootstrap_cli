---
doc_type: feature
adw_id: chore_Tac_13_Task_24
date: 2026-02-04
idk:
  - agent-experts
  - self-improving-agents
  - expertise-files
  - meta-agentic
  - act-learn-reuse
  - domain-specialization
  - progressive-disclosure
tags:
  - feature
  - documentation
  - tac-13
related_code:
  - tac_bootstrap_cli/README.md
  - .claude/commands/experts/cli/question.md
  - .claude/commands/experts/cli/self-improve.md
  - .claude/commands/expert-orchestrate.md
  - .claude/commands/expert-parallel.md
---

# Agent Experts (TAC-13) Documentation

**ADW ID:** chore_Tac_13_Task_24
**Date:** 2026-02-04
**Specification:** specs/issue-586-adw-chore_Tac_13_Task_24-chore_planner-update-cli-readme-tac13.md

## Overview

This chore adds comprehensive documentation for the TAC-13 Agent Experts feature to the CLI README. The documentation explains self-improving agent experts that follow an Act → Learn → Reuse loop, maintaining domain-specific knowledge in YAML-based expertise files that evolve with the codebase.

## What Was Built

- New TAC-13 section in `tac_bootstrap_cli/README.md` (62 lines added)
- Comprehensive explanation of agent experts concept and self-improvement loop
- Decision criteria for when to use experts vs generic agents
- Four concrete usage examples with copy-pasteable bash commands
- Expert domains comparison table covering CLI, ADW, and Commands domains
- Meta-agentic capabilities documentation (meta-prompt, meta-agent)
- Integration notes connecting TAC-13 with TAC-9 and TAC-12 features
- Progressive disclosure learning path for users

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/README.md`: Added 62-line TAC-13 Agent Experts section between existing TAC-9 (line ~389) and TAC-12 (line 390) sections

### Key Changes

- **Expertise Files Concept**: Introduced YAML-based mental models that persist domain knowledge and evolve through self-improvement cycles
- **Act → Learn → Reuse Loop**: Documented the core pattern where experts act on tasks, learn from validation, and reuse accumulated knowledge
- **Specialization vs Generalization**: Clear decision criteria explaining when domain experts outperform generic agents
- **Usage Examples**: Four progressive commands from basic queries (`/experts:cli:question`) to advanced orchestration (`/expert-parallel`)
- **Expert Domains Table**: Structured comparison of three expert types (CLI, ADW, Commands) with their coverage areas and available commands
- **Meta-Agentic Tools**: Documentation for `/meta-prompt` and `/meta-agent` commands enabling system extensibility
- **Integration Mapping**: Connected TAC-13 to TAC-9 (documentation loading) and TAC-12 (orchestration) for cohesive feature ecosystem

## How to Use

### Query an Expert

Ask domain-specific questions to specialized experts:

```bash
/experts:cli:question "How does template registration work?"
```

### Self-Improve Expert Knowledge

Update expert expertise after making code changes:

```bash
/experts:cli:self-improve true
```

### Orchestrate Expert Workflow

Run full plan → build → improve cycle with an expert:

```bash
/expert-orchestrate cli "Add new template for hooks"
```

### Scale Experts in Parallel

Run multiple expert instances for high-confidence validation:

```bash
/expert-parallel cli "Review scaffold service logic" 5
```

## Configuration

No additional configuration required. Expert commands are available after TAC-13 implementation. Expert domains included:

- **cli**: tac-bootstrap CLI, templates, scaffold service
- **adw**: AI Developer Workflows, state management (optional)
- **commands**: Slash command structure, variables (optional)

## Testing

Verify README structure and integrity:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Check linting for documentation quality:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Smoke test CLI functionality:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Validate markdown table rendering:

```bash
cat tac_bootstrap_cli/README.md | grep -A 5 "Agent Experts (TAC-13)"
```

## Notes

**Design Decisions:**
- Section placed between TAC-9 and TAC-12 to maintain chronological TAC feature ordering
- Progressive disclosure pattern: basic queries → orchestration → parallel scaling → meta-agentic extension
- Expertise files described as "mental models" to clarify their role as accumulated knowledge bases
- Meta-agentic capabilities positioned as advanced extensibility layer

**Integration Points:**
- TAC-9 (Intelligent Documentation Loading): Expertise files are specialized documentation for experts
- TAC-12 (Multi-Agent Orchestration): Expert agents can be orchestrated for complex multi-phase workflows
- Future TAC features can reference this section for expert-aware implementations

**Content Strategy:**
- Keep explanations concise (2-3 sentences per concept) for readability
- Prioritize actionable examples over theoretical explanations
- Use exact command syntax that exists in `.claude/commands/experts/`
- Maintain consistency with existing TAC-9 and TAC-12 documentation style

**Quality Considerations:**
- All usage examples are copy-pasteable without modification
- Markdown table properly formatted with aligned columns
- Code blocks use bash syntax highlighting
- No broken links or references
- Style matches surrounding README sections
