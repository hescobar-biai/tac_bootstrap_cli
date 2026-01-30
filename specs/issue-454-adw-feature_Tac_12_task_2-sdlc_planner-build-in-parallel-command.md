# Feature: Create build_in_parallel.md Command File

## Metadata
issue_number: `454`
adw_id: `feature_Tac_12_task_2`
issue_json: `{"number":454,"title":"[Task 2/49] [FEATURE] Create build_in_parallel.md command file","body":"## Description\n\nCreate a slash command for parallel build operations using build-agent subagents. Based on real TAC-12 implementation with detailed file specifications.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/build_in_parallel.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_in_parallel.md.j2`\n\n## Key Features\n- Uses `.claude/agents/build-agent.md` subagent\n- Model: claude-sonnet-4-5-20250929\n- 8-step workflow with detailed file specifications\n- Parallel batch execution pattern\n- Comprehensive reporting format\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/build_in_parallel.md`\n\n## Wave 1 - New Commands (Task 2 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_2"}`

## Feature Description

This feature implements a slash command `/build_in_parallel` that enables parallel build operations across multiple components or modules. The command orchestrates parallel execution by spawning multiple specialized `build-agent` subagents, each handling a specific build target. This approach dramatically reduces total build time for multi-component projects while maintaining comprehensive error tracking and reporting.

The command implements an 8-step workflow that:
1. Identifies all buildable targets in the project
2. Groups targets into logical batches based on dependencies
3. Spawns parallel build-agent instances using Claude Code's Task tool
4. Monitors execution progress across all parallel builds
5. Collects results from each build agent
6. Aggregates errors and issues across all builds
7. Generates a comprehensive markdown report
8. Exits with appropriate status code

The implementation leverages the reference file from TAC-12 project, which has proven this pattern in production use.

## User Story

As a **developer working on a multi-component project**
I want to **build multiple targets in parallel automatically**
So that **I can drastically reduce total build time and quickly identify all build failures across the entire codebase**

## Problem Statement

Modern projects often consist of multiple buildable components (microservices, libraries, frontend/backend, etc.) that can be built independently. Building these sequentially is inefficient and time-consuming. Additionally, sequential builds may hide failures in later components, requiring multiple build cycles to discover all issues. Developers need a way to:

- Build multiple independent targets simultaneously
- Minimize total build time through parallelization
- Get comprehensive visibility into all build failures at once
- Control parallelism to avoid resource exhaustion
- Maintain detailed logs and reports for debugging

The standard `/build` command handles single targets well, but lacks orchestration capabilities for parallel multi-target scenarios.

## Solution Statement

The `/build_in_parallel` command solves this by implementing a sophisticated orchestration layer on top of specialized build-agent subagents. The solution:

1. **Auto-discovery**: Automatically identifies all buildable targets in the project
2. **Smart batching**: Groups targets by dependency layers to maximize safe parallelism
3. **Parallel execution**: Launches multiple build-agents concurrently using Claude Code's Task tool
4. **Fail-through behavior**: Continues all builds even if some fail, providing complete visibility
5. **Comprehensive reporting**: Aggregates results with timing metrics, error details, and recommendations
6. **Resource control**: Configurable concurrency limits to prevent system overload

By delegating individual file builds to specialized agents while maintaining centralized orchestration, the command achieves both speed and reliability.

## Relevant Files

### Existing Files

- **/.claude/commands/build.md** (line 1-26)
  - Provides reference for single-target build command structure
  - Shows standard command markdown format and variables usage

- **tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2** (line 1-30)
  - Template example showing Jinja2 variable usage: `{{ config.commands.build }}`
  - Demonstrates conditional rendering and command templating patterns

- **tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py** (line 279-324)
  - Commands list registration at lines 279-324
  - Pattern: each command added to list, then file created via template in loop at 326-332
  - Need to add `"build_in_parallel"` to this list

- **/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/build_in_parallel.md**
  - **Reference implementation** - proven workflow from production TAC-12 project
  - Contains complete 8-step workflow with detailed instructions
  - Includes build-agent specification format and parallel execution patterns
  - Critical source for accurate implementation

### New Files

- **.claude/commands/build_in_parallel.md**
  - Base command file for TAC Bootstrap repository
  - Direct copy from TAC-12 reference with minimal adaptations
  - Serves as template source for CLI generation

- **tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_in_parallel.md.j2**
  - Jinja2 template for generating command in scaffolded projects
  - Based on base file with templated variables:
    - `{{ config.model.name }}` for model specification
    - `{{ config.project.name }}` for project context
    - Optional: `{{ config.agents.build_agent_path }}` if path varies
  - Workflow steps remain static (TAC methodology)

## Implementation Plan

### Phase 1: Foundation (Reference Acquisition)

Read and analyze the reference implementation from TAC-12 to understand:
- Complete workflow structure and step-by-step instructions
- Build-agent specification format (how to provide context to subagents)
- Parallel execution patterns (batching strategy, Task tool usage)
- Reporting format (markdown structure, metrics, error aggregation)
- Error handling approach (fail-through vs fail-fast)

This phase ensures we accurately replicate the proven implementation.

### Phase 2: Core Implementation (Base File Creation)

Create the base command file `.claude/commands/build_in_parallel.md` by:
1. Copying content from TAC-12 reference file
2. Adapting any TAC-12-specific paths or references to be generic
3. Ensuring model specification uses `claude-sonnet-4-5-20250929`
4. Verifying all 8 workflow steps are complete and detailed
5. Confirming build-agent specification format is comprehensive

### Phase 3: Template Creation (Jinja2 Templating)

Create the Jinja2 template `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_in_parallel.md.j2` by:
1. Starting from the base file created in Phase 2
2. Identifying configuration values to template:
   - Model name: `{{ config.model.name }}`
   - Project name references: `{{ config.project.name }}`
   - Build agent path (if needed): `{{ config.agents.build_agent_path }}`
3. Keeping workflow instructions static (TAC methodology)
4. Following existing template patterns from `build.md.j2`

### Phase 4: Integration (Scaffold Service Update)

Update `scaffold_service.py` to register the new command:
1. Add `"build_in_parallel"` to commands list (line ~323, maintain alphabetical order)
2. Verify the existing loop at lines 326-332 will automatically create the file
3. No additional changes needed - leverages existing infrastructure

## Step by Step Tasks

### Task 1: Read TAC-12 Reference Implementation
- Read the file `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/build_in_parallel.md`
- Analyze the 8-step workflow structure
- Understand build-agent specification format
- Note parallel execution patterns and Task tool usage
- Document reporting format and error handling approach

### Task 2: Create Base Command File
- Create `.claude/commands/build_in_parallel.md`
- Copy content from TAC-12 reference file
- Adapt TAC-12-specific references to be generic/TAC Bootstrap appropriate
- Ensure model is `claude-sonnet-4-5-20250929` in frontmatter
- Verify workflow completeness and clarity
- Add markdown frontmatter with:
  ```yaml
  ---
  model: claude-sonnet-4-5-20250929
  description: Build the codebase in parallel by delegating file creation to build-agents
  argument-hint: [path-to-plan]
  ---
  ```

### Task 3: Create Jinja2 Template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_in_parallel.md.j2`
- Start from base file content
- Template model name: `model: {{ config.model.name }}`
- Template project-specific paths if present
- Keep workflow steps static
- Follow patterns from existing templates like `build.md.j2`
- Ensure proper Jinja2 syntax and conditionals

### Task 4: Update Scaffold Service
- Edit `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate commands list (around line 279-324)
- Add `"build_in_parallel"` to the list
- Maintain alphabetical/logical ordering
- Verify existing loop (lines 326-332) handles new command
- Do NOT modify loop - existing infrastructure is sufficient

### Task 5: Validation
- Run validation commands to ensure no regressions
- Verify files are created correctly
- Check template rendering works
- Ensure command appears in scaffold service list
- **Execute all validation commands** (see Validation Commands section)

## Testing Strategy

### Unit Tests

No new unit tests required for this task. This is a file creation task, not code implementation. Testing is via validation commands.

### Manual Testing

1. **Template Rendering Test**
   - Generate a test project using `tac-bootstrap`
   - Verify `.claude/commands/build_in_parallel.md` is created
   - Check file content matches expected format
   - Confirm Jinja2 variables are properly rendered

2. **Command Execution Test** (if build-agent exists)
   - Navigate to generated project
   - Run `/build_in_parallel <test-plan>`
   - Verify parallel execution occurs
   - Check report format and completeness

### Edge Cases

1. **Missing build-agent.md**
   - Command should check for `.claude/agents/build-agent.md`
   - Provide clear error message if missing
   - Direct user to create it or run setup

2. **Single target project**
   - Command should handle single-target gracefully
   - No parallelization needed, but workflow should complete
   - Report should still be generated

3. **All builds fail**
   - Ensure all failures are collected
   - Exit with non-zero status
   - Report should show all errors

4. **Resource limits**
   - Concurrency parameter should be respected
   - Default of 4 parallel agents is conservative
   - Users can override via --concurrency flag

## Acceptance Criteria

- [ ] Base command file `.claude/commands/build_in_parallel.md` exists
- [ ] Content matches TAC-12 reference implementation workflow
- [ ] Frontmatter includes model `claude-sonnet-4-5-20250929` and description
- [ ] 8-step workflow is complete and detailed
- [ ] Build-agent specification format is comprehensive
- [ ] Jinja2 template `.../build_in_parallel.md.j2` exists
- [ ] Template uses `{{ config.model.name }}` for model
- [ ] Workflow steps are static (not templated)
- [ ] `scaffold_service.py` includes `"build_in_parallel"` in commands list
- [ ] All validation commands pass with zero regressions
- [ ] Generated projects include the command file
- [ ] Template renders correctly in test scaffolding

## Validation Commands

Execute all commands to validate with zero regressions:

```bash
# Unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help

# Verify new command in scaffold service
cd tac_bootstrap_cli && grep -n "build_in_parallel" tac_bootstrap/application/scaffold_service.py

# Verify template exists
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_in_parallel.md.j2

# Verify base file exists
ls -la .claude/commands/build_in_parallel.md
```

## Notes

### Design Decisions

1. **Direct Copy from TAC-12**: Using proven implementation reduces risk and ensures quality
2. **Minimal Templating**: Workflow steps are TAC methodology, should remain consistent across projects
3. **Leverage Existing Infrastructure**: No changes to scaffold service loop needed
4. **Build-agent Dependency**: This command assumes build-agent.md exists (likely created in Task 1)

### Future Enhancements

- Add build caching support to avoid rebuilding unchanged targets
- Implement dependency graph analysis for smarter batching
- Add --dry-run flag to preview what would be built
- Support custom build-agent configurations per target type
- Add metrics export for build performance tracking

### Dependencies

- Requires `.claude/agents/build-agent.md` to exist (likely Wave 1 Task 1)
- Depends on Claude Code Task tool for parallel agent spawning
- Uses model `claude-sonnet-4-5-20250929` for orchestration

### TAC-12 Integration Context

This is Task 2 of 49 in the TAC-12 integration project, specifically Wave 1 (New Commands). Wave 1 focuses on adding new slash commands that exist in TAC-12 but not in TAC Bootstrap. This command is particularly valuable as it demonstrates:
- Advanced agent orchestration patterns
- Parallel execution best practices
- Comprehensive error handling and reporting
- Real-world proven workflow from production use

The successful implementation of this command provides a template for other Wave 1 command additions.
