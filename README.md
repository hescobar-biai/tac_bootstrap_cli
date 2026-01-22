# TAC Bootstrap

CLI en Python que crea o inyecta una **Agentic Layer** basada en Claude Code para acelerar ingenieria con patrones TAC (Tactical Agentic Coding).

## Problema que Resuelve

Muchos equipos usando IA siguen trabajando "en loop" (chat/IDE) y no logran:
- Estandarizar prompts de ingenieria
- Orquestar flujos repetibles (plan/build/test/review/ship)
- Ejecutar en paralelo (worktrees / entornos aislados)
- Tener trazabilidad completa (logs, specs, evidencias)
- Integrar triggers automaticos (cron/webhook/tareas)

## Solucion

TAC Bootstrap genera automaticamente toda la infraestructura agentica:

```
proyecto/
├── .claude/                    # Configuracion Claude Code
│   ├── settings.json           # Permisos y hooks
│   ├── commands/               # 25+ comandos slash
│   │   ├── prime.md            # Priming del agente
│   │   ├── feature.md          # Planificacion features
│   │   ├── implement.md        # Ejecucion de planes
│   │   └── ...
│   └── hooks/                  # Automatizacion
│       ├── pre_tool_use.py     # Validacion pre-ejecucion
│       └── post_tool_use.py    # Logging post-ejecucion
├── adws/                       # AI Developer Workflows
│   ├── adw_modules/            # Modulos compartidos
│   ├── adw_sdlc_iso.py         # Workflow SDLC completo
│   └── adw_triggers/           # Triggers automaticos
├── scripts/                    # Scripts de utilidad
├── specs/                      # Especificaciones
├── logs/                       # Logs de sesiones
└── config.yml                  # Fuente de verdad
```

## Comandos

```bash
# Crear proyecto nuevo con Agentic Layer
tac-bootstrap init my-project

# Inyectar Agentic Layer en proyecto existente
tac-bootstrap add-agentic --repo .

# Validar setup
tac-bootstrap doctor --repo .

# Re-generar desde config.yml
tac-bootstrap render --config config.yml

# Actualizar proyecto existente a la última versión
tac-bootstrap upgrade
```

## Actualizar Proyectos Existentes

Si tienes un proyecto creado con una versión anterior de TAC Bootstrap, puedes actualizarlo a los templates más recientes:

```bash
# Verificar qué se actualizaría
tac-bootstrap upgrade --dry-run

# Actualizar con backup (por defecto)
tac-bootstrap upgrade

# Actualizar sin backup
tac-bootstrap upgrade --no-backup

# Forzar actualización aunque las versiones coincidan
tac-bootstrap upgrade --force

# Actualizar proyecto específico
tac-bootstrap upgrade ./path/to/project
```

### Qué se Actualiza

El comando upgrade actualiza:
- `adws/` - AI Developer Workflows
- `.claude/` - Configuración de Claude Code
- `scripts/` - Scripts de utilidad

Se preserva:
- `src/` - Tu código de aplicación
- `config.yml` - Tu configuración (solo se actualiza la versión)
- Cualquier archivo personalizado que hayas agregado

### Backup

Por defecto, se crea un backup en `.tac-backup-{timestamp}/` antes de actualizar.
Elimínalo manualmente después de confirmar que la actualización funciona correctamente.

## Flujo de Usuario

```
tac-bootstrap init
       |
       v
¿Proyecto NUEVO o EXISTENTE?
       |
   [NUEVO]              [EXISTENTE]
       |                     |
       v                     v
  Pregunta:            Auto-detecta:
  - Lenguaje           - Lenguaje
  - Framework          - Framework
  - Arquitectura       - Package manager
  - Comandos
       |                     |
       v                     v
    GENERA AGENTIC LAYER
       |
       v
  Proyecto listo para
  trabajar con agentes!
```

## Stack Soportado

| Lenguaje | Frameworks | Package Managers |
|----------|------------|------------------|
| Python | FastAPI, Django, Flask | uv, poetry, pip |
| TypeScript | Next.js, Nest.js, Express | pnpm, npm, bun |
| JavaScript | Next.js, Express, React | pnpm, npm, bun |
| Go | Gin, Echo | go |

## Arquitecturas Soportadas

- **Simple** - Estructura plana
- **Layered** - Controllers/Services/Repositories
- **DDD** - Domain-Driven Design
- **Clean** - Clean Architecture
- **Hexagonal** - Ports & Adapters

---

## Desarrollo del Generador

Este repositorio contiene el codigo fuente del generador TAC Bootstrap.

### Estructura del Generador

```
tac_bootstrap/
├── .claude/                    # [TEMPLATE] Comandos y hooks de ejemplo
│   ├── commands/               # 25+ comandos slash como templates
│   └── hooks/                  # Hooks Python como templates
├── adws/                       # [TEMPLATE] AI Developer Workflows
│   ├── adw_modules/            # Modulos reutilizables
│   └── adw_triggers/           # Triggers para automatizacion
├── scripts/                    # [TEMPLATE] Scripts de utilidad
├── ai_docs/                    # Documentacion de referencia (TAC 1-8)
├── PLAN_TAC_BOOTSTRAP.md       # Plan de implementacion detallado
└── tac_bootstrap_cli/          # [A CREAR] CLI Python del generador
    ├── domain/models.py        # Modelos Pydantic
    ├── application/            # Servicios (scaffold, detect, doctor)
    ├── infrastructure/         # Templates Jinja2, filesystem
    └── interfaces/cli.py       # Comandos Typer
```

### Plan de Implementacion

Ver [PLAN_TAC_BOOTSTRAP.md](PLAN_TAC_BOOTSTRAP.md) para el plan completo con:
- 9 fases de desarrollo
- Cada tarea como prompt para agente LLM
- Codigo de templates completo
- Criterios de aceptacion

### Desarrollo con Agentic Coding

Cada tarea del plan esta escrita como un prompt completo. Para implementar:

```bash
# 1. Abrir el plan
cat PLAN_TAC_BOOTSTRAP.md

# 2. Copiar el prompt de la tarea (ej: TAREA 1.1)
# 3. Ejecutar con Claude Code
claude -p "[prompt de la tarea]"

# 4. Verificar criterios de aceptacion
# 5. Continuar con siguiente tarea
```

### Comandos Disponibles (Desarrollo)

```bash
# Slash commands para desarrollo
/prime              # Preparar contexto del proyecto
/feature            # Planificar nueva funcionalidad
/implement <plan>   # Ejecutar un plan
/test               # Correr tests
/commit             # Crear commit

# ADW Workflows
uv run adws/adw_sdlc_iso.py --issue 123
uv run adws/adw_patch_iso.py --issue 456 --fix "descripcion"
```

### Development with Makefile

El CLI incluye un `Makefile` en `tac_bootstrap_cli/` con comandos convenientes para desarrollo.

#### Quick Commands

| Comando | Descripción |
|---------|-------------|
| `make install` | Instalar dependencias |
| `make install-dev` | Instalar con dependencias de desarrollo |
| `make dev` | Ejecutar CLI en modo desarrollo (smoke test) |
| `make lint` | Verificar código con ruff |
| `make lint-fix` | Verificar código con auto-fix |
| `make format` | Formatear código con ruff |
| `make typecheck` | Verificar tipos con mypy |
| `make test` | Correr todos los tests |
| `make test-v` | Correr tests con salida verbose |
| `make test-cov` | Correr tests con reporte de coverage |
| `make test-watch` | Correr tests en modo watch |
| `make build` | Construir paquete wheel |
| `make clean` | Limpiar archivos generados y caches |
| `make cli-help` | Mostrar ayuda del CLI |
| `make cli-version` | Mostrar versión del CLI |
| `make help` | Mostrar todos los comandos disponibles |

#### Development Workflow

1. Clonar el repositorio
   ```bash
   git clone <repo-url>
   cd tac_bootstrap
   ```

2. Instalar dependencias de desarrollo
   ```bash
   cd tac_bootstrap_cli
   make install-dev
   ```

3. Hacer cambios en el código

4. Verificar y formatear código
   ```bash
   make lint format
   ```

5. Ejecutar tests
   ```bash
   make test
   ```

6. Hacer commit de cambios
   ```bash
   git add .
   git commit -m "descripcion del cambio"
   ```

#### Running the CLI locally

```bash
# Ver ayuda general
make cli-help

# Ver versión
make cli-version

# Probar comando init (ejemplo)
uv run tac-bootstrap init my-project --dry-run

# Probar comando doctor (ejemplo)
uv run tac-bootstrap doctor
```

**Nota:** Los comandos `make` deben ejecutarse desde el directorio `tac_bootstrap_cli/` o usando `make -C tac_bootstrap_cli <target>` desde la raíz del repositorio.

### Publicar CLI al Repositorio de Distribución

El CLI se distribuye en un repositorio separado usando **git subtree**. Esto permite mantener el desarrollo en el monorepo pero publicar solo el CLI.

#### Configuración Inicial (ya realizada)

```bash
# Remote de distribución
git remote add tac-cli-dist https://github.com/celes-app/tac-cli-dist.git
```

#### Publicar Cambios

Después de hacer cambios en `tac_bootstrap_cli/`:

```bash
# 1. Commit tus cambios normalmente
git add .
git commit -m "feat: descripcion del cambio"

# 2. Push al monorepo (origin)
git push origin main

# 3. Sincronizar al repo de distribución
git subtree push --prefix=tac_bootstrap_cli tac-cli-dist main
```

#### Crear un Release

Después de sincronizar cambios importantes:

```bash
# 1. Actualizar versión en pyproject.toml (tac_bootstrap_cli/pyproject.toml)
# version = "0.2.0"

# 2. Commit y sincronizar
git add . && git commit -m "chore: bump version to 0.2.0"
git push origin main
git subtree push --prefix=tac_bootstrap_cli tac-cli-dist main

# 3. Crear release en GitHub
gh release create v0.2.0 \
  --repo celes-app/tac-cli-dist \
  --title "v0.2.0" \
  --notes "Release notes aquí"
```

> **Nota**: El tag en el README del CLI (`git clone --branch v0.1.0`) debe actualizarse cuando se crea un nuevo release.

#### Repositorios

| Repositorio | URL | Contenido |
|-------------|-----|-----------|
| Monorepo (desarrollo) | `hescobar-biai/tac_bootstrap_cli` | Todo el proyecto |
| Distribución (público) | `celes-app/tac-cli-dist` | Solo `tac_bootstrap_cli/` |

---

## Arquitectura Interna

### Modelos de Dominio

```python
# config.yml -> TACConfig
TACConfig
├── project: ProjectSpec       # nombre, lenguaje, framework, arquitectura
├── paths: PathsSpec           # rutas de directorios
├── commands: CommandsSpec     # start, test, lint, build
├── agentic: AgenticSpec       # worktrees, logging, safety
└── claude: ClaudeConfig       # settings.json, comandos
```

### Flujo de Generacion

```
config.yml
    |
    v
TACConfig (Pydantic validation)
    |
    v
ScaffoldService.build_plan()
    |
    v
ScaffoldPlan (lista de operaciones)
    |
    v
ScaffoldService.apply_plan()
    |
    v
Templates Jinja2 renderizados
    |
    v
Archivos generados en disco
```

---

## Referencia: Curso TAC

Este proyecto implementa los conceptos del curso **Tactical Agentic Coding (TAC)**:

| Leccion | Concepto | Implementacion |
|---------|----------|----------------|
| TAC-1 | Stop Coding | CLI genera codigo, no lo escribes |
| TAC-2 | KPIs Agenticos | Tracking en adw_modules |
| TAC-3 | Templates | .claude/commands/*.md |
| TAC-4 | ADWs | adws/*.py workflows |
| TAC-5 | Feedback Loops | hooks/ + tests |
| TAC-6 | Review & Document | /review, /document |
| TAC-7 | Zero-Touch | adw_sdlc_zte_iso.py |
| TAC-8 | Prioritize Agentics | 50%+ tiempo en capa agentica |

Ver [ai_docs/doc/](ai_docs/doc/) para documentacion completa del curso.

---

## Licencia

MIT
