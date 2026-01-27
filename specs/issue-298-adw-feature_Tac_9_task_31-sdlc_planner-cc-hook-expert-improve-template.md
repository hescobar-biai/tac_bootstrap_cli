# Feature: Add cc_hook_expert_improve.md.j2 Expert Command Template

## Metadata
issue_number: `298`
adw_id: `feature_Tac_9_task_31`
issue_json: `{"number":298,"title":"Add cc_hook_expert_improve.md.j2 expert command template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_31\n\n**Description:**\nCreate Jinja2 template for Claude Code hook expert improve command. Third step in Plan-Build-Improve cycle (self-improvement).\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md` (CREATE - rendered)\n\n"}`

## Feature Description
Create a Jinja2 template for the `cc_hook_expert_improve` command that guides AI agents through the improvement (continuous learning) phase of Claude Code hook expert development. This is the third and final step in the Plan-Build-Improve expert workflow cycle. The template will provide expert methodology for analyzing recent hook-related changes, extracting learnings and best practices, and updating the plan and build expert commands with new knowledge to maintain cutting-edge expertise while keeping workflows stable.

## User Story
As a TAC Bootstrap user
I want to generate expert improve commands for hook development continuous learning
So that my generated projects can guide AI agents through self-improvement workflows that analyze their own work and update expert knowledge with discovered patterns and best practices

## Problem Statement
The TAC Bootstrap CLI has the planning phase (`cc_hook_expert_plan`) and build phase (`cc_hook_expert_build`) but lacks the continuous improvement phase for Claude Code hook development. Users need an improve-phase expert command that guides agents through:
1. Reviewing recent hook-related changes via git commands
2. Identifying successful patterns and potential improvements
3. Extracting actionable learnings from implementation experiences
4. Selectively updating the `## Expertise` sections of plan and build commands
5. Maintaining expert knowledge currency without disrupting stable workflows
6. Determining relevance and stopping early if no learnings are found

This template must create workflow closure for the expert cycle, preserve workflow stability by only updating expertise sections, and follow established patterns (YAML frontmatter, Jinja2 variables, expert workflow structure).

## Solution Statement
Create a Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2` that:
- Uses YAML frontmatter with analysis-focused tools (Read, Edit, Bash, Grep, Glob)
- Takes no required arguments (analyzes recent work automatically via git)
- Guides agents through Establish Expertise → Analyze Changes → Determine Relevance → Extract & Apply Learnings → Report workflow
- Reviews uncommitted changes, staged changes, and recent commits for hook-related files
- Evaluates if changes contain new expertise worth capturing (early exit if not relevant)
- Updates ONLY the `## Expertise` sections of plan/build commands with discovered knowledge
- Preserves workflow stability by never modifying `## Workflow` sections
- Uses minimal Jinja2 variables ({{ config.project.name }}, expertise paths)
- Provides expert guidance as static content with dynamic paths via config

## Relevant Files
Files needed for implementation:

### Reference Files
- `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md` - Source command to convert to template
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md.j2` - Planning phase template (expertise update target)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md.j2` - Build phase template (expertise update target)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/implement.md.j2` - Implementation command pattern
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Config schema for available variables

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2` - The template to create
- `.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md` - Rendered version in this repo

## Implementation Plan

### Phase 1: Foundation
Read and understand the source command structure, workflow phases, and integration points with plan/build commands.

### Phase 2: Core Implementation
Convert the source command to a Jinja2 template with appropriate variables, preserving the self-improvement methodology and early-exit logic.

### Phase 3: Integration
Render the template in this repository's `.claude/commands/` directory to validate it works and complete the expert workflow cycle.

## Step by Step Tasks

### Task 1: Read and Analyze Source Command
- Read `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md` (already done above)
- Identify sections: frontmatter, instructions, workflow phases, report format
- Note dynamic elements that need Jinja2 variables vs static expert content
- Understand the self-improvement cycle: analyze → evaluate relevance → update expertise

### Task 2: Identify Jinja2 Variable Requirements
- Determine what needs to be configurable via `config`:
  - Project name: `{{ config.project.name }}`
  - Paths to expert commands for updating expertise sections
  - Git commands (likely static, not configurable)
  - Documentation paths (ai_docs)
- Keep variables minimal - most content is static expert guidance
- List all identified variables for implementation

### Task 3: Create Jinja2 Template
- Create directory: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/`
- Create file: `cc_hook_expert_improve.md.j2`
- Convert source command to template:
  - Add YAML frontmatter with tools: Read, Edit, Bash, Grep, Glob
  - Add description: "Review hook changes and update expert knowledge with improvements"
  - Convert static content with minimal Jinja2 variables
  - Preserve all workflow phases and early-exit logic
  - Maintain report format structure
- Follow established pattern from cc_hook_expert_plan.md.j2 and cc_hook_expert_build.md.j2

### Task 4: Add Expertise Section (if needed)
- Determine if this command needs its own `## Expertise` section
- If yes, add expertise about:
  - When and how to perform self-improvement
  - Criteria for determining relevance
  - Best practices for updating expertise without disrupting workflows
  - Git analysis techniques for extracting learnings
- If no, omit this section (likely case since this is the improvement command itself)

### Task 5: Validate Template Syntax
- Review template for:
  - Valid Jinja2 syntax
  - Proper YAML frontmatter
  - Consistent variable usage
  - Markdown formatting
- Check against patterns in plan and build templates
- Ensure no absolute paths or hardcoded values that should be variables

### Task 6: Render Template in Repository
- Update CLI renderer/generator to include new template (if needed)
- Render template to `.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md`
- Use actual config values from this repository
- Verify rendered output matches expected format

### Task 7: Test Integration with Expert Workflow
- Verify complete expert cycle works:
  - Plan phase (cc_hook_expert_plan) → Build phase (cc_hook_expert_build) → Improve phase (cc_hook_expert_improve)
- Check that improve command references are correct:
  - Can read plan and build commands
  - Can update their expertise sections
  - Preserves workflow sections unchanged
- Manual smoke test: review the rendered command for correctness

### Task 8: Validate and Run Tests
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
- Check YAML frontmatter parsing
- Validate markdown structure

### Integration Tests
- Test complete expert workflow cycle (plan → build → improve)
- Verify improve command can read and update plan/build commands
- Check git analysis functionality works correctly
- Test early-exit logic when no relevant changes found

### Edge Cases
- No recent changes (git history empty)
- No hook-related changes (only other file types)
- Malformed expertise sections in target commands
- Missing plan or build commands
- Git commands fail (not in git repo)

## Acceptance Criteria
1. Jinja2 template created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2`
2. Template uses YAML frontmatter with appropriate tools (Read, Edit, Bash, Grep, Glob)
3. Template includes all workflow phases from source command
4. Template preserves early-exit logic for irrelevant changes
5. Template uses minimal, appropriate Jinja2 variables (project name, paths)
6. Rendered command created at `.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md`
7. Rendered command can analyze git history and extract learnings
8. Rendered command can update expertise sections of plan and build commands
9. Complete expert workflow cycle (plan → build → improve) is functional
10. All tests pass with zero regressions

## Validation Commands
Execute all commands to validate with zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Key Design Decisions
1. **Early Exit Logic**: The improve command must determine relevance early and stop if no learnings are found to avoid wasted work
2. **Selective Updates**: Only update `## Expertise` sections, never `## Workflow` sections, to maintain workflow stability
3. **No Required Arguments**: Command analyzes recent work automatically via git, no user input needed
4. **Git-Based Analysis**: Uses `git diff`, `git diff --cached`, and `git log` to review recent changes
5. **Self-Referential**: This command updates other expert commands but likely doesn't need its own expertise section

### Workflow Context
This completes the Plan-Build-Improve expert workflow cycle:
- **Plan** (cc_hook_expert_plan): Design the hook implementation approach
- **Build** (cc_hook_expert_build): Execute the planned implementation
- **Improve** (cc_hook_expert_improve): Analyze work and update expert knowledge

The improve phase creates a feedback loop that continuously enhances expert commands based on real-world usage patterns and discoveries.

### Future Enhancements
- Could add metrics tracking (how many learnings captured over time)
- Could support analyzing specific commit ranges via arguments
- Could add ability to update other expert command sections beyond expertise
- Could integrate with CI/CD to auto-improve after successful hooks
