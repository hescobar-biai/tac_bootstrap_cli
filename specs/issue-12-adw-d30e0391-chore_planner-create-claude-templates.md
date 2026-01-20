# Chore: Crear templates para .claude/ (settings y comandos base)

## Metadata
issue_number: `12`
adw_id: `d30e0391`
issue_json: `{"number":12,"title":"TAREA 3.2: Crear templates para .claude/ (settings y comandos base)","body":"# Prompt para Agente\n\n## Contexto\nTAC Bootstrap genera la carpeta `.claude/` con:\n- `settings.json` - permisos y hooks para Claude Code\n- `commands/*.md` - comandos slash reutilizables\n\nEstos archivos deben ser templates Jinja2 parametrizables que se renderizan\ncon el TACConfig del usuario.\n\n## Objetivo\nCrear los templates Jinja2 para `.claude/settings.json` y los comandos base:\nprime, start, build, test, feature, bug, chore, patch, implement, commit,\npull_request, review, document, health_check.\n\n## Directorio Base\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/`\n\n## Archivos a Crear\n\n### 1. `settings.json.j2`\nTemplate para `.claude/settings.json`:\n\n```jinja2\n{\n  \"permissions\": {\n    \"allow\": [\n      \"Bash(mkdir:*)\",\n      \"Bash({{ config.project.package_manager.value }}:*)\",\n      \"Bash(find:*)\",\n      \"Bash(mv:*)\",\n      \"Bash(grep:*)\",\n      \"Bash(ls:*)\",\n      \"Bash(cp:*)\",\n      \"Write\",\n      \"Bash(chmod:*)\",\n      \"Bash(touch:*)\",\n      \"Bash(git:*)\"\n    ],\n    \"deny\": [\n      \"Bash(git push --force:*)\",\n      \"Bash(git push -f:*)\",\n      \"Bash(rm -rf:*)\",\n      \"Bash(rm -r /:*)\"\n    ]\n  },\n  \"hooks\": {\n    \"PreToolUse\": [\n      {\n        \"matcher\": \"\",\n        \"hooks\": [\n          {\n            \"type\": \"command\",\n            \"command\": \"{{ config.project.package_manager.value }} run $CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py || true\"\n          }\n        ]\n      }\n    ],\n    \"PostToolUse\": [\n      {\n        \"matcher\": \"\",\n        \"hooks\": [\n          {\n            \"type\": \"command\",\n            \"command\": \"{{ config.project.package_manager.value }} run $CLAUDE_PROJECT_DIR/.claude/hooks/post_tool_use.py || true\"\n          }\n        ]\n      }\n    ],\n    \"Stop\": [\n      {\n        \"matcher\": \"\",\n        \"hooks\": [\n          {\n            \"type\": \"command\",\n            \"command\": \"{{ config.project.package_manager.value }} run $CLAUDE_PROJECT_DIR/.claude/hooks/stop.py || true\"\n          }\n        ]\n      }\n    ]\n  }\n}\n```\n\n### 2. `commands/prime.md.j2`\n```jinja2\n# Prime\n\nPrepare the agent with project context.\n\n## Variables\n- $ARGUMENTS: Optional focus area\n\n## Instructions\n\n1. Read and understand the project structure:\n   - Project: {{ config.project.name }}\n   - Language: {{ config.project.language.value }}\n   - Framework: {{ config.project.framework.value if config.project.framework else 'none' }}\n   - Architecture: {{ config.project.architecture.value }}\n\n2. Key directories:\n   - App code: `{{ config.paths.app_root }}/`\n   - Specs: `{{ config.paths.specs_dir }}/`\n   - ADWs: `{{ config.paths.adws_dir }}/`\n   - Scripts: `{{ config.paths.scripts_dir }}/`\n\n3. Available commands:\n   - Start: `{{ config.commands.start }}`\n   - Test: `{{ config.commands.test }}`\n{% if config.commands.lint %}\n   - Lint: `{{ config.commands.lint }}`\n{% endif %}\n{% if config.commands.build %}\n   - Build: `{{ config.commands.build }}`\n{% endif %}\n\n4. Rules:\n   - Never modify files in: {{ config.agentic.safety.forbidden_paths | join(', ') }}\n   - Always run tests before completing work\n   - Follow {{ config.project.architecture.value }} architecture patterns\n\n## Report\nConfirm you understand the project context and are ready to work.\n```\n\n### 3. `commands/start.md.j2`\n```jinja2\n# Start\n\nStart the application.\n\n## Instructions\n\n1. Ensure dependencies are installed\n2. Run the start command:\n   ```bash\n   {{ config.commands.start }}\n   ```\n3. Verify the application is running\n4. Report the URL/port if applicable\n\n## Report\n- Status: running/failed\n- URL: (if applicable)\n- Notes: any issues encountered\n```\n\n### 4. `commands/test.md.j2`\n```jinja2\n# Test\n\nRun the test suite.\n\n## Variables\n- $ARGUMENTS: Optional test path or pattern\n\n## Instructions\n\n1. Run tests:\n   ```bash\n   {{ config.commands.test }} $ARGUMENTS\n   ```\n\n2. If tests fail:\n   - Analyze the failure output\n   - Identify the root cause\n   - Do NOT attempt to fix unless explicitly asked\n\n3. Report results\n\n## Report\n- Total tests: X\n- Passed: X\n- Failed: X\n- Failures: (list if any)\n```\n\n### 5. `commands/feature.md.j2`\n```jinja2\n# Feature Planning\n\nPlan a new feature implementation.\n\n## Variables\n- $ARGUMENTS: Feature description or issue reference\n\n## Instructions\n\n1. **Understand the Request**\n   - Parse the feature description from $ARGUMENTS\n   - Identify acceptance criteria\n   - List any ambiguities to clarify\n\n2. **Research the Codebase**\n   - Find related existing code\n   - Identify files that need modification\n   - Note any patterns to follow\n\n3. **Design the Solution**\n   - Break down into discrete tasks\n   - Identify dependencies between tasks\n   - Consider edge cases and error handling\n\n4. **Create the Plan**\n   Write a plan file to `{{ config.paths.specs_dir }}/` with:\n   - Summary of the feature\n   - List of files to modify/create\n   - Step-by-step implementation tasks\n   - Test cases to add\n   - Definition of done\n\n## Plan Format\n```markdown\n# Feature: [Name]\n\n## Summary\n[1-2 sentence description]\n\n## Files to Modify\n- `path/to/file.py` - [what changes]\n- `path/to/new_file.py` - [create new]\n\n## Implementation Steps\n1. [ ] Step one\n2. [ ] Step two\n...\n\n## Test Cases\n- [ ] Test case 1\n- [ ] Test case 2\n\n## Definition of Done\n- [ ] All tests pass\n- [ ] Code follows {{ config.project.architecture.value }} patterns\n- [ ] No linting errors\n```\n\n## Report\n- Plan file created: `{{ config.paths.specs_dir }}/feature-[name].md`\n- Ready for implementation: yes/no\n- Questions/blockers: (if any)\n```\n\n### 6. `commands/bug.md.j2`\n```jinja2\n# Bug Planning\n\nPlan a bug fix.\n\n## Variables\n- $ARGUMENTS: Bug description or issue reference\n\n## Instructions\n\n1. **Understand the Bug**\n   - Parse the bug description from $ARGUMENTS\n   - Identify expected vs actual behavior\n   - Determine reproduction steps if not provided\n\n2. **Investigate**\n   - Find the relevant code\n   - Identify the root cause\n   - Check for related issues\n\n3. **Plan the Fix**\n   - Determine the minimal fix\n   - Identify any side effects\n   - Plan regression tests\n\n4. **Create the Plan**\n   Write a plan file to `{{ config.paths.specs_dir }}/`\n\n## Plan Format\n```markdown\n# Bug: [Title]\n\n## Description\n[What is broken]\n\n## Root Cause\n[Why it's broken]\n\n## Fix\n[How to fix it]\n\n## Files to Modify\n- `path/to/file.py` - [what changes]\n\n## Test Cases\n- [ ] Test that reproduces the bug\n- [ ] Test for regression\n\n## Definition of Done\n- [ ] Bug is fixed\n- [ ] Tests pass\n- [ ] No regression introduced\n```\n\n## Report\n- Plan file created: `{{ config.paths.specs_dir }}/bug-[name].md`\n- Root cause identified: yes/no\n- Ready for implementation: yes/no\n```\n\n### 7. `commands/chore.md.j2`\n```jinja2\n# Chore Planning\n\nPlan a maintenance task (refactoring, dependencies, config, etc).\n\n## Variables\n- $ARGUMENTS: Chore description\n\n## Instructions\n\n1. **Understand the Task**\n   - Parse the chore description from $ARGUMENTS\n   - Identify scope and boundaries\n   - Determine success criteria\n\n2. **Plan the Work**\n   - List all changes needed\n   - Identify risks or breaking changes\n   - Plan verification steps\n\n3. **Create the Plan**\n   Write a plan file to `{{ config.paths.specs_dir }}/`\n\n## Plan Format\n```markdown\n# Chore: [Title]\n\n## Description\n[What needs to be done]\n\n## Changes\n- [ ] Change 1\n- [ ] Change 2\n\n## Files to Modify\n- `path/to/file` - [what changes]\n\n## Verification\n- [ ] Tests pass\n- [ ] Build succeeds\n- [ ] No breaking changes\n\n## Definition of Done\n- [ ] All changes complete\n- [ ] Verified working\n```\n\n## Report\n- Plan file created: `{{ config.paths.specs_dir }}/chore-[name].md`\n```\n\n### 8. `commands/implement.md.j2`\n```jinja2\n# Implement\n\nExecute a plan file.\n\n## Variables\n- $1: Path to the plan file (e.g., `{{ config.paths.specs_dir }}/feature-auth.md`)\n\n## Instructions\n\n1. **Read the Plan**\n   - Load and parse the plan file from $1\n   - Understand all tasks and their order\n   - Note the definition of done\n\n2. **Execute Tasks**\n   For each task in the plan:\n   - Mark task as in-progress\n   - Implement the change\n   - Verify it works\n   - Mark task as complete\n\n3. **Validate**\n   - Run tests: `{{ config.commands.test }}`\n{% if config.commands.lint %}\n   - Run linter: `{{ config.commands.lint }}`\n{% endif %}\n{% if config.commands.typecheck %}\n   - Run typecheck: `{{ config.commands.typecheck }}`\n{% endif %}\n\n4. **Report Results**\n   Update the plan file with completion status\n\n## Report\n- Plan: $1\n- Tasks completed: X/Y\n- Tests: pass/fail\n- Ready for review: yes/no\n```\n\n### 9. `commands/commit.md.j2`\n```jinja2\n# Commit\n\nCreate a git commit with proper message format.\n\n## Variables\n- $ARGUMENTS: Optional commit message override\n\n## Instructions\n\n1. **Check Status**\n   ```bash\n   git status\n   git diff --staged\n   ```\n\n2. **Stage Changes** (if needed)\n   - Stage only relevant files\n   - Do NOT stage: {{ config.agentic.safety.forbidden_paths | join(', ') }}\n\n3. **Create Commit**\n   - Use conventional commit format: `type(scope): description`\n   - Types: feat, fix, chore, docs, refactor, test\n   - Keep description under 72 characters\n\n4. **Commit Message Format**\n   ```\n   type(scope): short description\n\n   - Detail 1\n   - Detail 2\n\n   Co-Authored-By: Claude <noreply@anthropic.com>\n   ```\n\n## Report\n- Commit created: yes/no\n- Hash: [commit hash]\n- Message: [commit message]\n```\n\n### 10. `commands/review.md.j2`\n```jinja2\n# Review\n\nReview implementation against the plan/spec.\n\n## Variables\n- $1: Path to the plan/spec file\n\n## Instructions\n\n1. **Load the Spec**\n   Read the plan file from $1\n\n2. **Verify Completion**\n   For each item in the plan:\n   - Check if implemented correctly\n   - Verify tests exist\n   - Note any deviations\n\n3. **Run Validation**\n   - Tests: `{{ config.commands.test }}`\n{% if config.commands.lint %}\n   - Lint: `{{ config.commands.lint }}`\n{% endif %}\n{% if config.commands.build %}\n   - Build: `{{ config.commands.build }}`\n{% endif %}\n\n4. **Check Quality**\n   - Code follows {{ config.project.architecture.value }} patterns\n   - No hardcoded values\n   - Error handling present\n   - No security issues\n\n5. **Generate Report**\n\n## Report Format\n```markdown\n# Review: [Plan Name]\n\n## Checklist\n- [ ] All tasks from plan completed\n- [ ] Tests pass\n- [ ] Lint passes\n- [ ] Build succeeds\n- [ ] Code quality acceptable\n\n## Issues Found\n- (list any issues)\n\n## Verdict\n- APPROVED / NEEDS_CHANGES\n```\n```\n\n### 11. `commands/document.md.j2`\n```jinja2\n# Document\n\nGenerate documentation for recent changes.\n\n## Variables\n- $ARGUMENTS: Feature/component to document\n\n## Instructions\n\n1. **Identify What to Document**\n   - Parse $ARGUMENTS for the target\n   - Find related code and specs\n\n2. **Generate Documentation**\n   Create/update docs in `app_docs/`:\n   - Overview of the feature\n   - Usage examples\n   - API reference (if applicable)\n   - Configuration options\n\n3. **Documentation Format**\n   ```markdown\n   # [Feature Name]\n\n   ## Overview\n   [What it does]\n\n   ## Usage\n   [How to use it]\n\n   ## Examples\n   [Code examples]\n\n   ## Configuration\n   [Any config options]\n   ```\n\n## Report\n- Documentation created: `app_docs/[name].md`\n```\n\n### 12. `commands/health_check.md.j2`\n```jinja2\n# Health Check\n\nValidate the project setup and agentic layer.\n\n## Instructions\n\n1. **Check Structure**\n   Verify these directories exist:\n   - `.claude/commands/`\n   - `{{ config.paths.adws_dir }}/`\n   - `{{ config.paths.specs_dir }}/`\n   - `{{ config.paths.scripts_dir }}/`\n\n2. **Check Configuration**\n   - `.claude/settings.json` is valid JSON\n   - `config.yml` exists and is valid\n\n3. **Check Commands**\n   Verify these work:\n   - Start: `{{ config.commands.start }}`\n   - Test: `{{ config.commands.test }}`\n\n4. **Check Git**\n   - Is a git repository\n   - Has remote configured (optional)\n\n## Report Format\n```\nHealth Check Results\n====================\nStructure:    [PASS/FAIL]\nConfig:       [PASS/FAIL]\nCommands:     [PASS/FAIL]\nGit:          [PASS/FAIL]\n\nIssues:\n- (list any issues found)\n```\n```\n\n## Criterios de Aceptacion\n1. [ ] Directorio `templates/claude/` creado\n2. [ ] `settings.json.j2` con permisos y hooks parametrizados\n3. [ ] 12 comandos base creados como templates\n4. [ ] Todos los templates usan variables de `config`\n5. [ ] Sintaxis Jinja2 valida en todos los archivos\n\n## Comandos de Verificacion\n```bash\ncd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli\nls -la tac_bootstrap/templates/claude/\nls -la tac_bootstrap/templates/claude/commands/\n\n# Test rendering\nuv run python -c \"\nfrom tac_bootstrap.infrastructure.template_repo import TemplateRepository\nfrom tac_bootstrap.domain.models import *\n\nrepo = TemplateRepository()\n\n# Create test config\nconfig = TACConfig(\n    project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV),\n    commands=CommandsSpec(start='uv run python -m app', test='uv run pytest', lint='uv run ruff check .'),\n    claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))\n)\n\n# Render settings.json\nresult = repo.render('claude/settings.json.j2', {'config': config})\nprint('=== settings.json ===')\nprint(result[:500])\n\n# Render a command\nresult = repo.render('claude/commands/prime.md.j2', {'config': config})\nprint('=== prime.md ===')\nprint(result[:500])\n\"\n```\n\n## NO hacer\n- No crear hooks aun (siguiente tarea)\n- No crear templates de adws aun"}`

## Chore Description

TAC Bootstrap CLI genera la carpeta `.claude/` con configuración para Claude Code. Esta tarea consiste en crear templates Jinja2 parametrizables para `settings.json` y 12 comandos slash base que se renderizarán con TACConfig del usuario.

Los templates deben:
- Usar variables de `config` (TACConfig) para parametrización
- Seguir sintaxis Jinja2 válida
- Incluir condicionales para campos opcionales
- Generar archivos funcionales en proyectos target

## Relevant Files

Archivos clave para completar la chore:

### Existing Files
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Sistema de renderizado Jinja2 con filtros personalizados
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - TACConfig y todos los modelos Pydantic
- `app_docs/feature-d2f77c7a-jinja2-template-infrastructure.md` - Documentación del sistema de templates
- `PLAN_TAC_BOOTSTRAP.md` - Plan maestro (TAREA 3.2)

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2` - Template para settings.json
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime.md.j2` - Comando /prime
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/start.md.j2` - Comando /start
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/test.md.j2` - Comando /test
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2` - Comando /build (falta en issue, agregar)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/feature.md.j2` - Comando /feature
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/bug.md.j2` - Comando /bug
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/chore.md.j2` - Comando /chore
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/patch.md.j2` - Comando /patch (falta en issue, agregar)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/implement.md.j2` - Comando /implement
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/commit.md.j2` - Comando /commit
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/pull_request.md.j2` - Comando /pull_request
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/review.md.j2` - Comando /review
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/document.md.j2` - Comando /document
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/health_check.md.j2` - Comando /health_check

## Step by Step Tasks

### Task 1: Crear estructura de directorios
- Crear `tac_bootstrap_cli/tac_bootstrap/templates/claude/`
- Crear `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/`

### Task 2: Crear template settings.json.j2
- Crear `settings.json.j2` con permisos y hooks parametrizados
- Usar `{{ config.project.package_manager.value }}` para comandos
- Incluir permisos allow/deny según especificación
- Configurar hooks PreToolUse, PostToolUse, Stop

### Task 3: Crear templates de comandos básicos (1-5)
- Crear `prime.md.j2` - Preparar agente con contexto del proyecto
- Crear `start.md.j2` - Iniciar aplicación
- Crear `test.md.j2` - Ejecutar suite de tests
- Crear `build.md.j2` - Construir proyecto (agregar, no está en issue)
- Todos deben usar variables de `config` (paths, commands, project)

### Task 4: Crear templates de comandos de planeación (6-8)
- Crear `feature.md.j2` - Planificar features
- Crear `bug.md.j2` - Planificar bug fixes
- Crear `chore.md.j2` - Planificar mantenimiento
- Crear `patch.md.j2` - Patch rápido (agregar, no está en issue)

### Task 5: Crear templates de comandos de ejecución (9-14)
- Crear `implement.md.j2` - Ejecutar plan
- Crear `commit.md.j2` - Crear git commit
- Crear `pull_request.md.j2` - Crear PR (agregar, no está en issue)
- Crear `review.md.j2` - Revisar implementación
- Crear `document.md.j2` - Generar documentación
- Crear `health_check.md.j2` - Validar proyecto

### Task 6: Validar templates con renderizado de prueba
- Ejecutar comandos de verificación del issue
- Verificar que templates se renderizan sin errores
- Verificar sintaxis Jinja2 válida
- Verificar que variables `config.*` existen en TACConfig

### Task 7: Ejecutar Validation Commands
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Comandos faltantes en el issue
El issue lista 12 comandos pero faltan algunos comandos importantes que existen en `.claude/commands/` del proyecto base:
- `build.md` - Construir proyecto
- `patch.md` - Patch rápido
- `pull_request.md` - Crear PR

Deben agregarse para completitud.

### Variables TACConfig disponibles
- `config.project.name` - Nombre del proyecto
- `config.project.language.value` - Lenguaje (python, typescript, etc)
- `config.project.framework.value` - Framework (fastapi, nextjs, etc)
- `config.project.architecture.value` - Arquitectura (simple, ddd, clean, etc)
- `config.project.package_manager.value` - Package manager (uv, npm, etc)
- `config.paths.*` - Todos los paths (app_root, specs_dir, adws_dir, scripts_dir, etc)
- `config.commands.*` - Todos los comandos (start, test, lint, build, etc)
- `config.agentic.safety.forbidden_paths` - Paths prohibidos

### Sintaxis Jinja2
- Usar `{{ variable }}` para interpolación
- Usar `{% if condition %}...{% endif %}` para condicionales
- Usar `{{ list | join(', ') }}` para filtros
- No usar `{{ config }}` directamente, siempre acceder a sub-atributos

### NO hacer
- No crear hooks aún (siguiente tarea 3.3)
- No crear templates de adws aún (tarea futura)
- No modificar TemplateRepository
- No crear tests todavía
