# Feature: Update cc_hook_expert_improve Template for Self-Improvement

## Metadata
issue_number: `308`
adw_id: `feature_Tac_10_task_3`
issue_json: `{"number":308,"title":"Crear template cc_hook_expert_improve.md.j2 para self-improvement","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_10_task_3\n\n- **Descripción**: Completar el sistema de expertos con el prompt de mejora continua (Level 7). Analiza cambios recientes y actualiza las secciones de Expertise de los prompts plan y build.\n- **Archivos**:\n  - Template Jinja2: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2`\n  - Archivo directo: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md`\n- **Contenido**:\n  - Workflow de 5 pasos: Establish Expertise, Analyze Recent Changes, Determine Relevance, Extract and Apply Learnings, Report\n  - Lógica de early return si no hay learnings relevantes\n  - Report format estructurado\n- **Nota**: El template .j2 usa variables Jinja2, el archivo .md es la versión renderizada para uso directo\n\n"}`

## Feature Description
Complete the Claude Code hook expert system with the self-improvement prompt (Level 7). This command analyzes the last 5 commits on the current branch, filters for changes in expert/automation layers (.claude/commands/experts/cc_hook_expert/, adws/adw_modules/, scripts/), and generates a structured markdown report with recommendations for updating the plan and build expert prompts. The command is manually triggered via `/cc_hook_expert_improve` and generates report output only (no automatic edits), allowing humans to review and apply improvements to critical expert infrastructure.

## User Story
As a TAC Bootstrap user
I want to manually trigger expert self-improvement analysis after milestone work
So that my generated projects can provide actionable recommendations for updating expert knowledge based on recent implementation learnings, while maintaining quality control over critical prompt modifications through human review

## Problem Statement
The existing cc_hook_expert_improve template was created in issue 298 but needs enhancements to complete Level 7 of the expert system. The current implementation needs:

1. **Manual trigger mechanism**: Command should be invoked via `/cc_hook_expert_improve` skill (not automatic hooks)
2. **Commit analysis scope**: Analyze last 5 commits via `git log -5 --stat` for deterministic, meaningful scope
3. **Relevance filtering**: Only proceed if changes touch `.claude/commands/experts/cc_hook_expert/`, `adws/adw_modules/`, or `scripts/` directories
4. **Report-only output**: Generate structured markdown report with recommendations (no automatic file edits)
5. **Structured report format**: Sections for Summary, Relevant Changes, Recommendations for Plan Expert, Recommendations for Build Expert, Suggested Actions
6. **Target prompt locations**: `.claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md` and `cc_hook_expert_build.md` (both .j2 template and rendered .md versions)
7. **Expertise section markers**: Look for `## Expertise` or `### Recent Learnings` sections in target prompts

This maintains a simple, safe approach where humans maintain quality control over critical expert prompt infrastructure.

## Solution Statement
Update the Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2` and its rendered version at `.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md` to implement a manual-trigger command that:

1. **Manual Invocation**: Registered in Skill tool, triggered via `/cc_hook_expert_improve` command
2. **Git Analysis**: Uses `git log -5 --stat` to review last 5 commits on current branch
3. **Path-Based Filtering**: Checks if any files match `.claude/commands/experts/cc_hook_expert/`, `adws/adw_modules/`, or `scripts/` directories
4. **Early Return**: If no matching files found, stops with "No expertise updates needed" message
5. **Report Generation**: Creates structured markdown report with:
   - Summary section
   - Relevant Changes section (lists matching files and changes)
   - Recommendations for Plan Expert (improvements for cc_hook_expert_plan.md)
   - Recommendations for Build Expert (improvements for cc_hook_expert_build.md)
   - Suggested Actions (how user should apply recommendations)
6. **Console Output**: Displays report to console only (user can redirect with `> improvement_report.md` if needed)
7. **Minimal Variables**: Uses `{{ config.project.name }}`, `{{ config.paths.experts_dir }}`, `{{ config.commands.expert_improve }}` for portability

## Relevant Files

### Files to Modify
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2` - Update template with new workflow and specifications
- `.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md` - Re-render with updated content

### Reference Files
- `.claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md` - Target for plan expert recommendations
- `.claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md` - Target for build expert recommendations
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Config schema for available Jinja2 variables
- `specs/issue-298-adw-feature_Tac_9_task_31-sdlc_planner-cc-hook-expert-improve-template.md` - Previous implementation plan

### Integration Points
- Skill tool registration (will need to register `/cc_hook_expert_improve` command)
- Git repository context (command must run in git repo)

### New Files
None - updating existing template and rendered files

## Implementation Plan

### Phase 1: Foundation
Read and understand the current cc_hook_expert_improve template structure, analyze the requirements from issue 308, and identify specific changes needed to implement the manual-trigger, report-only workflow.

### Phase 2: Core Implementation
Update the template with new workflow phases, git analysis logic, path-based filtering, early-return mechanism, and structured report format. Add minimal Jinja2 variables for portability.

### Phase 3: Integration
Re-render the template in this repository's `.claude/commands/experts/cc_hook_expert/` directory, validate the report generation works correctly, and ensure skill registration path is documented.

## Step by Step Tasks

### Task 1: Read Current Implementation
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2`
- Read `.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md`
- Identify current workflow structure and what needs to change
- Note existing Jinja2 variables and patterns

### Task 2: Update Template - Frontmatter and Variables
- Update YAML frontmatter:
  - `allowed-tools: Read, Bash, Grep, Glob` (removed Edit - report only)
  - `description: Review hook changes and update expert knowledge with improvements`
  - `model: sonnet`
- Update Variables section:
  - Remove arguments variable (manual trigger, no args needed)
  - Add: `PROJECT_NAME: {{ config.project.name }}`
  - Add: `EXPERTS_DIR: {{ config.paths.experts_dir }}`
  - Add: `EXPERT_IMPROVE_CMD: {{ config.commands.expert_improve }}`

### Task 3: Update Template - Phase 1 (Establish Expertise)
- Keep existing foundation reading:
  - `ai_docs/uv-scripts-guide.md`
  - `ai_docs/claude-code-hooks.md`
  - `ai_docs/claude-code-slash-commands.md`
- Update current expert state reading:
  - Use `{{ config.paths.experts_dir }}` variable for expert command paths
  - Read `cc_hook_expert_plan.md` and `cc_hook_expert_build.md`
  - Note current `## Expertise` sections

### Task 4: Update Template - Phase 2 (Analyze Recent Changes)
- Replace git analysis section with:
  - Primary command: `git log -5 --stat` - Review last 5 commits with file statistics
  - Explain scope: "Last 5 commits on current branch provides deterministic, meaningful scope"
  - Parse commit messages and changed files from git output
- Remove uncommitted/staged change analysis (simplify to committed work only)
- Focus on identifying hook-related files in output

### Task 5: Update Template - Phase 3 (Determine Relevance)
- Update relevance criteria to path-based filtering:
  - "Changes must touch files in: `.claude/commands/experts/cc_hook_expert/`, `adws/adw_modules/`, or `scripts/` directories"
  - "These are the expert/automation layers. Changes to business logic elsewhere don't improve the expert system itself."
- Add explicit early return decision point:
  - "CRITICAL DECISION POINT: If NO files match these paths, STOP HERE and skip to Phase 5 with 'No expertise updates needed' report"
  - "If YES - files match these paths, PROCEED to Phase 4"

### Task 6: Update Template - Phase 4 (Extract and Apply Learnings)
- Remove Edit tool usage (report only, no automatic edits)
- Update workflow to report generation:
  - Analyze matching files for patterns, improvements, best practices
  - Categorize learnings by target expert (plan vs build)
  - Structure recommendations for each expert prompt
- Add guidance for what to recommend:
  - For Plan Expert: specification patterns, architecture decisions, security considerations
  - For Build Expert: implementation patterns, error handling, testing strategies, code quality

### Task 7: Update Template - Phase 5 (Report)
- Define structured report format:
  ```markdown
  # Expert Improvement Analysis Report

  ## Summary
  [Brief overview of analysis scope and findings]

  ## Relevant Changes
  [List of files changed in last 5 commits that match expert/automation paths]
  - File: path/to/file
    - Change type: added/modified/deleted
    - Lines changed: +X -Y
    - Commits: commit hash(es)

  ## Recommendations for Plan Expert
  ### Update Section: [## Expertise or specific subsection]
  **Pattern Discovered:** [Description]
  **Context:** [When/where in recent work]
  **Recommendation:** [Specific text to add or modify in cc_hook_expert_plan.md]
  **Rationale:** [Why this improves planning guidance]

  [Additional recommendations...]

  ## Recommendations for Build Expert
  ### Update Section: [## Expertise or specific subsection]
  **Pattern Discovered:** [Description]
  **Context:** [When/where in recent work]
  **Recommendation:** [Specific text to add or modify in cc_hook_expert_build.md]
  **Rationale:** [Why this improves build guidance]

  [Additional recommendations...]

  ## Suggested Actions
  1. Review recommendations above
  2. Open `.claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md` (and .j2 template)
  3. Locate the `## Expertise` or `### Recent Learnings` sections
  4. Manually add/update content based on recommendations
  5. Repeat for `cc_hook_expert_build.md` (and .j2 template)
  6. Test updated expert commands in a sample workflow
  7. Commit changes with descriptive message
  ```
- Add note: "Output to console only. User can redirect with `> report.md` if desired."

### Task 8: Update Template - Add Expertise Section
- Add `## Expertise` section after instructions with guidance on:
  - **When to Run**: After milestone work, major hook implementations, pattern discoveries
  - **How to Use**: Manual trigger via `/cc_hook_expert_improve`, no arguments needed
  - **What It Does**: Analyzes last 5 commits, filters for expert/automation files, generates actionable recommendations
  - **Safety**: Report-only approach ensures human review of critical prompt changes
  - **Git Analysis Best Practices**: Commands to use, how to interpret output, pattern identification tips

### Task 9: Validate Template Syntax
- Check Jinja2 syntax is valid
- Verify YAML frontmatter structure
- Ensure all variable references are consistent
- Validate markdown formatting
- Test template renders without errors

### Task 10: Re-render Template
- Use TAC Bootstrap CLI (or manual Jinja2 rendering) to generate:
  - `.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md`
- Use config values from this repository:
  - `config.project.name = "tac-bootstrap"`
  - `config.paths.experts_dir = ".claude/commands/experts"`
  - `config.commands.expert_improve = "/cc_hook_expert_improve"` (or appropriate value)
- Verify rendered output looks correct

### Task 11: Document Skill Registration
- Add comment in template explaining this command should be registered in Skill tool
- Recommend skill name: `cc_hook_expert_improve`
- Describe when users should invoke: "After completing milestone work, run `/cc_hook_expert_improve` to analyze recent changes and get expert improvement recommendations"

### Task 12: Test Report Generation (Manual Smoke Test)
- Verify the rendered command can:
  - Run `git log -5 --stat` successfully
  - Parse git output for file paths
  - Filter files by expert/automation paths
  - Generate structured markdown report
  - Display report to console
- Test early return: If no matching files, should stop with "No expertise updates needed"
- Test full flow: If matching files, should generate complete report with all sections

### Task 13: Validate and Run Tests
Execute all validation commands to ensure zero regressions:
- Run: `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Run: `cd tac_bootstrap_cli && uv run ruff check .`
- Run: `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Run: `cd tac_bootstrap_cli && uv run tac-bootstrap --help`
- Fix any issues discovered
- Ensure all tests pass

## Testing Strategy

### Unit Tests
- Test template rendering with various config values
- Verify Jinja2 variables are properly substituted
- Validate YAML frontmatter parsing
- Check markdown structure in rendered output

### Integration Tests
- Test git log parsing logic (may need mock git repo)
- Verify path filtering correctly identifies expert/automation files
- Test early return when no relevant files found
- Test report generation with sample git output

### Manual Testing
- Create sample commits touching expert files
- Run rendered command manually
- Verify report structure and content quality
- Test early return with non-expert file changes
- Confirm console output is readable

### Edge Cases
- Empty git history (less than 5 commits)
- Git repository not initialized
- All 5 commits touch only non-expert files (early return test)
- Mix of expert and non-expert files (should filter correctly)
- No `## Expertise` sections in target prompts (should note this in recommendations)
- Binary files or very large diffs in commits

## Acceptance Criteria

1. Template updated at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2` with manual-trigger workflow
2. YAML frontmatter updated: tools are Read, Bash, Grep, Glob (no Edit)
3. Git analysis uses `git log -5 --stat` to review last 5 commits
4. Path-based filtering implemented for `.claude/commands/experts/cc_hook_expert/`, `adws/adw_modules/`, `scripts/` directories
5. Early return logic: stops with "No expertise updates needed" if no matching files
6. Structured report format implemented with all required sections (Summary, Relevant Changes, Recommendations for Plan/Build Experts, Suggested Actions)
7. Report output goes to console only (no automatic file edits)
8. Jinja2 variables used: `{{ config.project.name }}`, `{{ config.paths.experts_dir }}`, `{{ config.commands.expert_improve }}`
9. Rendered command updated at `.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md`
10. Template includes `## Expertise` section with guidance on when/how to use
11. Documentation includes skill registration note for `/cc_hook_expert_improve` command
12. All tests pass with zero regressions

## Validation Commands
Execute all commands to validate with zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Key Design Decisions from Auto-Resolved Clarifications

1. **Manual Trigger Only**: Via `/cc_hook_expert_improve` command (registered in Skill tool)
   - Rationale: Self-improvement should be deliberate, not automatic. Running after every commit would be noisy and expensive. Manual control allows users to trigger after meaningful milestone work.

2. **Last 5 Commits Scope**: Uses `git log -5 --stat`
   - Rationale: Simple, deterministic, and covers typical feature/fix scope. Users can run more frequently if needed. Avoids complexity of tracking last-run timestamps.

3. **Path-Based Relevance Filter**: `.claude/commands/experts/cc_hook_expert/`, `adws/adw_modules/`, `scripts/`
   - Rationale: These are the expert/automation layers. Changes to business logic elsewhere don't improve the expert system itself. Simple path-based filter is easy to implement and understand.

4. **Report-Only (No Auto-Edits)**: Generates structured report, user manually applies recommendations
   - Rationale: Self-modifying prompts risk corruption or drift. Human-in-the-loop ensures quality control. Safer for critical infrastructure like expert prompts.

5. **Console Output Only**: No file storage, user can redirect if needed
   - Rationale: Simplest approach. No need to manage report file lifecycle, locations, or cleanup. Unix philosophy: output to stdout.

6. **Minimal Jinja2 Variables**: `{{ config.project.name }}`, `{{ config.paths.experts_dir }}`, `{{ config.commands.expert_improve }}`
   - Rationale: Command doesn't need extensive project config since it operates on its own expert files. Paths make it portable across projects.

7. **Structured Markdown Report**: Sections for Summary, Relevant Changes, Recommendations for Plan/Build Experts, Suggested Actions
   - Rationale: Markdown is readable and parseable. Structure helps users quickly find actionable items. No artificial limits - let content dictate length.

### Workflow Context

This completes the Plan-Build-Improve expert workflow cycle:
- **Plan** (cc_hook_expert_plan): Design the hook implementation approach
- **Build** (cc_hook_expert_build): Execute the planned implementation
- **Improve** (cc_hook_expert_improve): Analyze work and generate improvement recommendations

The improve phase creates a feedback loop that enhances expert commands based on real-world usage, while maintaining safety through human review.

### Future Enhancements

- Could add `--commits N` argument to analyze more/fewer commits
- Could add `--paths` argument to override default filter paths
- Could add `--output FILE` argument to save report to file automatically
- Could integrate with CI/CD to auto-generate reports after merges to main
- Could add metrics tracking (learnings captured count over time)
- Could support analyzing specific commit ranges via arguments
