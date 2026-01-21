# Plan de Completación: TAC Bootstrap CLI

> Este documento contiene las tareas pendientes para completar el CLI al 100%.
> Cada tarea está escrita como un prompt para ejecución con agentic coding.

---

## Estado Actual: 90% Completado

### Gaps Identificados:
1. 4 templates de comandos faltantes
2. Tests de CLI y wizard incompletos
3. Falta Makefile para facilitar desarrollo

---

## TAREA 1: Crear Template `lint.md.j2`

**Archivo a crear:** `tac_bootstrap/templates/claude/commands/lint.md.j2`

**Prompt:**
```
Crea el template Jinja2 para el comando slash /lint.

Este comando debe:
1. Ejecutar el linter configurado en config.commands.lint
2. Mostrar errores encontrados de forma clara
3. Sugerir fixes automáticos si están disponibles

Usa como referencia los templates existentes en:
- tac_bootstrap/templates/claude/commands/test.md.j2
- tac_bootstrap/templates/claude/commands/build.md.j2

El template debe usar las variables:
- {{ config.project.name }}
- {{ config.commands.lint }}
- {{ config.project.language }}

Incluye secciones para:
- Descripción del comando
- Pasos de ejecución
- Manejo de errores
- Output esperado
```

**Criterios de aceptación:**
- [ ] Template renderiza sin errores
- [ ] Usa variables de config correctamente
- [ ] Sigue el mismo formato que otros comandos

---

## TAREA 2: Crear Template `prepare_app.md.j2`

**Archivo a crear:** `tac_bootstrap/templates/claude/commands/prepare_app.md.j2`

**Prompt:**
```
Crea el template Jinja2 para el comando slash /prepare_app.

Este comando prepara la aplicación para ejecución:
1. Verifica dependencias instaladas
2. Configura variables de entorno necesarias
3. Ejecuta migraciones si aplica
4. Valida que la app puede iniciarse

Usa como referencia:
- tac_bootstrap/templates/claude/commands/start.md.j2
- El comando /prepare_app en ../../.claude/commands/prepare_app.md

Variables disponibles:
- {{ config.project.name }}
- {{ config.project.language }}
- {{ config.project.framework }}
- {{ config.commands.start }}
- {{ config.paths.app_root }}

El comando debe ser idempotente (ejecutar múltiples veces no causa problemas).
```

**Criterios de aceptación:**
- [ ] Template renderiza sin errores
- [ ] Cubre preparación para diferentes lenguajes
- [ ] Es idempotente

---

## TAREA 3: Crear Template `install.md.j2`

**Archivo a crear:** `tac_bootstrap/templates/claude/commands/install.md.j2`

**Prompt:**
```
Crea el template Jinja2 para el comando slash /install.

Este comando instala dependencias del proyecto:
1. Detecta el package manager (uv, npm, poetry, etc.)
2. Ejecuta el comando de instalación apropiado
3. Verifica instalación exitosa
4. Reporta cualquier error de dependencias

Variables disponibles:
- {{ config.project.package_manager }}
- {{ config.project.language }}
- {{ config.paths.app_root }}

Mapeo de package managers a comandos:
- uv -> uv sync
- poetry -> poetry install
- pip -> pip install -r requirements.txt
- npm -> npm install
- pnpm -> pnpm install
- yarn -> yarn install
- bun -> bun install

Incluye manejo de errores común (network, permissions, version conflicts).
```

**Criterios de aceptación:**
- [ ] Template renderiza sin errores
- [ ] Soporta todos los package managers del enum
- [ ] Incluye verificación post-instalación

---

## TAREA 4: Crear Template `track_agentic_kpis.md.j2`

**Archivo a crear:** `tac_bootstrap/templates/claude/commands/track_agentic_kpis.md.j2`

**Prompt:**
```
Crea el template Jinja2 para el comando slash /track_agentic_kpis.

Este comando trackea los KPIs de Tactical Agentic Coding:
1. SIZE: Trabajo delegable a agentes por ejecución
2. ATTEMPTS: Iteraciones requeridas post-ejecución
3. STREAK: Ejecuciones one-shot exitosas consecutivas
4. PRESENCE: Tiempo humano requerido durante ejecución

El comando debe:
1. Leer logs de ejecuciones anteriores en {{ config.paths.logs_dir }}
2. Calcular métricas agregadas
3. Mostrar tendencias (mejorando/empeorando)
4. Sugerir acciones para mejorar KPIs

Usa como referencia:
- El comando existente en ../../.claude/commands/track_agentic_kpis.md
- Documentación TAC en ai_docs/doc/

Output en formato tabla con Rich.
```

**Criterios de aceptación:**
- [ ] Template renderiza sin errores
- [ ] Define los 4 KPIs claramente
- [ ] Incluye cálculo y visualización

---

## TAREA 5: Completar Tests de CLI

**Archivo a modificar:** `tests/test_cli.py`

**Prompt:**
```
Expande los tests en tests/test_cli.py para cubrir todos los comandos del CLI.

Actualmente solo hay 2 tests triviales. Necesitamos tests para:

1. **test_version_command**: Verificar que muestra versión correcta
2. **test_init_dry_run**: Probar init con --dry-run
3. **test_init_with_options**: Probar init con --language, --framework
4. **test_add_agentic_dry_run**: Probar add-agentic con --dry-run
5. **test_doctor_healthy**: Probar doctor en directorio válido
6. **test_doctor_with_fix**: Probar doctor --fix
7. **test_render_dry_run**: Probar render con --dry-run

Usa CliRunner de Typer para invocar comandos.
Usa tmp_path fixture de pytest para crear directorios temporales.

Referencia los tests existentes en:
- tests/test_scaffold_service.py
- tests/test_doctor_service.py

Cada test debe verificar:
- Exit code correcto
- Output contiene texto esperado
- No hay excepciones no manejadas
```

**Criterios de aceptación:**
- [ ] Al menos 7 tests nuevos
- [ ] Cobertura de todos los comandos principales
- [ ] Tests pasan con `uv run pytest tests/test_cli.py -v`

---

## TAREA 6: Crear Tests de Wizard

**Archivo a crear:** `tests/test_wizard.py`

**Prompt:**
```
Crea tests para el módulo wizard en tests/test_wizard.py.

El wizard usa Rich para prompts interactivos. Para testear:
1. Mockear rich.prompt.Prompt
2. Mockear rich.console.Console

Tests a crear:

1. **test_select_from_enum**: Verificar selección de enums
2. **test_run_init_wizard_defaults**: Wizard con valores por defecto
3. **test_run_init_wizard_custom**: Wizard con valores custom
4. **test_run_add_agentic_wizard**: Wizard para repos existentes
5. **test_wizard_cancellation**: Verificar manejo de Ctrl+C

Usa pytest-mock o unittest.mock para los mocks.

Referencia:
- tac_bootstrap/interfaces/wizard.py
- Patrones de mock en tests existentes
```

**Criterios de aceptación:**
- [ ] Al menos 5 tests
- [ ] Mocks funcionan correctamente
- [ ] Tests pasan sin interacción manual

---

## TAREA 7: Habilitar Tests @skip en scaffold_service

**Archivo a modificar:** `tests/test_scaffold_service.py`

**Prompt:**
```
Revisa tests/test_scaffold_service.py y habilita los tests marcados con @pytest.mark.skip.

Actualmente hay ~15 tests deshabilitados con reason="Requires real templates".

Para cada test @skip:
1. Analiza qué template necesita
2. Verifica que el template existe
3. Si existe, remueve el decorador @skip
4. Si no existe, documenta cuál falta

Los templates están en: tac_bootstrap/templates/

Después de habilitar, corre:
uv run pytest tests/test_scaffold_service.py -v

Asegúrate de que todos los tests pasen.
```

**Criterios de aceptación:**
- [ ] Todos los @skip removidos o justificados
- [ ] Tests pasan después de habilitarlos
- [ ] Cobertura de scaffold_service > 80%

---

## TAREA 8: Crear Makefile

**Archivo a crear:** `Makefile`

**Prompt:**
```
Crea un Makefile en la raíz de tac_bootstrap_cli/ con comandos útiles para desarrollo.

Comandos a incluir:

# Instalación
install:        Instalar dependencias con uv
install-dev:    Instalar con dependencias de desarrollo

# Desarrollo
dev:            Correr CLI en modo desarrollo
lint:           Ejecutar ruff check
lint-fix:       Ejecutar ruff con auto-fix
format:         Formatear código con ruff format
typecheck:      Ejecutar mypy

# Testing
test:           Correr todos los tests
test-v:         Correr tests con verbose
test-cov:       Correr tests con coverage report
test-watch:     Correr tests en modo watch (si pytest-watch está disponible)

# Build
build:          Construir paquete wheel
clean:          Limpiar archivos generados (__pycache__, .pytest_cache, etc.)

# CLI
cli-help:       Mostrar ayuda del CLI
cli-version:    Mostrar versión
cli-init-dry:   Ejemplo de init con dry-run
cli-doctor:     Ejemplo de doctor

# Utilidades
help:           Mostrar ayuda de todos los comandos

Usa variables para rutas:
PYTHON := uv run python
PYTEST := uv run pytest
CLI := uv run tac-bootstrap

Incluye .PHONY para todos los targets.
```

**Criterios de aceptación:**
- [ ] Makefile funciona con `make <comando>`
- [ ] Todos los comandos documentados
- [ ] `make help` muestra todos los comandos

---

## TAREA 9: Documentar Makefile en README

**Archivo a modificar:** `README.md`

**Prompt:**
```
Actualiza README.md para documentar los comandos del Makefile.

Agrega una nueva sección "## Development" después de "## Installation" con:

### Quick Commands

| Comando | Descripción |
|---------|-------------|
| `make install` | Instalar dependencias |
| `make test` | Correr tests |
| `make lint` | Verificar código |
| `make format` | Formatear código |
| ... | ... |

### Development Workflow

1. Clonar el repo
2. `make install-dev`
3. Hacer cambios
4. `make lint format`
5. `make test`
6. Commit

### Running the CLI locally

```bash
make cli-help           # Ver ayuda
make cli-init-dry       # Probar init
make cli-doctor         # Probar doctor
```

Mantén el estilo y formato existente del README.
```

**Criterios de aceptación:**
- [ ] Nueva sección "Development" agregada
- [ ] Tabla con todos los comandos make
- [ ] Ejemplos de uso claros

---

## Orden de Ejecución Recomendado

```
1. TAREA 8: Crear Makefile (facilita desarrollo)
2. TAREA 9: Documentar Makefile en README
3. TAREA 1-4: Crear los 4 templates faltantes
4. TAREA 7: Habilitar tests @skip
5. TAREA 5-6: Completar tests de CLI y wizard
```

---

## Verificación Final

Después de completar todas las tareas:

```bash
# Verificar que todo funciona
make install-dev
make lint
make test-cov

# Probar CLI end-to-end
make cli-init-dry
```

**Definición de Done:**
- [ ] `make test` pasa sin errores
- [ ] `make lint` sin warnings
- [ ] Cobertura > 80%
- [ ] CLI genera proyectos correctamente
