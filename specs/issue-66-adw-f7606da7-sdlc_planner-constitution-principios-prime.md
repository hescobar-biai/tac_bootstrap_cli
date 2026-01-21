# Feature: Constitution/Principios Gobernantes en /prime

## Metadata
issue_number: `66`
adw_id: `f7606da7`
issue_json: `{"number":66,"title":"Tarea 2: Constitution/Principios Gobernantes en /prime","body":"### Descripción\nExtender el comando `/prime` para generar un archivo `constitution.md` que defina los principios gobernantes del proyecto. Inspirado en `/speckit.constitution`.\n\n### Beneficio\n- Consistencia en decisiones de desarrollo\n- Onboarding más rápido para nuevos agentes/desarrolladores\n- Reglas claras para code review\n\n### Prompt para Ejecutar\n\n```\nNecesito extender el comando /prime en TAC Bootstrap CLI para que genere un archivo de constitution/principios gobernantes.\n\nEl archivo constitution.md debe incluir secciones para:\n1. **Principios de Código**\n   - Estilo de código preferido\n   - Patrones a usar/evitar\n   - Convenciones de naming\n\n2. **Estándares de Testing**\n   - Cobertura mínima esperada\n   - Tipos de tests requeridos\n   - Estrategia de mocking\n\n3. **Arquitectura**\n   - Estructura de carpetas\n   - Separación de responsabilidades\n   - Dependencias permitidas\n\n4. **UX/DX Guidelines**\n   - Manejo de errores\n   - Mensajes al usuario\n   - Documentación requerida\n\n5. **Performance**\n   - Límites aceptables\n   - Optimizaciones requeridas\n\nArchivos a modificar:\n- tac_bootstrap_cli/tac_bootstrap/templates/commands/prime.md.j2\n- Crear nuevo template: templates/constitution.md.j2\n\nEl constitution debe ser parametrizable con {{ config.* }} para adaptarse a cada proyecto generado.\n```\n\n### Archivos Involucrados\n- `templates/commands/prime.md.j2`\n- Nuevo: `templates/constitution.md.j2`\n\n### Criterios de Aceptación\n- [ ] `/prime` genera `constitution.md` en el proyecto\n- [ ] Constitution tiene las 5 secciones definidas\n- [ ] Valores parametrizables con config\n- [ ] Otros comandos pueden referenciar el constitution"}`

## Feature Description
Extend the `/prime` command in TAC Bootstrap CLI to generate a `constitution.md` file that defines the project's governing principles and standards. This "project constitution" serves as a single source of truth for development decisions, code review guidelines, testing standards, and architectural patterns.

The constitution will provide:
1. Clear coding principles (style, patterns, naming conventions)
2. Testing standards (coverage, test types, mocking strategy)
3. Architectural guidelines (structure, separation of concerns, allowed dependencies)
4. UX/DX guidelines (error handling, user messaging, documentation requirements)
5. Performance expectations (acceptable limits, required optimizations)

## User Story
As a developer or AI agent working on a TAC Bootstrap-generated project
I want a `constitution.md` file that defines the project's governing principles
So that I can make consistent development decisions, understand code review expectations, onboard quickly, and maintain architectural coherence without asking for clarification on every decision

## Problem Statement
Currently, the `/prime` command prepares context by reading project files and configuration, but it does not:
- Establish clear coding standards and principles for the project
- Define testing expectations and coverage requirements
- Document architectural patterns and constraints
- Provide UX/DX guidelines for error handling and messaging
- Set performance expectations and optimization requirements

This leads to:
- Inconsistent code styles across features
- Unclear testing requirements
- Architectural drift as features are added
- Different error handling patterns
- Ambiguous performance expectations
- Slower onboarding for new agents/developers
- Repeated questions during code review about what is acceptable

## Solution Statement
Extend the `/prime` command to generate a `constitution.md` file that serves as the project's governing principles document. The constitution will be:
1. **Parametrizable**: Uses `{{ config.* }}` template variables to adapt to each project's language, framework, architecture, and tooling
2. **Comprehensive**: Covers coding principles, testing standards, architecture, UX/DX, and performance
3. **Actionable**: Provides specific, concrete guidelines rather than vague aspirations
4. **Referenceable**: Can be cited by other commands (like `/review`, `/implement`, `/test`) to enforce standards

The implementation will:
- Create a new Jinja2 template `constitution.md.j2` in `templates/structure/`
- Modify `prime.md.j2` to include constitution generation instructions
- Populate the constitution with language/framework-specific best practices
- Make the constitution available for reference by other slash commands
- Generate the constitution in the project root (or configured location) during `/prime` execution

## Relevant Files

**Existing Templates to Modify:**
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime.md.j2` - Main prime command that needs to generate the constitution file

**New Templates to Create:**
- `tac_bootstrap_cli/tac_bootstrap/templates/structure/constitution.md.j2` - The constitution template with 5 sections (coding, testing, architecture, UX/DX, performance)

**Reference Files (for understanding patterns):**
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Shows config structure and available template variables
- `config.yml` - Project config with language, framework, architecture, package_manager
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/conditional_docs.md.j2` - Shows how to integrate documentation into commands

**Test Files:**
- `tac_bootstrap_cli/tests/` - Will need tests for constitution generation

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/structure/constitution.md.j2` - Constitution template

## Implementation Plan

### Phase 1: Foundation
1. Research existing constitution/principles patterns in software projects
2. Analyze the config.yml schema to understand available template variables
3. Study language/framework-specific best practices for each supported language (Python, TypeScript, Go, Rust, Java)
4. Review existing template structure in `templates/structure/` for naming and organization patterns

### Phase 2: Core Implementation
1. Create `constitution.md.j2` template with 5 main sections:
   - Coding Principles
   - Testing Standards
   - Architecture Guidelines
   - UX/DX Guidelines
   - Performance Expectations
2. Populate each section with parametrizable content based on:
   - `config.project.language`
   - `config.project.framework`
   - `config.project.architecture`
   - `config.project.package_manager`
   - `config.commands.*`
3. Add language-specific coding standards (e.g., PEP 8 for Python, gofmt for Go)
4. Add framework-specific patterns (e.g., FastAPI best practices, Next.js conventions)
5. Add architecture-specific guidelines (e.g., DDD layering, hexagonal ports/adapters)

### Phase 3: Integration
1. Modify `prime.md.j2` to include constitution generation step
2. Add instruction to write `constitution.md` to project root
3. Add "Read Constitution" step to other relevant commands (`/review`, `/implement`, `/build`)
4. Update `conditional_docs.md.j2` to include constitution in appropriate conditions
5. Test constitution generation with different config combinations

## Step by Step Tasks

### Task 1: Create Constitution Template Structure
- Create file `tac_bootstrap_cli/tac_bootstrap/templates/structure/constitution.md.j2`
- Add markdown structure with 5 main sections
- Add template header with project name and generation timestamp
- Add frontmatter explaining the constitution's purpose

### Task 2: Implement Coding Principles Section
- Add language-specific style guides (PEP 8, Airbnb JS, gofmt, etc.)
- Add common patterns to use based on framework (e.g., FastAPI dependency injection, React hooks)
- Add anti-patterns to avoid (e.g., mutable default args in Python)
- Add naming conventions (snake_case, camelCase, PascalCase based on language)
- Make all content conditional on `config.project.language` and `config.project.framework`

### Task 3: Implement Testing Standards Section
- Add test coverage expectations (minimum %, critical paths)
- Add test types required (unit, integration, e2e based on project type)
- Add mocking strategy (when to mock, what to mock)
- Add test organization patterns (co-located vs separate test directory)
- Add framework-specific test tools (pytest, jest, go test, cargo test)
- Reference `config.commands.test` for test execution

### Task 4: Implement Architecture Guidelines Section
- Add architecture-specific folder structure based on `config.project.architecture`
- For DDD: domain/, application/, infrastructure/, interfaces/
- For layered: presentation/, business/, data/
- For clean: entities/, use_cases/, adapters/, frameworks/
- Add separation of concerns principles
- Add dependency rules (e.g., domain can't depend on infrastructure)
- Add allowed external dependencies and how to add new ones

### Task 5: Implement UX/DX Guidelines Section
- Add error handling patterns (exceptions vs errors vs results)
- Add user messaging guidelines (error messages, success messages, logs)
- Add logging standards (levels, format, what to log)
- Add documentation requirements (docstrings, README, API docs)
- Add CLI output formatting (for CLI projects)
- Add API response formats (for API projects)

### Task 6: Implement Performance Expectations Section
- Add performance limits based on project type (API latency, build time, test time)
- Add optimization requirements (when to optimize, what to optimize)
- Add profiling guidelines (how to measure performance)
- Add caching strategies
- Add database query optimization patterns (for backend projects)

### Task 7: Modify Prime Command Template
- Open `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime.md.j2`
- Add step to generate `constitution.md` file
- Add instruction: "Generate project constitution from template"
- Add step to read the generated constitution
- Add constitution path to "Read" section
- Update "Report" section to mention constitution availability

### Task 8: Update Conditional Documentation
- Modify `conditional_docs.md.j2` to reference constitution
- Add condition: "When making code changes, read constitution.md for guidelines"
- Add constitution to relevant command documentation (review, implement)

### Task 9: Create Unit Tests
- Create test file `tac_bootstrap_cli/tests/templates/test_constitution_template.py`
- Test constitution renders correctly with different config combinations
- Test all 5 sections are present
- Test language-specific content is included/excluded correctly
- Test framework-specific content is included/excluded correctly
- Test architecture-specific content is included/excluded correctly

### Task 10: Validation and Documentation
- Run all validation commands (see Validation Commands below)
- Manually test `/prime` command generates constitution
- Verify constitution content is accurate for each language/framework
- Update this spec with any lessons learned
- Mark all acceptance criteria as complete

## Testing Strategy

### Unit Tests
- **Template Rendering**: Test `constitution.md.j2` renders without errors for all language/framework combinations
- **Content Inclusion**: Test language-specific sections are included/excluded based on config
- **Variable Substitution**: Test all `{{ config.* }}` variables are correctly substituted
- **Section Completeness**: Test all 5 required sections are present in rendered output

### Integration Tests
- **Prime Command Flow**: Test `/prime` command successfully generates constitution.md
- **File Creation**: Test constitution.md is created in correct location
- **Content Accuracy**: Test generated constitution matches expected content for sample configs

### Edge Cases
- Project with `framework: none` - should still generate valid constitution
- Minimal config (only required fields) - should use sensible defaults
- Multiple languages in same project (e.g., Python backend + TypeScript frontend) - handle primary language
- Custom architecture not in standard list - should fall back to general principles

## Acceptance Criteria
- [ ] `/prime` command generates `constitution.md` file in project root
- [ ] Constitution contains all 5 required sections:
  - [ ] Coding Principles
  - [ ] Testing Standards
  - [ ] Architecture Guidelines
  - [ ] UX/DX Guidelines
  - [ ] Performance Expectations
- [ ] Constitution uses parametrizable content via `{{ config.* }}` variables
- [ ] Language-specific best practices are included based on `config.project.language`
- [ ] Framework-specific patterns are included based on `config.project.framework`
- [ ] Architecture-specific guidelines are included based on `config.project.architecture`
- [ ] Other commands (review, implement) can reference the constitution
- [ ] Constitution content is actionable and specific (not vague)
- [ ] Template renders successfully for all supported languages (Python, TypeScript, JavaScript, Go, Rust, Java)
- [ ] Unit tests pass for constitution template rendering
- [ ] Integration tests verify constitution generation in `/prime` flow

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Constitution Content Strategy
The constitution should be:
1. **Opinionated but Reasonable**: Provide clear guidance, not wishy-washy "it depends" advice
2. **Contextual**: Adapt to the project's language, framework, and architecture
3. **Actionable**: Include specific examples and patterns, not abstract principles
4. **Reference-able**: Other commands should be able to cite specific sections

### Template Variables Available
From `config.yml` schema (see `models.py`):
- `config.project.name` - Project name
- `config.project.language.value` - python, typescript, go, rust, java
- `config.project.framework.value` - fastapi, nextjs, gin, axum, spring, none
- `config.project.architecture.value` - simple, layered, ddd, clean, hexagonal
- `config.project.package_manager.value` - uv, poetry, pnpm, npm, cargo, go, maven
- `config.commands.*` - start, test, lint, typecheck, format, build
- `config.paths.*` - app_root, specs_dir, adws_dir, etc.

### Language-Specific Guidelines Examples
- **Python**: PEP 8, type hints, virtual environments, import ordering
- **TypeScript**: Strict mode, no `any`, ESLint, Prettier
- **Go**: gofmt, golangci-lint, interfaces over concrete types
- **Rust**: clippy, cargo fmt, ownership patterns, error handling with Result
- **Java**: Checkstyle, immutability, dependency injection

### Framework-Specific Patterns Examples
- **FastAPI**: Pydantic models, dependency injection, async/await, APIRouter
- **Next.js**: Server components, client components, App Router, data fetching patterns
- **Gin**: Middleware patterns, context usage, error handling
- **Axum**: Extractors, state management, tower services
- **Spring Boot**: Annotations, dependency injection, JPA best practices

### Architecture-Specific Guidelines Examples
- **DDD**: Ubiquitous language, aggregates, entities, value objects, repositories
- **Clean**: Dependency rule (inner layers can't depend on outer), use cases, entities
- **Hexagonal**: Ports and adapters, domain isolation, infrastructure at edges
- **Layered**: Presentation → Business → Data access, no skip-layer dependencies
- **Simple**: Single module, clear separation by file, minimal abstractions

### Future Enhancements
- Allow custom constitution sections via config
- Support multiple languages in a single project (monorepo)
- Generate language/framework decision trees
- Integration with linters to enforce constitution rules
- Constitution changelog tracking as project evolves
