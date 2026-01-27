# TAC Bootstrap - Guia para Agentes

## Descripcion del Proyecto

TAC Bootstrap es una CLI en Python que genera Agentic Layers para proyectos.
Este repositorio sirve como:
1. **Generador**: El CLI que crea la estructura para otros proyectos
2. **Template Base**: Los archivos en `.claude/`, `adws/`, `scripts/` son templates

## Estructura del Proyecto

```
tac_bootstrap/
├── .claude/                    # [TEMPLATE] Usar como base para templates Jinja2
│   ├── settings.json           # Permisos y hooks
│   ├── commands/               # 25+ comandos slash
│   └── hooks/                  # Scripts de automatizacion
├── adws/                       # [TEMPLATE] AI Developer Workflows
│   ├── adw_modules/            # Modulos reutilizables
│   ├── adw_*_iso.py            # Workflows aislados
│   └── adw_triggers/           # Triggers automaticos
├── scripts/                    # [TEMPLATE] Scripts de utilidad
├── ai_docs/doc/                # Documentacion del curso TAC (1-8)
├── PLAN_TAC_BOOTSTRAP.md       # Plan de implementacion (LEER PRIMERO)
└── tac_bootstrap_cli/          # [A CREAR] CLI del generador
```

## Plan de Implementacion

El archivo `PLAN_TAC_BOOTSTRAP.md` contiene el plan completo con:
- 9 fases de desarrollo
- Cada tarea escrita como prompt para agente
- Codigo de ejemplo completo
- Criterios de aceptacion

**IMPORTANTE**: Seguir el plan en orden. Cada tarea depende de las anteriores.

## Comandos Disponibles

### Para Desarrollo del Generador
```bash
/prime                  # Preparar contexto
/scout "<task>" [scale] # Explorar codebase para encontrar archivos relevantes
/feature <desc>         # Planificar feature
/implement <plan>       # Ejecutar plan
/test                   # Correr tests
/review <plan>          # Revisar implementacion
/commit                 # Crear commit
```

### ADW Workflows
```bash
uv run adws/adw_sdlc_iso.py --issue <num>       # SDLC completo
uv run adws/adw_patch_iso.py --issue <num>      # Patch rapido
```

## Reglas de Desarrollo

1. **No modificar archivos en**:
   - `.env`
   - `secrets/`
   - Credenciales

2. **Siempre correr tests** antes de completar trabajo:
   ```bash
   uv run pytest
   ```

3. **Seguir arquitectura DDD** para el generador:
   - `domain/` - Modelos Pydantic
   - `application/` - Servicios de negocio
   - `infrastructure/` - Templates, filesystem
   - `interfaces/` - CLI Typer

4. **Templates Jinja2** deben usar variable `config`:
   ```jinja2
   {{ config.project.name }}
   {{ config.commands.start }}
   ```

## Flujo de Trabajo Recomendado

```
1. Leer PLAN_TAC_BOOTSTRAP.md
2. Identificar siguiente tarea
3. Ejecutar prompt de la tarea
4. Verificar criterios de aceptacion
5. Commit con mensaje descriptivo
6. Continuar con siguiente tarea
```

## Dependencias

- Python 3.10+
- uv (package manager)
- Typer, Rich, Jinja2, Pydantic, PyYAML

## Referencias

- [PLAN_TAC_BOOTSTRAP.md](PLAN_TAC_BOOTSTRAP.md) - Plan detallado
- [ai_docs/doc/](ai_docs/doc/) - Curso TAC completo
- [adws/README.md](adws/README.md) - Documentacion ADW
