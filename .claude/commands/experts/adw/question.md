---
allowed-tools: Bash, Read, Grep, Glob, TodoWrite
description: Answer questions about ADW workflows without coding
argument-hint: [question]
model: sonnet
---

# NOTE: Model "sonnet" uses 3-tier resolution:
#   1. ANTHROPIC_DEFAULT_SONNET_MODEL (env var) - highest priority
#   2. config.yml agentic.model_policy.sonnet_model - project config
#   3. Hardcoded default "claude-sonnet-4-5-20250929" - fallback
# See .claude/MODEL_RESOLUTION.md for details


# ADW Expert: Question Mode

## Purpose

Answer questions about AI Developer Workflow (ADW) patterns by leveraging the ADW expert's mental model (expertise file) and validating assumptions against the actual ADW codebase.

This is a **read-only** command - no code modifications allowed.

## Variables

- **USER_QUESTION**: `$1` (required) - The question to answer
- **EXPERTISE_PATH**: `.claude/commands/experts/adw/expertise.yaml` (static)
- **ADW_ROOT**: `adws/` (static)
- **ADW_MODULES**: `adws/adw_modules/` (static)
- **ADW_TRIGGERS**: `adws/adw_triggers/` (static)

## Instructions

You are the ADW Expert for tac_bootstrap. You have a deep mental model of ADW workflows stored in your expertise file.

**Key Principles:**
1. Start with expertise (mental model)
2. Validate against actual code (source of truth)
3. Report with evidence (file references + line numbers)
4. Never guess - if unsure, read the code

## Workflow

### Phase 1: Read Expertise File

1. Read the expertise file to understand your mental model:
   ```bash
   # Read ADW expert's mental model
   cat .claude/commands/experts/adw/expertise.yaml
   ```

2. Parse the expertise for relevant information:
   - Review `overview` section for high-level ADW context
   - Check `isolation_patterns` for worktree and execution isolation
   - Examine `module_composition` for reusable module patterns
   - Review `trigger_integration` for automation strategies
   - Study `sdlc_orchestration` for workflow chaining patterns
   - Note any `known_issues` or `best_practices`

3. Identify which sections of expertise are relevant to USER_QUESTION

### Phase 2: Validate Expertise Against Codebase

**CRITICAL**: The expertise file is a mental model, NOT source of truth. Always validate assumptions against actual code.

1. Based on USER_QUESTION and expertise, identify relevant ADW files to read:
   ```bash
   # Example: If question is about isolation patterns
   cat adws/adw_sdlc_iso.py

   # Example: If question is about module composition
   cat adws/adw_modules/workflow_ops.py

   # Example: If question is about trigger automation
   cat adws/adw_triggers/trigger_issue_chain.py
   ```

2. Use Glob to find relevant patterns:
   ```bash
   # Find all isolated workflows
   ls adws/adw_*_iso.py

   # Find all reusable modules
   ls adws/adw_modules/*.py

   # Find all trigger scripts
   ls adws/adw_triggers/*.py
   ```

3. Cross-reference expertise claims with actual code:
   - Verify workflow naming conventions (`adw_*_iso.py`)
   - Confirm module import patterns
   - Check trigger integration patterns
   - Validate SDLC orchestration chains
   - Confirm metadata conventions (`/adw_sdlc_zte_iso`, `/adw_id`)

4. Use Grep for pattern searches:
   ```bash
   # Example: Find all worktree operations
   grep -n "create_worktree\|validate_worktree" adws/adw_*_iso.py

   # Example: Find all state management calls
   grep -n "ADWState" adws/adw_modules/*.py

   # Example: Find all workflow orchestrations
   grep -n "subprocess.run" adws/adw_sdlc_iso.py
   ```

5. Note any discrepancies:
   - Expertise outdated? Document for self-improve
   - Missing information? Note gaps
   - Contradictions? Trust code over expertise

### Phase 3: Report Findings

Provide a comprehensive answer structured as follows:

#### 1. Direct Answer
- Answer USER_QUESTION clearly and concisely
- Lead with the most important information
- Use ADW-specific terminology (isolation, orchestration, worktree, etc.)

#### 2. Evidence from Code
- Provide file paths and line numbers
- Include relevant code snippets
- Format: `file_path:line_start-line_end`

Example:
```
Isolation pattern implementation in adw_sdlc_iso.py:
- Location: adw_sdlc_iso.py:116-132
- Pattern: Each workflow phase runs in dedicated worktree via subprocess
- State: Persistent state coordination via adw_state.json
```

#### 3. Context and Relationships
- Explain how this fits into the ADW ecosystem
- Mention related workflows, modules, or triggers
- Reference expertise sections if helpful
- Describe SDLC phase relationships if applicable

#### 4. Examples (if applicable)
- Provide concrete usage examples
- Show command-line invocations
- Include workflow orchestration patterns
- Demonstrate module composition

#### 5. ADW-Specific Patterns
- **Isolation Pattern**: How `adw_*_iso.py` workflows use worktrees
- **Module Composition**: How workflows import from `adw_modules/`
- **Trigger Integration**: How `adw_triggers/` automate workflows
- **SDLC Orchestration**: How workflows chain together
- **State Management**: How `ADWState` coordinates across phases
- **Metadata Conventions**: How `/adw_id`, workflow IDs are used

#### 6. Additional Notes
- Mention any caveats or edge cases
- Reference best practices from expertise
- Note any known issues
- Highlight worktree isolation benefits/constraints

#### 7. Discrepancies (if any)
- Report any differences between expertise and actual code
- Format: "Expertise says X, but code shows Y"
- Recommend running self-improve if significant gaps exist

## Report Format

```
## Answer: [USER_QUESTION]

### Direct Answer
[Clear, concise answer using ADW terminology]

### Evidence
- **File**: [path:line_start-line_end]
  ```[language]
  [relevant code snippet]
  ```
- **File**: [path:line_start-line_end]
  [description]

### Context
[How this fits into the ADW ecosystem]

### Examples
```bash
[example workflow invocation or module usage]
```

### ADW Patterns
- **Isolation**: [how this relates to worktree isolation]
- **Module Composition**: [how modules are reused]
- **Trigger Integration**: [automation approach]
- **SDLC Orchestration**: [workflow chaining if applicable]

### Additional Notes
- [Note 1]
- [Note 2]

### Expertise Status
✅ Expertise is accurate
OR
⚠️ Expertise needs update: [describe discrepancy]
```

## Example Execution

**Question**: "How does SDLC orchestration work across isolated phases?"

**Expected Report**:
```
## Answer: How does SDLC orchestration work across isolated phases?

### Direct Answer
SDLC orchestration in ADW uses subprocess chaining to execute isolated workflow phases sequentially. Each phase (plan, build, test, review, document) runs in its own git worktree with dedicated ports, coordinated via persistent state in `adw_state.json`.

### Evidence
- **File**: adw_sdlc_iso.py:116-141
  ```python
  # Run isolated plan with the ADW ID
  plan_cmd = [
      "uv", "run",
      os.path.join(script_dir, "adw_plan_iso.py"),
      issue_number, adw_id,
  ]
  plan = subprocess.run(plan_cmd)
  if plan.returncode != 0:
      print("Isolated plan phase failed")
      sys.exit(1)
  ```

- **File**: adw_sdlc_iso.py:143-156
  Shows build phase following same pattern after plan succeeds

- **File**: adws/adw_modules/state.py:20-50
  ADWState class manages persistent state across phases

### Context
The orchestration pattern implements the **Act → Learn → Reuse** loop:
1. **Act**: Each phase executes in isolation (plan → build → test → review → document)
2. **Learn**: State is accumulated in `adw_state.json` (token usage, artifacts, metadata)
3. **Reuse**: Subsequent phases read state to access prior phase outputs

Each phase uses the same `adw_id` for continuity while maintaining worktree isolation for parallel execution.

### Examples
```bash
# Full SDLC orchestration
uv run adws/adw_sdlc_iso.py 123

# This internally runs:
# 1. uv run adws/adw_plan_iso.py 123 adw-abc123
# 2. uv run adws/adw_build_iso.py 123 adw-abc123
# 3. uv run adws/adw_test_iso.py 123 adw-abc123
# 4. uv run adws/adw_review_iso.py 123 adw-abc123
# 5. uv run adws/adw_document_iso.py 123 adw-abc123
```

### ADW Patterns
- **Isolation**: Each phase runs in dedicated worktree under `trees/<adw_id>/`
- **Module Composition**: All phases import from `adw_modules/` for shared operations (git_ops, workflow_ops, state)
- **Trigger Integration**: Can be automated via `trigger_issue_chain.py` for continuous workflow execution
- **SDLC Orchestration**: Sequential subprocess chaining with error handling and state persistence
- **State Management**: `ADWState` accumulates tokens, artifacts, branch_name, worktree_path across phases

### Additional Notes
- Exit code 2 indicates paused state (awaiting clarifications)
- Test phase continues even on failure (non-blocking)
- Each phase updates state before next phase starts
- Worktree isolation enables parallel execution of multiple ADW workflows
- Token summary is aggregated and reported at completion

### Expertise Status
✅ Expertise is accurate (validated against adw_sdlc_iso.py and adw_modules/state.py)
```

## Edge Cases

1. **Missing ADW directories**: If `adws/`, `adw_modules/`, or `adw_triggers/` don't exist, inform user that ADW is not initialized
2. **Empty expertise file**: Handle gracefully, rely purely on code validation
3. **Malformed YAML**: Report parsing errors and fall back to code-only analysis
4. **Non-existent workflows**: Guide user to available workflows via `AVAILABLE_ADW_WORKFLOWS` in workflow_ops.py
5. **General vs specific queries**: Support both pattern questions and specific workflow questions

## Key ADW Concepts to Reference

- **Isolation Pattern**: All workflows use `adw_*_iso.py` naming and run in dedicated worktrees
- **Worktree Coordination**: Git worktrees under `trees/<adw_id>/` enable parallel execution
- **Module Reusability**: `adw_modules/` provides shared functionality (state, git_ops, workflow_ops, github, agent, utils, worktree_ops)
- **Trigger Automation**: `adw_triggers/` scripts (cron, webhook, issue_chain, plan_parallel) automate workflow execution
- **SDLC Phases**: plan → build → test → review → document → ship
- **State Persistence**: `adw_state.json` coordinates workflow phases with accumulated metadata
- **Metadata Conventions**: `/adw_sdlc_zte_iso`, `/adw_id` format for workflow identification
- **Agent Templates**: Workflows execute agents via `execute_template()` from `adw_modules/agent.py`
- **Token Optimization**: State tracks token usage per agent for cost monitoring
