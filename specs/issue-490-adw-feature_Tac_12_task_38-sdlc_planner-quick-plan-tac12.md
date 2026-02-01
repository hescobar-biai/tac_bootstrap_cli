# Feature: Update quick-plan.md with TAC-12 Improvements

## Metadata
issue_number: `490`
adw_id: `feature_Tac_12_task_38`
issue_json: `{"number": 490, "title": "[Task 38/49] [FEATURE] Update quick-plan.md with TAC-12 improvements", "body": "Update quick-plan.md command with COMPLETE TAC-12 implementation including scouts."}`

## Feature Description

Update the quick-plan.md command to implement complete TAC-12 improvements featuring scout-based parallel codebase exploration. The enhanced quick-plan command will deploy 3 base scout agents and 5 fast scout agents in parallel to explore the codebase before generating implementation plans. The command will also implement task-type and complexity determination, conditional plan format sections, and expand from the current 48 lines to approximately 250-300 lines.

This makes quick-plan a more powerful planning tool that combines rapid scout exploration with intelligent plan generation, positioned as a simpler alternative to plan_w_scouters (which is 477 lines).

## User Story

As a developer using TAC Bootstrap
I want quick-plan to explore the codebase in parallel using scouts
So that my implementation plans are informed by actual code patterns and architectural constraints

## Problem Statement

The current quick-plan.md command is a basic planning prompt that:
- Does NOT explore the codebase before planning
- Cannot identify relevant files or architectural patterns
- Generates generic plans without task-specific structure
- Has no concept of task type (chore vs feature vs refactor) or complexity level
- Cannot generate conditional plan sections based on task characteristics
- Is missing TAC-12 improvements that would make it significantly more powerful

This limits the quality and accuracy of generated implementation plans, requiring developers to manually discover relevant files and patterns.

## Solution Statement

Merge the scout-based workflow from plan_w_scouters.md into quick-plan.md to create a lean, powerful planning command that:

1. **Accepts simple requirements**: Takes a user prompt and analyzes it
2. **Deploys parallel scouts**: Launches 3 base scouts + 5 fast scouts in PARALLEL
   - 3 base scouts (scout-report-suggest): Architectural patterns, infrastructure, surface-level
   - 5 fast scouts (scout-report-suggest-fast): Quick parallel explorers
3. **Determines task characteristics**: Analyzes input to determine:
   - Task type: chore | feature | refactor | fix | enhancement
   - Complexity: simple | medium | complex
4. **Generates conditional plans**: Includes different sections based on task type/complexity:
   - Problem Statement (if feature OR medium/complex)
   - Solution Approach (if feature OR medium/complex)
   - Implementation Phases (if medium/complex)
   - Testing Strategy (if feature OR medium/complex)
5. **References scout findings**: Uses discovered files and patterns in the plan

The solution maintains quick-plan's simplicity (simpler than plan_w_scouters, more powerful than current version) while adding TAC-12 scout orchestration.

## Relevant Files

### Current/Template Files to Update
1. `.claude/commands/quick-plan.md` (base command file) - 48 lines
   - Frontmatter with allowed-tools, description, model
   - Purpose section
   - Variables section (USER_PROMPT, PLAN_OUTPUT_DIRECTORY)
   - Instructions section (basic planning guidance)
   - Report section (output format)

2. `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2` (template file) - 48 lines
   - Identical to base file (currently no Jinja2 variables)
   - Will be updated to mirror base with optional Jinja2 templating

### Reference Files for Scout Implementation
3. `.claude/commands/plan_w_scouters.md` (reference) - 477 lines
   - Complete scout exploration workflow (Steps 1-9)
   - Task tool parameters for Explore agents
   - Scout coordination and result aggregation
   - High-confidence file scoring algorithm
   - Conditional plan format sections
   - Graceful failure handling

### Specification Documents
4. `ai_docs/doc/plan_tasks_Tac_12_v2_UPDATED.md` - Task 38 spec at lines 485-509
   - Variables: TOTAL_BASE_SCOUT_SUBAGENTS: 3, TOTAL_FAST_SCOUT_SUBAGENTS: 5
   - Workflow steps for scout deployment
   - Task type and complexity determination
   - Conditional section logic

5. `ai_docs/doc/plan_tasks_Tac_12_v3_FINAL.md` - Comprehensive specification
   - Task 38 details with full metadata
   - Workflow context and integration points

### Related Files (for context)
6. `CLAUDE.md` - Project instructions and patterns
7. `PLAN_TAC_BOOTSTRAP.md` - Master plan reference
8. `ai_docs/doc/` - TAC course documentation

## Implementation Plan

### Phase 1: Analysis and Foundation
Understand current quick-plan implementation, plan_w_scouters reference, and TAC-12 specifications. Identify which components from plan_w_scouters should be merged into quick-plan while keeping it simpler.

### Phase 2: Update Base Command File
Modify `.claude/commands/quick-plan.md` to include:
- Updated frontmatter (add Task tool, update description)
- Enhanced Variables section (add TOTAL_BASE_SCOUT_SUBAGENTS and TOTAL_FAST_SCOUT_SUBAGENTS)
- Expanded Instructions section (scout workflow and task/complexity logic)
- Scout Exploration Workflow subsection (Steps 1-4 of plan_w_scouters pattern)
- Task Type & Complexity Determination section
- Conditional Plan Format section with adaptive sections
- Updated Plan Format with conditional sections
- Enhanced Report section

### Phase 3: Update Template File
Synchronize `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2` with base file updates. Apply Jinja2 templating only to configuration variables (if any).

### Phase 4: Validation
- Verify syntax and markdown formatting
- Check that both base and template files are synchronized
- Ensure TAC-12 specifications are fully implemented
- Confirm conditional logic matches v2_UPDATED/v3_FINAL specs

## Step by Step Tasks

### Task 1: Read and analyze current quick-plan.md
- Read the current base command file (48 lines)
- Understand the simple structure and purpose
- Note the current Variables and Instructions sections
- Identify what needs to be expanded

### Task 2: Read and analyze plan_w_scouters.md
- Read the full plan_w_scouters.md reference (477 lines)
- Extract scout configuration and workflow steps (Steps 1-9)
- Identify which sections are simple enough for quick-plan
- Note the conditional plan format logic

### Task 3: Study TAC-12 specifications
- Review plan_tasks_Tac_12_v2_UPDATED.md Task 38 section (lines 485-509)
- Review plan_tasks_Tac_12_v3_FINAL.md Task 38 section
- Verify exact variable names and scout counts (3 base + 5 fast)
- Document task type/complexity determination rules
- Document conditional section inclusion logic

### Task 4: Design updated quick-plan.md structure
- Plan the new section hierarchy
- Design scout workflow steps (simplified from plan_w_scouters but complete)
- Design task type/complexity determination logic
- Design conditional plan format sections
- Estimate new line count (~250-300 lines)
- Ensure balance between power and simplicity

### Task 5: Update frontmatter in quick-plan.md
- Change `allowed-tools` from "Read, Write, Edit, Glob, Grep" to "Task, Read, Write, Edit, Glob, Grep, WebFetch"
- Update description to mention scout-based exploration
- Keep model as claude-opus-4-1-20250805 (or verify current)

### Task 6: Expand Variables section
- Keep existing: USER_PROMPT: $ARGUMENTS, PLAN_OUTPUT_DIRECTORY: specs/
- Add: TOTAL_BASE_SCOUT_SUBAGENTS: 3
- Add: TOTAL_FAST_SCOUT_SUBAGENTS: 5

### Task 7: Rewrite Instructions section
- Add initial requirement analysis instructions
- Add section for scout exploration workflow (simplified)
- Add section for task type determination (chore|feature|refactor|fix|enhancement)
- Add section for complexity determination (simple|medium|complex)
- Add section for conditional plan format logic
- Maintain clarity and conciseness

### Task 8: Add Scout Exploration Workflow subsection
Based on plan_w_scouters.md pattern but simplified:
- Step 1: Parse user prompt to understand requirements
- Step 2: Launch 3 base scouts + 5 fast scouts in PARALLEL
  - Base Scout 1: Architectural patterns & domain logic
  - Base Scout 2: Infrastructure & integration patterns
  - Base Scout 3: Application services and workflows
  - Fast Scout 1-5: Quick surface-level pattern scans
- Step 3: Wait for scout completion and aggregate results
- Step 4: Identify high-confidence files (found by multiple scouts)
- Step 5: Extract architectural patterns and similar implementations

### Task 9: Add Task Type & Complexity Determination section
- Analyze USER_PROMPT to determine task type
- Task types: chore (simple changes), feature (new functionality), refactor (structure changes), fix (bug fixes), enhancement (improvements)
- Analyze scope/scale to determine complexity
- Complexity levels: simple (1-2 files), medium (3-5 files), complex (5+ files, architectural)
- Document rules for each determination

### Task 10: Add Conditional Plan Format section
- Document which sections are always included
- Document conditional inclusion logic:
  - Problem Statement: include if (task_type == feature) OR (complexity in [medium, complex])
  - Solution Approach: include if (task_type == feature) OR (complexity in [medium, complex])
  - Implementation Phases: include if complexity == complex
  - Testing Strategy: include if (task_type == feature) OR (complexity in [medium, complex])
- Provide template examples for each section

### Task 11: Update Plan Format section
- Add frontmatter with metadata
- Add Scout Exploration Summary section
- Add conditional sections based on task type/complexity
- Maintain clear structure with examples
- Reference scout findings in relevant sections

### Task 12: Synchronize template file
- Read the current template file
- Apply all changes from quick-plan.md to the template
- Verify structure matches exactly
- Apply Jinja2 templating only if configuration variables exist

### Task 13: Run validation checks
- Verify markdown syntax in both files
- Check that both files are synchronized
- Verify variable names match specifications (TOTAL_BASE_SCOUT_SUBAGENTS: 3, TOTAL_FAST_SCOUT_SUBAGENTS: 5)
- Verify task type and complexity rules are documented
- Verify conditional logic matches TAC-12 specs
- Check estimated line count (target: ~250-300 lines)
- Verify referenced patterns match plan_w_scouters.md

### Task 14: Verify TAC-12 compliance
Execute Validation Commands and verify:
- Both files have been updated
- Scout workflow is properly documented
- Task type/complexity determination is clear
- Conditional plan sections are properly specified
- File is ready for integration in next phase (Task 39: data_types.py)

## Testing Strategy

### Unit Tests
- Verify quick-plan.md parses correctly as YAML frontmatter
- Verify all Variables are defined and substitutable
- Verify all Instructions sections are clear and actionable
- Test Plan Format sections with various task types/complexity levels

### Edge Cases
- Test with minimal user prompts (should still generate plans)
- Test with very detailed prompts (should handle gracefully)
- Test with each task type (chore, feature, refactor, fix, enhancement)
- Test with each complexity level (simple, medium, complex)
- Test with prompts that don't clearly indicate type/complexity (should use defaults)
- Test with scout failures (should continue gracefully)

## Acceptance Criteria

1. ✅ Base file `.claude/commands/quick-plan.md` has been updated to include complete TAC-12 implementation
2. ✅ Template file `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2` is synchronized with base file
3. ✅ Both files include Variables: TOTAL_BASE_SCOUT_SUBAGENTS: 3 and TOTAL_FAST_SCOUT_SUBAGENTS: 5
4. ✅ Quick-plan includes complete scout exploration workflow (Steps 1-5 at minimum)
5. ✅ Task type determination is documented (chore|feature|refactor|fix|enhancement)
6. ✅ Complexity determination is documented (simple|medium|complex)
7. ✅ Conditional Plan Format sections are fully specified with clear inclusion rules
8. ✅ File has expanded from 48 lines to approximately 250-300 lines
9. ✅ Frontmatter includes Task tool in allowed-tools
10. ✅ Plan Format section includes all conditional sections with examples
11. ✅ Both files follow markdown and YAML formatting standards
12. ✅ File is ready for next phase: Task 39 (data_types.py SlashCommand Literal update)

## Validation Commands

Run all commands to validate implementation:

```bash
# Check markdown syntax in base file
python -c "import yaml; f=open('./.claude/commands/quick-plan.md'); yaml.safe_load(f.read().split('---')[1])" && echo "✅ Base file YAML valid"

# Check markdown syntax in template file
python -c "import yaml; f=open('./tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2'); yaml.safe_load(f.read().split('---')[1])" && echo "✅ Template file YAML valid"

# Verify Variables are defined
grep -A 5 "## Variables" ./.claude/commands/quick-plan.md | grep "TOTAL_BASE_SCOUT_SUBAGENTS" && echo "✅ Base scout count defined"
grep -A 5 "## Variables" ./.claude/commands/quick-plan.md | grep "TOTAL_FAST_SCOUT_SUBAGENTS" && echo "✅ Fast scout count defined"

# Verify Scout Exploration Workflow section exists
grep -c "Scout Exploration Workflow" ./.claude/commands/quick-plan.md && echo "✅ Scout workflow documented"

# Verify Conditional Plan Format section exists
grep -c "Conditional Plan Format" ./.claude/commands/quick-plan.md && echo "✅ Conditional format documented"

# Count lines to verify expansion
wc -l ./.claude/commands/quick-plan.md && echo "Target: ~250-300 lines"

# Verify both files are synchronized
diff ./.claude/commands/quick-plan.md <(sed 's/{{ /\${/g; s/ }}/}/g' ./tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2) && echo "✅ Files synchronized"
```

## Notes

### Architecture Alignment
- Follows TAC-12 scout-based planning pattern established in plan_w_scouters.md
- Maintains consistency with TAC Bootstrap CLI architectural patterns (DDD, service layer, template system)
- Quick-plan positioned as "lean scout-based planning" vs plan_w_scouters as "comprehensive scout-based planning"

### Scout Configuration Rationale
- 3 base scouts: Cover domain logic, infrastructure, and application services
- 5 fast scouts: Rapid parallel explorers for quick pattern detection
- 8 total scouts: Balanced parallel execution for codebase exploration without overwhelming agent coordination
- Specification source: plan_tasks_Tac_12_v2_UPDATED.md lines 485-509

### Task Type Classification
Used to determine plan depth and sections:
- **chore**: Simple housekeeping tasks (dependency updates, minor fixes)
- **feature**: New functionality requiring planning and testing
- **refactor**: Structural improvements with impact analysis
- **fix**: Bug fixes with investigation and testing
- **enhancement**: Improvements to existing features

### Complexity Classification
Used to determine sections and depth:
- **simple**: Changes to 1-2 files, straightforward implementation
- **medium**: Changes to 3-5 files, requires some architectural consideration
- **complex**: Changes to 5+ files, architectural impact, needs detailed planning

### Conditional Section Logic
- Problem Statement: Appears in plans for features and complex tasks (helps clarify scope)
- Solution Approach: Appears in plans for features and complex tasks (explains architecture)
- Implementation Phases: Only for complex tasks (helps break down large work)
- Testing Strategy: Appears in plans for features and complex tasks (ensures quality)

### Wave 6 Context
This task is Task 38 of 49 in Wave 6 (Robustify Existing Commands). It updates the quick-plan command to include complete TAC-12 scout-based planning. Task 39 will update data_types.py to add "/quick-plan" to the SlashCommand Literal.

### Dependencies
- **Previous Tasks**: Scout agents (scout-report-suggest, scout-report-suggest-fast) must be created in earlier tasks
- **Next Task**: Task 39 requires updating data_types.py to register quick-plan command
- **Reference Implementation**: `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan_w_scouters.md` (477 lines)

### Related Commands
- `/scout` - General codebase exploration
- `/plan_w_scouters` - Comprehensive scout-based planning (477 lines, 3 base scouts)
- `/quick-plan` - NEW - Lean scout-based planning (250-300 lines, 3 base + 5 fast scouts)
- `/feature` - Basic planning without scouts (legacy)
- `/plan_w_docs` - Planning with documentation exploration

### Integration Points
- Variables used by downstream tasks and templates
- Scout agent coordination follows Task orchestration pattern from TAC-10 Level 4
- Plan output format feeds into `/implement` command for execution
- Command registration in data_types.py (Task 39)
- Template synchronization ensures consistent behavior across generated projects

### Specifications Alignment
- ✅ Matches plan_tasks_Tac_12_v2_UPDATED.md Task 38 (lines 485-509)
- ✅ Matches plan_tasks_Tac_12_v3_FINAL.md Task 38
- ✅ References plan_w_scouters.md pattern (simpler version)
- ✅ Follows CLAUDE.md template guidelines
- ✅ Maintains PLAN_TAC_BOOTSTRAP.md task ordering
