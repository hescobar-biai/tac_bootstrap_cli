---
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, TodoWrite
description: Self-improve ADW expertise by validating against codebase
argument-hint: [check_git_diff] [focus_area]
model: sonnet
---

# NOTE: Model "sonnet" uses 3-tier resolution:
#   1. ANTHROPIC_DEFAULT_SONNET_MODEL (env var) - highest priority
#   2. config.yml agentic.model_policy.sonnet_model - project config
#   3. Hardcoded default "claude-sonnet-4-5-20250929" - fallback
# See .claude/MODEL_RESOLUTION.md for details


# ADW Expert: Self-Improve Mode

## Purpose

Maintain and update the ADW expert's mental model (expertise.yaml) by validating it against the actual codebase and incorporating new knowledge.

This is the **Learn** step in the Act → Learn → Reuse loop.

## Variables

- **CHECK_GIT_DIFF**: `$1` (default: `false`) - If `true`, focus on recently changed files
- **FOCUS_AREA**: `$2` (default: empty) - Optional area to focus on (e.g., "state_management", "github_integration", "workflow_orchestration", "worktree_operations")
- **SUMMARY_MODE**: `$3` (default: `true`) - If `true`, use summarized diffs and selective file reading for token optimization
- **EXPERTISE_FILE**: `.claude/commands/experts/adw/expertise.yaml` (static)
- **ADW_ROOT**: `adws/` (static)
- **ADW_MODULES**: `adws/adw_modules/` (static)
- **MAX_LINES**: `1000` (static)

## Instructions

You are the ADW Expert updating your mental model. Follow the 7-phase workflow strictly:

1. **Check git diff** (if requested)
2. **Read current expertise**
3. **Validate against codebase**
4. **Identify discrepancies**
5. **Update expertise**
6. **Enforce line limit**
7. **Validate YAML syntax**

**Key Principles:**
- Expertise is a mental model, NOT source of truth
- Focus on patterns and high-value knowledge
- Keep under 1000 lines (compress if needed)
- Always validate YAML syntax before finishing

## Workflow

### Phase 1: Check Git Diff (Conditional)

**Execute only if CHECK_GIT_DIFF is `true`**

#### Summary Mode (SUMMARY_MODE = true)

Use compact diff summaries to minimize token usage:

1. Get summary of changes:
   ```bash
   # High-level stats only
   git diff --stat HEAD -- adws/

   # Just list changed files
   git diff --name-status HEAD -- adws/
   ```

2. Identify changed files and focus areas:
   ```bash
   # List only filenames
   changed_files=$(git diff --name-only HEAD -- adws/)
   echo "$changed_files"
   ```

3. For critical changes, get focused diffs:
   ```bash
   # Only if state.py changed - get function-level diff
   if echo "$changed_files" | grep -q "state.py"; then
       git diff HEAD -- adws/adw_modules/state.py | grep -A 3 -B 3 "^def "
   fi

   # Only if workflow_ops.py changed
   if echo "$changed_files" | grep -q "workflow_ops.py"; then
       git diff HEAD -- adws/adw_modules/workflow_ops.py | grep -A 3 -B 3 "^def "
   fi
   ```

4. Note focus areas based on changed files:
   - If `adw_modules/state.py` changed → focus on state management
   - If `adw_modules/github.py` or `git_ops.py` changed → focus on GitHub integration
   - If `adw_modules/workflow_ops.py` changed → focus on workflow orchestration
   - If `adw_modules/worktree_ops.py` changed → focus on worktree operations
   - If `adw_*_iso.py` changed → focus on isolation patterns

5. Update FOCUS_AREA internally based on findings

**Token Impact:** ~5K tokens instead of 500K-1M tokens

#### Full Mode (SUMMARY_MODE = false)

Use complete diffs for comprehensive validation:

1. Run git diff to see recent changes:
   ```bash
   # Check unstaged changes
   git diff HEAD -- adws/

   # Check staged changes
   git diff --cached -- adws/

   # Check last commit
   git log -1 --stat --oneline -- adws/
   ```

2. Identify changed files in ADW domain:
   ```bash
   # List changed files
   git diff --name-only HEAD -- adws/
   ```

3. Note focus areas based on changes (same as summary mode)

4. Update FOCUS_AREA internally based on findings

**Token Impact:** 500K-1M tokens (original behavior)

**If CHECK_GIT_DIFF is `false`**: Skip to Phase 2

### Phase 2: Read Current Expertise

1. Read the existing expertise file:
   ```bash
   cat .claude/commands/experts/adw/expertise.yaml
   ```

2. Parse the structure:
   - Note `last_updated` date
   - Review all `isolation_patterns` components
   - Check `module_composition` patterns
   - Review `trigger_integration` workflows
   - Examine `sdlc_orchestration` chains
   - Review `recent_changes` entries

3. Identify sections to validate:
   - If FOCUS_AREA is set: prioritize that section
   - Otherwise: validate all sections systematically

4. Track current line count:
   ```bash
   wc -l .claude/commands/experts/adw/expertise.yaml
   ```

### Phase 3: Validate Expertise Against Codebase

**Systematic validation of expertise claims**

#### Summary Mode Validation (SUMMARY_MODE = true)

**Focus on changed files only** - don't re-validate entire codebase:

1. If `CHECK_GIT_DIFF=true` and `changed_files` exists, validate only changed files:
   ```bash
   # Read ONLY files that changed (use grep to extract relevant sections)
   for file in $changed_files; do
       echo "=== Validating $file ==="
       # Extract only class and function definitions
       grep -n "^class\|^def " "$file"
   done
   ```

2. Validate expertise claims about changed files:
   ```bash
   # Check if line numbers shifted
   # Verify function signatures match
   # Update descriptions if logic changed

   # Example: If state.py changed
   if echo "$changed_files" | grep -q "state.py"; then
       # Check class exists
       grep -n "class ADWState" adws/adw_modules/state.py

       # Verify key methods
       grep -n "def load\|def save\|def update" adws/adw_modules/state.py
   fi
   ```

3. Skip files that didn't change (trust existing expertise)

4. Quick discovery scan for new files only:
   ```bash
   # Find any new workflows
   find adws -name "adw_*_iso.py" | grep -v __pycache__

   # Find any new modules
   find adws/adw_modules -name "*.py" | grep -v __pycache__
   ```

**Token Impact:** ~50K tokens (only changed files)

#### Full Mode Validation (SUMMARY_MODE = false)

**Comprehensive validation** - re-verify entire codebase:

1. **Validate Overview Section**:
   ```bash
   # Check if key_files exist and are current
   for file in $(grep -A 10 "key_files:" .claude/commands/experts/adw/expertise.yaml | grep "- " | sed 's/.*- "\(.*\)"/\1/'); do
       test -f "$file" && echo "✓ $file" || echo "✗ MISSING: $file"
   done
   ```

2. **Validate Isolation Patterns**:
   ```bash
   # For each isolated workflow in isolation_patterns
   # Example: Validate adw_sdlc_iso.py

   # Read the actual file
   cat adws/adw_sdlc_iso.py

   # Check if documented workflow exists
   grep -n "def main" adws/adw_sdlc_iso.py

   # Verify worktree isolation patterns
   grep -n "create_worktree\|validate_worktree" adws/adw_sdlc_iso.py

   # Check subprocess orchestration
   grep -n "subprocess.run" adws/adw_sdlc_iso.py
   ```

3. **Validate Module Composition**:
   ```bash
   # Verify ADW modules described in expertise
   # Example: State management module

   # Read state.py
   cat adws/adw_modules/state.py

   # Check class exists
   grep -n "class ADWState" adws/adw_modules/state.py

   # Verify key methods
   grep -n "def load\|def save\|def update" adws/adw_modules/state.py

   # Example: GitHub integration module
   cat adws/adw_modules/github.py

   # Check authentication patterns
   grep -n "GITHUB_TOKEN\|get_issue\|create_pr" adws/adw_modules/github.py
   ```

4. **Validate Workflow Orchestration**:
   ```bash
   # Verify workflow orchestration patterns
   # Example: SDLC phase chaining

   # Find phase execution patterns
   grep -n "plan_cmd\|build_cmd\|test_cmd" adws/adw_sdlc_iso.py

   # Verify error handling
   grep -A 3 "returncode" adws/adw_sdlc_iso.py

   # Check state coordination
   grep -n "ADWState" adws/adw_*_iso.py
   ```

5. **Discover New Information**:
   ```bash
   # Find workflows not yet documented
   find adws -name "adw_*_iso.py" | grep -v __pycache__

   # Check for new modules
   find adws/adw_modules -name "*.py" | grep -v __pycache__

   # Find new important functions
   grep -rn "^def " adws/adw_modules/
   grep -rn "^class " adws/adw_modules/
   ```

6. **Check for Architectural Changes**:
   - New isolated workflows?
   - New ADW modules?
   - Changed orchestration patterns?
   - New trigger integrations?
   - Updated state management patterns?

**Token Impact:** 300-500K tokens (full file reads)

### Phase 4: Identify Discrepancies

**Document ALL differences between expertise and reality**

Create a discrepancies report:

```markdown
## Discrepancies Found

### Outdated Information
- [ ] Expertise says: "X is at line 100"
      Reality: X is at line 120 (moved due to new imports)

- [ ] Expertise documents: old_workflow()
      Reality: old_workflow() was renamed to new_workflow()

### Missing Information
- [ ] New workflow added: `adws/adw_new_iso.py`
      Not documented in expertise

- [ ] New module added: `adw_modules/new_module.py`
      Should be documented in module_composition

### Incorrect Information
- [ ] Expertise: "Orchestration uses pattern X"
      Reality: Pattern changed to Y in recent refactor

### Gaps in Coverage
- [ ] No documentation for: `adw_modules/worktree_ops.py`
- [ ] Missing workflow: "How worktree cleanup works"
```

### Phase 5: Update Expertise File

**Apply updates based on discrepancies**

1. **Update Overview** (if needed):
   ```yaml
   overview:
     description: "Updated description if ADW system changed"
     key_files:
       - "add new important ADW files"
       - "remove obsolete files"
     last_updated: "2026-02-03"  # Always update date
   ```

2. **Update Isolation Patterns**:
   ```yaml
   isolation_patterns:
     adw_sdlc_iso:
       location: "adws/adw_sdlc_iso.py"
       key_operations:
         - name: "main"
           line_start: 50  # Update if moved
           line_end: 200
           logic: "Orchestrates SDLC phases in isolated worktrees"
         - name: "run_plan_phase"
           line_start: 116
           line_end: 141
           logic: "Executes plan phase via subprocess in dedicated worktree"
   ```

3. **Update Module Composition**:
   ```yaml
   module_composition:
     state_management:
       location: "adws/adw_modules/state.py"
       class: "ADWState"
       key_methods:
         - name: "load"
           line_start: 30
           signature: "@classmethod def load(cls, adw_id: str) -> ADWState"
           logic: "Loads persistent state from adw_state.json"
         - name: "save"
           line_start: 50
           signature: "def save(self) -> None"
           logic: "Persists state to adw_state.json"
   ```

4. **Update Workflow Orchestration**:
   ```yaml
   sdlc_orchestration:
     phase_chaining:
       pattern: |
         1. SDLC orchestrator (adw_sdlc_iso.py) runs
         2. Each phase (plan, build, test, review, document) executes via subprocess
         3. Phases run in isolated worktrees (trees/<adw_id>/)
         4. State coordinated via ADWState (adw_state.json)
         5. Error handling: exit code 0=success, 1=failure, 2=paused
       files:
         - "adws/adw_sdlc_iso.py:116-200"
         - "adws/adw_modules/state.py:20-100"
   ```

5. **Add Recent Changes**:
   ```yaml
   recent_changes:
     - date: "2026-02-03"
       description: "Added new worktree cleanup automation"
       files: ["adw_modules/worktree_ops.py", "adw_triggers/cleanup_worktrees.py"]
     - date: "2026-02-01"
       description: "Updated GitHub integration with better error handling"
       files: ["adw_modules/github.py"]
     # Keep only 5 most recent entries
   ```

6. **Use Edit tool for updates**:
   ```bash
   # Update specific sections using Edit tool
   # Example: Update line numbers for a method
   ```

7. **Or use Write tool for major changes**:
   ```bash
   # If expertise needs significant restructuring, rewrite entire file
   ```

### Phase 6: Enforce Line Limit

**Ensure expertise stays under 1000 lines**

1. Check current line count:
   ```bash
   wc -l .claude/commands/experts/adw/expertise.yaml
   ```

2. **If under 1000 lines**: Proceed to Phase 7

3. **If over 1000 lines**: Compress using these strategies:

   **Strategy 1: Remove Old Recent Changes**
   ```yaml
   recent_changes:
     # Keep only 3-5 most recent, remove older ones
     - date: "2026-02-03"
       description: "Latest change"
   ```

   **Strategy 2: Consolidate Similar Patterns**
   ```yaml
   # Before (verbose):
   isolation_patterns:
     adw_plan_iso:
       location: "adws/adw_plan_iso.py"
       logic: "Runs plan phase in isolation"
     adw_build_iso:
       location: "adws/adw_build_iso.py"
       logic: "Runs build phase in isolation"

   # After (consolidated):
   isolation_patterns:
     phase_workflows:
       pattern: "All SDLC phases follow isolation pattern"
       instances: ["plan:adws/adw_plan_iso.py", "build:adws/adw_build_iso.py"]
       logic: "Each phase runs in dedicated worktree via subprocess"
   ```

   **Strategy 3: Use Line Ranges Instead of Details**
   ```yaml
   # Before:
   key_methods:
     - name: "method_1"
       line_start: 10
       line_end: 20
     - name: "method_2"
       line_start: 25
       line_end: 35

   # After:
   key_methods_range:
     lines: "10-35"
     count: 2
     purpose: "State management helper methods"
   ```

   **Strategy 4: Remove Obvious Information**
   ```yaml
   # Remove patterns that are self-evident from code
   # Keep only non-obvious ADW knowledge and relationships
   # Focus on: state coordination, worktree isolation, orchestration patterns
   ```

4. After compression, verify:
   ```bash
   wc -l .claude/commands/experts/adw/expertise.yaml
   # Must be <= 1000
   ```

### Phase 7: Validate YAML Syntax

**Final validation before finishing**

1. Validate YAML syntax:
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('.claude/commands/experts/adw/expertise.yaml'))"
   ```

2. **If validation passes**:
   ```
   ✓ YAML syntax is valid
   ```

3. **If validation fails**:
   - Read error message
   - Fix syntax errors (indentation, quotes, colons)
   - Re-run validation
   - Repeat until valid

4. Verify structure:
   ```bash
   # Check required top-level keys exist
   grep -E "^(overview|isolation_patterns|module_composition|sdlc_orchestration):" .claude/commands/experts/adw/expertise.yaml
   ```

5. Final checks:
   ```bash
   # Line count
   lines=$(wc -l < .claude/commands/experts/adw/expertise.yaml)
   echo "✓ Line count: $lines / 1000"

   # YAML valid
   python3 -c "import yaml; yaml.safe_load(open('.claude/commands/experts/adw/expertise.yaml'))" && echo "✓ Valid YAML"

   # Required keys present
   grep -q "^overview:" .claude/commands/experts/adw/expertise.yaml && echo "✓ Has overview"
   grep -q "^isolation_patterns:" .claude/commands/experts/adw/expertise.yaml && echo "✓ Has isolation_patterns"
   grep -q "^module_composition:" .claude/commands/experts/adw/expertise.yaml && echo "✓ Has module_composition"
   ```

## Report Format

Provide a detailed report of the self-improve run:

```markdown
# ADW Expert Self-Improve Report

## Execution Summary
- **Date**: 2026-02-03
- **Check Git Diff**: [true/false]
- **Focus Area**: [area or "full validation"]
- **Duration**: [X] phases completed

## Phase 1: Git Diff Analysis
[If CHECK_GIT_DIFF was true]
- Changed files: [list]
- Focus areas identified: [areas]

## Phase 2: Current Expertise Review
- Last updated: [date from expertise]
- Line count: [X] / 1000
- Sections reviewed: [list]

## Phase 3: Validation Results
- Workflows validated: [count]
- Modules verified: [count]
- Patterns checked: [count]

## Phase 4: Discrepancies Found
### Outdated Information
- [Item 1]
- [Item 2]

### Missing Information
- [Item 1]
- [Item 2]

### Incorrect Information
- [Item 1]

## Phase 5: Updates Applied
- Overview: [updated/unchanged]
- Isolation Patterns: [X updates]
- Module Composition: [X updates]
- SDLC Orchestration: [X updates]
- Recent Changes: [added entry]

Specific updates:
1. [Update description]
2. [Update description]

## Phase 6: Line Limit Enforcement
- Before: [X] lines
- After: [Y] lines
- Status: ✅ Under 1000 / ⚠️ Compressed to fit

Compression applied:
- [Strategy used if compressed]

## Phase 7: Validation
- YAML syntax: ✅ Valid
- Required keys: ✅ Present
- Line count: ✅ [Y] / 1000

## ADW-Specific Findings
### State Management
- [Findings about state.py patterns]

### GitHub Integration
- [Findings about github.py, git_ops.py]

### Workflow Orchestration
- [Findings about workflow_ops.py, tool_sequencer.py]

### Worktree Operations
- [Findings about worktree_ops.py patterns]

## Recommendations
- [Any recommendations for manual review]
- [Suggestions for next self-improve run]

## Next Steps
- Run `/experts:adw:question` to verify updated expertise
- Consider self-improve again after next major ADW changes
```

## Success Criteria

Self-improve is successful if:
1. ✅ All 7 phases completed
2. ✅ Expertise is valid YAML
3. ✅ Line count ≤ 1000
4. ✅ All discrepancies documented and addressed
5. ✅ `last_updated` field updated to current date
6. ✅ Report is comprehensive and actionable
