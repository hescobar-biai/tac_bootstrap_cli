# Chore: Documentar Makefile en README

## Metadata
issue_number: `51`
adw_id: `e2c9e980`
issue_json: `{"number":51,"title":"TAREA 9: Documentar Makefile en README","body":"**Archivo a modificar:** `README.md`\n\n**Prompt:**\n```\nActualiza README.md para documentar los comandos del Makefile.\n\nAgrega una nueva sección \"## Development\" después de \"## Installation\" con:\n\n### Quick Commands\n\n| Comando | Descripción |\n|---------|-------------|\n| `make install` | Instalar dependencias |\n| `make test` | Correr tests |\n| `make lint` | Verificar código |\n| `make format` | Formatear código |\n| ... | ... |\n\n### Development Workflow\n\n1. Clonar el repo\n2. `make install-dev`\n3. Hacer cambios\n4. `make lint format`\n5. `make test`\n6. Commit\n\n### Running the CLI locally\n\n```bash\nmake cli-help           # Ver ayuda\nmake cli-init-dry       # Probar init\nmake cli-doctor         # Probar doctor\n```\n\nMantén el estilo y formato existente del README.\n```\n\n**Criterios de aceptación:**\n- [ ] Nueva sección \"Development\" agregada\n- [ ] Tabla con todos los comandos make\n- [ ] Ejemplos de uso claros\n"}`

## Chore Description
Esta chore actualiza el `README.md` principal del repositorio para documentar los comandos del Makefile disponibles en `tac_bootstrap_cli/Makefile`. El Makefile fue creado en una tarea anterior (issue #49) y contiene comandos útiles para desarrollo, testing y build que facilitan el trabajo en el CLI.

Se debe agregar una nueva sección "## Development" después de la sección "## Installation" que incluya:
- Una tabla con todos los comandos make disponibles y su descripción
- Un workflow recomendado de desarrollo
- Ejemplos de uso del CLI usando make

La documentación debe seguir el estilo y formato existente del README.

## Relevant Files

### Files to Modify
- `README.md` - README principal del repositorio que necesita documentación del Makefile
  - Actualmente no tiene sección de Development
  - Tiene secciones de Comandos, Flujo de Usuario, Stack Soportado, etc.
  - La nueva sección irá después de las secciones existentes de comandos

### Files to Read
- `tac_bootstrap_cli/Makefile` - Makefile con comandos de desarrollo (ya leído)
  - Contiene comandos de instalación, desarrollo, testing, build y CLI examples
  - Tiene 18 comandos principales: install, install-dev, dev, lint, lint-fix, format, typecheck, test, test-v, test-cov, test-watch, build, clean, cli-help, cli-version, cli-init-dry, cli-doctor, help

### New Files
Ninguno - solo se modifica README.md existente.

## Step by Step Tasks

### Task 1: Leer estructura actual del README.md
- Identificar la ubicación exacta donde insertar la nueva sección "## Development"
- Verificar el formato y estilo existente (markdown, tablas, código)
- Confirmar que actualmente no existe una sección Development

### Task 2: Crear contenido de la sección Development
- Crear tabla markdown con todos los comandos make del Makefile
- Organizar comandos por categorías: Instalación, Desarrollo, Testing, Build, CLI Examples
- Escribir workflow de desarrollo paso a paso
- Incluir ejemplos de uso del CLI con make

### Task 3: Insertar nueva sección en README.md
- Agregar la sección "## Development" después de la sección de comandos existente
- Mantener el formato y estilo consistente con el resto del README
- Verificar que los enlaces y formato markdown funcionen correctamente

### Task 4: Validar cambios
- Revisar que el README.md se vea correctamente formateado
- Verificar que todos los comandos del Makefile estén documentados
- Confirmar que los ejemplos sean claros y útiles
- Ejecutar comandos de validación

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `cat README.md` - Verificar formato visualmente
- `make -C tac_bootstrap_cli help` - Verificar que comandos documentados existan

## Notes
- El Makefile está en `tac_bootstrap_cli/Makefile`, no en la raíz del repo
- El README.md está en la raíz del repositorio
- Los comandos make deben ejecutarse con `make -C tac_bootstrap_cli <target>` o desde el directorio tac_bootstrap_cli/
- Mantener consistencia con el estilo bilingüe español/inglés del README existente
- Los criterios de aceptación requieren: nueva sección Development, tabla completa de comandos, ejemplos claros
