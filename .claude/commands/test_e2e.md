# E2E Test Runner

Ejecutar tests end-to-end (E2E) usando Playwright browser automation (MCP Server).

## Nota para TAC Bootstrap CLI

Este comando está diseñado para proyectos que generará TAC Bootstrap CLI que tengan UI web.
Para el desarrollo del CLI mismo, usar `/test` que ejecuta tests unitarios de Python.

## Cuándo Usar Este Comando

- Cuando el proyecto generado tenga una UI web (frontend)
- Cuando existan archivos de test en `.claude/commands/e2e/`
- NO usar para el desarrollo del CLI tac-bootstrap en sí

## Variables

adw_id: $ARGUMENT si se proporciona, de lo contrario generar hex string de 8 caracteres
agent_name: $ARGUMENT si se proporciona, de lo contrario usar 'test_e2e'
e2e_test_file: $ARGUMENT
application_url: $ARGUMENT si se proporciona, de lo contrario determinar de configuración de puerto:
  - Si `.ports.env` existe, usar http://localhost:${FRONTEND_PORT}
  - De lo contrario usar default http://localhost:5173

## Instructions

- Si `application_url` no se proporciona, verificar `.ports.env`:
  - Si existe, usar http://localhost:${FRONTEND_PORT}
  - De lo contrario usar default http://localhost:5173
- Leer el `e2e_test_file`
- Digerir el `User Story` para entender qué se valida
- IMPORTANTE: Ejecutar los `Test Steps` detallados en `e2e_test_file` usando Playwright
- Revisar `Success Criteria` y si alguno falla, marcar test como fallido
- Capturar screenshots según especificado
- IMPORTANTE: Retornar resultados en el formato del `Output Format`
- Inicializar Playwright browser en modo headed para visibilidad
- Usar la URL determinada de `application_url`
- Permitir tiempo para operaciones async y visibilidad de elementos
- Si hay error, marcar test como fallido inmediatamente y explicar qué paso falló

## Setup

Leer y Ejecutar `.claude/commands/prepare_app.md` para preparar la aplicación.

## Screenshot Directory

<absolute path to codebase>/agents/<adw_id>/<agent_name>/img/<directory name based on test file name>/*.png

Cada screenshot debe guardarse con nombre descriptivo. La estructura de directorios asegura que:
- Screenshots están organizados por ADW ID (workflow run)
- Se almacenan bajo el nombre de agente especificado
- Cada test tiene su propio subdirectorio basado en el nombre del archivo de test

## Report

- Retornar exclusivamente el JSON output especificado en el archivo de test
- Capturar errores inesperados
- IMPORTANTE: Asegurar que todos los screenshots estén en `Screenshot Directory`

### Output Format

```json
{
  "test_name": "Test Name Here",
  "status": "passed|failed",
  "screenshots": [
    "<absolute path>/agents/<adw_id>/<agent_name>/img/<test name>/01_<descriptive name>.png"
  ],
  "error": null
}
```
