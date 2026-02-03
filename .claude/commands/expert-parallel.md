---
allowed-tools:
  - Task
  - Read
  - TodoWrite
  - Write
description: "Parallel expert consensus - spawn 3-10 agents for validation"
argument-hint: "[expert_domain] [task] [num_agents]"
model: sonnet
---

# Parallel Expert Scaling - Consensus Validation

Spawn 3-10 independent expert agents to analyze the same task in parallel, then synthesize their outputs into a consensus report identifying agreement patterns, conflicts, and recommendations.

## Variables

- **EXPERT_DOMAIN**: `$1` (required) - Domain of expertise (e.g., "security", "architecture", "performance")
- **TASK**: `$2` (required) - Task description for expert analysis
- **NUM_AGENTS**: `$3` (optional, default: 3) - Number of parallel agents to spawn (range: 3-10)

## Purpose

This meta-command implements the TAC-13 "parallel expert consensus" pattern for validation and decision-making. Unlike `/parallel_subagents` which decomposes work into different subtasks, this command sends the SAME task to MULTIPLE independent experts to gather diverse perspectives and identify consensus.

**Use cases:**
- Complex architectural decisions requiring multiple viewpoints
- Security analysis where diverse threat models matter
- Performance optimization with different optimization strategies
- Design reviews where competing perspectives add value
- Risk assessment where groupthink must be avoided

## Instructions

### Phase 1: Input Validation

**Validate EXPERT_DOMAIN:**
- Check that `$1` is provided and non-empty
- If missing or empty, display error:
  ```
  ❌ Expert domain is required.

  Usage: /expert-parallel [expert_domain] [task] [num_agents]

  Example domains:
  - security: Security and vulnerability analysis
  - architecture: System design and architecture
  - performance: Performance optimization
  - devops: Infrastructure and deployment
  - testing: Test strategy and quality assurance

  Example: /expert-parallel "security" "evaluate authentication approach for API" 5
  ```
- Stop execution if validation fails

**Validate TASK:**
- Check that `$2` is provided and non-empty
- If missing or empty, display error:
  ```
  ❌ Task description is required.

  Usage: /expert-parallel [expert_domain] [task] [num_agents]

  Example: /expert-parallel "architecture" "assess microservices vs monolith" 3
  ```
- Stop execution if validation fails

**Validate NUM_AGENTS:**
- If `$3` not provided: default to 3
- If provided: validate it's an integer
- Range checking:
  - If NUM_AGENTS < 3: Display error:
    ```
    ❌ Minimum 3 agents required for meaningful consensus.

    Provided: {NUM_AGENTS}
    Valid range: 3-10
    Default: 3
    ```
  - If NUM_AGENTS > 10: Cap at 10 and display warning:
    ```
    ⚠️  Capping at 10 agents (requested: {NUM_AGENTS})

    Running 10+ agents can take significant time (30min × 10 = 5 hours compute).
    If you need more agents, consider running multiple batches.
    ```
- If not a valid integer: Display error:
  ```
  ❌ NUM_AGENTS must be a valid integer (3-10).

  Provided: {$3}
  Using default: 3
  ```
- Continue with validated NUM_AGENTS value

**If all validations pass, continue to Phase 2**

### Phase 2: Initialize and Spawn Agents

**Display start banner:**
```
🔍 Parallel Expert Consensus Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Domain: {EXPERT_DOMAIN}
Task: {TASK}
Agents: {NUM_AGENTS}
Timeout: 30 minutes per agent

Spawning {NUM_AGENTS} independent experts...
```

**Create todo list to track execution:**
```
Use TodoWrite tool to create:
- 🚀 Spawn {NUM_AGENTS} parallel expert agents
- 📊 Monitor agent execution and collect results
- 🧩 Synthesize consensus report with opus model
```

Set first todo (Spawn) to `in_progress`.

**Spawn all agents in parallel using Task tool:**

CRITICAL: Use a SINGLE message with MULTIPLE Task tool invocations (one per agent).

For each agent i from 1 to NUM_AGENTS:
```
Task:
  subagent_type: "general-purpose"
  description: "Expert {i}/{NUM_AGENTS} analysis"
  prompt: "You are Expert #{i} specializing in {EXPERT_DOMAIN}.

Your role: Provide independent expert analysis on the following task. Work completely independently without coordinating with other experts.

TASK: {TASK}

Instructions:
1. Analyze the task from your expert perspective in {EXPERT_DOMAIN}
2. Provide thorough analysis with specific recommendations
3. Consider edge cases, risks, and trade-offs
4. Structure your response with clear sections:
   - Analysis
   - Key Findings
   - Recommendations
   - Risks/Trade-offs

Be detailed and specific. Your output will be aggregated with other experts for consensus analysis."
  model: "sonnet"
```

**Important**: All Task invocations must be in a SINGLE message for parallel execution.

### Phase 3: Monitor Execution

**Mark spawn todo as completed, set monitor todo to in_progress**

**Wait for all agents to complete (blocking wait)**

The Task tool will handle the blocking wait automatically. As agents complete, optionally display progress:

```
Agent 1/{NUM_AGENTS} completed ✓
Agent 2/{NUM_AGENTS} completed ✓
Agent 3/{NUM_AGENTS} completed ✓
...
```

**Collect results:**
- Store each agent's output in a list
- Track which agents succeeded vs failed
- Count successful completions

**Error handling:**
- If 0-1 agents succeed: Display error and ABORT:
  ```
  ❌ Insufficient successful agents for consensus analysis.

  Successful: {success_count}/{NUM_AGENTS}
  Required minimum: 2

  Most agents failed. This suggests:
  - Task may be unclear or ambiguous
  - Domain may be too specialized
  - Timeout may be insufficient

  Review the task description and try again.
  ```
- If 2+ agents succeed but some failed: Continue with warning:
  ```
  ⚠️  Some agents failed, continuing with successful results

  Successful: {success_count}/{NUM_AGENTS}
  Failed: {failure_count}/{NUM_AGENTS}

  Proceeding with partial consensus analysis...
  ```
- If all agents succeed: Display success message:
  ```
  ✅ All {NUM_AGENTS} agents completed successfully!
  ```

**Mark monitor todo as completed, set synthesis todo to in_progress**

### Phase 4: Synthesis with Opus

**Display synthesis banner:**
```
🧩 Synthesizing consensus report...

Analyzing {success_count} expert outputs with claude-opus-4-5 model...
```

**Store full agent outputs in scratchpad:**
- Use Write tool to save each agent output
- File path pattern: `/private/tmp/claude/-Users-hernandoescobar-Documents-Celes-tac-bootstrap-trees-feature-Tac-13-Task-17/43266a97-fb7b-4509-a973-0ca4bafb2b43/scratchpad/expert-parallel-agent-{i}-{timestamp}.md`
- Create index file linking to all outputs

**Perform consensus analysis:**

Use Task tool to spawn an opus-powered synthesis agent:
```
Task:
  subagent_type: "general-purpose"
  description: "Synthesize expert consensus"
  prompt: "You are a meta-analyst synthesizing insights from {success_count} independent experts in {EXPERT_DOMAIN}.

Your task: Analyze the following {success_count} expert outputs and produce a structured consensus report.

EXPERT OUTPUTS:
{Include all successful agent outputs here, labeled as Expert 1, Expert 2, etc.}

Instructions:
1. Identify CONSENSUS areas where multiple experts agree (quantify: 'X/Y experts agree...')
2. Identify CONFLICTS where experts disagree (explain different perspectives)
3. Extract common THEMES and patterns across responses
4. Synthesize actionable RECOMMENDATIONS based on consensus
5. Call out DIVERGENCES explicitly with categorized viewpoints
6. Rate confidence levels: Strong (≥80% agreement), Moderate (60-79%), Weak (<60%)

Produce a detailed markdown report with these sections:
- Executive Summary
- Consensus Findings (with agreement counts)
- Conflicting Perspectives (with supporting evidence)
- Synthesized Recommendations
- Areas of Divergence
- Confidence Assessment

Be specific, quantitative, and transparent about agreement levels."
  model: "opus"
```

Wait for synthesis agent to complete.

**Mark synthesis todo as completed**

### Phase 5: Generate Final Report

**Extract synthesis output from opus agent**

**Create final report with metadata and full context:**

```markdown
# Parallel Expert Consensus Report

**Generated**: {timestamp}
**Domain**: {EXPERT_DOMAIN}
**Task**: {TASK}
**Agents**: {success_count}/{NUM_AGENTS} successful

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{Insert full synthesis output from opus agent here}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Full Expert Outputs

Individual expert analyses are available in the scratchpad directory:

{List links to all individual agent output files}

To view full outputs: `cat <file_path>`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Methodology

- **Isolation**: Each expert analyzed independently without coordination
- **Aggregation**: Opus model synthesized outputs for consensus patterns
- **Transparency**: Full individual outputs preserved for reference
- **Validation**: {success_count} independent perspectives for robustness

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Analysis completed successfully** 🎉
```

**Display report to stdout**

**Optionally save report to file:**
- File path: `.claude/reports/expert-parallel-{timestamp}.md`
- Only create if `.claude/reports/` directory exists
- If directory doesn't exist, skip file save (stdout is sufficient)

### Phase 6: Completion Message

**Display final status:**
```
✅ Parallel expert consensus completed!

Results:
- Domain: {EXPERT_DOMAIN}
- Agents: {success_count}/{NUM_AGENTS}
- Consensus patterns identified: {key count from synthesis}
- Conflicts identified: {conflict count from synthesis}

Report displayed above.

Next Steps:
- Review consensus findings and recommendations
- Consider conflicting perspectives for decision-making
- Reference full expert outputs for detailed context
- Use insights to inform architectural/security/design decisions
```

## Error Handling Strategy

**Validation failures (Phase 1):**
- Display clear error messages with usage examples
- Stop execution immediately
- Provide guidance on valid inputs

**Agent spawn failures (Phase 2):**
- Rare (Task tool handles spawning robustly)
- If Task tool fails: Display error and abort

**Agent execution failures (Phase 3):**
- Partial failure tolerance: Continue with ≥2 successful agents
- Display warnings for partial failures
- Abort only if <2 agents succeed

**Synthesis failures (Phase 4):**
- Retry synthesis once with same inputs
- If retry fails: Display error and provide direct access to agent outputs:
  ```
  ❌ Synthesis failed after retry.

  Individual expert outputs are available at:
  {List file paths}

  You can review outputs manually and synthesize consensus yourself.
  ```

## Success Criteria

Parallel expert consensus is successful if:
1. ✅ All inputs validated (domain, task, num_agents)
2. ✅ NUM_AGENTS in valid range (3-10)
3. ✅ All agents spawned in parallel (single message, multiple Task calls)
4. ✅ ≥2 agents complete successfully
5. ✅ Full agent outputs stored in scratchpad
6. ✅ Opus model performs synthesis successfully
7. ✅ Consensus report generated with required sections
8. ✅ Agreement levels quantified (X/Y experts)
9. ✅ Conflicts explicitly identified and explained
10. ✅ Report displayed with metadata and methodology

## Notes

**Key Design Principles:**
- **Complete isolation**: Agents work independently until synthesis (prevent groupthink)
- **Partial failure tolerance**: Continue with ≥2 successes
- **Opus-powered synthesis**: Use strongest model for complex aggregation
- **Transparency**: Full outputs preserved and linked
- **Quantitative**: Count agreement levels (7/10 experts agree...)

**Differences from /parallel_subagents:**
- `/parallel_subagents`: Task decomposition (different subtasks)
- `/expert-parallel`: Expert consensus (same task, multiple perspectives)
- Different use cases, complementary patterns

**Resource Considerations:**
- 30min timeout per agent (configurable in Task tool)
- 3 agents = ~1.5hr compute
- 10 agents = ~5hr compute
- Cap at 10 to balance thoroughness with practicality

**Example Domains:**
- security: Authentication, authorization, vulnerability analysis
- architecture: System design, scalability, patterns
- performance: Optimization strategies, bottleneck identification
- devops: Infrastructure, CI/CD, deployment strategies
- testing: Test strategies, coverage, quality assurance
- data: Data modeling, pipelines, governance
- frontend: UI/UX, accessibility, performance
- backend: API design, microservices, data flow

**Integration with TAC-13 Meta-Agentics:**
- Part of meta-agentic layer (agents creating agent workflows)
- Complements `/expert-orchestrate` (plan→build→improve)
- Enables validation and decision-making with diverse perspectives
- Supports high-stakes decisions requiring consensus
