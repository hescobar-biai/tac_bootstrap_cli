# Feature: Template canonical_idk.yml

## Metadata
issue_number: `180`
adw_id: `feature_6_5`
issue_json: `{"number":180,"title":"Tarea 6.5: Template canonical_idk.yml","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_6_5\n\n***Tipo**: feature\n**Ganancia**: Vocabulario controlado de keywords por dominio. Los generadores usan estos terminos para mantener consistencia terminologica en toda la documentacion del proyecto.\n\n**Instrucciones para el agente**:\n\n1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/config/canonical_idk.yml.j2`\n2. Crear renderizado en raiz: `canonical_idk.yml`\n2. Contenido segun el lenguaje/framework del proyecto:\n   ```yaml\n   # Canonical IDK Vocabulary for {{ config.project.name }}\n   # Used by fractal documentation generators to maintain consistent terminology\n\n   domains:\n   {% if config.project.language == \"python\" %}\n     backend:\n       - api-gateway, routing, middleware, authentication, authorization\n       - database, repository, orm, migration, session-management\n       - service-layer, use-case, business-logic, domain-model\n       - validation, serialization, dto, schema\n       - error-handling, exception, http-status\n       - dependency-injection, factory, singleton\n     testing:\n       - unit-test, integration-test, fixture, mock, assertion\n       - test-coverage, parametrize, conftest\n   {% endif %}\n   {% if config.project.language == \"typescript\" %}\n     frontend:\n       - component, hook, state-management, context, reducer\n       - routing, navigation, page, layout\n       - rendering, virtual-dom, reconciliation, hydration\n       - styling, css-modules, tailwind, theme\n     backend:\n       - controller, middleware, guard, interceptor, pipe\n       - module, provider, injectable, decorator\n       - dto, entity, repository, service\n   {% endif %}\n     infrastructure:\n       - deployment, ci-cd, docker, kubernetes\n       - monitoring, logging, metrics, alerting\n       - configuration, environment, secrets\n     documentation:\n       - docstring, jsdoc, fractal-docs, idk-keywords\n       - readme, changelog, api-reference\n   ```\n\n**Criterios de aceptacion**:\n- Template genera YAML valido para Python y TypeScript\n- Keywords son relevantes al ecosistema del lenguaje\n- Vocabulario es extensible (usuarios pueden agregar sus propios terminos)\nFASE 6: Documentacion Fractal como Skill\n\n**Objetivo**: Incluir los generadores de documentacion fractal como parte de los proyectos generados, con slash command para invocacion facil.\n\n**Ganancia de la fase**: Proyectos generados incluyen herramientas de documentacion automatica que mantienen docs sincronizados con el codigo, usando LLM local o remoto.\n\n---\n"}`

## Feature Description
This feature creates a Jinja2 template for the `canonical_idk.yml` file, which defines a controlled vocabulary of domain-specific keywords. This vocabulary file is used by fractal documentation generators (gen_docstring_jsdocs.py and gen_docs_fractal.py) to maintain consistent terminology across all project documentation.

The template conditionally includes language-specific vocabulary sections based on the project's configuration:
- **Python projects**: Backend (API, database, domain patterns) and testing vocabulary
- **TypeScript projects**: Frontend (React/component patterns) and backend (NestJS/framework patterns) vocabulary
- **All projects**: Infrastructure and documentation vocabulary (universal domains)

The generated file serves as a reference for documentation generators and can be extended by users to include project-specific terminology.

## User Story
As a developer using a TAC Bootstrap-generated project
I want a canonical vocabulary file that defines domain keywords for my project language
So that fractal documentation generators use consistent, relevant terminology across all generated docs

## Problem Statement
Fractal documentation generators need a controlled vocabulary to:
- Identify relevant domain keywords for IDK (I Don't Know) annotation
- Maintain consistency in terminology across documentation
- Provide language-appropriate technical vocabulary
- Allow users to extend vocabulary with project-specific terms

Without a canonical vocabulary file:
- Documentation generators would need hardcoded keywords (inflexible)
- Different generators might use inconsistent terminology
- No easy way for users to customize vocabulary for their domain
- Keywords might not be relevant to the project's language/framework
- No central reference for what terminology is "canonical" for the project

The project needs:
- A template that generates language-appropriate vocabulary
- Graceful handling of unsupported languages (fallback to universal domains)
- Clear structure that's easy for users to extend
- Valid YAML syntax that can be parsed by Python scripts
- Integration with Phase 5 config generation pipeline

## Solution Statement
Create a Jinja2 template (`canonical_idk.yml.j2`) that renders a YAML vocabulary file. The template will:

1. **Use config.project.language to determine vocabulary sections**
   - Check if language is "python" → include backend + testing domains
   - Check if language is "typescript" → include frontend + backend domains
   - Always include infrastructure + documentation domains
   - Gracefully handle other languages (only universal domains)

2. **Structure vocabulary by domain**
   - Each domain is a key (backend, frontend, testing, infrastructure, documentation)
   - Keywords are lists of comma-separated strings
   - Groups related concepts on same line for readability
   - Example: `- api-gateway, routing, middleware, authentication, authorization`

3. **Use language enums correctly**
   - Template compares against enum values: `config.project.language == "python"`
   - Domain models use ProgrammingLanguage enum (already exists in models.py)
   - Jinja2 will receive the enum value as string after serialization

4. **Follow YAML best practices**
   - Include header comment with project name and purpose
   - Use proper indentation (2 spaces)
   - Quote strings only when necessary
   - Ensure valid YAML structure

5. **Enable extensibility**
   - Clear domain structure makes it easy to add new domains
   - Users can add project-specific keywords to existing domains
   - Comments guide users on how to extend vocabulary

6. **Integrate with config generation**
   - Template placed in `tac_bootstrap_cli/tac_bootstrap/templates/config/`
   - Rendered during project scaffolding (same as config.yml)
   - Uses existing template rendering infrastructure
   - No new dependencies required

The template will be stored in the CLI and rendered to `canonical_idk.yml` in the root of GENERATED projects (not in tac_bootstrap repo itself). This follows the pattern established for config.yml template.

## Relevant Files

### Config Template Examples
- `tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2` - Reference template structure
- `tac_bootstrap_cli/tac_bootstrap/templates/config/.gitignore.j2` - Simple config template example

### Domain Models
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - TACConfig, ProgrammingLanguage enum
- `tac_bootstrap_cli/tac_bootstrap/domain/value_objects.py` - Enum definitions

### Template Rendering
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Template rendering service
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Project generation orchestration

### Documentation Generators (consumers of this file)
- `scripts/gen_docstring_jsdocs.py` - Uses IDK keywords for docstring generation (Task 6.1)
- `scripts/gen_docs_fractal.py` - Uses IDK keywords for fractal docs (Task 6.2)
- `scripts/run_generators.sh` - Orchestrator that uses this vocabulary (Task 6.3)

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/config/canonical_idk.yml.j2` - Template to create

## Implementation Plan

### Phase 1: Template Creation
Create the Jinja2 template with proper structure:
- Header comment with project name and purpose
- Conditional sections based on language
- Language-appropriate vocabulary for Python and TypeScript
- Universal domains (infrastructure, documentation)
- Valid YAML syntax with proper indentation

### Phase 2: Validation
Verify the template:
- Jinja2 syntax is valid
- Rendered YAML is valid for both Python and TypeScript
- Keywords are relevant and correctly categorized
- Graceful handling of unsupported languages

### Phase 3: Integration Check
Ensure template integrates with existing infrastructure:
- Template location follows convention (templates/config/)
- Uses config object structure correctly
- No new dependencies required
- Ready for rendering during project generation

## Step by Step Tasks

### Task 1: Create canonical_idk.yml.j2 Template
Create file at `tac_bootstrap_cli/tac_bootstrap/templates/config/canonical_idk.yml.j2` with:

1. **Header section**:
   ```jinja2
   # Canonical IDK Vocabulary for {{ config.project.name }}
   # Used by fractal documentation generators to maintain consistent terminology
   #
   # This file defines domain-specific keywords organized by category.
   # Documentation generators use these terms to identify relevant concepts.
   #
   # You can extend this vocabulary by adding new domains or keywords.
   # Format: Each domain contains a list of comma-separated keyword strings.

   domains:
   ```

2. **Python-specific sections** (conditional):
   ```jinja2
   {% if config.project.language.value == "python" %}
     backend:
       - api-gateway, routing, middleware, authentication, authorization
       - database, repository, orm, migration, session-management
       - service-layer, use-case, business-logic, domain-model
       - validation, serialization, dto, schema
       - error-handling, exception, http-status
       - dependency-injection, factory, singleton
     testing:
       - unit-test, integration-test, fixture, mock, assertion
       - test-coverage, parametrize, conftest
   {% endif %}
   ```

3. **TypeScript-specific sections** (conditional):
   ```jinja2
   {% if config.project.language.value == "typescript" %}
     frontend:
       - component, hook, state-management, context, reducer
       - routing, navigation, page, layout
       - rendering, virtual-dom, reconciliation, hydration
       - styling, css-modules, tailwind, theme
     backend:
       - controller, middleware, guard, interceptor, pipe
       - module, provider, injectable, decorator
       - dto, entity, repository, service
   {% endif %}
   ```

4. **Universal domains** (always included):
   ```jinja2
     infrastructure:
       - deployment, ci-cd, docker, kubernetes
       - monitoring, logging, metrics, alerting
       - configuration, environment, secrets
     documentation:
       - docstring, jsdoc, fractal-docs, idk-keywords
       - readme, changelog, api-reference
   ```

5. Verify indentation:
   - Top-level `domains:` key has no indentation
   - Domain names (backend, frontend, etc.) have 2 spaces
   - Keyword lists have 4 spaces
   - Consistent with YAML standards

### Task 2: Verify Template Syntax
1. Check Jinja2 syntax:
   - Conditionals are properly opened and closed
   - Variable references use correct object path (config.project.language.value)
   - No syntax errors in template

2. Test enum value comparison:
   - Verify that `config.project.language.value == "python"` works correctly
   - Check that enum is serialized to string in template context
   - Confirm both "python" and "typescript" comparisons work

3. Verify YAML will be valid:
   - Proper indentation (2 spaces)
   - List syntax is correct (dash + space + content)
   - No special characters that need escaping
   - Comments are properly formatted

### Task 3: Validate Vocabulary Content
1. Python vocabulary review:
   - Backend keywords cover common patterns (FastAPI, Django, Flask)
   - Testing keywords relevant to pytest ecosystem
   - Keywords grouped logically (auth together, database together, etc.)

2. TypeScript vocabulary review:
   - Frontend keywords cover React/modern component patterns
   - Backend keywords cover NestJS/Express patterns
   - Terminology is accurate and current

3. Universal vocabulary review:
   - Infrastructure keywords apply to any language
   - Documentation keywords are technology-agnostic
   - Terms are broad enough to be useful across projects

### Task 4: Edge Case Testing
1. Test with Python language:
   - Manually render template with config.project.language = "python"
   - Verify backend and testing sections appear
   - Verify infrastructure and documentation appear

2. Test with TypeScript language:
   - Manually render template with config.project.language = "typescript"
   - Verify frontend and backend sections appear
   - Verify infrastructure and documentation appear

3. Test with unsupported language:
   - Manually render template with config.project.language = "ruby"
   - Verify only infrastructure and documentation appear
   - Verify YAML is still valid

4. Validate rendered YAML:
   - Use Python yaml.safe_load() to parse rendered content
   - Verify no YAML syntax errors
   - Confirm structure matches expectations

### Task 5: Run Validation Commands
Execute all validation commands to ensure zero regressions.

## Testing Strategy

### Template Syntax Validation
1. Verify Jinja2 template can be parsed (no syntax errors)
2. Verify rendered output is valid YAML for all language cases
3. Check indentation is consistent and correct

### Content Validation
1. **Python rendering**: Contains backend, testing, infrastructure, documentation
2. **TypeScript rendering**: Contains frontend, backend, infrastructure, documentation
3. **Other language rendering**: Contains only infrastructure, documentation
4. **Keyword relevance**: Each keyword is appropriate for its domain

### Integration Validation
1. Template location follows convention (templates/config/)
2. Uses config object structure correctly (config.project.language.value)
3. No new dependencies required
4. Ready for integration with scaffold_service.py (Phase 5 infrastructure)

### Manual Testing
Since this is a template file, automated tests would require:
- Mock TACConfig objects
- Template rendering infrastructure
- YAML validation

For this task, manual validation is sufficient:
1. Visually inspect template syntax
2. Manually test rendering with sample configs
3. Validate YAML with `python -c "import yaml; yaml.safe_load(open('test.yml'))"`

## Acceptance Criteria
- ✅ Template file created at `tac_bootstrap_cli/tac_bootstrap/templates/config/canonical_idk.yml.j2`
- ✅ Template uses correct Jinja2 syntax (no syntax errors)
- ✅ Template generates valid YAML for Python projects
- ✅ Template generates valid YAML for TypeScript projects
- ✅ Template generates valid YAML for unsupported languages (infrastructure + documentation only)
- ✅ Python vocabulary includes backend and testing domains with relevant keywords
- ✅ TypeScript vocabulary includes frontend and backend domains with relevant keywords
- ✅ Infrastructure and documentation domains always included
- ✅ Keywords are logically grouped and relevant to their ecosystem
- ✅ YAML structure is extensible (users can easily add domains/keywords)
- ✅ Template uses `config.project.language.value` correctly
- ✅ Indentation follows YAML standards (2 spaces)
- ✅ Header comment explains purpose and usage

## Validation Commands
Run all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Design Decisions

1. **Language enum value comparison**: Use `config.project.language.value == "python"` instead of `config.project.language == "python"` because the domain model uses ProgrammingLanguage enum. The `.value` accessor gets the string value for comparison.

2. **Graceful degradation**: Unsupported languages get only universal domains (infrastructure, documentation). This is better than failing or showing empty file. Users can manually add their language-specific domains.

3. **No rendering for tac_bootstrap repo itself**: Unlike Task 6.4 where we created both template and rendered version, this task only creates the template. The canonical_idk.yml is rendered during PROJECT GENERATION, not in the tac_bootstrap repo itself. This matches the pattern of config.yml.

4. **Keyword grouping**: Related keywords on the same line (e.g., "routing, middleware, authentication") makes the file more readable and easier to extend. Each line represents a conceptual cluster.

5. **No validation logic in template**: Template just generates YAML. Validation happens at parse time (YAML library) and usage time (documentation generators). Keep template simple.

6. **UTF-8 with LF line endings**: Standard for YAML files and Python ecosystem. Jinja2 outputs UTF-8 by default.

### Integration Notes

This template will be integrated with project generation in a future task (not part of this task):
- `scaffold_service.py` will render this template during project initialization
- Template will be rendered to `<project_root>/canonical_idk.yml`
- Same rendering infrastructure as config.yml (already exists)

### Vocabulary Extension

Users can extend the vocabulary by:
1. Adding new domains (e.g., `security:`, `performance:`)
2. Adding keywords to existing domains
3. Creating domain-specific sub-sections

Example user extension:
```yaml
domains:
  backend:
    - api-gateway, routing, middleware, authentication, authorization
    - custom-keyword-1, custom-keyword-2  # User addition

  custom-domain:  # User addition
    - domain-specific, keywords, here
```

### Future Enhancements

1. **Framework-specific vocabulary**: Could add vocabulary based on config.project.framework (FastAPI vs Django, React vs Vue)
2. **Architecture-specific vocabulary**: DDD vs Clean vs MVC vocabulary
3. **Multi-language support**: Projects using both Python backend and TypeScript frontend
4. **YAML schema validation**: Add JSON Schema or Pydantic model to validate structure
5. **Vocabulary merging**: Allow projects to import vocabulary from external sources

### Dependencies

This template is consumed by:
- Task 6.1: `gen_docstring_jsdocs.py` - Reads IDK keywords for docstring generation
- Task 6.2: `gen_docs_fractal.py` - Reads IDK keywords for fractal documentation
- Task 6.3: `run_generators.sh` - Orchestrator assumes this file exists

The template does NOT depend on those tasks (they depend on it).

### Related Tasks

- **Task 6.1** (Issue 169): Generator that reads this vocabulary
- **Task 6.2** (Issue 170): Generator that reads this vocabulary
- **Task 6.3** (Issue 171): Orchestrator that assumes this file exists
- **Task 6.4** (Issue 179): Slash command that triggers generators using this vocabulary
- **Phase 5 tasks**: Config generation infrastructure this integrates with
