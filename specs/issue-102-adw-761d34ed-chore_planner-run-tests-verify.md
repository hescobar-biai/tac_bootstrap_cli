# Chore: Ejecutar tests y verificar sincronización base-template

## Metadata
issue_number: `102`
adw_id: `761d34ed`
issue_json: `{"number":102,"title":"Tarea 3: Ejecutar tests y verificar","body":"/chore\n**Prompt para el agente**:\n\n```\nEjecuta los tests del proyecto para verificar que los cambios no rompieron nada:\n\nuv run pytest\n\nSi hay errores:\n1. Lee el mensaje de error completo\n2. Identifica el archivo y línea con el problema\n3. Corrige el error en AMBOS archivos (base y template) si aplica\n4. Vuelve a ejecutar los tests\n\nTodos los tests deben pasar antes de continuar.\n\nVerifica también que los archivos base y template estén sincronizados:\n- adws/adw_modules/workflow_ops.py debe tener resolve_clarifications()\n- tac_bootstrap_cli/.../workflow_ops.py.j2 debe tener la misma función (con {% raw %} en el JSON)\n- adws/adw_plan_iso.py NO debe tener sys.exit(2) para clarificaciones\n- tac_bootstrap_cli/.../adw_plan_iso.py.j2 debe tener los mismos cambios\n```\n"}`

## Chore Description
Esta tarea verifica la integridad del proyecto después de implementar la función `resolve_clarifications()` en la Tarea 2. Los objetivos son:

1. **Ejecutar tests** y corregir errores hasta que pasen (máximo 3 intentos)
2. **Verificar sincronización** entre archivos base y templates Jinja2:
   - `workflow_ops.py` debe tener `resolve_clarifications()`
   - Template `workflow_ops.py.j2` debe tener la misma función con `{% raw %}` en JSON
   - `adw_plan_iso.py` NO debe tener `sys.exit(2)` en manejo de clarificaciones
   - Template `adw_plan_iso.py.j2` debe reflejar los cambios de auto-resolución

3. **Auto-sync** si hay diferencias: copiar lógica del archivo base al template con sintaxis Jinja2 apropiada

## Relevant Files
Archivos involucrados en la tarea:

### Archivos base (código funcional)
- `adws/adw_modules/workflow_ops.py` - Contiene `resolve_clarifications()` implementada en Tarea 2
- `adws/adw_plan_iso.py` - Workflow de planning que usa auto-resolución sin `sys.exit(2)`

### Templates Jinja2 (para proyectos generados)
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2` - Template de workflow_ops
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2` - Template de adw_plan_iso

### Tests
- `tests/` - Tests del proyecto (ubicación exacta a determinar)

### New Files
No se crean archivos nuevos en esta tarea.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Ejecutar tests (1er intento)
- Ejecutar: `uv run pytest`
- Capturar output completo con errores/warnings
- Si todos pasan → continuar a Task 4
- Si hay errores → continuar a Task 2

### Task 2: Analizar y corregir errores de tests (hasta 3 intentos)
- Leer mensaje de error completo identificando:
  - Archivo y número de línea
  - Tipo de error (import, sintaxis, assertion, etc)
  - Si el error está en archivo base o template
- Corregir error:
  - Si está en archivo base → aplicar fix
  - Si está en template → aplicar fix con sintaxis Jinja2 correcta
  - Si la lógica debe estar sincronizada → corregir AMBOS archivos
- Volver a ejecutar: `uv run pytest`
- Repetir hasta que pasen o se alcancen 3 intentos
- Si después de 3 intentos aún hay errores → reportar y detener

### Task 3: Verificar sincronización workflow_ops.py ↔ workflow_ops.py.j2
- Leer `adws/adw_modules/workflow_ops.py` líneas 269-354 (función `resolve_clarifications()`)
- Leer `tac_bootstrap_cli/.../workflow_ops.py.j2` líneas 269-354
- Comparar:
  - ¿Existe la función `resolve_clarifications()` en template?
  - ¿Tiene los mismos parámetros y lógica?
  - ¿JSON strings tienen `{% raw %}...{% endraw %}`? (ver línea 304-307)
- Si hay diferencias → auto-sync:
  - Copiar función del base al template
  - Wrappear JSON literal con `{% raw %}{% endraw %}`
  - Usar `Edit` tool para actualizar template
- Verificar no rompe tests: `uv run pytest`

### Task 4: Verificar adw_plan_iso.py NO tiene sys.exit(2)
- Ejecutar: `grep -n "sys.exit(2)" adws/adw_plan_iso.py`
- Si encuentra match → ERROR: el archivo base aún tiene código de pausa manual
- Si no encuentra → continuar

### Task 5: Verificar sincronización adw_plan_iso.py ↔ adw_plan_iso.py.j2
- Leer sección de clarificaciones en `adws/adw_plan_iso.py` (líneas 128-207)
- Leer misma sección en template `tac_bootstrap_cli/.../adw_plan_iso.py.j2`
- Comparar:
  - ¿Template tiene la llamada a `resolve_clarifications()`?
  - ¿Tiene el mismo flujo: detectar → resolver → continuar?
  - ¿NO tiene `sys.exit(2)` para pausas?
- Si hay diferencias → auto-sync:
  - Identificar bloques diferentes
  - Copiar lógica del base al template
  - Mantener variables Jinja2 existentes (ej: `{{ config.project.name }}`)
  - Usar `Edit` tool para actualizar
- Verificar no rompe tests: `uv run pytest`

### Task 6: Validación final
- Ejecutar todos los comandos de validación:
  - `uv run pytest` - Tests unitarios (deben pasar 100%)
  - `grep -n "resolve_clarifications" adws/adw_modules/workflow_ops.py` - Debe encontrar función
  - `grep -n "resolve_clarifications" tac_bootstrap_cli/.../workflow_ops.py.j2` - Debe encontrar función
  - `grep -n "sys.exit(2)" adws/adw_plan_iso.py` - NO debe encontrar
- Si todo pasa → tarea completada
- Si algo falla → reportar discrepancia específica

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `uv run pytest` - Tests unitarios (deben pasar todos)
- `grep -n "resolve_clarifications" adws/adw_modules/workflow_ops.py` - Verificar función existe
- `grep -n "resolve_clarifications" tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2` - Verificar en template
- `grep -n "sys.exit(2)" adws/adw_plan_iso.py` - NO debe encontrar (exit code 1 esperado)

## Notes

### Contexto de Auto-Resolved Clarifications
Esta tarea verifica los cambios implementados en issue #100 donde se agregó auto-resolución de clarificaciones:
- Función `resolve_clarifications()` en `workflow_ops.py`
- Integración en `adw_plan_iso.py` sin pausas (`sys.exit(2)` removido)
- Templates `.j2` deben estar sincronizados para proyectos generados

### Manejo de JSON en Templates Jinja2
En templates `.j2`, los strings JSON literales con llaves deben wrapped:
```jinja2
prompt = f"""Return JSON:
{% raw %}{{
  "decisions": [{{"question": "...", "decision": "..."}}]
}}{% endraw %}"""
```

Sin `{% raw %}`, Jinja2 interpreta `{{ }}` como variables a sustituir.

### Límite de reintentos
Máximo 3 ciclos de fix-and-retry para tests. Después de 3 fallos reportar y solicitar guía humana.

### Equivalencia semántica vs exacta
Al comparar base vs template, buscar equivalencia funcional:
- Lógica idéntica
- Parámetros iguales
- `{% raw %}` es esperado y válido en templates
- Variables Jinja2 como `{{ config.x }}` son válidas en templates
