# Constitution Principles in /prime Command

**ADW ID:** f7606da7
**Date:** 2026-01-21
**Specification:** specs/issue-66-adw-f7606da7-sdlc_planner-constitution-principios-prime.md

## Overview

Extended the `/prime` command in TAC Bootstrap CLI to generate a comprehensive `constitution.md` file that defines project-specific governing principles across five key areas: coding standards, testing requirements, architectural guidelines, UX/DX patterns, and performance expectations. This constitution serves as a single source of truth for development decisions and code review standards.

## What Was Built

- **Constitution Template**: 909-line Jinja2 template (`constitution.md.j2`) with parametrizable content
- **Prime Command Integration**: Modified `/prime` command to include constitution generation
- **Conditional Documentation**: Added constitution to conditional documentation guide
- **Language-Specific Content**: Support for Python, TypeScript/JavaScript, Go, Rust, and Java
- **Framework-Specific Patterns**: Integration with FastAPI, Next.js, Gin, Axum, Spring Boot
- **Architecture-Specific Guidelines**: DDD, Clean, Hexagonal, Layered, Simple architectures

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime.md.j2`: Added constitution.md to files to read, included constitution principles in report
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/conditional_docs.md.j2`: Added constitution.md with conditions for when to reference it (code writing, testing, architecture, UX/DX, performance)

### Files Created

- `tac_bootstrap_cli/tac_bootstrap/templates/structure/constitution.md.j2`: Complete 909-line constitution template with five major sections

### Key Changes

1. **Constitution Template Structure**: Created comprehensive template with five main sections:
   - **Coding Principles**: Language-specific style guides (PEP 8, Airbnb JS, gofmt, rustfmt, Checkstyle), framework patterns, anti-patterns to avoid, naming conventions
   - **Testing Standards**: Coverage requirements, test types (unit/integration/e2e), mocking strategies, test organization patterns, framework-specific test tools
   - **Architecture Guidelines**: Folder structure based on architecture type (DDD, Clean, Hexagonal, Layered, Simple), separation of concerns, dependency rules, allowed dependencies
   - **UX/DX Guidelines**: Error handling patterns, user messaging standards, logging guidelines, documentation requirements, CLI/API formatting
   - **Performance Expectations**: Latency limits, optimization requirements, profiling guidelines, caching strategies, database query optimization

2. **Parametrization with Config Variables**: Template uses `{{ config.* }}` variables to adapt content based on:
   - `config.project.language.value`: python, typescript, javascript, go, rust, java
   - `config.project.framework.value`: fastapi, nextjs, gin, axum, spring, none
   - `config.project.architecture.value`: simple, layered, ddd, clean, hexagonal
   - `config.project.package_manager.value`: uv, poetry, pnpm, npm, cargo, go, maven
   - `config.commands.*`: start, test, lint, typecheck, format, build

3. **Prime Command Integration**: Modified prime.md.j2:21 to include constitution.md in files to read, and prime.md.j2:74-79 to report constitution principles loaded

4. **Conditional Documentation**: Added constitution.md to conditional_docs.md.j2:26-32 with specific triggers for code writing, testing, architecture decisions, UX/DX work, and performance optimization

## How to Use

### Generating Constitution

1. Create or update a project with TAC Bootstrap CLI:
   ```bash
   cd tac_bootstrap_cli && uv run tac-bootstrap init my-project
   ```

2. Run the `/prime` command in the generated project:
   ```bash
   /prime
   ```

3. The `constitution.md` file will be generated in the project root with content customized to your project's language, framework, and architecture

### Referencing Constitution

The constitution is automatically included in:
- `/prime` - Loads constitution principles into context
- `/review` - References constitution during code review
- `/implement` - Uses constitution guidelines during implementation

Conditional documentation triggers constitution reading when:
- Writing or reviewing code (coding style and patterns)
- Writing tests (testing standards)
- Making architectural decisions (architecture guidelines)
- Handling errors or user-facing messages (UX/DX guidelines)
- Optimizing or investigating performance (performance expectations)

## Configuration

The constitution template adapts based on `config.yml` settings:

```yaml
project:
  name: "my-project"
  language: python          # python, typescript, javascript, go, rust, java
  framework: fastapi        # fastapi, nextjs, gin, axum, spring, none
  architecture: ddd         # simple, layered, ddd, clean, hexagonal
  package_manager: uv       # uv, poetry, pnpm, npm, cargo, go, maven

commands:
  test: "pytest tests/ -v"
  lint: "ruff check ."
  format: "ruff format ."
  typecheck: "mypy ."
```

## Testing

The feature includes comprehensive validation across different configurations:

```bash
# Run unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Run linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test CLI
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Test constitution generation with different language/framework combinations:
- Python + FastAPI + DDD
- TypeScript + Next.js + Clean Architecture
- Go + Gin + Hexagonal
- Rust + Axum + Layered
- Java + Spring Boot + Simple

## Notes

### Design Decisions

1. **Opinionated but Contextual**: The constitution provides specific, actionable guidance adapted to the project's technology stack rather than generic advice

2. **Single Source of Truth**: By generating constitution during `/prime`, it becomes available to all subsequent commands for reference

3. **Comprehensive Coverage**: Five sections ensure all major development concerns are addressed (code style, testing, architecture, UX/DX, performance)

4. **Framework Integration**: Constitution references project-specific commands from config (test, lint, format) to maintain consistency

### Constitution Content Examples

**Python + FastAPI + DDD:**
- PEP 8 style guide with type hints
- FastAPI dependency injection patterns
- DDD ubiquitous language and aggregates
- Pytest with 80% coverage requirement
- API latency <200ms for p95

**TypeScript + Next.js + Clean:**
- Strict mode, no `any` type
- Server Components default, client when needed
- Dependency rule (inner layers don't depend on outer)
- Jest + React Testing Library
- Build time <60s, page load <1s

### Future Enhancements

- Custom constitution sections via config
- Monorepo support with multiple languages
- Constitution version tracking
- Linter integration to enforce constitution rules
- Constitution validation during CI/CD
