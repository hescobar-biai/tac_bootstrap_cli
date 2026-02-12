---
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, TodoWrite
description: Self-improve CLI expertise by validating against codebase
argument-hint: [check_git_diff] [focus_area]
model: sonnet
---

# NOTE: Model "sonnet" uses 3-tier resolution:
#   1. ANTHROPIC_DEFAULT_SONNET_MODEL (env var) - highest priority
#   2. config.yml agentic.model_policy.sonnet_model - project config
#   3. Hardcoded default "claude-sonnet-4-5-20250929" - fallback
# See .claude/MODEL_RESOLUTION.md for details


# CLI Expert: Self-Improve Mode

## Purpose

Maintain and update the CLI expert's mental model (expertise.yaml) by validating it against the actual codebase and incorporating new knowledge.

This is the **Learn** step in the Act → Learn → Reuse loop.

## Variables

- **CHECK_GIT_DIFF**: `$1` (default: `false`) - If `true`, focus on recently changed files
- **FOCUS_AREA**: `$2` (default: empty) - Optional area to focus on (e.g., "templates", "scaffold_service", "cli_commands")
- **SUMMARY_MODE**: `$3` (default: `true`) - If `true`, use summarized diffs and selective file reading for token optimization
- **EXPERTISE_FILE**: `.claude/commands/experts/cli/expertise.yaml` (static)
- **CLI_ROOT**: `tac_bootstrap_cli/tac_bootstrap/` (static)
- **MAX_LINES**: `1000` (static)

## Instructions

You are the CLI Expert updating your mental model. Follow the 7-phase workflow strictly:

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
   git diff --stat HEAD -- tac_bootstrap_cli/

   # Just list changed files
   git diff --name-status HEAD -- tac_bootstrap_cli/
   ```

2. Identify changed files and focus areas:
   ```bash
   # List only filenames
   changed_files=$(git diff --name-only HEAD -- tac_bootstrap_cli/)
   echo "$changed_files"
   ```

3. For critical changes, get focused diffs:
   ```bash
   # Only if scaffold_service.py changed - get function-level diff
   if echo "$changed_files" | grep -q "scaffold_service.py"; then
       git diff HEAD -- tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py | grep -A 3 -B 3 "^def "
   fi

   # Only if cli.py changed
   if echo "$changed_files" | grep -q "cli.py"; then
       git diff HEAD -- tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py | grep -A 3 -B 3 "^def "
   fi
   ```

4. Note focus areas based on changed files:
   - If `scaffold_service.py` changed → focus on template registration
   - If `cli.py` changed → focus on CLI commands
   - If `templates/` changed → focus on template patterns
   - If `domain/` changed → focus on data models

5. Update FOCUS_AREA internally based on findings

**Token Impact:** ~5K tokens instead of 500K-1M tokens

#### Full Mode (SUMMARY_MODE = false)

Use complete diffs for comprehensive validation:

1. Run git diff to see recent changes:
   ```bash
   # Check unstaged changes
   git diff HEAD -- tac_bootstrap_cli/

   # Check staged changes
   git diff --cached -- tac_bootstrap_cli/

   # Check last commit
   git log -1 --stat --oneline -- tac_bootstrap_cli/
   ```

2. Identify changed files in CLI domain:
   ```bash
   # List changed files
   git diff --name-only HEAD -- tac_bootstrap_cli/
   ```

3. Note focus areas based on changes (same as summary mode)

4. Update FOCUS_AREA internally based on findings

**Token Impact:** 500K-1M tokens (original behavior)

**If CHECK_GIT_DIFF is `false`**: Skip to Phase 2

### Phase 2: Read Current Expertise

1. Read the existing expertise file:
   ```bash
   cat .claude/commands/experts/cli/expertise.yaml
   ```

2. Parse the structure:
   - Note `last_updated` date
   - Review all `core_implementation` components
   - Check `key_operations` workflows
   - Review `recent_changes` entries

3. Identify sections to validate:
   - If FOCUS_AREA is set: prioritize that section
   - Otherwise: validate all sections systematically

4. Track current line count:
   ```bash
   wc -l .claude/commands/experts/cli/expertise.yaml
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

   # Example: If scaffold_service.py changed
   if echo "$changed_files" | grep -q "scaffold_service.py"; then
       # Check class exists
       grep -n "class ScaffoldService" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py

       # Verify key methods
       grep -n "def _add_claude_code_commands\|def scaffold_project" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
   fi
   ```

3. Skip files that didn't change (trust existing expertise)

4. Quick discovery scan for new files only:
   ```bash
   # Find any new CLI files
   find tac_bootstrap_cli/tac_bootstrap -name "*.py" | grep -v __pycache__
   ```

**Token Impact:** ~50K tokens (only changed files)

#### Full Mode Validation (SUMMARY_MODE = false)

**Comprehensive validation** - re-verify entire codebase:

1. **Validate Overview Section**:
   ```bash
   # Check if key_files exist and are current
   for file in $(grep -A 10 "key_files:" .claude/commands/experts/cli/expertise.yaml | grep "- " | sed 's/.*- "\(.*\)"/\1/'); do
       test -f "$file" && echo "✓ $file" || echo "✗ MISSING: $file"
   done
   ```

2. **Validate Core Implementation**:
   ```bash
   # For each component in core_implementation
   # Example: Validate scaffold_service component

   # Read the actual file
   cat tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py

   # Check if documented classes exist
   grep -n "class ScaffoldService" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py

   # Verify method signatures
   grep -n "def _add_claude_code_commands" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py

   # Check line numbers are accurate
   sed -n '150,200p' tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
   ```

3. **Validate Key Operations**:
   ```bash
   # Verify workflow patterns described in expertise
   # Example: Template registration workflow

   # Find actual registration calls
   grep -n "plan.add_file" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py

   # Verify pattern matches expertise description
   grep -A 3 "plan.add_file" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
   ```

4. **Discover New Information**:
   ```bash
   # Find files not yet documented
   find tac_bootstrap_cli/tac_bootstrap -name "*.py" | grep -v __pycache__

   # Check for new important functions
   grep -rn "^def " tac_bootstrap_cli/tac_bootstrap/application/
   grep -rn "^class " tac_bootstrap_cli/tac_bootstrap/domain/
   ```

5. **Check for Architectural Changes**:

**Token Impact:** 300-500K tokens (full file reads)
   - New modules or packages?
   - Moved files?
   - Refactored functions?
   - New patterns introduced?

### Phase 4: Identify Discrepancies

**Document ALL differences between expertise and reality**

Create a discrepancies report:

```markdown
## Discrepancies Found

### Outdated Information
- [ ] Expertise says: "X is at line 100"
      Reality: X is at line 120 (moved due to new imports)

- [ ] Expertise documents: method_old()
      Reality: method_old() was renamed to method_new()

### Missing Information
- [ ] New file added: `templates/claude/commands/new-command.md.j2`
      Not documented in expertise

- [ ] New method in ScaffoldService: `_add_tac_13_templates()`
      Should be documented in key_operations

### Incorrect Information
- [ ] Expertise: "Template registration uses pattern X"
      Reality: Pattern changed to Y in recent refactor

### Gaps in Coverage
- [ ] No documentation for: `infrastructure/filesystem.py`
- [ ] Missing workflow: "How entity generation works"
```

### Phase 5: Update Expertise File

**Apply updates based on discrepancies**

1. **Update Overview** (if needed):
   ```yaml
   overview:
     description: "Updated description if system changed"
     key_files:
       - "add new important files"
       - "remove obsolete files"
     last_updated: "2026-02-03"  # Always update date
   ```

2. **Update Core Implementation**:
   ```yaml
   core_implementation:
     scaffold_service:
       location: "tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py"
       key_methods:
         - name: "_add_claude_code_commands"
           line_start: 150  # Update if moved
           line_end: 200
           signature: "def _add_claude_code_commands(self, plan: ScaffoldPlan) -> None"
           logic: "Registers all command templates using plan.add_file() pattern"
         - name: "_add_tac_13_templates"  # NEW method found
           line_start: 205
           line_end: 230
           signature: "def _add_tac_13_templates(self, plan: ScaffoldPlan) -> None"
           logic: "Registers TAC-13 agent expert templates"
   ```

3. **Update Key Operations**:
   ```yaml
   key_operations:
     template_registration:
       workflow: |
         1. ScaffoldService.__init__ loads config
         2. _add_claude_code_commands() registers base templates
         3. _add_tac_13_templates() registers expert templates  # UPDATED
         4. Each template: action, template path, reason
         5. render_template() processes .j2 files
   ```

4. **Add Recent Changes**:
   ```yaml
   recent_changes:
     - date: "2026-02-03"
       description: "Added TAC-13 agent expert templates"
       files: ["scaffold_service.py", "templates/claude/commands/experts/"]
     - date: "2026-02-01"
       description: "Refactored template registration pattern"
       files: ["scaffold_service.py"]
     # Keep only 5 most recent entries
   ```

5. **Use Edit tool for updates**:
   ```bash
   # Update specific sections using Edit tool
   # Example: Update line numbers for a method
   ```

6. **Or use Write tool for major changes**:
   ```bash
   # If expertise needs significant restructuring, rewrite entire file
   ```

### Phase 6: Enforce Line Limit

**Ensure expertise stays under 1000 lines**

1. Check current line count:
   ```bash
   wc -l .claude/commands/experts/cli/expertise.yaml
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
   key_methods:
     - name: "method_a"
       line_start: 10
       logic: "Does X"
     - name: "method_b"
       line_start: 20
       logic: "Does X"

   # After (consolidated):
   key_methods:
     - pattern: "X-type methods"
       instances: ["method_a:10", "method_b:20"]
       logic: "Does X"
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
     purpose: "Helper methods for X"
   ```

   **Strategy 4: Remove Obvious Information**
   ```yaml
   # Remove patterns that are self-evident from code
   # Keep only non-obvious knowledge and relationships
   ```

4. After compression, verify:
   ```bash
   wc -l .claude/commands/experts/cli/expertise.yaml
   # Must be <= 1000
   ```

### Phase 7: Validate YAML Syntax

**Final validation before finishing**

1. Validate YAML syntax:
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('.claude/commands/experts/cli/expertise.yaml'))"
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
   grep -E "^(overview|core_implementation|key_operations):" .claude/commands/experts/cli/expertise.yaml
   ```

5. Final checks:
   ```bash
   # Line count
   lines=$(wc -l < .claude/commands/experts/cli/expertise.yaml)
   echo "✓ Line count: $lines / 1000"

   # YAML valid
   python3 -c "import yaml; yaml.safe_load(open('.claude/commands/experts/cli/expertise.yaml'))" && echo "✓ Valid YAML"

   # Required keys present
   grep -q "^overview:" .claude/commands/experts/cli/expertise.yaml && echo "✓ Has overview"
   grep -q "^core_implementation:" .claude/commands/experts/cli/expertise.yaml && echo "✓ Has core_implementation"
   ```

## Report Format

Provide a detailed report of the self-improve run:

```markdown
# CLI Expert Self-Improve Report

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
- Files validated: [count]
- Methods verified: [count]
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
- Core Implementation: [X updates]
- Key Operations: [X updates]
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

## Recommendations
- [Any recommendations for manual review]
- [Suggestions for next self-improve run]

## Next Steps
- Run `/experts:cli:question` to verify updated expertise
- Consider self-improve again after next major CLI changes
```

## Success Criteria

Self-improve is successful if:
1. ✅ All 7 phases completed
2. ✅ Expertise is valid YAML
3. ✅ Line count ≤ 1000
4. ✅ All discrepancies documented and addressed
5. ✅ `last_updated` field updated to current date
6. ✅ Report is comprehensive and actionable
