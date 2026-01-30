# Prime

Preparar contexto del proyecto TAC Bootstrap.

## Run
```bash
git ls-files
```

## Read
- README.md
- CLAUDE.md
- PLAN_TAC_BOOTSTRAP.md
- config.yml
- adws/README.md

## Read Conditional
Usar `.claude/commands/conditional_docs.md` para determinar documentación adicional.

## Understand

### Proyecto: TAC Bootstrap CLI
- **Objetivo**: CLI en Python que genera Agentic Layers para proyectos
- **Stack**: Python 3.10+, Typer, Rich, Jinja2, Pydantic
- **Arquitectura**: DDD (Domain-Driven Design)

### Estructura Principal
```
tac_bootstrap/
├── .claude/commands/       # [TEMPLATE] Comandos slash (27 archivos)
├── .claude/hooks/          # [TEMPLATE] Hooks de automatización
├── adws/                   # [TEMPLATE] AI Developer Workflows
├── scripts/                # [TEMPLATE] Scripts de utilidad
├── prompts/templates/      # [TEMPLATE] Meta-prompts
├── ai_docs/doc/            # Documentación curso TAC (1-8)
├── PLAN_TAC_BOOTSTRAP.md   # Plan de implementación detallado
├── config.yml              # Configuración del proyecto
└── tac_bootstrap_cli/      # [A CREAR] CLI del generador
```

### Comandos de Desarrollo
```bash
# Scripts para desarrollo
./scripts/dev_test.sh       # Tests del CLI
./scripts/dev_lint.sh       # Linting
./scripts/dev_build.sh      # Build

# ADW Workflows
uv run adws/adw_sdlc_iso.py --issue <num>
```

### Plan de Trabajo
El archivo PLAN_TAC_BOOTSTRAP.md contiene 9 fases:
1. Setup del proyecto (0-10%)
2. Modelos de dominio (10-20%)
3. Sistema de templates (20-40%)
4. CLI con Typer (40-55%)
5. Servicio de scaffold (55-70%)
6. Servicio de detección (70-80%)
7. Servicio doctor (80-90%)
8. Tests (90-95%)
9. Documentación (95-100%)

## Report
- Resumen del proyecto TAC Bootstrap
- Estado actual del desarrollo (qué fases están completas)
- Siguiente tarea a implementar según el plan
- Archivos clave para la tarea actual

## Related Commands
- `/prime_cc` - Claude Code-optimized version that includes this context plus Claude Code-specific configuration (commands, hooks, settings)
