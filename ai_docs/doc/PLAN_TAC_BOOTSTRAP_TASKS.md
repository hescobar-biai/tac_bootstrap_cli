# Plan de tareas — TAC Bootstrap (mejoras)

Orden sugerido de ejecucion. Cada tarea indica tipo al inicio y especifica archivo raiz y template.

1) [Bug] Corregir estructura y consistencia de `config.yml` con el schema actual
- Archivo raiz: `config.yml`
- Archivo template: `tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2`
- Objetivo: alinear claves/indentacion con `TACConfig` (project/paths/commands/agentic/claude/templates/bootstrap) y eliminar claves fuera de seccion.
- Criterio de aceptacion: `tac-bootstrap render` puede cargar y validar el YAML sin errores.

2) [Feature] Agregar modo de ejecucion unica (`--once`) en triggers cron
- Archivo raiz: `adws/adw_triggers/trigger_cron.py`
- Archivo template: `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2`
- Objetivo: permitir un ciclo de verificacion y salida limpia sin bucle de scheduler.
- Criterio de aceptacion: `uv run adws/adw_triggers/trigger_cron.py --once` ejecuta un ciclo y termina.

3) [Feature] Agregar modo de ejecucion unica (`--once`) en trigger de cadena
- Archivo raiz: `adws/adw_triggers/trigger_issue_chain.py`
- Archivo template: `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_issue_chain.py.j2`
- Objetivo: permitir un ciclo para validar rapidamente el orden de issues.
- Criterio de aceptacion: `uv run adws/adw_triggers/trigger_issue_chain.py --issues 1,2,3 --once` ejecuta un ciclo y termina.

4) [Feature] Documentar el trigger de cadena en el README de ADWs
- Archivo raiz: `adws/README.md`
- Archivo template: `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2`
- Objetivo: explicar uso, orden de ejecucion y ejemplos de comando.
- Criterio de aceptacion: README incluye seccion con ejemplos y comportamiento de espera hasta cierre del issue anterior.

5) [Chore] Enumerar triggers disponibles en paquete `adw_triggers`
- Archivo raiz: `adws/adw_triggers/__init__.py`
- Archivo template: `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/__init__.py.j2`
- Objetivo: agregar docstring breve con listado actualizado de triggers y su proposito.
- Criterio de aceptacion: el modulo expone documentacion clara en una sola fuente.

6) [Feature] Incluir configuracion de intervalos en docs de triggers
- Archivo raiz: `adws/README.md`
- Archivo template: `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2`
- Objetivo: explicar `--interval` y la relacion con `agentic.cron_interval` en config.
- Criterio de aceptacion: README menciona el valor por defecto y como overridearlo.

7) [Chore] Actualizar CHANGELOG con nueva version
- Archivo raiz: `CHANGELOG.md`
- Archivo template: `tac_bootstrap_cli/tac_bootstrap/templates/CHANGELOG.md.j2` (si aplica; crear si no existe)
- Objetivo: registrar cambios de triggers y configuracion.
- Criterio de aceptacion: nueva version agregada con lista de cambios, fecha y semver.
