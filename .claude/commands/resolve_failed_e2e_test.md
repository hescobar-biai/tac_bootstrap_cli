# Resolve Failed E2E Test

Arreglar un test E2E específico que está fallando usando los detalles de falla proporcionados.

## Nota para TAC Bootstrap CLI

Este comando está diseñado para proyectos que generará TAC Bootstrap CLI que tengan UI web.
Para el desarrollo del CLI mismo, usar `/resolve_failed_test` para tests unitarios de Python.

## Instructions

1. **Analizar la Falla del Test E2E**
   - Revisar el JSON data en `Test Failure Input`, prestando atención a:
     - `test_name`: Nombre del test fallido
     - `test_path`: Path al archivo de test (necesario para re-ejecución)
     - `error`: Error específico que ocurrió
     - `screenshots`: Screenshots capturados mostrando el estado de falla
   - Entender qué valida el test desde perspectiva de interacción de usuario

2. **Entender Ejecución del Test**
   - Leer `.claude/commands/test_e2e.md` para entender cómo se ejecutan tests E2E
   - Leer el archivo de test especificado en el campo `test_path` del JSON
   - Notar los pasos del test, user story y criterios de éxito

3. **Reproducir la Falla**
   - IMPORTANTE: Usar `test_path` del JSON para re-ejecutar el test E2E específico
   - Seguir el patrón de ejecución de `.claude/commands/test_e2e.md`
   - Observar el comportamiento del browser y confirmar que puedes reproducir la falla exacta
   - Comparar el error que ves con el error reportado en el JSON

4. **Arreglar el Issue**
   - Basado en tu reproducción, identificar la causa raíz
   - Hacer cambios mínimos y enfocados para resolver solo esta falla
   - Considerar issues E2E comunes:
     - Cambios en selectores de elementos
     - Issues de timing (elementos no listos)
     - Cambios de layout UI
     - Modificaciones de lógica de aplicación
   - Asegurar que el fix alinea con el user story y propósito del test

5. **Validar el Fix**
   - Re-ejecutar el mismo test E2E paso a paso usando `test_path` para confirmar que pasa
   - IMPORTANTE: El test debe completarse exitosamente antes de considerarlo resuelto
   - NO ejecutar otros tests o la suite completa
   - Enfocarse solo en arreglar este test E2E específico

## Test Failure Input

$ARGUMENTS

## Report

Proveer resumen conciso de:
- Causa raíz identificada (ej., elemento faltante, issue de timing, selector incorrecto)
- Fix específico aplicado
- Confirmación de que el test E2E ahora pasa después del fix
