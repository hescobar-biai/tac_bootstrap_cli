# Feature: Wizard Interactivo para Entity Fields

## Metadata
issue_number: `148`
adw_id: `feature_2_5`
issue_json: `{"number":148,"title":"Tarea 2.5: Wizard interactivo para entity fields","body":"/feature\n/adw_sdlc_iso\n/adw_id: feature_2_5\n\n**Tipo**: feature\n**Ganancia**: Los usuarios pueden definir campos de la entidad de forma guiada, sin necesidad de memorizar la sintaxis de --fields.\n\n**Instrucciones para el agente**:\n\n1. Modificar `tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py`\n2. Agregar funcion `run_entity_wizard() -> EntitySpec`:\n   - Prompt para nombre de entidad (PascalCase)\n   - Prompt para capability name (kebab-case, default = nombre en kebab)\n   - Loop para agregar campos:\n     - Nombre del campo (snake_case)\n     - Tipo (seleccionar de FieldType enum)\n     - Required? (y/n, default y)\n     - Unique? (y/n, default n)\n     - Indexed? (y/n, default n)\n     - Max length? (solo para str, default None)\n     - \"Agregar otro campo?\" (y/n)\n   - Opciones adicionales:\n     - Authorized templates? (y/n)\n     - Async mode? (y/n)\n     - Domain events? (y/n)\n   - Mostrar resumen y confirmar\n3. Usar Rich para formatear prompts y tabla de resumen\n\n**Criterios de aceptacion**:\n- Wizard guia al usuario paso a paso\n- Muestra tabla resumen antes de confirmar\n- Valida inputs en tiempo real (PascalCase, snake_case, etc.)\n- Permite cancelar en cualquier momento\n\n# FASE 2: Comando `generate entity`\n\n**Objetivo**: Agregar un nuevo comando CLI que genera entidades CRUD completas siguiendo la vertical slice architecture.\n\n**Ganancia de la fase**: Los desarrolladores pueden crear entidades completas (domain, schemas, service, repo, routes) con un solo comando, eliminando el trabajo manual de copiar y adaptar boilerplate.\n"}`

## Feature Description
Implementar un wizard interactivo que guíe a los usuarios paso a paso en la creación de especificaciones de entidades para la generación CRUD. El wizard usará Rich para proporcionar una experiencia de terminal moderna y profesional, con validación en tiempo real de inputs (PascalCase para entidades, snake_case para campos, kebab-case para capabilities) y una tabla de resumen antes de la confirmación final.

Esta funcionalidad es parte de la FASE 2 del proyecto TAC Bootstrap, que se enfoca en agregar capacidades de generación de código CRUD completo.

## User Story
As a desarrollador usando TAC Bootstrap
I want to definir entidades CRUD de forma guiada mediante un wizard interactivo
So that puedo crear especificaciones de entidades sin memorizar sintaxis de CLI flags y evitar errores de formato en nombres y tipos de campos.

## Problem Statement
Actualmente, los desarrolladores deben memorizar la sintaxis exacta de los flags `--fields` para definir entidades CRUD mediante la CLI. Esto es propenso a errores de formato, tipeo incorrecto de tipos de campos, y problemas con convenciones de nombres (PascalCase vs snake_case vs kebab-case). No existe validación en tiempo real, lo que significa que los errores solo se descubren después de ejecutar el comando completo.

La falta de un wizard guiado reduce la velocidad de desarrollo y aumenta la fricción para nuevos usuarios que no están familiarizados con la estructura de EntitySpec.

## Solution Statement
Crear una función `run_entity_wizard()` en el módulo `wizard.py` que guíe interactivamente a los usuarios a través de:

1. **Nombre de entidad** con validación PascalCase en tiempo real
2. **Capability name** con conversión automática a kebab-case (con opción de override)
3. **Loop de campos** donde cada campo requiere:
   - Nombre (validado como snake_case)
   - Tipo (selección de FieldType enum)
   - Required, Unique, Indexed (prompts con defaults sensatos)
   - Max length (solo para tipos string/text)
4. **Opciones de generación** (auth templates, async mode, domain events)
5. **Tabla de resumen** usando Rich Table para review visual
6. **Confirmación final** con opción de editar o cancelar

El wizard usará los componentes Rich existentes (Prompt, Confirm, IntPrompt, Table) y seguirá los patrones establecidos en `run_init_wizard()` y `run_add_agentic_wizard()`. Retornará un objeto EntitySpec validado o None si el usuario cancela.

## Relevant Files
Archivos necesarios para implementar esta feature:

### Existing Files
- `tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py` - Módulo donde se agregará `run_entity_wizard()`. Ya contiene patrones de wizards interactivos usando Rich (select_from_enum, _show_config_summary).
- `tac_bootstrap_cli/tac_bootstrap/domain/entity_config.py` - Define EntitySpec y FieldSpec con validadores. El wizard retornará instancias de EntitySpec que ya incluyen toda la lógica de validación (PascalCase, kebab-case, snake_case, reserved names).
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Define FieldType enum (líneas 135-147) con los tipos disponibles: STR, INT, FLOAT, BOOL, DATETIME, UUID, TEXT, DECIMAL, JSON. También define otra versión de EntitySpec (líneas 593-684) que usa la misma estructura.

### New Files
Ninguno. Toda la implementación se agrega al archivo existente `wizard.py`.

## Implementation Plan

### Phase 1: Foundation
**Objetivo**: Preparar helpers de validación y conversión de nombres antes de implementar el wizard principal.

**Tareas**:
1. Agregar función helper `_to_kebab_case(name: str) -> str` en wizard.py
   - Convierte PascalCase a kebab-case usando regex: `re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()`
   - Ejemplo: "UserProfile" -> "user-profile"
2. Agregar función helper `_validate_entity_name_format(name: str) -> tuple[bool, str]`
   - Retorna (is_valid, error_message)
   - Verifica PascalCase: starts with uppercase, alphanumeric only
   - Verifica que no sea keyword de Python usando `keyword.iskeyword()`
3. Agregar función helper `_validate_field_name_format(name: str) -> tuple[bool, str]`
   - Retorna (is_valid, error_message)
   - Verifica snake_case: starts with lowercase, alphanumeric + underscores
   - Verifica que no sea keyword de Python
   - Verifica que no esté en RESERVED_FIELD_NAMES (importar de entity_config)
4. Importar dependencias necesarias al inicio del archivo:
   - `import keyword`
   - `import re` (ya debería estar importado)
   - `from rich.prompt import IntPrompt` (agregar a imports existentes)
   - `from tac_bootstrap.domain.entity_config import EntitySpec, FieldSpec, FieldType, RESERVED_FIELD_NAMES`

### Phase 2: Core Implementation
**Objetivo**: Implementar la función principal del wizard y sus componentes.

**Tareas**:
1. Crear skeleton de `run_entity_wizard() -> EntitySpec | None`
   - Mostrar panel de bienvenida usando Rich Panel
   - Retornar None al inicio (será completado en pasos siguientes)
2. Implementar sección de Entity Name prompt:
   - Loop hasta obtener nombre válido (PascalCase, no keyword)
   - Usar `_validate_entity_name_format()` para validación
   - Re-prompt con mensaje de error claro si inválido
   - Print confirmación con checkmark verde
3. Implementar sección de Capability Name prompt:
   - Calcular default usando `_to_kebab_case(entity_name)`
   - Permitir override con Prompt.ask(default=calculated_kebab)
   - Validar formato kebab-case si usuario override el default
   - Print confirmación con checkmark verde
4. Implementar loop de campos:
   - Inicializar `fields: list[FieldSpec] = []`
   - While True loop con opción de salir
   - Para cada campo:
     - Prompt field name (validar con `_validate_field_name_format()`)
     - Usar `select_from_enum()` para FieldType (mostrar opciones en tabla)
     - Confirm.ask() para required (default=True)
     - Confirm.ask() para unique (default=False)
     - Confirm.ask() para indexed (default=False)
     - Si field_type in (FieldType.STRING, FieldType.TEXT): IntPrompt para max_length
     - Crear FieldSpec y append a fields list
     - Confirm.ask("Agregar otro campo?") - si No, break
   - Después del loop: validar que fields no esté vacío, si vacío re-iniciar loop con mensaje de error
5. Implementar sección de opciones adicionales:
   - Confirm.ask("Generate with authentication templates?") -> enable_auth
   - Confirm.ask("Use async repository pattern?") -> enable_async
   - Confirm.ask("Include domain events support?") -> enable_events
6. Implementar tabla de resumen y confirmación:
   - Crear función helper `_show_entity_summary(entity_spec: EntitySpec)`
   - Mostrar tabla con: Entity Name, Capability, Field count, Auth, Async, Events
   - Mostrar tabla de campos con columnas: Name, Type, Required, Unique, Indexed, Max Length
   - Confirm.ask("Proceed with this configuration?")
   - Si No: preguntar "Edit or Cancel?" -> Edit reinicia wizard, Cancel retorna None
   - Si Yes: retornar EntitySpec construido

### Phase 3: Integration
**Objetivo**: Probar el wizard de forma standalone y preparar para integración con comando CLI.

**Tareas**:
1. Agregar docstring completa a `run_entity_wizard()` con:
   - Descripción de propósito
   - Returns: EntitySpec or None
   - Raises: SystemExit si cancela (opcional, evaluar si es necesario)
   - Examples de uso básico
2. Crear script de prueba manual en scratchpad:
   - `scratchpad/test_entity_wizard.py`
   - Importar y llamar `run_entity_wizard()`
   - Print el EntitySpec resultante
   - Ejecutar manualmente para verificar UX
3. Validar que todas las validaciones funcionan:
   - Ingresar entity name inválido (lowercase, con espacios, keyword)
   - Ingresar field name inválido (PascalCase, keyword, reserved)
   - Intentar crear entity sin campos
   - Cancelar en diferentes puntos del wizard
4. Validar que el objeto EntitySpec retornado es válido:
   - Tiene todos los campos esperados
   - Los FieldSpec tienen tipos correctos
   - Las validaciones de Pydantic no lanzan errores

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Preparar helpers de validación y conversión
- Agregar función `_to_kebab_case(name: str) -> str` con regex conversion
- Agregar función `_validate_entity_name_format(name: str) -> tuple[bool, str]` con validación PascalCase y keywords
- Agregar función `_validate_field_name_format(name: str) -> tuple[bool, str]` con validación snake_case y reserved names
- Importar dependencias necesarias: keyword, re, IntPrompt, entity_config models

### Task 2: Implementar skeleton del wizard principal
- Crear función `run_entity_wizard() -> EntitySpec | None` con panel de bienvenida
- Agregar docstring inicial
- Retornar None temporalmente

### Task 3: Implementar prompts de Entity Name y Capability Name
- Implementar loop de Entity Name con validación PascalCase
- Implementar Capability Name prompt con conversión automática a kebab-case
- Agregar confirmaciones visuales con checkmarks

### Task 4: Implementar loop de campos
- Crear while loop para agregar campos iterativamente
- Implementar prompts para: field name, type, required, unique, indexed, max_length
- Validar que al menos un campo sea agregado
- Usar `select_from_enum()` para selección de FieldType

### Task 5: Implementar opciones adicionales y resumen
- Agregar prompts para enable_auth, enable_async, enable_events
- Crear función `_show_entity_summary()` con Rich Tables
- Mostrar resumen de entidad y campos
- Implementar confirmación final con opción Edit/Cancel

### Task 6: Testing y validación
- Crear script de prueba manual en scratchpad
- Ejecutar wizard con diferentes inputs (válidos e inválidos)
- Verificar que EntitySpec retornado es válido
- Verificar que las cancelaciones funcionan correctamente
- **EJECUTAR VALIDATION COMMANDS**

## Testing Strategy

### Unit Tests
Crear tests en `tac_bootstrap_cli/tests/test_wizard.py`:

1. **Test helpers de conversión**:
   - `test_to_kebab_case()`: UserProfile -> user-profile, Product -> product
   - `test_validate_entity_name_format_valid()`: nombres PascalCase válidos
   - `test_validate_entity_name_format_invalid()`: lowercase, con espacios, keywords
   - `test_validate_field_name_format_valid()`: nombres snake_case válidos
   - `test_validate_field_name_format_invalid()`: PascalCase, keywords, reserved names

2. **Test wizard flow** (usando mocks para input):
   - `test_entity_wizard_complete_flow()`: flujo completo hasta EntitySpec
   - `test_entity_wizard_cancel_early()`: cancelar en entity name prompt
   - `test_entity_wizard_cancel_at_confirmation()`: cancelar en confirmación final
   - `test_entity_wizard_minimum_fields()`: crear entidad con 1 solo campo
   - `test_entity_wizard_multiple_fields()`: crear entidad con múltiples campos
   - `test_entity_wizard_string_with_max_length()`: campo str con max_length

### Edge Cases
1. **Entity name edge cases**:
   - Nombre de 1 carácter (debe fallar, mínimo 2)
   - Nombre que es keyword de Python ("Class", "def", "return")
   - Nombre con números (válido: "User2", inválido: "2User")

2. **Field name edge cases**:
   - Campo con nombre reservado ("id", "created_at", "updated_at")
   - Campo que es keyword de Python ("class", "def")
   - Campo con SQLAlchemy conflicts ("query", "metadata")

3. **Fields list edge cases**:
   - Intentar confirmar sin agregar campos (debe reiniciar loop)
   - Agregar 10+ campos (verificar que tabla se muestra correctamente)

4. **Cancellation edge cases**:
   - Cancelar presionando Ctrl+C (debe retornar None o SystemExit)
   - Cancelar en confirmación final y elegir "Edit" (debe reiniciar)
   - Cancelar en confirmación final y elegir "Cancel" (debe retornar None)

## Acceptance Criteria
- [ ] El wizard guía al usuario paso a paso desde entity name hasta confirmación final
- [ ] Muestra tabla de resumen usando Rich Table antes de confirmar, incluyendo tabla de campos
- [ ] Valida entity name como PascalCase en tiempo real con re-prompt en caso de error
- [ ] Valida field names como snake_case en tiempo real con re-prompt en caso de error
- [ ] Valida que capability sea kebab-case con conversión automática desde entity name
- [ ] Permite cancelar en cualquier momento retornando None sin errores
- [ ] Muestra prompt de max_length solo para tipos FieldType.STRING y FieldType.TEXT
- [ ] Permite agregar múltiples campos mediante loop con confirmación "Agregar otro campo?"
- [ ] Requiere al menos 1 campo antes de permitir confirmación final
- [ ] Retorna EntitySpec válido que pasa todas las validaciones de Pydantic
- [ ] No permite nombres de campo reservados (id, created_at, etc.) ni keywords de Python
- [ ] Usa componentes Rich consistentes con el resto de wizard.py (Prompt, Confirm, Table)
- [ ] Opciones adicionales (auth, async, events) funcionan correctamente como boolean flags
- [ ] Si el usuario no confirma el resumen, ofrece "Edit or Cancel" con funcionalidad correcta

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- Esta feature es parte de FASE 2 del proyecto TAC Bootstrap que agrega capacidades de generación CRUD
- El wizard seguirá los patrones existentes en `run_init_wizard()` para consistencia de UX
- Usar imports de `entity_config.py` en lugar de `models.py` para EntitySpec y FieldSpec, ya que `entity_config.py` tiene las validaciones más completas y documentación más detallada
- El FieldType enum está disponible en `domain.entity_config.FieldType` con valores: STRING, INTEGER, FLOAT, BOOLEAN, DATETIME, UUID, TEXT, DECIMAL, JSON
- La conversión PascalCase -> kebab-case debe usar regex para mantener consistencia: `re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()`
- El wizard debe ser user-friendly: mensajes de error claros, defaults sensatos, confirmaciones visuales
- La tabla de resumen debe mostrar DOS tablas: una para metadata de la entidad (nombre, capability, opciones) y otra para los campos (con todas sus propiedades)
- Considerar agregar colores en la tabla de resumen: verde para campos required, cyan para unique, amarillo para indexed
