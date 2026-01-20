# Chore: Crear templates para scripts/ y config/

## Metadata
issue_number: `18`
adw_id: `feff53ac`
issue_json: `{"number":18,"title":"TAREA 3.5: Crear templates para scripts/ y config/","body":"# Prompt para Agente..."}`

## Chore Description
Crear templates Jinja2 para archivos de scripts utilitarios y configuración que serán generados por TAC Bootstrap CLI. Estos templates permitirán generar una estructura completa de scripts de desarrollo (start.sh, test.sh, lint.sh, build.sh), archivos de configuración (config.yml, .mcp.json, .gitignore), y documentación README para distintos directorios.

Los templates deben:
1. Usar variables de configuración del modelo `TACConfig` (tac_bootstrap_cli/tac_bootstrap/domain/models.py:408)
2. Generar scripts bash ejecutables y multiplataforma
3. Incluir condicionales para comandos opcionales (lint, build, typecheck, format)
4. Generar archivos de configuración válidos (YAML, JSON)
5. Seguir las convenciones de naming y estructura del proyecto TAC Bootstrap

## Relevant Files
Archivos para completar la chore:

### Modelos y Referencias
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Modelos Pydantic con TACConfig, PathsSpec, CommandsSpec, etc. que se usarán en los templates
- `config.yml` - Archivo de configuración actual de TAC Bootstrap, referencia para el template
- `.mcp.json` - Configuración MCP actual, referencia para el template
- `.gitignore` - Configuración actual de gitignore, referencia para el template
- `scripts/dev_start.sh` - Script de desarrollo actual, referencia para el template
- `scripts/dev_test.sh` - Script de testing actual, referencia para el template

### Templates Existentes
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/` - Templates de ADWs como referencia del estilo
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/` - Templates de comandos Claude como referencia del estilo

### New Files
Los siguientes archivos se crearán en `tac_bootstrap_cli/tac_bootstrap/templates/`:

**Scripts (4 archivos):**
- `scripts/start.sh.j2` - Template para iniciar la aplicación
- `scripts/test.sh.j2` - Template para ejecutar tests
- `scripts/lint.sh.j2` - Template para ejecutar linter
- `scripts/build.sh.j2` - Template para construir el proyecto

**Config (3 archivos):**
- `config/config.yml.j2` - Template del archivo de configuración principal
- `config/.mcp.json.j2` - Template de configuración MCP servers
- `config/.gitignore.j2` - Template de gitignore

**Structure READMEs (3 archivos):**
- `structure/specs/README.md.j2` - Documentación del directorio specs/
- `structure/app_docs/README.md.j2` - Documentación del directorio app_docs/
- `structure/ai_docs/README.md.j2` - Documentación del directorio ai_docs/

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Crear estructura de directorios para templates
Crear los directorios necesarios dentro de `tac_bootstrap_cli/tac_bootstrap/templates/`:
- `scripts/` - Para templates de scripts bash
- `config/` - Para templates de configuración (yml, json, gitignore)
- `structure/specs/` - Para README de specs
- `structure/app_docs/` - Para README de app_docs
- `structure/ai_docs/` - Para README de ai_docs

### Task 2: Crear templates de scripts bash
Crear los 4 templates de scripts en `tac_bootstrap_cli/tac_bootstrap/templates/scripts/`:

**start.sh.j2:**
- Header con comentario descriptivo
- `set -e` para fail-fast
- Echo del mensaje de inicio con `{{ config.project.name }}`
- Comando de start: `{{ config.commands.start }}`

**test.sh.j2:**
- Header con comentario descriptivo
- `set -e` para fail-fast
- Echo del mensaje de tests
- Comando de test: `{{ config.commands.test }}`

**lint.sh.j2:**
- Header con comentario descriptivo
- `set -e` para fail-fast
- Condicional `{% if config.commands.lint %}` para verificar si existe el comando
- Echo del mensaje de linter
- Comando de lint: `{{ config.commands.lint }}`
- Else con mensaje "No lint command configured"

**build.sh.j2:**
- Header con comentario descriptivo
- `set -e` para fail-fast
- Condicional `{% if config.commands.build %}` para verificar si existe el comando
- Echo del mensaje de build
- Comando de build: `{{ config.commands.build }}`
- Else con mensaje "No build command configured"

### Task 3: Crear template config.yml.j2
Crear `tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2`:

Debe incluir todas las secciones del modelo TACConfig:
- Header con comentario y link a docs
- version: 1
- Sección `project:` con todos los campos de ProjectSpec (name, mode, repo_root, language, framework, architecture, package_manager)
- Sección `paths:` con todos los campos de PathsSpec (app_root, agentic_root, prompts_dir, adws_dir, specs_dir, logs_dir, scripts_dir, worktrees_dir)
- Sección `commands:` con comandos requeridos (start, test) y condicionales para opcionales (lint, build, typecheck, format)
- Sección `agentic:` con provider, model_policy (default, heavy), worktrees (enabled, max_parallel), logging (level, capture_agent_transcript)
- Sección `claude:` con settings (project_name, preferred_style, allow_shell)

Usar condicionales Jinja2 `{% if config.project.framework %}` para campos opcionales.
Usar filtro `| lower` para convertir booleanos a minúsculas en YAML.
Usar `.value` para acceder al valor de enums (ej: `{{ config.project.language.value }}`).

### Task 4: Crear template .mcp.json.j2
Crear `tac_bootstrap_cli/tac_bootstrap/templates/config/.mcp.json.j2`:

JSON simple con:
- mcpServers object
- playwright server con command "npx"
- args array con @playwright/mcp@latest, --isolated, --config, ./playwright-mcp-config.json

Usar formato JSON válido con indentación de 2 espacios.

### Task 5: Crear template .gitignore.j2
Crear `tac_bootstrap_cli/tac_bootstrap/templates/config/.gitignore.j2`:

Debe incluir:
- Header con comentario "Generated for {{ config.project.name }}"
- Sección Environment (.env, .env.local, etc.)
- Sección Logs con `{{ config.paths.logs_dir }}/` y *.log
- Sección "Agent outputs (can be large)" con agents/
- Sección "Git worktrees" con `{{ config.paths.worktrees_dir }}/`
- Sección Python (__pycache__, *.py[cod], .venv/, etc.)
- Sección Node (node_modules/, .npm, .pnpm-store/)
- Sección IDE (.idea/, .vscode/, *.swp, etc.)
- Sección OS (.DS_Store, Thumbs.db)
- Sección "Build outputs" (dist/, build/, *.egg)
- Sección "Test coverage" (.coverage, htmlcov/, .pytest_cache/)
- Sección "Secrets (never commit!)" (secrets/, *.pem, *.key, credentials.json)

### Task 6: Crear READMEs de estructura
Crear 3 templates de README en `tac_bootstrap_cli/tac_bootstrap/templates/structure/`:

**specs/README.md.j2:**
- Título "# Specifications"
- Descripción: "Este directorio contiene las especificaciones de issues y features."
- Sección "## Estructura" con árbol de archivos usando `{{ config.paths.specs_dir }}/`
- Explicación de cada tipo de archivo (feature-*.md, bug-*.md, chore-*.md, issue-*.md)
- Sección "## Formato" con ejemplo de estructura markdown de spec

**app_docs/README.md.j2:**
- Título "# Application Documentation"
- Descripción: "Documentacion de {{ config.project.name }}."
- Sección "## Estructura" con subdirectorios (features/, api/, guides/)
- Sección "## Generacion" con comando de ejemplo usando claude -p "/document [feature]"

**ai_docs/README.md.j2:**
- Título "# AI Documentation"
- Descripción: "Documentacion generada por agentes para {{ config.project.name }}."
- Nota: "Este directorio contiene documentacion auto-generada durante el desarrollo."

### Task 7: Verificar templates creados
Verificar que se crearon todos los archivos:
- Contar templates: `find tac_bootstrap_cli/tac_bootstrap/templates -name "*.j2" | wc -l` debe mostrar ~40+ templates
- Verificar directorios: scripts/, config/, structure/ existen
- Verificar que todos los archivos .j2 tienen extensión correcta

### Task 8: Test de rendering del template config.yml
Ejecutar el código de verificación para probar que config.yml.j2 se renderiza correctamente:

```python
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import *

repo = TemplateRepository()
config = TACConfig(
    project=ProjectSpec(
        name='my-app',
        language=Language.PYTHON,
        package_manager=PackageManager.UV,
        framework=Framework.FASTAPI
    ),
    commands=CommandsSpec(
        start='uv run python -m app',
        test='uv run pytest',
        lint='uv run ruff check .'
    ),
    claude=ClaudeConfig(
        settings=ClaudeSettings(project_name='my-app')
    )
)

result = repo.render('config/config.yml.j2', {'config': config})
print(result)
```

Verificar que:
- Se renderiza sin errores
- Las variables se sustituyen correctamente
- Los condicionales funcionan
- El YAML generado es válido

### Task 9: Ejecutar tests y validaciones
Ejecutar todos los comandos de validación para asegurar cero regresiones.

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Variables de Configuración Disponibles
Los templates tienen acceso al objeto `config` que es una instancia de `TACConfig` con:
- `config.project.*` - ProjectSpec (name, language, framework, etc.)
- `config.paths.*` - PathsSpec (app_root, logs_dir, etc.)
- `config.commands.*` - CommandsSpec (start, test, lint, etc.)
- `config.agentic.*` - AgenticSpec (provider, model_policy, worktrees, etc.)
- `config.claude.*` - ClaudeConfig (settings, commands)
- `config.templates.*` - TemplatesConfig (plan_template, etc.)
- `config.bootstrap.*` - BootstrapConfig (create_git_repo, etc.)

### Convenciones de Templates
1. **Enums**: Usar `.value` para acceder al valor del enum: `{{ config.project.language.value }}`
2. **Booleanos en YAML**: Usar filtro `| lower`: `{{ config.agentic.worktrees.enabled | lower }}`
3. **Condicionales**: Usar `{% if config.commands.lint %}` para campos opcionales
4. **Comments**: Incluir headers descriptivos en todos los archivos generados
5. **Paths**: Usar variables de `config.paths` para rutas dinámicas

### Criterios de Aceptación
- [ ] Directorio `templates/scripts/` con 4 scripts (start.sh.j2, test.sh.j2, lint.sh.j2, build.sh.j2)
- [ ] Directorio `templates/config/` con 3 archivos (config.yml.j2, .mcp.json.j2, .gitignore.j2)
- [ ] Directorio `templates/structure/` con 3 READMEs (specs/README.md.j2, app_docs/README.md.j2, ai_docs/README.md.j2)
- [ ] Todos los templates usan variables de config correctamente
- [ ] Test de rendering de config.yml.j2 pasa sin errores
- [ ] Todos los tests unitarios pasan
- [ ] Linting pasa sin errores
