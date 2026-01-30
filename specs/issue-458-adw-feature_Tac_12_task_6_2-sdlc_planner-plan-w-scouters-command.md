# Feature: Create plan_w_scouters.md command file

## Metadata
issue_number: `458`
adw_id: `feature_Tac_12_task_6_2`
issue_json: `{"number":458,"title":"[Task 6/49] [FEATURE] Create plan_w_scouters.md command file","body":"## Description\n\nCreate a planning command that uses scout subagents for codebase exploration.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/plan_w_scouters.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2`\n\n## Key Features\n- Multiple parallel scout agents\n- Both base and fast scouts\n- Comprehensive codebase analysis\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan_w_scouters.md`\n\n## Wave 1 - New Commands (Task 6 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_6_2"}`

## Documentation Exploration Summary

Based on comprehensive codebase exploration, I identified key patterns for implementing the plan_w_scouters command:

### Relevant Documentation Found

1. **Scout Command Specification** (`.claude/commands/scout.md`) - Complete implementation of parallel codebase exploration
   - Uses Task tool with subagent_type="Explore" for parallel agent launch
   - Defines SCALE parameter (2-10) controlling number of parallel strategies
   - Documents frequency-based relevance scoring for aggregated results
   - Uses model="haiku" for fast exploration execution

2. **Plan with Docs Command** (`.claude/commands/plan_w_docs.md`) - Documentation exploration before planning
   - Launches Explore agents with thoroughness="medium"
   - Sequential documentation search pattern (ai_docs → app_docs → specs)
   - Graceful degradation when documentation is missing
   - Provides structured workflow: Search → Summarize → Identify Gaps → Plan

3. **Quick Plan Command** (`.claude/commands/quick-plan.md`) - Scout-based planning workflow
   - Deploys 3 base scouts (agent-scout-report-suggest) + 5 fast scouts (agent-scout-report-suggest-fast)
   - Launches all scouts in parallel with divide-and-conquer strategy
   - Consolidates results and manually validates for missing files
   - Uses TOTAL_BASE_SCOUT_SUBAGENTS and TOTAL_FAST_SCOUT_SUBAGENTS variables

4. **Parallel Subagents Command** (`.claude/commands/parallel_subagents.md`) - General parallel orchestration pattern
   - Single message with multiple Task tool calls for parallel execution
   - Clear separation between parallel and sequential execution contexts
   - Model selection guidance (haiku for straightforward, sonnet/opus for complex)

5. **Explore Agent Documentation** (`app_docs/feature-feature_Tac_11_task_3-scout-slash-command.md`) - Agent configuration details
   - Thoroughness levels: "quick", "medium", "very thorough"
   - Read-only exploration using Glob, Grep, Read tools
   - Performance characteristics: medium thoroughness ~1-2 minutes with SCALE=4

### Documentation Gaps

- No explicit definition distinguishing "base scouts" vs "fast scouts" in terms of configuration parameters (inferred from quick-plan.md pattern)
- Limited guidance on optimal scout count for different project sizes
- No documented patterns for consolidating scout results into actionable file lists

## Feature Description

Create a slash command `/plan_w_scouters` that combines comprehensive planning with parallel scout-based codebase exploration. This command will launch multiple scout agents in parallel to explore the codebase before creating an implementation plan, ensuring all relevant files are identified and architectural patterns are understood. The command follows the proven plan_w_docs pattern but replaces sequential documentation exploration with parallel scout-based file discovery.

## User Story

As a developer creating implementation plans
I want to use multiple parallel scout agents to explore the codebase
So that I can identify all relevant files and patterns before planning, reducing the risk of missing critical dependencies or architectural constraints

## Problem Statement

The existing `/plan_w_docs` command performs sequential documentation exploration which is thorough for documentation but may miss code patterns not yet documented. The `/scout` command performs parallel codebase exploration but doesn't integrate this into the planning workflow. Developers need a planning command that combines the thoroughness of parallel scout exploration with the structured planning workflow, ensuring plans are informed by actual codebase structure, not just documentation.

## Solution Statement

Implement `/plan_w_scouters` command that:
1. Accepts issue metadata (issue_number, adw_id, issue_json) as input
2. Launches multiple parallel scout agents (configurable count) to explore the codebase using different strategies
3. Uses 2 medium/thorough base scouts + 1 quick fast scout pattern (total: 3 scouts by default)
4. Aggregates scout results to identify high-confidence files relevant to the task
5. Uses findings to inform all plan sections (Solution Statement, Implementation Plan, Relevant Files)
6. Follows the same plan format and validation as plan_w_docs
7. Exposes minimal configuration via Jinja2 template variables (project name/type, scout scale/count)

This approach leverages parallel compute for fast, comprehensive codebase understanding while maintaining the structured planning workflow that ensures implementation success.

## Relevant Files

Files needed to implement the feature:

- `.claude/commands/scout.md` - Reference implementation for parallel scout pattern and SCALE parameter behavior
- `.claude/commands/plan_w_docs.md` - Base structure for planning command with exploration workflow
- `.claude/commands/quick-plan.md` - Pattern for launching base + fast scout agents in parallel
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:279-329` - Commands list where plan_w_scouters must be registered
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_docs.md.j2` - Jinja2 template structure to follow

### New Files

- `.claude/commands/plan_w_scouters.md` - Base command file in repository
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2` - Jinja2 template for CLI generation

## Implementation Plan

### Phase 1: Foundation
- Read and analyze reference files (scout.md, plan_w_docs.md, quick-plan.md) to extract patterns
- Design command structure following plan_w_docs but replacing documentation exploration with scout-based exploration
- Define scout configuration: 2 base scouts (medium thoroughness) + 1 fast scout (quick thoroughness)

### Phase 2: Core Implementation
- Create `.claude/commands/plan_w_scouters.md` with complete command specification
- Implement workflow: Parse Input → Launch Parallel Scouts → Aggregate Results → Create Plan → Save & Report
- Define strategy-specific prompts for base and fast scouts with divide-and-conquer approach
- Create Jinja2 template `plan_w_scouters.md.j2` with config variable interpolation

### Phase 3: Integration
- Update `scaffold_service.py` to include "plan_w_scouters" in commands list (after "plan_w_docs")
- Validate template syntax and config variable usage follows existing patterns
- Ensure graceful degradation when scouts fail (continue with partial results)

## Step by Step Tasks

### Task 1: Create Base Command File (.claude/commands/plan_w_scouters.md)

- Add frontmatter with allowed-tools and description
- Define variables section: issue_number ($1), adw_id ($2), issue_json ($3)
- Implement Instructions section emphasizing RELATIVE path usage and scout-based exploration
- Create Scout Exploration Workflow section with 3 parallel scouts:
  - Base Scout 1: Architectural patterns and domain logic exploration (medium thoroughness)
  - Base Scout 2: Infrastructure and integration patterns (medium thoroughness)
  - Fast Scout: Quick surface-level scan for obvious patterns (quick thoroughness)
- Define workflow steps: Parse Input → Launch Scouts → Aggregate → Plan → Save
- Add graceful handling for scout failures
- Include Relevant Files section listing key project files
- Define Plan Format matching plan_w_docs but with "Scout Exploration Summary" instead of "Documentation Exploration Summary"
- Add Report section with CRITICAL OUTPUT FORMAT requirements
- Include examples showing usage patterns

### Task 2: Create Jinja2 Template (templates/claude/commands/plan_w_scouters.md.j2)

- Copy structure from plan_w_scouters.md
- Replace hardcoded values with Jinja2 config variables:
  - `{{ config.project.name }}` for project name
  - `{{ config.project.type }}` for project type
  - `{{ config.paths.specs_dir }}` for specs directory
  - `{{ config.paths.app_root }}` for application root (conditional)
  - `{{ config.commands.install }}` for install command
  - `{{ config.commands.test }}` for test command
  - `{{ config.commands.lint }}` for lint command
  - `{{ config.commands.typecheck }}` for type check command
- Add optional scout configuration variables with defaults:
  - `{{ config.scout.default_scale | default('medium') }}` for scout thoroughness
  - `{{ config.scout.parallel_count | default(3) }}` for total scout count
- Validate template renders correctly with test config

### Task 3: Update Scaffold Service Command Registration

- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate commands list in `_add_claude_files` method (around line 279)
- Add "plan_w_scouters" to commands list after "plan_w_docs" entry
- Ensure indentation and formatting matches existing entries
- Verify comment grouping (should be in "# TAC-12: Enhanced planning commands" section)

### Task 4: Validate Implementation

- Read generated `.claude/commands/plan_w_scouters.md` to verify structure
- Read `plan_w_scouters.md.j2` template to verify Jinja2 syntax
- Check `scaffold_service.py` includes "plan_w_scouters" in commands list
- Verify file locations match specification:
  - Base: `.claude/commands/plan_w_scouters.md`
  - Template: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2`
- Confirm config variable usage follows existing template patterns
- Validate workflow steps are clear and actionable

## Testing Strategy

### Unit Tests

No unit tests required for this task as it involves:
1. Creating markdown command files (not executable code)
2. Creating Jinja2 templates (validated by template engine)
3. Updating static command list in scaffold service

Validation will be performed through:
- File existence checks
- Template syntax validation (Jinja2 will error on invalid syntax)
- Manual review of generated content structure

### Edge Cases

- Scout agents fail to complete: Command should continue with partial results and log warning
- No files discovered by scouts: Command should still create plan with warning about limited findings
- Issue JSON missing or malformed: Command should abort with clear error message
- Specs directory doesn't exist: Write tool will fail appropriately with file system error

## Acceptance Criteria

1. Base command file `.claude/commands/plan_w_scouters.md` exists and contains:
   - Frontmatter with allowed-tools: Task, Read, Glob, Grep, WebFetch
   - Variables section accepting issue_number, adw_id, issue_json
   - Scout Exploration Workflow launching 3 parallel scouts (2 base + 1 fast)
   - Plan Format matching plan_w_docs structure with scout-specific sections
   - Report section with CRITICAL OUTPUT FORMAT requirements

2. Jinja2 template `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2` exists and contains:
   - All config variable interpolations using {{ config.* }} syntax
   - Default values for optional scout configuration
   - Conditional rendering for optional paths (app_root, commands)
   - Valid Jinja2 syntax (no template errors)

3. Scaffold service updated:
   - `scaffold_service.py` includes "plan_w_scouters" in commands list
   - Entry appears after "plan_w_docs" in TAC-12 section
   - Formatting matches existing command entries

4. Template variables follow existing schema:
   - Uses config.project.name, config.project.type
   - Uses config.paths.specs_dir for specs location
   - Uses config.commands.* for command references
   - Optional scout config with sensible defaults

5. Command functionality:
   - Launches scouts in parallel (single message with multiple Task calls)
   - Uses Task tool with subagent_type="Explore"
   - Aggregates scout results before planning
   - Creates plan file with RELATIVE path
   - Returns only the relative path (machine-parsable output)

## Validation Commands

Run all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test CLI
- `cat .claude/commands/plan_w_scouters.md` - Verify base file exists and has correct structure
- `cat tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2` - Verify template exists
- `grep -n "plan_w_scouters" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Verify registration

## Notes

### Implementation References

- The `/scout` command (scout.md) provides the foundation for parallel agent launching and result aggregation
- The `/plan_w_docs` command provides the planning workflow structure and report format
- The `/quick-plan` command demonstrates the base + fast scout pattern (3 base + 5 fast)
- For this command, we use a lighter 2 base + 1 fast scout pattern to balance thoroughness with cost

### Scout Configuration Rationale

**Why 2 base + 1 fast scout pattern?**
- Base scouts (medium thoroughness): Deep analysis of architectural patterns and implementation details
- Fast scout (quick thoroughness): Rapid surface-level scan for obvious patterns and quick wins
- Total of 3 scouts balances comprehensive coverage with reasonable execution time (~1-2 minutes)
- Can be overridden via config.scout.parallel_count if users need more/less coverage

**Thoroughness Levels:**
- Base scouts use "medium" thoroughness (standard for exploration tasks)
- Fast scout uses "quick" thoroughness (rapid initial scan)
- Users can customize via config.scout.default_scale template variable

### Divide and Conquer Strategy

Each scout should receive different exploration direction:
- Base Scout 1: Focus on domain logic, business rules, service layer
- Base Scout 2: Focus on infrastructure, data access, integrations
- Fast Scout: Broad surface scan across all layers for quick pattern identification

### Template Variable Design

Minimal template exposure keeps implementation details in command logic:
- Expose: project.name, project.type (vary per project)
- Expose: scout.default_scale, scout.parallel_count (may need tuning)
- Hardcode: scout strategies, aggregation logic, workflow steps (implementation details)

### Future Enhancements

- Support for scout strategy customization via additional config variables
- Integration with /implement to auto-feed discovered high-confidence files
- Caching of scout results to avoid re-exploring same prompts
- Advanced aggregation with ML-based relevance scoring beyond frequency

### Related Commands

- `/scout` - General-purpose parallel codebase exploration (no planning)
- `/plan_w_docs` - Planning with sequential documentation exploration
- `/quick-plan` - Fast planning with 8 parallel scouts (3 base + 5 fast)
- `/feature` - Basic planning without exploration (legacy)

### Reference File Status

Attempted to read reference file at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan_w_scouters.md` but path was inaccessible. Implementation based on analysis of scout.md, plan_w_docs.md, and quick-plan.md patterns which provide sufficient context for creating a working implementation.
