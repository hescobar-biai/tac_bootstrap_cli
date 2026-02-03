---
doc_type: feature
adw_id: feature_Tac_13_Task_17
date: 2026-02-03
idk:
  - parallel-agents
  - consensus-analysis
  - meta-agentic
  - expert-validation
  - opus-synthesis
  - task-spawning
tags:
  - feature
  - meta-agentic
  - tac-13
related_code:
  - .claude/commands/expert-parallel.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Parallel Expert Scaling Command

**ADW ID:** feature_Tac_13_Task_17
**Date:** 2026-02-03
**Specification:** specs/issue-579-adw-feature_Tac_13_Task_17-sdlc_planner-parallel-expert-scaling.md

## Overview

The `/expert-parallel` command implements a parallel expert consensus pattern that spawns 3-10 independent agents to analyze the same task simultaneously. Unlike task decomposition patterns, this meta-command gathers diverse perspectives from multiple experts working in complete isolation, then uses Claude Opus to synthesize their outputs into a structured consensus report with quantified agreement levels, identified conflicts, and actionable recommendations.

## What Was Built

- **Working implementation**: `.claude/commands/expert-parallel.md` - Complete slash command with 6-phase workflow
- **Jinja2 template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2` - Template for CLI-generated projects
- **Command registration**: Added "expert-parallel" to scaffold_service.py commands list
- **4-phase execution workflow**: Validation → Spawn → Monitor → Synthesis → Report → Completion
- **Partial failure tolerance**: Continues with minimum 2 successful agents
- **Opus-powered synthesis**: Uses strongest model for complex consensus analysis

## Technical Implementation

### Files Modified

- `.claude/commands/expert-parallel.md`: New working implementation (403 lines)
  - Frontmatter with allowed-tools: Task, Read, TodoWrite, Write
  - Model: sonnet (command orchestration), opus (synthesis phase)
  - 3 required variables: EXPERT_DOMAIN ($1), TASK ($2), NUM_AGENTS ($3, default: 3)

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2`: New Jinja2 template (403 lines)
  - Identical to working implementation (no project-specific variables needed)
  - Ready for CLI scaffold generation

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Registration update (+1 line)
  - Added "expert-parallel" to commands list at line 346
  - Follows established pattern after "expert-orchestrate"

### Key Changes

1. **Complete Agent Isolation Pattern**: Each agent receives identical task prompt with expert number and domain, works independently without coordination until synthesis phase to prevent groupthink.

2. **Parallel Spawning with Single Message**: Uses single message with multiple Task tool invocations (3-10 calls) for true parallel execution, not sequential spawning.

3. **Partial Failure Tolerance**: Continues execution if ≥2 agents succeed, displays warnings for partial failures, aborts only if <2 successes (insufficient for consensus).

4. **Opus Synthesis Agent**: Spawns separate general-purpose agent with opus model to aggregate outputs, quantify agreement levels (e.g., "7/10 experts agree..."), identify conflicting perspectives with evidence, and generate structured markdown report.

5. **Transparency and Traceability**: Stores full individual agent outputs in scratchpad directory, links to outputs in final report, preserves methodology section explaining isolation/aggregation approach.

## How to Use

### Basic Usage (Default 3 Agents)

```bash
/expert-parallel "security" "evaluate authentication approach for API"
```

### Custom Agent Count

```bash
/expert-parallel "architecture" "assess microservices vs monolith for this project" 5
```

### Example Domains

- **security**: Authentication, authorization, vulnerability analysis
- **architecture**: System design, scalability, patterns
- **performance**: Optimization strategies, bottleneck identification
- **devops**: Infrastructure, CI/CD, deployment strategies
- **testing**: Test strategies, coverage, quality assurance
- **data**: Data modeling, pipelines, governance
- **frontend**: UI/UX, accessibility, performance
- **backend**: API design, microservices, data flow

### Expected Output

The command generates a structured consensus report with:
- **Executive Summary**: High-level synthesis
- **Consensus Findings**: Areas of agreement with quantified support (e.g., "8/10 experts agree...")
- **Conflicting Perspectives**: Divergent viewpoints with supporting evidence
- **Synthesized Recommendations**: Actionable next steps based on consensus
- **Areas of Divergence**: Explicitly marked areas without consensus
- **Confidence Assessment**: Strong (≥80%), Moderate (60-79%), Weak (<60%)
- **Methodology**: Transparency section explaining isolation/aggregation approach
- **Full Expert Outputs**: Links to individual agent outputs in scratchpad

## Configuration

### Input Validation

- **EXPERT_DOMAIN**: Required, non-empty string
- **TASK**: Required, non-empty string
- **NUM_AGENTS**: Optional integer (3-10 range)
  - Default: 3
  - Minimum: 3 (required for meaningful consensus)
  - Maximum: 10 (capped for resource constraints: 30min × 10 = 5hrs compute)

### Agent Configuration

- **Timeout**: 30 minutes per agent (allows thorough expert-level analysis)
- **Model**: Sonnet for individual expert agents (orchestration uses sonnet, synthesis uses opus)
- **Isolation**: Complete independence until synthesis (no inter-agent communication)

### Error Handling

- **Validation failures**: Clear error messages with usage examples, immediate stop
- **Agent spawn failures**: Rare (Task tool handles robustly), displays error and aborts
- **Agent execution failures**: Partial tolerance (≥2 successes), warnings for partial failures, abort if <2
- **Synthesis failures**: Retry once, then provide direct access to agent outputs for manual synthesis

## Testing

### Verify Installation

```bash
# Check template file exists
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2 && echo "✓ Template"

# Check registration
grep "expert-parallel" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered"

# Check implementation file
test -f .claude/commands/expert-parallel.md && echo "✓ Repo file"
```

### Run Unit Tests

```bash
# Run pytest suite
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Run linting
cd tac_bootstrap_cli && uv run ruff check .

# Run type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test CLI
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Manual Testing - Valid Inputs

```bash
# Test with default (3 agents)
/expert-parallel "security" "evaluate authentication approach for API"

# Test with custom agent count
/expert-parallel "architecture" "assess microservices vs monolith for this project" 5

# Test different domains
/expert-parallel "performance" "identify optimization strategies for database queries" 4
```

### Manual Testing - Edge Cases

```bash
# Empty domain - should display error
/expert-parallel "" "test task" 3

# Empty task - should display error
/expert-parallel "domain" "" 3

# Too few agents - should display error
/expert-parallel "domain" "task" 2

# Too many agents - should cap at 10 with warning
/expert-parallel "domain" "task" 15

# Non-integer agents - should display error and use default
/expert-parallel "domain" "task" "invalid"

# Missing NUM_AGENTS - should use default (3)
/expert-parallel "security" "analyze API security"
```

## Notes

### Design Decisions

1. **Why opus for synthesis?** Aggregating 3-10 agent outputs, identifying patterns, quantifying agreement, and resolving conflicts requires the strongest reasoning capability. The cost is justified by consensus analysis quality.

2. **Why 3-10 agent range?** Minimum 3 provides basic triangulation for consensus. Maximum 10 balances resource constraints (30min × 10 = 5hrs compute) with practical ceiling for consensus analysis. More agents = diminishing returns.

3. **Why blocking monitor vs non-blocking?** Simplicity and user expectations. Non-blocking monitoring adds significant complexity (polling, state management) without clear benefit. Users expect results and can wait for completion.

4. **Why minimum 2 successes?** Single agent success provides no consensus data. Two agents enable basic agreement/disagreement analysis, though results will note limited confidence.

5. **Why 30min agent timeout?** Expert-level analysis requires thorough exploration. Shorter timeouts rush analysis; longer timeouts have diminishing returns. 30min matches typical deep-dive exploration sessions.

### Differences from /parallel_subagents

- **/parallel_subagents**: Task decomposition (different subtasks executed in parallel)
- **/expert-parallel**: Expert consensus (same task analyzed by multiple independent experts)
- Different use cases, complementary patterns in meta-agentic toolkit

### TAC-13 Meta-Agentics Context

This is Task 17 of the TAC-13 meta-agentics implementation. It builds on:
- Tasks 1-12: Expert frameworks (question, self-improve, expertise.yaml)
- Task 13: Meta-prompt generator (`/meta-prompt`)
- Task 14: Meta-agent generator (`/meta-agent`)
- Task 16: Expert orchestrator (`/expert-orchestrate` - plan→build→improve)
- Task 17: **Parallel expert scaling** (`/expert-parallel` - this feature)

The complete meta-agentic layer enables: prompts that create prompts, agents that create agents, orchestrators that manage workflows, and consensus mechanisms that validate decisions through diverse expert perspectives.

### Future Enhancements (Out of Scope)

- Resume capability for partial failures (YAGNI for initial version)
- Dynamic timeout adjustment based on task complexity
- Agent diversity enforcement (different models, different prompting strategies)
- Consensus confidence scoring algorithm
- Integration with /expert-orchestrate for full plan→build→validate workflow

### Resource Considerations

- **3 agents**: ~1.5hr compute time
- **5 agents**: ~2.5hr compute time
- **10 agents**: ~5hr compute time
- Cap at 10 balances thoroughness with practicality
- Synthesis with opus adds ~5-10min for complex aggregation

### Integration Patterns

Can be combined with other meta-commands:
1. Use `/expert-orchestrate` to plan→build→improve a feature
2. Use `/expert-parallel` to validate architectural decisions during planning
3. Use `/scout` to explore codebase before expert analysis
4. Use `/review` to validate implementation quality with expert consensus
