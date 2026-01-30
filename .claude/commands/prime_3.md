# Prime 3 - Deep Context Loading

Load comprehensive codebase context through a progressive 3-level exploration strategy.

## Variables

None required - this command uses project configuration from TAC Bootstrap.

## Instructions

**Purpose:**
This command provides deep, comprehensive codebase understanding through three progressive exploration levels. It extends `/prime` with architectural analysis and pattern discovery, giving agents the context needed for complex implementation tasks without requiring parallel agent orchestration.

**Exploration Strategy:**
- **Level 1 (Base Context)**: Execute `/prime` to load project fundamentals
- **Level 2 (Architectural Structure)**: Explore directory structure, module organization, and service boundaries
- **Level 3 (Deep Patterns)**: Discover coding patterns, dependencies, testing conventions, and common utilities

**When to Use:**
- Before implementing complex features requiring architectural understanding
- When you need to understand module patterns and dependencies
- For tasks that will touch multiple parts of the codebase
- When you want comprehensive context without the complexity of `/scout`

**When NOT to Use:**
- For simple, single-file tasks (use `/prime` instead)
- When you need parallel exploration with custom search strategies (use `/scout` instead)
- For quick orientation (use `/prime` or `/prime_cc` instead)

## Run

### Level 1: Base Context

1. **Execute /prime command:**
   - Read and execute `.claude/commands/prime.md` top to bottom
   - This loads: README, CLAUDE.md, config.yml, constitution.md, plan files
   - Establishes project purpose, architecture, and development conventions

### Level 2: Architectural Structure

2. **Explore directory structure:**
   ```bash
   git ls-tree -r --name-only HEAD | head -100
   ```
   - Understand overall project organization
   - Identify main directories and their purposes
   - Note module groupings and architectural layers

3. **List key directories:**
   ```bash
   find . -type d -maxdepth 3 ! -path "*/\.*" ! -path "*/node_modules/*" ! -path "*/venv/*" ! -path "*/__pycache__/*" | sort
   ```
   - Map directory hierarchy
   - Identify architectural boundaries (domain, application, infrastructure, etc.)
   - Understand module organization patterns

### Level 3: Deep Patterns & Dependencies

4. **Discover class and function definitions:**
   - Use Grep tool with pattern: `^class |^def |^function |^export (class|function)`
   - Parameters: `output_mode: "files_with_matches"`, `-i: false`
   - Identify key modules and their components
   - Note frequently-used base classes or utilities

5. **Analyze import patterns:**
   - Use Grep tool with pattern: `^import |^from .* import|^require\(|^export .*from`
   - Parameters: `output_mode: "files_with_matches"`
   - Understand dependency relationships between modules
   - Identify commonly-imported utilities and helpers

6. **Find test patterns:**
   - Use Glob tool with pattern: `**/*test*.py` or `**/*test*.ts` or `**/*.spec.*` (based on language)
   - Understand testing conventions and structure
   - Note test utilities and fixtures

7. **Identify decorators and annotations:**
   - Use Grep tool with pattern: `@[A-Za-z]|# type:|: [A-Z][a-zA-Z]*\[`
   - Parameters: `output_mode: "files_with_matches"`
   - Discover common decorators, type hints, and annotations
   - Understand coding patterns and conventions

## Read

### Level 1 Files (from /prime)
- README.md
- CLAUDE.md
- PLAN_TAC_BOOTSTRAP.md (or equivalent plan file)
- config.yml
- constitution.md
- adws/README.md (if exists)

### Level 2 Files (Architectural Understanding)
- Main application entry point (main.py, index.ts, app.py, etc.)
- Top-level __init__.py or index files in main directories
- Key module README files (if they exist)
- Package configuration files (pyproject.toml, package.json, etc.)

### Level 3 Files (Pattern Discovery)
- Base classes, abstract classes, or interfaces (identified via grep)
- Common utility modules (utils.py, helpers.ts, common/*, shared/*)
- Configuration or constants files (config.py, constants.ts, settings/*)
- Key test fixtures or test utilities (conftest.py, test_helpers.ts)

## Understand

### After Level 1: Base Context
You should understand:
- Project name, language, framework, and architecture
- Development commands (start, test, lint, build)
- High-level project goals and structure
- Constitutional principles and coding standards
- Active development plan and current tasks

### After Level 2: Architectural Structure
You should understand:
- Directory organization and module groupings
- Architectural layers (if using DDD, MVC, etc.)
- Main application components and their locations
- Service boundaries and module responsibilities
- Package/dependency management approach

### After Level 3: Deep Patterns & Dependencies
You should understand:
- Common coding patterns and conventions
- Frequently-used base classes and utilities
- Import patterns and module dependencies
- Testing patterns and test organization
- Decorators, annotations, and type usage patterns
- Shared helpers and utility functions

### Architectural Patterns to Identify

**Domain-Driven Design (DDD):**
- `domain/` - Models, entities, value objects
- `application/` - Services, use cases
- `infrastructure/` - External integrations, persistence
- `interfaces/` - API, CLI, controllers

**Model-View-Controller (MVC):**
- `models/` - Data models
- `views/` - Templates, UI components
- `controllers/` - Request handlers

**Layered Architecture:**
- `core/` or `lib/` - Core business logic
- `services/` - Application services
- `api/` or `routes/` - API endpoints
- `db/` or `data/` - Data access layer

## Examples

### Example 1: Basic Usage
```
User: /prime_3
Agent: Executing Level 1: Base Context...
       Running /prime command...
       [loads README, CLAUDE.md, config.yml, constitution.md, PLAN]

       Project: tac-bootstrap (Python/DDD/uv)

       Executing Level 2: Architectural Structure...
       Exploring directory structure...
       Found DDD structure: domain/, application/, infrastructure/, interfaces/
       Reading main entry points...

       Executing Level 3: Deep Patterns & Dependencies...
       Discovering class definitions...
       Found 45 classes across 23 files
       Analyzing import patterns...
       Common imports: Pydantic models, Typer CLI, Rich console
       Checking test patterns...
       Found pytest-based tests in tests/ directory

       Summary:
       - Project: tac-bootstrap CLI generator
       - Architecture: DDD with 4 layers
       - 45+ classes, 23+ modules
       - Testing: pytest with 80+ tests
       - Common patterns: Pydantic models, Typer commands, Jinja2 templates

       Ready for complex implementation tasks.
```

### Example 2: Understanding Gained
```
After /prime_3, agent knows:
  ✓ Project basics (name, language, architecture, commands)
  ✓ Directory structure and module organization
  ✓ DDD layers: domain, application, infrastructure, interfaces
  ✓ Key classes: ProjectConfig, ScaffoldService, TemplateEngine
  ✓ Common patterns: Pydantic validation, Rich output, Typer CLI
  ✓ Test structure: pytest in tests/ directory
  ✓ Dependencies: Pydantic, Typer, Jinja2, Rich, PyYAML
  ✓ Ready to implement features across multiple modules
```

### Example 3: Planning After Prime 3
```
User: /prime_3
Agent: [executes all 3 levels]

       Context loaded. Ready for implementation planning.

User: Add a new validation service
Agent: Based on prime_3 context, I understand:
       - New service should go in application/ layer (DDD pattern)
       - Should use Pydantic for validation (common pattern)
       - Should follow existing service patterns (ScaffoldService, DetectionService)
       - Tests should go in tests/application/
       - Should integrate with Rich for output

       I'll create application/validation_service.py following these patterns...
```

## Report

Report to the user:

**Level 1 Summary:**
- Project name and key characteristics
- Development commands available
- Constitutional principles loaded
- Current development state

**Level 2 Summary:**
- Directory structure and organization
- Architectural pattern identified (DDD, MVC, Layered, etc.)
- Main modules and their locations
- Key entry points and package structure

**Level 3 Summary:**
- Number of classes/functions discovered
- Common coding patterns identified
- Import patterns and dependencies
- Testing conventions and structure
- Frequently-used utilities and helpers

**Overall Readiness:**
- Comprehensive context loaded
- Ready for complex implementation tasks
- Architectural patterns understood
- Coding conventions identified

**Format:**
```
Prime 3 context loaded for: tac-bootstrap

Level 1: Base Context
  ✓ Project: tac-bootstrap (Python/DDD/uv)
  ✓ README, CLAUDE.md, config.yml, constitution.md loaded
  ✓ Commands: uv run tac-bootstrap, uv run pytest, uv run ruff, uv run mypy

Level 2: Architectural Structure
  ✓ Directory structure: DDD with domain/, application/, infrastructure/, interfaces/
  ✓ Main modules: {list key modules}
  ✓ Entry point: tac_bootstrap_cli/tac_bootstrap/cli/main.py
  ✓ Package manager: uv with pyproject.toml

Level 3: Deep Patterns & Dependencies
  ✓ {N} classes across {M} files
  ✓ Common patterns: Pydantic models, Typer commands, Rich console output
  ✓ Key utilities: {list common utilities}
  ✓ Testing: pytest with {N} tests
  ✓ Common imports: Pydantic, Typer, Jinja2, Rich, PyYAML

Architectural Understanding:
  - Domain Layer: {describe}
  - Application Layer: {describe}
  - Infrastructure Layer: {describe}
  - Interfaces Layer: {describe}

Common Patterns Identified:
  - {pattern 1}
  - {pattern 2}
  - {pattern 3}

Ready for complex implementation tasks with full architectural context.
Constitution principles and coding standards loaded.
```

## Notes

**Progressive Loading:**
Each level builds on the previous one. Level 1 provides foundation, Level 2 adds structure, Level 3 adds patterns. This progressive approach ensures you understand "why" (purpose) before "how" (architecture) before "what" (patterns).

**Comparison to Other Commands:**
- `/prime` - Quick, basic context loading (Level 1 only)
- `/prime_cc` - Claude Code-specific optimizations (Level 1 + tooling)
- `/prime_3` - Deep architectural and pattern understanding (Level 1 + 2 + 3)
- `/scout` - Parallel exploration with custom search strategies (different use case)

**Performance:**
- Level 1: ~30 seconds (executes /prime)
- Level 2: ~30 seconds (directory exploration, key file reads)
- Level 3: ~60 seconds (pattern discovery via grep/glob)
- Total: ~2 minutes for comprehensive context

**Best Practices:**
1. Use `/prime_3` at the start of complex implementation sessions
2. Results give you enough context to plan multi-file changes
3. Combine with `/scout` if you need task-specific file discovery
4. Re-run if project structure has significantly changed

**Limitations:**
- Does not execute code or run dynamic analysis
- May miss runtime-only patterns or dynamically loaded modules
- Grep-based pattern discovery is static code analysis only
- Large codebases (>1000 files) may take longer

**Future Enhancements:**
- Cache results to avoid re-exploration in same session
- Add `/prime_5` with even deeper exploration (5 levels)
- Support for language-specific pattern detection
- Integration with code analysis tools (AST parsing)
