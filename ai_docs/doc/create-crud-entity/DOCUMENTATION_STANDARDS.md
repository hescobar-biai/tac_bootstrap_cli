# Documentation Standards for Generated Code

This file supplements the main skill with documentation standards for generated code. All code produced by this skill should follow these docstring patterns.

## Docstring Format (IDK-First)

Every public function, class, and module must use the following structure:

```python
"""
IDK: keyword-1, keyword-2, keyword-3

Responsibility:
- What this symbol is responsible for

Invariants:
- Rules that must never be violated

Inputs:
- param_name (type): description

Outputs:
- Return type and meaning

Failure Modes:
- Exception/error conditions

Related Docs:
- Path to related documentation
"""
```

### IDK (Information Dense Keywords)

IDK are domain-specific terms that enable semantic routing and expert discovery.

**Rules:**
- Use 2-5 keywords per docstring
- Prefer domain terms over natural language
- Use lowercase, hyphenated format

**Examples by Layer:**

| Layer | IDK Examples |
|-------|--------------|
| Domain | `domain-entity`, `value-object`, `aggregate-root`, `business-rule` |
| Application | `use-case`, `dto`, `orchestration`, `validation` |
| Infrastructure | `repository`, `orm-mapping`, `data-access`, `persistence` |
| API | `http-endpoint`, `request-handler`, `pagination`, `auth-filter` |

---

## Templates by Code Type

### Module-Level Docstring

```python
"""
IDK: {{layer}}, {{domain}}, {{pattern}}

Module: {{module_name}}

Responsibility:
- Primary purpose of this module

Key Components:
- Class/function names and their roles

Invariants:
- Module-level rules

Related Docs:
- docs/{{capability}}/{{layer}}.md
"""
```

### Class Docstring

```python
class {{EntityName}}Service:
    """
    IDK: use-case, orchestration, {{entity}}-management

    Responsibility:
    - Orchestrate {{entity}} business logic
    - Enforce domain invariants
    - Coordinate with repository layer

    Invariants:
    - All mutations go through this service
    - Entity code uniqueness enforced
    - Audit fields always populated

    Collaborators:
    - {{EntityName}}Repository: data persistence
    - {{EntityName}}: domain model

    Failure Modes:
    - EntityNotFoundError: entity doesn't exist
    - DuplicateEntityError: code already taken

    Related Docs:
    - docs/{{capability}}/application/service.md
    """
```

### Function/Method Docstring

```python
def create(
    self,
    data: {{EntityName}}Create,
    user_id: str | None = None,
) -> {{EntityName}}Response:
    """
    IDK: entity-creation, duplicate-check, audit-trail

    Responsibility:
    - Create new {{entity}} with validation
    - Check for duplicate codes
    - Set audit fields (created_by, created_at)

    Invariants:
    - Code must be unique
    - created_at/created_by always set
    - Returns persisted entity

    Inputs:
    - data ({{EntityName}}Create): creation payload
    - user_id (str | None): creator ID for audit

    Outputs:
    - {{EntityName}}Response: created entity

    Failure Modes:
    - DuplicateEntityError: code exists
    - ValidationError: invalid data
    """
```

### Repository Docstring

```python
class {{EntityName}}Repository(BaseRepository[{{EntityName}}Model]):
    """
    IDK: repository, data-access, {{entity}}-persistence

    Responsibility:
    - CRUD operations for {{entity}}
    - Query abstractions
    - Transaction boundary

    Invariants:
    - All queries filter soft-deleted by default
    - Returns ORM models, not domain entities

    Collaborators:
    - Session: database connection
    - {{EntityName}}Model: ORM mapping

    Related Docs:
    - docs/{{capability}}/infrastructure/repository.md
    """
```

### Domain Entity Docstring

```python
class {{EntityName}}(Entity):
    """
    IDK: domain-entity, {{domain}}, aggregate-root

    Responsibility:
    - Represent {{entity}} domain concept
    - Encapsulate business rules
    - Validate entity invariants

    Invariants:
    - code is immutable after creation
    - state transitions follow: inactive(0) -> active(1) -> deleted(2)
    - version increments on update

    State:
    - 0: inactive
    - 1: active
    - 2: deleted (soft)

    Related Docs:
    - docs/{{capability}}/domain/{{entity}}.md
    """
```

### Route/Endpoint Docstring

```python
@router.post("/", response_model={{EntityName}}Response)
def create_{{entity}}(
    data: {{EntityName}}Create,
    service: {{EntityName}}Service = Depends(get_{{entity}}_service),
    user_id: str = Header(..., alias="X-User-ID"),
) -> {{EntityName}}Response:
    """
    IDK: http-endpoint, create-operation, {{entity}}-api

    Responsibility:
    - Accept HTTP POST for {{entity}} creation
    - Delegate to service layer
    - Return created entity

    Inputs:
    - data ({{EntityName}}Create): request body
    - user_id (str): from X-User-ID header

    Outputs:
    - {{EntityName}}Response: 201 Created

    Failure Modes:
    - 400: validation error
    - 409: duplicate code
    - 500: internal error

    Related Docs:
    - docs/{{capability}}/api/routes.md
    """
```

### Schema/DTO Docstring

```python
class {{EntityName}}Create(BaseCreate):
    """
    IDK: dto, create-schema, input-validation

    Responsibility:
    - Validate {{entity}} creation input
    - Define required fields for creation

    Invariants:
    - code is required and non-empty
    - name is required

    Fields:
    - code (str): unique business identifier
    - name (str): display name
    - {{custom_fields}}

    Related Docs:
    - docs/{{capability}}/application/schemas.md
    """
```

---

## Quick Reference

### Mandatory Sections

| Code Type | Required Sections |
|-----------|-------------------|
| Module | IDK, Responsibility, Key Components |
| Class | IDK, Responsibility, Invariants, Failure Modes |
| Function | IDK, Responsibility, Inputs, Outputs, Failure Modes |
| Schema | IDK, Responsibility, Fields |

### IDK Vocabulary by Capability

| Capability Type | Common IDKs |
|-----------------|-------------|
| CRUD Entity | `entity-crud`, `soft-delete`, `audit-trail`, `pagination` |
| Authorized | `rbac`, `row-level-security`, `permission-check` |
| Async | `async-io`, `non-blocking`, `concurrent-access` |

---

## Anti-Patterns

**DO NOT:**
- Restate the code in prose
- Describe "how" line-by-line
- Leave speculative statements
- Duplicate information across levels
- Use vague terms ("handles stuff", "does things")

**DO:**
- Focus on why, constraints, domain meaning
- Use domain-specific terminology
- Be verifiable against code
- Link to related documentation

---

## Validation Checklist

Before generating code, verify docstrings:

- [ ] IDK keywords present and domain-relevant
- [ ] Responsibility clearly stated
- [ ] Invariants documented for classes
- [ ] Failure modes listed for functions
- [ ] Inputs/Outputs typed and described
- [ ] No prose/narrative padding