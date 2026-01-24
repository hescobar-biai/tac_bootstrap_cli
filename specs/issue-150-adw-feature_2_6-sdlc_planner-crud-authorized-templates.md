# Feature: Templates CRUD authorized (optional multi-tenant templates)

## Metadata
issue_number: `150`
adw_id: `feature_2_6`
issue_json: `{"number":150,"title":"Tarea 2.6: Templates CRUD authorized (opcional)","body":"/feature\n/adw_sdlc_iso\n/adw_id: feature_2_6\n\n***Tipo**: feature\n**Ganancia**: Variantes de los templates que incluyen verificacion de permisos a nivel de row (owner/organization). Para proyectos multi-tenant.\n\n**Instrucciones para el agente**:\n\n1. Crear directorio `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_authorized/`\n2. Crear variantes de:\n   - `routes_authorized.py.j2`: Endpoints que extraen user_id del token y lo pasan al service\n   - `service_authorized.py.j2`: Service que filtra por owner/organization_id\n   - `repository_authorized.py.j2`: Repository que agrega filtro de owner a todas las queries\n3. Los templates authorized extienden los basicos agregando:\n   - Dependency `get_current_user` en routes\n   - Filtro `organization_id` en repository queries\n   - Verificacion de ownership en update/delete\n\n**Criterios de aceptacion**:\n- `tac-bootstrap generate entity Product --authorized` genera con templates authorized\n- Las queries filtran por organization_id del usuario autenticado\n- DELETE solo permite al owner\n\n# FASE 2: Comando `generate entity`\n\n**Objetivo**: Agregar un nuevo comando CLI que genera entidades CRUD completas siguiendo la vertical slice architecture.\n\n**Ganancia de la fase**: Los desarrolladores pueden crear entidades completas (domain, schemas, service, repo, routes) con un solo comando, eliminando el trabajo manual de copiar y adaptar boilerplate.\n"}`

## Feature Description

Esta feature crea templates Jinja2 alternativos para generar entidades CRUD con autenticación y autorización multi-tenant integradas. Los templates "authorized" generan código que:

- Extrae `user_id` y `organization_id` del token JWT en las rutas
- Filtra automáticamente todas las queries por `organization_id` en el repositorio
- Establece automáticamente `organization_id` y `created_by` en operaciones CREATE
- Valida que usuarios solo puedan acceder/modificar recursos de su organización
- Retorna 404 en lugar de 403 para prevenir filtración de información

Los templates authorized son variantes independientes de los templates básicos en `crud_basic/`, permitiendo generar entidades con autorización desde el inicio usando el flag `--authorized`.

## User Story

As a developer building a multi-tenant SaaS application
I want to generate CRUD entities with organization-level isolation built-in
So that I don't have to manually add authorization logic to every endpoint and query

## Problem Statement

En aplicaciones multi-tenant, cada entidad requiere:
- Filtrado por `organization_id` en TODAS las queries para evitar acceso cruzado
- Establecer `organization_id` automáticamente en CREATE (nunca confiar en el cliente)
- Validación de ownership en UPDATE/DELETE
- Extracción de contexto de usuario del token JWT

Implementar esto manualmente es:
- Propenso a errores críticos de seguridad (olvidar filtrar una query)
- Repetitivo (mismo patrón en cada entidad)
- Difícil de auditar (lógica de autorización dispersa)

Los templates básicos de `crud_basic/` no incluyen autorización, requiriendo modificación manual.

## Solution Statement

Crear 3 templates Jinja2 en `templates/capabilities/crud_authorized/` que son variantes de los templates básicos con lógica de autorización multi-tenant:

**routes_authorized.py.j2**:
- Dependency `get_current_user` que extrae y valida JWT
- Inyecta `user_id` y `organization_id` en todos los endpoints
- Pasa contexto de usuario al service layer

**service_authorized.py.j2**:
- Recibe `user_id` y `organization_id` en operaciones
- Pasa `organization_id` a repository para filtrado
- Establece `organization_id` y `created_by` en CREATE

**repository_authorized.py.j2**:
- Recibe `organization_id` en constructor o métodos
- Aplica filtro `.filter(Model.organization_id == org_id)` a TODAS las queries
- Previene acceso cruzado a nivel de datos

El approach es standalone templates: no usan herencia de Jinja2, son archivos completos que duplican parte del código de `crud_basic/` pero con autorización integrada.

## Relevant Files

Archivos existentes para referencia:

- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/routes.py.j2` - Template básico de routes sin autorización
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/service.py.j2` - Template básico de service
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/repository.py.j2` - Template básico de repository
- `tac_bootstrap_cli/tac_bootstrap/domain/entity_config.py` - EntitySpec con flag `authorized`
- `tac_bootstrap_cli/tac_bootstrap/application/entity_generator_service.py` - Service que selecciona templates
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` - CLI con flag `--authorized` (líneas 634, 660, 791)

### New Files

Templates a crear:
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_authorized/routes_authorized.py.j2` - Routes con JWT authentication
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_authorized/service_authorized.py.j2` - Service con contexto de usuario
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_authorized/repository_authorized.py.j2` - Repository con filtrado por org

Archivos a modificar:
- `tac_bootstrap_cli/tac_bootstrap/application/entity_generator_service.py` - Seleccionar templates authorized cuando `entity_spec.authorized == True`

Tests:
- `tac_bootstrap_cli/tests/test_authorized_templates.py` - Tests de renderizado de templates authorized

## Implementation Plan

### Phase 1: Foundation - Auth dependency template
Crear el directorio `templates/capabilities/crud_authorized/` y diseñar el dependency `get_current_user` que se inyectará en routes. Este dependency debe:
- Extraer token del header `Authorization: Bearer <token>`
- Validar formato JWT (mock validation para template)
- Retornar objeto con `user_id` y `organization_id`
- Raise 401 si token falta o es inválido
- Raise 401 si `organization_id` no está en el token

### Phase 2: Core Implementation - Authorized templates
Crear los 3 templates en orden de dependencias:

**1. repository_authorized.py.j2**:
- Constructor recibe `session: Session` como básico
- Agregar parámetro `organization_id: str` a todos los métodos de query (get_by_id, get_all, search)
- Aplicar filtro `.filter({{ config.entity.name }}Model.organization_id == organization_id)` a TODAS las queries
- Método `create()` no necesita modificación (service establece organization_id)
- Método `update()` valida ownership filtrando por id + organization_id
- Método `delete()` valida ownership filtrando por id + organization_id

**2. service_authorized.py.j2**:
- Métodos reciben `user_id: str` y `organization_id: str` adicionales
- Método `create()`: establece `data.organization_id = organization_id` y `data.created_by = user_id` antes de guardar
- Método `get_by_id()`: pasa `organization_id` al repository
- Método `get_all()`: pasa `organization_id` al repository
- Método `update()`: pasa `organization_id` al repository (retorna None si no existe/no pertenece a org)
- Método `soft_delete()`: pasa `organization_id` al repository (retorna None si no existe/no pertenece a org)

**3. routes_authorized.py.j2**:
- Importar y usar dependency `get_current_user` que retorna `CurrentUser` con `user_id` y `organization_id`
- Inyectar `current_user: CurrentUser = Depends(get_current_user)` en TODOS los endpoints
- Pasar `current_user.user_id` y `current_user.organization_id` a service en cada operación
- Retornar 404 cuando service retorna None (en lugar de 403, para evitar filtración de info)

### Phase 3: Integration - Selector de templates y tests
Modificar `EntityGeneratorService.build_generation_plan()` para seleccionar templates authorized cuando `entity_spec.authorized == True`:

```python
if entity_spec.authorized:
    routes_template = "capabilities/crud_authorized/routes_authorized.py.j2"
    service_template = "capabilities/crud_authorized/service_authorized.py.j2"
    repo_template = "capabilities/crud_authorized/repository_authorized.py.j2"
else:
    routes_template = "capabilities/crud_basic/routes.py.j2"
    # ... basic templates
```

Crear tests que validen:
- Templates renderizan Python válido
- Filtro `organization_id` aparece en todas las queries del repository
- Routes tienen dependency `get_current_user` en todos los endpoints
- Service establece `organization_id` y `created_by` en CREATE

## Step by Step Tasks

IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create authorized templates directory
- Crear directorio `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_authorized/`
- Verificar que el directorio existe y está vacío

### Task 2: Design CurrentUser model and get_current_user dependency
- En el template routes_authorized.py.j2, incluir la definición de `CurrentUser` (Pydantic model con `user_id` y `organization_id`)
- Incluir el dependency `get_current_user()` que:
  - Extrae token del header Authorization
  - Mock validation (TODO comment para producción)
  - Decodifica JWT y extrae user_id y organization_id
  - Raise HTTPException 401 si falta token o organization_id
  - Retorna CurrentUser instance

### Task 3: Create repository_authorized.py.j2
- Copiar estructura base de `crud_basic/repository.py.j2`
- Agregar parámetro `organization_id: str` a:
  - `get_by_id(id: str, organization_id: str)`
  - `get_all(skip: int, limit: int, organization_id: str)`
  - `search(query: str, skip: int, limit: int, organization_id: str)` (si tiene campos de texto)
  - Métodos custom por campos indexados
- Aplicar filtro `.filter({{ config.entity.name }}Model.organization_id == organization_id)` en cada query
- Incluir TODO comment: "# TODO: Add audit logging for authorization failures"
- Agregar docstring explicando que todas las queries filtran por organization_id

### Task 4: Create service_authorized.py.j2
- Copiar estructura base de `crud_basic/service.py.j2`
- Agregar parámetros `user_id: str` y `organization_id: str` a métodos:
  - `create(data, user_id, organization_id)`
  - `get_by_id(id, organization_id)`
  - `get_all(skip, limit, organization_id)`
  - `update(id, data, organization_id)`
  - `soft_delete(id, organization_id)`
- En `create()`: establecer `data.organization_id = organization_id` y `data.created_by = user_id`
- Pasar `organization_id` a todos los métodos del repository
- Incluir docstring explicando auto-setting de organization_id en CREATE

### Task 5: Create routes_authorized.py.j2
- Copiar estructura base de `crud_basic/routes.py.j2`
- Agregar imports para JWT y security:
  - `from fastapi import APIRouter, Depends, HTTPException, status, Header`
  - `from typing import Optional`
- Incluir definición de `CurrentUser` Pydantic model
- Incluir dependency `get_current_user(authorization: str = Header(...))`
- Modificar TODOS los endpoints para:
  - Inyectar `current_user: CurrentUser = Depends(get_current_user)`
  - Pasar `current_user.user_id` y `current_user.organization_id` al service
- Cambiar manejo de "not found" para retornar 404 en lugar de 403
- Incluir TODO comment: "# TODO: Replace mock JWT validation with your actual auth system"

### Task 6: Modify EntityGeneratorService to use authorized templates
- En `entity_generator_service.py`, modificar método `build_generation_plan()`
- Agregar lógica para seleccionar templates:
  ```python
  if entity_spec.authorized:
      routes_template = "capabilities/crud_authorized/routes_authorized.py.j2"
      service_template = "capabilities/crud_authorized/service_authorized.py.j2"
      repo_template = "capabilities/crud_authorized/repository_authorized.py.j2"
  else:
      routes_template = "capabilities/crud_basic/routes.py.j2"
      service_template = "capabilities/crud_basic/service.py.j2"
      repo_template = "capabilities/crud_basic/repository.py.j2"
  ```
- Mantener templates de domain, schemas, orm_model sin cambios (son iguales para basic y authorized)

### Task 7: Create tests for authorized templates
- Crear `tests/test_authorized_templates.py`
- Test 1: `test_repository_authorized_renders_with_org_filter` - verificar que filtro organization_id aparece en queries
- Test 2: `test_service_authorized_sets_organization_id_on_create` - verificar que CREATE establece organization_id y created_by
- Test 3: `test_routes_authorized_has_get_current_user_dependency` - verificar que todos los endpoints tienen dependency
- Test 4: `test_authorized_templates_render_valid_python` - compile() exitoso para cada template
- Usar EntitySpec con `authorized=True` para renderizar templates

### Task 8: Add domain model fields for authorization
- Verificar que `orm_model.py.j2` incluye campos necesarios para autorización:
  - `organization_id: str` (indexed, required)
  - `created_by: str` (optional)
- Si no existen, agregar lógica condicional en template para incluirlos cuando `entity_spec.authorized == True`
- Los campos deben agregarse automáticamente, no requieren que el usuario los especifique en FieldSpec

### Task 9: Update CLI help text for --authorized flag
- En `cli.py`, agregar descripción detallada al flag `--authorized`:
  ```python
  authorized: Annotated[bool, typer.Option(
      "--authorized",
      help="Generate with multi-tenant authorization (organization-level isolation)"
  )] = False,
  ```
- Agregar ejemplo en docstring del comando `generate entity`

### Task 10: Integration test - Generate entity with --authorized
- Crear test end-to-end que ejecuta:
  ```bash
  tac-bootstrap generate entity Product --authorized --no-interactive \
    --fields "name:str:required,price:float:required"
  ```
- Verificar que genera 6 archivos (domain, schemas, service, repository, orm_model, routes)
- Verificar que repository tiene filtros de organization_id
- Verificar que routes tienen get_current_user dependency

### Task 11: Documentation and examples
- Crear `docs/authorized_entities.md` con:
  - Explicación de cuándo usar `--authorized`
  - Ejemplo de generación con flag
  - Explicación de qué hace cada template
  - TODO para implementar JWT validation real
  - Nota sobre necesidad de migración de base de datos para agregar organization_id
- Agregar sección en README.md sobre multi-tenant entities

### Task 12: Run validation commands
- Ejecutar todos los comandos de validación para asegurar cero regresiones
- Verificar que tests nuevos y existentes pasan

## Testing Strategy

### Unit Tests
- `test_repository_authorized_template_renders` - Template renderiza sin errores
- `test_repository_authorized_has_org_filter` - Queries incluyen filtro organization_id
- `test_service_authorized_template_renders` - Template renderiza sin errores
- `test_service_authorized_sets_ownership` - CREATE establece organization_id y created_by
- `test_routes_authorized_template_renders` - Template renderiza sin errores
- `test_routes_authorized_has_auth_dependency` - Todos los endpoints tienen get_current_user
- `test_entity_generator_selects_authorized_templates` - Service usa templates correctos cuando authorized=True

### Edge Cases
- EntitySpec con `authorized=True` y `async_mode=True` - debe generar repository async authorized
- EntitySpec con solo 1 campo - templates deben renderizar correctamente
- EntitySpec con campo `organization_id` en fields - debe lanzar error (campo reservado)
- generate entity sin `--fields` ni `--interactive` - debe fallar con mensaje claro

## Acceptance Criteria
- `tac-bootstrap generate entity Product --authorized --no-interactive --fields "name:str"` genera 6 archivos sin errores
- Repository generado filtra TODAS las queries por `organization_id`
- Service generado establece `organization_id` y `created_by` en CREATE desde token
- Routes generadas tienen dependency `get_current_user` inyectado en TODOS los endpoints
- DELETE retorna 404 cuando recurso no existe o no pertenece a organización del usuario
- Templates renderizan Python sintácticamente válido (verificado con compile())
- Tests unitarios cubren renderizado de cada template authorized
- Documentación explica cuándo usar `--authorized` y cómo implementar JWT validation real

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `cd tac_bootstrap_cli && uv run tac-bootstrap generate entity --help` - Smoke test del comando generate

## Notes

**Design decisions**:
- **Standalone templates**: No usar herencia de Jinja2 para extender templates básicos. Duplicar código pero mantener claridad.
- **404 vs 403**: Retornar 404 para recursos fuera de organización previene filtración de información sobre qué IDs existen.
- **Auto-inject organization_id**: El ORM model template debe agregar campos `organization_id` y `created_by` automáticamente cuando `authorized=True`, sin requerir que usuario los especifique.
- **Mock JWT validation**: Template incluye validación JWT mock con TODO comment para reemplazar con sistema real.
- **No role-based access**: Templates solo implementan organización-level isolation. Roles y permisos más granulares se agregan manualmente.

**Future enhancements** (no implementar ahora):
- Templates con role-based access control (admin puede ver todo)
- Audit logging de intentos de acceso no autorizado
- Support para usuarios multi-organización
- Templates para recursos públicos (no requieren organización)

**Dependencies**:
- Requiere que `crud_basic/` templates estén completos (Tarea 2.2 - issue 142)
- Requiere que EntitySpec tenga campo `authorized` (Tarea 2.1 - issue 140)
- Requiere que CLI tenga flag `--authorized` (Tarea 2.4 - issue 146)
