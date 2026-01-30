# Feature: Create prime_3.md Command for Deep 3-Level Context Loading

## Metadata
issue_number: `460`
adw_id: `feature_Tac_12_task_8_2`
issue_json: `{"number":460,"title":"[Task 8/49] [FEATURE] Create prime_3.md command file","body":"## Description\n\nCreate a deep priming command with 3 levels of exploration.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/prime_3.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_3.md.j2`\n\n## Key Features\n- 3-level deep context loading\n- Comprehensive codebase understanding\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/prime_3.md`\n\n## Wave 1 - New Commands (Task 8 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_8_2"}`

## Feature Description
Create a new slash command `/prime_3` that provides deep, comprehensive codebase context loading through a progressive 3-level exploration strategy. This command extends the basic `/prime` command with two additional exploration levels, providing agents with architectural understanding, module patterns, dependency graphs, and coding conventions without requiring the parallel agent overhead of `/scout`.

Level 1 establishes base context (via `/prime`), Level 2 adds architectural and structural understanding, and Level 3 adds deep pattern and dependency discovery. This progressive approach ensures agents have comprehensive context for complex tasks while maintaining a simple, sequential execution model.

## User Story
As a Claude Code agent
I want to execute `/prime_3` to load deep context about the codebase
So that I can understand not just the project basics, but also the architecture, module patterns, dependencies, and coding conventions before starting complex implementation tasks

## Problem Statement
The current `/prime` command loads only basic project context (README, CLAUDE.md, config.yml, constitution.md), which is sufficient for simple tasks but insufficient for complex features requiring architectural understanding. The `/scout` command provides deep exploration but uses parallel agents and requires specific search tasks. There's a gap for a sequential, comprehensive context loader that provides deeper understanding than `/prime` without the complexity of `/scout`.

Agents working on complex tasks often need to:
- Understand directory structure and module organization
- Discover architectural patterns and service boundaries
- Learn dependency relationships and import patterns
- Identify coding conventions and testing patterns

Without this context, agents may make suboptimal architectural decisions or miss important patterns.

## Solution Statement
Create a `/prime_3` command that loads context in three progressive levels:

**Level 1: Base Context**
- Execute `/prime` to load core project files (README, CLAUDE.md, config.yml, constitution.md, plan files)
- This establishes the foundational understanding of project purpose, architecture, and conventions

**Level 2: Architectural Structure**
- Use `git ls-tree` to explore directory structure and file organization
- Read key module files to understand service boundaries and major components
- Identify architectural patterns (DDD layers, service patterns, etc.)

**Level 3: Deep Patterns & Dependencies**
- Use Grep to discover common coding patterns (class definitions, decorators, imports)
- Analyze dependency relationships between modules
- Identify testing patterns and conventions
- Discover frequently-used utilities and helpers

The command will follow the same Jinja2 templating pattern as `prime.md.j2` and `prime_cc.md.j2`, using config variables for project-specific paths and commands.

## Relevant Files
Files necessary to implement the feature:

**Existing Files to Read:**
- `.claude/commands/prime.md` - Base priming command to understand Level 1 pattern
- `.claude/commands/prime_cc.md` - Extended priming for Claude Code context (pattern reference)
- `.claude/commands/scout.md` - Parallel exploration command (for comparison)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime.md.j2` - Template for prime command
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2` - Template for prime_cc command
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service that creates .claude/ structure

**Files to Modify:**
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Add 'prime_3' to commands list (line 279-331)

### New Files
- `.claude/commands/prime_3.md` - Base command file for TAC Bootstrap repository
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_3.md.j2` - Jinja2 template for CLI generation

## Implementation Plan

### Phase 1: Foundation
1. Read existing prime commands to understand the pattern and structure
2. Read scaffold_service.py to understand how commands are registered
3. Design the 3-level exploration strategy based on existing patterns

### Phase 2: Core Implementation
1. Create `.claude/commands/prime_3.md` with 3-level exploration strategy
2. Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_3.md.j2` with Jinja2 variables
3. Update `scaffold_service.py` to include 'prime_3' in commands list

### Phase 3: Integration
1. Validate that the command follows existing patterns and conventions
2. Ensure Jinja2 template uses correct config variables
3. Verify command registration in scaffold_service.py

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Read and understand existing prime command patterns
- Read `.claude/commands/prime.md` to understand base context loading
- Read `.claude/commands/prime_cc.md` to understand extended context pattern
- Read `.claude/commands/scout.md` to understand exploration approach
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime.md.j2` to understand Jinja2 variables
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2` to understand extended template pattern

### Task 2: Design 3-level exploration strategy
- Define Level 1: Execute /prime for base context
- Define Level 2: Explore architecture via directory structure and module organization
- Define Level 3: Discover patterns via grep searches for imports, classes, decorators, tests
- Document the strategy in a clear, executable format

### Task 3: Create base command file `.claude/commands/prime_3.md`
- Write command header with description
- Add Variables section (none required - uses project config)
- Add Instructions section explaining the 3-level approach
- Add Run section with commands for each level
- Add Read section with files to read at each level
- Add Understand section with what the agent should learn
- Add Examples section showing expected usage
- Add Report section with output format

### Task 4: Create Jinja2 template `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_3.md.j2`
- Convert prime_3.md to Jinja2 template
- Replace hardcoded values with config variables:
  - `{{ config.project.name }}`
  - `{{ config.project.language.value }}`
  - `{{ config.project.framework.value }}` (if exists)
  - `{{ config.project.architecture.value }}`
  - `{{ config.project.package_manager.value }}`
  - `{{ config.paths.adws_dir }}`
  - `{{ config.paths.scripts_dir }}`
  - `{{ config.paths.specs_dir }}`
  - `{{ config.paths.app_root }}`
  - `{{ config.commands.start }}`
  - `{{ config.commands.test }}`
  - `{{ config.commands.lint }}`
  - `{{ config.commands.build }}`
- Use Jinja2 conditionals for optional sections (`{% if config.paths.adws_dir %}`)

### Task 5: Register command in scaffold_service.py
- Read `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` lines 270-340
- Add 'prime_3' to the commands list (after 'prime_cc', before other commands)
- Verify the command will be processed in the loop that creates .md and .j2 files

### Task 6: Validate implementation
- Verify `.claude/commands/prime_3.md` follows the pattern of prime.md and prime_cc.md
- Verify Jinja2 template uses correct config variables matching prime.md.j2 pattern
- Verify command is registered in scaffold_service.py commands list
- Ensure command is invocable as `/prime_3` (underscore, not hyphen)

### Task 7: Run validation commands
- Execute all validation commands to ensure zero regressions
- Verify unit tests pass
- Verify linting passes
- Verify type checking passes
- Verify smoke test passes

## Testing Strategy

### Unit Tests
- **Command Registration**: Verify 'prime_3' is in the commands list in scaffold_service.py
- **Template Rendering**: Verify prime_3.md.j2 renders correctly with sample config
- **File Creation**: Verify scaffold service creates both .claude/commands/prime_3.md and the template

### Edge Cases
- **Missing Config Variables**: Template should handle missing optional variables gracefully (e.g., no framework, no adws_dir)
- **Different Project Types**: Template should work for Python/TypeScript/JavaScript projects
- **Empty Directories**: Level 2 exploration should handle empty or minimal directory structures

## Acceptance Criteria
1. **Base Command File**: `.claude/commands/prime_3.md` exists and contains:
   - Clear description of 3-level exploration strategy
   - Level 1: Execute /prime for base context
   - Level 2: Directory structure and module exploration commands
   - Level 3: Pattern discovery via grep searches
   - Report section with expected output format
   - Examples showing usage

2. **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_3.md.j2` exists and:
   - Uses config variables matching prime.md.j2 pattern
   - Has Jinja2 conditionals for optional sections
   - Renders valid markdown when processed
   - Maintains same structure as prime_3.md but with templating

3. **Command Registration**: `scaffold_service.py` includes 'prime_3' in commands list (lines 279-331)

4. **Command Invocation**: Command is accessible as `/prime_3` (underscore notation)

5. **Pattern Consistency**: Follows the same structure and conventions as prime.md and prime_cc.md

6. **Zero Regressions**: All validation commands pass successfully

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The command should provide comprehensive context without the complexity of parallel agents
- Use sequential execution (Level 1 -> Level 2 -> Level 3) for simplicity
- Pattern discovery in Level 3 should use targeted grep searches, not exhaustive scans
- The command complements `/prime` (basic) and `/scout` (parallel exploration) with a middle ground
- Consider the command successful if it provides enough context for complex implementation tasks
- Future enhancement: Could add a `/prime_5` for even deeper exploration with 5 levels
- The reference file at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/prime_3.md` was not accessible, so design is based on existing patterns in this repository
