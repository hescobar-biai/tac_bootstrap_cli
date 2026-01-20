# Chore: Crear infraestructura de templates Jinja2

## Metadata
issue_number: `9`
adw_id: `d2f77c7a`
issue_json: `{"number":9,"title":"TAREA 3.1: Crear infraestructura de templates Jinja2","body":"# Prompt para Agente\n\n## Contexto\nTAC Bootstrap genera archivos a partir de templates Jinja2. Necesitamos una clase\nTemplateRepository que maneje la carga y renderizado de templates.\n\nLos templates estaran en `tac_bootstrap/templates/` y se renderizaran con un contexto\nque contiene el TACConfig completo.\n\n## Objetivo\nCrear la clase TemplateRepository que:\n1. Carga templates desde el directorio de templates del paquete\n2. Renderiza templates con contexto\n3. Lista templates disponibles por categoria\n4. Maneja errores de template no encontrado\n\n## Archivo a Crear\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py`"}`

## Chore Description
Implementar la infraestructura base para el sistema de templates Jinja2 que TAC Bootstrap utilizará para generar archivos en los proyectos destino. Esta infraestructura incluye:

1. **TemplateRepository**: Clase principal que gestiona la carga y renderizado de templates Jinja2
2. **Custom Filters**: Filtros personalizados para conversión de casos (snake_case, kebab-case, PascalCase)
3. **Error Handling**: Manejo robusto de errores para templates no encontrados o fallos de renderizado
4. **Template Discovery**: Funcionalidad para listar y descubrir templates por categoría

La clase utilizará el directorio `tac_bootstrap/templates/` como base y recibirá objetos `TACConfig` como contexto para el renderizado.

## Relevant Files

### Existing Files
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Contiene `TACConfig` que será el contexto principal para renderizado
- `tac_bootstrap_cli/pyproject.toml` - Ya incluye `jinja2>=3.1.2` como dependencia
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/__init__.py` - Package donde se agregará el nuevo módulo

### New Files
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Clase `TemplateRepository` con toda la lógica de templates
- `tac_bootstrap_cli/tests/test_template_repo.py` - Tests unitarios para `TemplateRepository`
- `tac_bootstrap_cli/tac_bootstrap/templates/.gitkeep` - Directorio para templates (ya existe pero vacío)

## Step by Step Tasks

### Task 1: Crear el módulo template_repo.py
- Crear archivo `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py`
- Implementar las excepciones personalizadas:
  - `TemplateNotFoundError`: Para templates no encontrados
  - `TemplateRenderError`: Para errores de renderizado
- Implementar la clase `TemplateRepository` con:
  - Constructor que configura el entorno Jinja2
  - Soporte para directorio de templates customizable
  - Configuración de autoescape, trim_blocks, lstrip_blocks, keep_trailing_newline

### Task 2: Implementar filtros personalizados
- Crear método `_register_filters()` que registre:
  - `to_snake_case()`: Convierte strings a snake_case
  - `to_kebab_case()`: Convierte strings a kebab-case
  - `to_pascal_case()`: Convierte strings a PascalCase
- Registrar los filtros en el entorno Jinja2

### Task 3: Implementar métodos de renderizado
- `render(template_name, context)`: Renderiza template desde archivo
- `render_string(template_str, context)`: Renderiza template desde string
- Manejo de excepciones Jinja2 (`TemplateNotFound`, etc.)
- Mensajes de error descriptivos con paths completos

### Task 4: Implementar métodos auxiliares
- `template_exists(template_name)`: Verifica si un template existe
- `list_templates(category)`: Lista templates disponibles, opcionalmente filtrados por categoría
- `get_template_content(template_name)`: Obtiene contenido raw del template sin renderizar

### Task 5: Crear tests unitarios
- Crear archivo `tac_bootstrap_cli/tests/test_template_repo.py`
- Tests para:
  - Inicialización del repositorio
  - Renderizado de templates básicos
  - Filtros personalizados (snake_case, kebab-case, pascal_case)
  - Manejo de errores (template no encontrado, error de renderizado)
  - `template_exists()` y `list_templates()`
  - `render_string()` para templates inline
- Usar fixtures con directorio temporal para templates de prueba

### Task 6: Validación completa
- Ejecutar todos los comandos de validación
- Verificar que todos los tests pasen
- Verificar que el linting pase sin errores
- Verificar que el CLI funcione correctamente (smoke test)

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Arquitectura DDD
Este módulo pertenece a la capa de infraestructura:
- **Domain**: `TACConfig` (ya existe en `domain/models.py`)
- **Infrastructure**: `TemplateRepository` (nuevo)
- **Application**: Services que usarán `TemplateRepository` (futuro)

### Configuración Jinja2
El entorno Jinja2 se configura con:
- `autoescape`: Solo HTML/XML para seguridad
- `trim_blocks=True`: Elimina primera newline después de tags de bloque
- `lstrip_blocks=True`: Elimina whitespace al inicio de bloques
- `keep_trailing_newline=True`: Preserva newline final en templates

### Custom Filters
Los filtros personalizados facilitan la generación de código:
```jinja2
{{ config.project.name | snake_case }}  # "my-app" → "my_app"
{{ config.project.name | kebab_case }}  # "MyApp" → "my-app"
{{ config.project.name | pascal_case }} # "my_app" → "MyApp"
```

### Estrategia de Tests
- Usar `pytest` con fixtures temporales
- Crear templates de prueba en memoria o en directorio temporal
- Probar casos edge: nombres vacíos, caracteres especiales, templates inexistentes
- Verificar que los filtros manejen correctamente diferentes formatos de entrada

### Relación con PLAN_TAC_BOOTSTRAP.md
Esta tarea corresponde a la **TAREA 3.1** de la Fase 3 del plan maestro. Es un prerequisito para:
- TAREA 3.2: Copiar templates base desde `.claude/`, `adws/`, `scripts/`
- TAREA 3.3: Crear TemplateGeneratorService
- TAREA 4.x: Generación de archivos reales en proyectos destino
