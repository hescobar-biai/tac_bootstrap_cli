# Chore: Crear templates para .claude/hooks/

## Metadata
issue_number: `14`
adw_id: `fbc4585b`
issue_json: `{"number":14,"title":"TAREA 3.3: Crear templates para .claude/hooks/","body":"# Prompt para Agente\n\n## Contexto\nLos hooks de Claude Code son scripts Python que se ejecutan automaticamente\nen diferentes eventos (PreToolUse, PostToolUse, Stop, etc).\n\nNecesitamos templates para estos hooks que:\n- Validen comandos peligrosos antes de ejecutar\n- Registren logs de operaciones\n- Sean parametrizables segun config.yml\n\n## Objetivo\nCrear templates Jinja2 para los hooks de `.claude/hooks/`:\n- pre_tool_use.py - validacion antes de ejecutar herramientas\n- post_tool_use.py - logging despues de ejecutar\n- stop.py - limpieza al terminar sesion\n- utils/constants.py - configuracion compartida"}`

## Chore Description
Esta tarea consiste en crear templates Jinja2 para los hooks de Claude Code que se ejecutan en diferentes eventos del ciclo de vida de una sesión. Los hooks son scripts Python que proporcionan:

1. **Validación preventiva (pre_tool_use.py)**: Valida comandos y operaciones antes de ejecutarlas para prevenir operaciones peligrosas
2. **Logging post-ejecución (post_tool_use.py)**: Registra todas las operaciones ejecutadas para debugging y auditoría
3. **Limpieza de sesión (stop.py)**: Genera resúmenes y realiza cleanup cuando termina una sesión
4. **Utilidades compartidas (utils/)**: Constantes y helpers usados por todos los hooks

Los templates deben ser parametrizables según config.yml y seguir las mejores prácticas de los hooks existentes en el repositorio.

## Relevant Files
Archivos clave para completar esta chore:

- **tac_bootstrap_cli/tac_bootstrap/domain/models.py** - Modelos Pydantic que definen la estructura de config (ProjectSpec, PathsSpec, SafetyConfig, etc)
- **tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py** - TemplateRepository para renderizar templates Jinja2
- **.claude/hooks/** - Directorio con hooks existentes que sirven de referencia para el contenido y estructura
  - `.claude/hooks/pre_tool_use.py` - Implementación actual de validación pre-ejecución
  - `.claude/hooks/post_tool_use.py` - Implementación actual de logging
  - `.claude/hooks/stop.py` - Implementación actual de cleanup
  - `.claude/hooks/utils/constants.py` - Constantes compartidas actuales
- **config.yml** - Configuración del proyecto que contiene safety.forbidden_paths, paths.logs_dir, etc
- **tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2** - Template existente para referencia de sintaxis Jinja2

### New Files
Los siguientes archivos serán creados:

1. `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_tool_use.py.j2` - Template para validación pre-tool
2. `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/post_tool_use.py.j2` - Template para logging post-tool
3. `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/stop.py.j2` - Template para cleanup de sesión
4. `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/__init__.py.j2` - Init file del módulo utils
5. `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2` - Template para constantes compartidas

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Crear estructura de directorios para hooks templates
- Crear directorio `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/`
- Crear subdirectorio `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/`
- Verificar que la estructura existe correctamente con `ls -la`

### Task 2: Crear template pre_tool_use.py.j2
- Crear archivo `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_tool_use.py.j2`
- Incluir shebang `#!/usr/bin/env python3` para hacerlo ejecutable
- Implementar validación de comandos Bash peligrosos usando `config.agentic.safety.forbidden_paths`
- Implementar validación de paths prohibidos para operaciones Write/Edit/Read
- Usar patrones de validación similares a `.claude/hooks/pre_tool_use.py` pero parametrizado
- Variables Jinja2 a usar: `{{ config.project.name }}`, `{{ config.agentic.safety.forbidden_paths }}`, `{{ config.paths.logs_dir }}`
- Retornar JSON con `{"decision": "allow"}` o `{"decision": "block", "reason": "..."}` vía stdout

### Task 3: Crear template post_tool_use.py.j2
- Crear archivo `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/post_tool_use.py.j2`
- Incluir shebang `#!/usr/bin/env python3`
- Implementar logging de operaciones a `{{ config.paths.logs_dir }}/{session_id}/post_tool_use.json`
- Capturar tool_name, tool_input, tool_output (truncado a 500 chars), timestamp
- Usar estructura de log similar a la implementación actual pero con paths parametrizados
- Manejar errores de logging sin fallar (logging es best-effort)
- Leer hook input desde `CLAUDE_HOOK_INPUT` environment variable

### Task 4: Crear template stop.py.j2
- Crear archivo `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/stop.py.j2`
- Incluir shebang `#!/usr/bin/env python3`
- Generar resumen de sesión en `{{ config.paths.logs_dir }}/{session_id}/summary.json`
- Incluir en el resumen: session_id, ended_at (timestamp), tool_uses count
- Contar tool uses leyendo el archivo post_tool_use.json
- Manejar caso donde el directorio de logs no existe (sesión sin actividad)

### Task 5: Crear template utils/__init__.py.j2
- Crear archivo `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/__init__.py.j2`
- Incluir docstring: `"""Hook utilities for {{ config.project.name }}."""`
- Mantener el archivo simple (solo docstring, sin exports adicionales)

### Task 6: Crear template utils/constants.py.j2
- Crear archivo `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2`
- Incluir shebang `#!/usr/bin/env python3`
- Definir constantes del proyecto: PROJECT_NAME, LANGUAGE, PACKAGE_MANAGER usando config
- Definir constantes de paths: LOG_DIR, SPECS_DIR, ADWS_DIR usando `{{ config.paths.* }}`
- Definir listas de safety: FORBIDDEN_PATHS, ALLOWED_PATHS usando `{% for path in config.agentic.safety.* %}`
- Todos los valores deben venir de variables de configuración (nada hardcoded)

### Task 7: Test rendering de templates con datos de prueba
- Crear script de prueba Python inline que:
  - Importa TemplateRepository y modelos del domain
  - Crea un TACConfig de prueba con todos los campos necesarios
  - Renderiza cada uno de los 5 templates creados
  - Imprime las primeras líneas de cada template renderizado para verificación
- Ejecutar con `uv run python -c "..."`
- Verificar que todos los templates renderizan sin errores
- Verificar que las variables Jinja2 se reemplazan correctamente

### Task 8: Verificar que todos los archivos están creados
- Ejecutar `ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/` para listar hooks principales
- Ejecutar `ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/` para listar utils
- Verificar que existen exactamente 5 archivos .j2:
  - pre_tool_use.py.j2
  - post_tool_use.py.j2
  - stop.py.j2
  - utils/__init__.py.j2
  - utils/constants.py.j2

### Task 9: Ejecutar comandos de validación
- Ejecutar todos los comandos listados en la sección "Validation Commands"
- Verificar que los tests unitarios pasan sin regresiones
- Verificar que el linting no reporta errores en los nuevos templates
- Verificar que el CLI funciona correctamente (smoke test)

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- Los hooks usan `#!/usr/bin/env python3` como shebang (no `#!/usr/bin/env -S uv run --script` como en el repo actual)
- El formato de los templates debe seguir el estándar de la issue (proporcionado en el body)
- Los templates deben ser autónomos - no depender de imports externos que puedan no estar disponibles
- La validación en pre_tool_use debe ser estricta para prevenir operaciones peligrosas
- El logging en post_tool_use debe ser best-effort (no fallar si hay error)
- Todos los paths deben usar Path() de pathlib para cross-platform compatibility
- Los loops Jinja2 para listas usan: `{% for item in list %}...{% endfor %}`
- Las variables Jinja2 usan: `{{ variable }}`
- Los templates generados deben ser válidos Python sin modificaciones
