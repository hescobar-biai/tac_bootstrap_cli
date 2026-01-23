# Wizard Interactivo para Entity Fields

**ADW ID:** feature_2_5
**Date:** 2026-01-23
**Specification:** specs/issue-148-adw-feature_2_5-sdlc_planner-wizard-interactive-entity-fields.md

## Overview

Se implementó un wizard interactivo completo para guiar a los usuarios en la creación de especificaciones de entidades CRUD. El wizard utiliza Rich para proporcionar una experiencia de terminal moderna con validación en tiempo real, conversión automática de formatos de nombres (PascalCase, snake_case, kebab-case), y tablas de resumen antes de la confirmación final. Esta funcionalidad elimina la necesidad de memorizar sintaxis de CLI flags y reduce significativamente los errores de formato durante la creación de entidades.

## What Was Built

- **Helper de conversión de nombres**: Función `_to_kebab_case()` que convierte PascalCase a kebab-case usando regex
- **Validadores de formato**: Funciones `_validate_entity_name_format()` y `_validate_field_name_format()` con validación completa de convenciones de nombres, keywords de Python, y nombres reservados
- **Wizard principal**: Función `run_entity_wizard()` con flujo interactivo guiado de 5 pasos
- **Sistema de resumen visual**: Función `_show_entity_summary()` que muestra dos tablas Rich (metadata de entidad y listado de campos)
- **Eliminación de código duplicado**: Removida la clase `EntitySpec` duplicada de `domain/models.py` (ahora solo existe en `domain/entity_config.py`)

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py`: Se agregaron ~350 líneas con toda la implementación del wizard interactivo, incluyendo helpers de validación, conversión de formatos, y el flujo principal del wizard
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py`: Se eliminaron 64 líneas con la definición duplicada de `EntitySpec` que existía previamente

### Key Changes

- **Imports agregados**: `keyword`, `re`, `IntPrompt` de rich, y todos los modelos necesarios desde `entity_config.py` (EntitySpec, FieldSpec, FieldType, RESERVED_FIELD_NAMES)
- **Validación robusta**: Se implementó validación en tiempo real para entity names (PascalCase), field names (snake_case), capability names (kebab-case), keywords de Python, y nombres reservados de SQLAlchemy
- **Conversión automática**: El capability name se genera automáticamente desde el entity name usando conversión PascalCase → kebab-case, con opción de override manual
- **Loop de campos con validación**: Los usuarios pueden agregar múltiples campos interactivamente con validación completa de cada propiedad (name, type, required, unique, indexed, max_length)
- **Resumen visual con Rich Tables**: Se muestran dos tablas separadas (metadata de entidad y campos) con colores semánticos (verde para required, cyan para unique, amarillo para indexed)
- **Opción Edit/Cancel**: Al final del wizard, si el usuario no confirma, puede elegir entre editar (reinicia el wizard) o cancelar (retorna None)

## How to Use

### Ejecutar el wizard desde código Python

```python
from tac_bootstrap.interfaces.wizard import run_entity_wizard

# Ejecutar el wizard interactivo
entity_spec = run_entity_wizard()

if entity_spec:
    print(f"Entidad creada: {entity_spec.name}")
    print(f"Campos: {len(entity_spec.fields)}")
else:
    print("Wizard cancelado")
```

### Flujo paso a paso del wizard

1. **Bienvenida**: Se muestra un panel de bienvenida con el título del wizard
2. **Entity Name**: Prompt para nombre de entidad en PascalCase (ej: "Product", "UserProfile")
   - Validación en tiempo real con re-prompt si inválido
   - Verifica que no sea keyword de Python
3. **Capability Name**: Prompt con default auto-generado en kebab-case (ej: "user-profile")
   - Permite override manual
4. **Fields Loop**: Agregar campos iterativamente
   - Nombre del campo (snake_case)
   - Tipo de campo (selección de enum: STRING, INTEGER, FLOAT, etc.)
   - Required? (default: True)
   - Unique? (default: False)
   - Indexed? (default: False)
   - Max length? (solo para STRING/TEXT, opcional)
   - Agregar otro campo? (continúa el loop si Yes)
5. **Opciones adicionales**:
   - Authentication templates? (default: False)
   - Async repository? (default: False)
   - Domain events? (default: False)
6. **Resumen y confirmación**:
   - Muestra tabla de metadata de la entidad
   - Muestra tabla detallada de campos con colores
   - Confirmar? Si No → Edit o Cancel

### Ejemplo de validaciones

```python
# Entity name válido: PascalCase
✓ Product, UserProfile, OAuth2Client

# Entity name inválido
✗ product (debe empezar con mayúscula)
✗ User-Profile (no permite guiones)
✗ Class (keyword de Python)

# Field name válido: snake_case
✓ user_name, email_address, is_active

# Field name inválido
✗ UserName (debe ser snake_case)
✗ id (nombre reservado)
✗ metadata (conflicto con SQLAlchemy)
```

## Configuration

No se requiere configuración adicional. El wizard usa las siguientes convenciones por default:

- **Entity name**: PascalCase (ej: "Product")
- **Capability name**: kebab-case auto-generado (ej: "product")
- **Field names**: snake_case (ej: "product_name")
- **Table name**: snake_case auto-generado desde entity name (ej: "products")
- **Required fields**: Default True
- **Unique fields**: Default False
- **Indexed fields**: Default False
- **Authentication**: Default False
- **Async mode**: Default False
- **Domain events**: Default False

## Testing

### Ejecutar tests del wizard

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_wizard.py -v
```

### Tests recomendados (a implementar en futuros PRs)

Según la especificación, se deben cubrir:

1. **Tests de helpers**:
   - `test_to_kebab_case()`: UserProfile → user-profile
   - `test_validate_entity_name_format_valid()`: nombres PascalCase válidos
   - `test_validate_entity_name_format_invalid()`: lowercase, keywords
   - `test_validate_field_name_format_valid()`: snake_case válidos
   - `test_validate_field_name_format_invalid()`: PascalCase, reserved names

2. **Tests de wizard flow** (con mocks):
   - `test_entity_wizard_complete_flow()`: flujo completo
   - `test_entity_wizard_cancel_early()`: cancelar en entity name
   - `test_entity_wizard_cancel_at_confirmation()`: cancelar al final
   - `test_entity_wizard_minimum_fields()`: 1 solo campo
   - `test_entity_wizard_multiple_fields()`: múltiples campos
   - `test_entity_wizard_string_with_max_length()`: campo con max_length

### Validación del código

```bash
# Tests unitarios
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- **Parte de FASE 2**: Esta feature es parte de la fase de generación de código CRUD del proyecto TAC Bootstrap
- **Código duplicado removido**: Se eliminó la clase `EntitySpec` duplicada de `models.py` para evitar confusión. La versión definitiva está en `entity_config.py` con validadores Pydantic más completos
- **Consistencia de UX**: El wizard sigue los mismos patrones de diseño que `run_init_wizard()` y `run_add_agentic_wizard()` para mantener consistencia en toda la CLI
- **Nombres reservados**: El wizard valida contra `RESERVED_FIELD_NAMES` (id, created_at, updated_at, deleted_at, metadata) y conflictos de SQLAlchemy (query, metadata, registry, mapper)
- **Conversión de nombres**: La regex de conversión PascalCase → kebab-case es: `re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()`
- **Colores semánticos**: La tabla de resumen usa verde para campos required, cyan para unique, amarillo para indexed, facilitando la lectura visual
- **Recursión para Edit**: La opción "Edit" en la confirmación final usa una llamada recursiva a `run_entity_wizard()` para reiniciar el wizard completo
- **FieldType enum**: Disponible en `domain.entity_config.FieldType` con valores: STRING, INTEGER, FLOAT, BOOLEAN, DATETIME, UUID, TEXT, DECIMAL, JSON

## Future Enhancements

Posibles mejoras para futuras iteraciones:

- Agregar opción de "Edit Field" para modificar campos existentes antes de confirmar
- Permitir re-ordenar campos en el resumen
- Agregar preview del código que se generará (domain model, schema, etc.)
- Soporte para relaciones entre entidades (foreign keys, many-to-many)
- Templates de entidades pre-configuradas (User, Product, Order, etc.)
- Exportar/importar entity specs desde/hacia archivos JSON/YAML
