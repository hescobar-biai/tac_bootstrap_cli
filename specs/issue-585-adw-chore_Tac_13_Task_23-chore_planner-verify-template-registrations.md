# Chore: Verify all template registrations in scaffold_service.py

## Metadata
issue_number: `585`
adw_id: `chore_Tac_13_Task_23`
issue_json: `{"number": 585, "title": "[TAC-13] Task 23: Verify all template registrations in scaffold_service.py", "body": "Verify that all agent expert templates (created in Tasks 4-17) are properly registered in scaffold_service.py. Templates should have been registered by their respective tasks. This task ensures completeness and adds comprehensive code block documentation."}`

## Chore Description
This chore verifies that all TAC-13 agent expert templates (Tasks 4-17) are properly registered in `scaffold_service.py`. The templates exist in the codebase and most registrations appear to be in place, but we need to:
1. Verify completeness of all expert template registrations
2. Add comprehensive inline code documentation
3. Ensure consistent registration patterns
4. Validate all template paths exist

## Relevant Files

### Files to Modify
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Main registration file (lines 482-551)
  - Contains the `_add_claude_files()` method where expert commands are registered
  - Already has registrations for CLI, ADW, and Commands experts
  - Needs verification and documentation enhancement

### Template Files to Verify (exist in codebase)
**CLI Expert** (Tasks 4-6):
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/question.md.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/expertise.yaml.j2`

**ADW Expert** (Tasks 7-9):
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/question.md.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/self-improve.md.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/expertise.yaml.j2`

**Commands Expert** (Tasks 10-12):
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/question.md.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/self-improve.md.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/expertise.yaml.j2`

**Hook Expert** (pre-existing):
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2`

### Files for Validation
- `tac_bootstrap_cli/tests/` - Test directory for validation
- `.claude/commands/experts/` - Generated command files to verify against

## Step by Step Tasks

### Task 1: Verify All Template Files Exist
**Goal**: Confirm all expected template files are present in the templates directory.

**Actions**:
1. Use Glob to list all expert template files:
   ```bash
   find tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts -name "*.j2" -type f | sort
   ```
2. Cross-reference with expected list (12 files total: 3 CLI + 3 ADW + 3 Commands + 3 Hook)
3. Document any missing templates
4. Verify directory structure matches expected pattern: `experts/<domain>/{question,self-improve,expertise}.*`

### Task 2: Audit Current Registrations in scaffold_service.py
**Goal**: Verify all templates are registered in the `_add_claude_files()` method.

**Actions**:
1. Read the current expert command registrations section (lines 487-551)
2. Extract all `plan.add_file()` calls related to expert templates
3. Create checklist of registered vs expected templates:
   - CLI Expert: question.md ✓, self-improve.md ✓, expertise.yaml ✓
   - ADW Expert: question.md ✓, self-improve.md ✓, expertise.yaml ✓
   - Commands Expert: question.md ✓, self-improve.md ✓, expertise.yaml ✓
   - Hook Expert: cc_hook_expert_plan.md ✓, cc_hook_expert_build.md ✓, cc_hook_expert_improve.md ✓
4. Identify any missing or incorrect registrations
5. Verify `FileAction` types are correct:
   - Use `FileAction.CREATE` for .md files (overwrite on regeneration)
   - Use `FileAction.CREATE` for expertise.yaml files (don't overwrite existing expertise)

### Task 3: Add Comprehensive Code Block Documentation
**Goal**: Document the expert registration section with clear, structured comments.

**Actions**:
1. Add a major section comment before expert commands (around line 487):
   ```python
   # ============================================================================
   # TAC-13: AGENT EXPERT COMMANDS
   # ============================================================================
   # Expert agents are self-learning command templates that maintain expertise files.
   # Each expert has 3 components:
   #   1. question.md    - Read-only Q&A using expertise file + codebase validation
   #   2. self-improve.md - 7-phase self-improvement workflow
   #   3. expertise.yaml  - Mental model (working memory, not source of truth)
   #
   # Pattern: experts/<domain>/{question,self-improve,expertise}.*
   # Domains: cli, adw, commands, cc_hook_expert
   # ============================================================================
   ```

2. Group registrations by expert domain with sub-comments:
   ```python
   # --- CLI Expert (Tasks 4-6): TAC Bootstrap CLI architecture ---
   # --- ADW Expert (Tasks 7-9): AI Developer Workflows ---
   # --- Commands Expert (Tasks 10-12): .claude/commands/* structure ---
   # --- Hook Expert (pre-existing): Claude Code hooks implementation ---
   ```

3. Add inline comments for each registration explaining:
   - Purpose of the command
   - When it should be used
   - Relationship to expertise file

### Task 4: Ensure Registration Consistency
**Goal**: Verify all registrations follow the same pattern and conventions.

**Actions**:
1. Verify all registrations use consistent structure:
   ```python
   plan.add_file(
       f".claude/commands/{cmd}",
       action=action,
       template=f"claude/commands/{cmd}.j2",
       reason="<descriptive reason>",
   )
   ```

2. Check that expertise files use correct action:
   ```python
   plan.add_file(
       ".claude/commands/experts/<domain>/expertise.yaml",
       action=FileAction.CREATE,  # Don't overwrite if exists
       template="claude/commands/experts/<domain>/expertise.yaml.j2",
       reason="<domain> expert expertise seed file",
   )
   ```

3. Verify reason strings are descriptive and consistent:
   - Pattern: "<Domain> expert <component type>"
   - Examples: "CLI expert question prompt", "ADW expert self-improve workflow"

4. Ensure correct directory structure is created (line 111):
   ```python
   (".claude/commands/experts", "Expert command groups"),
   ```

### Task 5: Validate Template Paths
**Goal**: Ensure all registered template paths actually exist in the templates directory.

**Actions**:
1. Extract all template paths from expert_commands list
2. For each template path, verify file exists:
   ```bash
   test -f tac_bootstrap_cli/tac_bootstrap/templates/<template_path>
   ```
3. Report any missing template files
4. Verify template filenames match registration paths exactly (case-sensitive)

### Task 6: Cross-Validate Against Implementation
**Goal**: Verify generated files in repo match registered templates.

**Actions**:
1. Check that repo has corresponding command files:
   ```bash
   ls .claude/commands/experts/*/question.md
   ls .claude/commands/experts/*/self-improve.md
   ls .claude/commands/experts/*/expertise.yaml
   ```
2. Verify file contents were generated from correct templates
3. Ensure expertise files exist and are not empty
4. Validate frontmatter structure in generated .md files

### Task 7: Document Expert Architecture
**Goal**: Add module-level documentation explaining the expert system.

**Actions**:
1. Update the module docstring in scaffold_service.py (lines 1-5) to mention expert registration:
   ```python
   """
   IDK: scaffold-service, plan-builder, code-generation, template-rendering, file-operations, expert-registration
   Responsibility: Builds scaffold plans from TACConfig and applies them to filesystem, including TAC-13 expert agent templates
   Invariants: Plans are idempotent, templates must exist, output directory must be writable, expert templates follow 3-component pattern
   """
   ```

2. Add comment explaining dual-strategy pattern before _add_claude_files():
   ```python
   def _add_claude_files(self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool) -> None:
       """Add .claude/ configuration files.

       Includes TAC-13 expert agent templates following the dual-strategy pattern:
       1. CLI Templates (Jinja2): In tac_bootstrap/templates/
       2. Repo Implementations: Generated in .claude/commands/
       3. Expertise Files: Working memory maintained by self-improve workflow
       """
   ```

### Task 8: Run Validation Commands
**Goal**: Ensure all changes pass tests and validation.

**Actions**:
1. Run unit tests:
   ```bash
   cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
   ```

2. Run linting:
   ```bash
   cd tac_bootstrap_cli && uv run ruff check .
   ```

3. Run smoke test:
   ```bash
   cd tac_bootstrap_cli && uv run tac-bootstrap --help
   ```

4. Test scaffold generation with expert templates:
   ```bash
   cd tac_bootstrap_cli && uv run tac-bootstrap wizard --dry-run
   ```

5. Verify all expert templates are listed in dry-run output

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `cd tac_bootstrap_cli && uv run tac-bootstrap wizard --dry-run` - Verify expert templates appear in plan

## Notes

### Current State
Based on analysis of scaffold_service.py:
- CLI expert registrations: PRESENT (lines 493-495, 508-513)
- ADW expert registrations: PRESENT (lines 497, 515-521, 523-526)
- Commands expert registrations: PRESENT (lines 529-542, 544-550)
- Hook expert registrations: PRESENT (lines 489-491)

All templates appear to be registered, but need:
1. Better code organization with section headers
2. Comprehensive inline documentation
3. Validation that paths are correct
4. Consistent comment style

### Expert System Pattern
Each expert follows the 3-component pattern:
1. **question.md** - Read-only queries using expertise + validation
2. **self-improve.md** - 7-phase improvement workflow
3. **expertise.yaml** - Mental model (working memory only)

### Registration Strategy
- **.md files**: Use `FileAction.CREATE` (overwrite on scaffold regeneration)
- **expertise.yaml files**: Use `FileAction.CREATE` (preserve user-modified expertise)
- All expert commands use `action=action` variable for consistency

### Dual Strategy Context
TAC-13 uses dual-layer pattern:
1. Templates (Jinja2) in CLI: Source of truth
2. Generated files in repo: Working implementations
3. Expertise files: Working memory updated by self-improve

### Integration Points
- Directory creation: Line 111 creates `.claude/commands/experts`
- Expert commands list: Lines 488-505 (needs expansion/documentation)
- Expertise file registrations: Lines 508-513, 515-521, 544-550

### Success Criteria
1. All 12 expert templates registered correctly
2. Code has clear section headers and inline documentation
3. All validation commands pass
4. Dry-run shows all expert templates in plan
5. Registration patterns are consistent across all experts
