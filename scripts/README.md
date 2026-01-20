# Scripts

Este directorio contiene scripts de utilidad organizados en dos categorías:

## Scripts de Desarrollo del CLI (`dev_*`)

Para desarrollar el generador TAC Bootstrap:

| Script | Descripción |
|--------|-------------|
| `dev_start.sh` | Ejecutar CLI en modo desarrollo |
| `dev_test.sh` | Correr tests del CLI |
| `dev_lint.sh` | Verificar linting del CLI |
| `dev_build.sh` | Construir paquete del CLI |

```bash
# Ejemplo de uso
./scripts/dev_test.sh
./scripts/dev_lint.sh
./scripts/dev_build.sh
```

## Scripts Template (Ejemplos)

Scripts que sirven como **templates/ejemplos** de lo que TAC Bootstrap genera para proyectos:

| Script | Descripción |
|--------|-------------|
| `start.sh` | Iniciar app de ejemplo (frontend + backend) |
| `stop_apps.sh` | Detener servicios |
| `check_ports.sh` | Verificar puertos disponibles |
| `copy_dot_env.sh` | Copiar archivo .env de ejemplo |
| `purge_tree.sh` | Limpiar worktrees de git |

## Scripts ADW

Scripts para el sistema AI Developer Workflow:

| Script | Descripción |
|--------|-------------|
| `aea_server_start.sh` | Iniciar servidor AEA |
| `aea_server_reset.sh` | Resetear servidor AEA |
| `expose_webhook.sh` | Exponer webhook con ngrok |
| `kill_trigger_webhook.sh` | Matar proceso de webhook |
| `clear_issue_comments.sh` | Limpiar comentarios de issues |
| `delete_pr.sh` | Eliminar PR |
| `reset_db.sh` | Resetear base de datos |

## Uso como Templates

Los scripts `start.sh`, `test.sh`, `lint.sh`, `build.sh` serán convertidos a templates Jinja2 en:
```
tac_bootstrap_cli/tac_bootstrap/templates/scripts/
```

Cuando se implemente TAREA 3.5 del plan.
