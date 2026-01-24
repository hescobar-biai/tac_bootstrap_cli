# Chore: Value Objects for Domain Model Validation

## Metadata
issue_number: `166`
adw_id: `chore_5_1`
issue_json: `{"number":166,"title":"Tarea 5.1: Value Objects","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_5_1\n\n**Tipo**: chore\n**Ganancia**: Validacion automatica en construccion. Un `ProjectName(\"Mi App!!\")` falla inmediatamente en vez de propagar el string invalido por todo el sistema.\n\n**Instrucciones para el agente**:\n\n1. Crear `tac_bootstrap_cli/tac_bootstrap/domain/value_objects.py`\n2. Value objects como Pydantic types con validacion:\n   ```python\n   class ProjectName(str):\n       \"\"\"Nombre de proyecto: lowercase, hyphens, no spaces, no special chars.\"\"\"\n       @classmethod\n       def __get_validators__(cls):\n           yield cls.validate\n       @classmethod\n       def validate(cls, v: str) -> \"ProjectName\":\n           sanitized = v.strip().lower().replace(\" \", \"-\")\n           sanitized = re.sub(r\"[^a-z0-9-]\", \"\", sanitized)\n           if not sanitized:\n               raise ValueError(\"Project name cannot be empty after sanitization\")\n           return cls(sanitized)\n\n   class TemplatePath(str):\n       \"\"\"Path relativo a un template que debe existir.\"\"\"\n       # Valida que no contiene '..' ni es absoluto\n\n   class SemanticVersion(str):\n       \"\"\"Version semantica X.Y.Z con comparacion.\"\"\"\n       @property\n       def tuple(self) -> tuple[int, int, int]:\n           ...\n       def __gt__(self, other): ...\n       def __lt__(self, other): ...\n   ```\n3. No romper la API existente: los value objects se usan internamente, los validators de Pydantic los aceptan como str\n\n**Criterios de aceptacion**:\n- ProjectName sanitiza correctamente (spaces, special chars)\n- TemplatePath rechaza paths peligrosos\n- SemanticVersion compara correctamente (0.2.2 < 0.3.0)\n- Tests existentes siguen pasando sin cambios\n\n- \n# FASE 5: Value Objects y IDK Docstrings\n\n**Objetivo**: Mejorar la calidad del codigo del CLI con value objects tipados y documentacion estandarizada.\n\n**Ganancia de la fase**: Codigo mas mantenible, menos bugs por strings invalidos, y documentacion que facilita la busqueda semantica por agentes AI.\n"}`

## Chore Description
Create domain value objects for TAC Bootstrap CLI to provide automatic validation and type safety for critical domain concepts. This prevents invalid string propagation throughout the system by failing fast at construction time.

The value objects will be:
- **ProjectName**: Sanitizes project names to lowercase-hyphen format, rejecting special characters and spaces
- **TemplatePath**: Validates relative template paths, rejecting directory traversal attempts and absolute paths
- **SemanticVersion**: Parses and compares semantic versions (X.Y.Z format) with proper comparison operators

These value objects inherit from `str` for compatibility with existing code and Pydantic v2 models, but add validation logic using modern Pydantic v2 patterns.

## Relevant Files

### Existing Files to Understand
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Main domain models using Pydantic BaseModel. Value objects will integrate here later but won't modify it initially
- `tac_bootstrap_cli/tac_bootstrap/domain/validators.py` - Existing domain validation patterns to follow for consistency
- `tac_bootstrap_cli/pyproject.toml` - Confirms Pydantic v2.5.0+ is available
- `tac_bootstrap_cli/tests/test_models.py` - Tests that must continue passing
- `tac_bootstrap_cli/tests/test_validators.py` - Test patterns to follow for value object tests

### New Files
- `tac_bootstrap_cli/tac_bootstrap/domain/value_objects.py` - New module containing ProjectName, TemplatePath, SemanticVersion classes
- `tac_bootstrap_cli/tests/test_value_objects.py` - Comprehensive tests for all three value objects

## Step by Step Tasks

### Task 1: Create value_objects.py with ProjectName
Create the new value objects module with the ProjectName class:
- Inherit from `str` for compatibility
- Use Pydantic v2 patterns (NOT deprecated `__get_validators__`)
- Implement `__new__` for string subclass construction
- Sanitize: strip, lowercase, replace spaces with hyphens
- Remove all non-alphanumeric-hyphen characters using regex
- Collapse consecutive hyphens into single hyphen
- Enforce 1-64 character length
- Provide clear error messages on validation failure
- Add comprehensive docstring with examples

### Task 2: Implement TemplatePath value object
Add TemplatePath class to value_objects.py:
- Inherit from `str`
- Validate format only (do NOT check filesystem)
- Reject absolute paths (starts with `/`)
- Reject parent directory traversal (contains `..`)
- Reject empty paths
- Allow relative paths including `./file`
- Provide clear error messages explaining security concerns
- Add docstring with security rationale and examples

### Task 3: Implement SemanticVersion value object
Add SemanticVersion class to value_objects.py:
- Inherit from `str`
- Parse strict X.Y.Z format (three numeric components)
- Provide `tuple` property returning `tuple[int, int, int]`
- Implement full comparison protocol: `__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__`
- Implement `__hash__` for use in sets/dicts
- Provide clear error messages for invalid formats
- Add docstring with version comparison examples

### Task 4: Create comprehensive test suite
Create `tests/test_value_objects.py` with tests for:

**ProjectName tests:**
- Valid sanitization: "My App!!" → "my-app"
- Space to hyphen conversion
- Special character removal
- Consecutive hyphen collapsing: "my--app" → "my-app"
- Empty string rejection (after sanitization)
- Maximum length enforcement (64 chars)
- Edge cases: numbers, single char, all hyphens

**TemplatePath tests:**
- Valid relative paths: "templates/config.yml"
- Valid dot-relative paths: "./templates/file"
- Reject absolute paths: "/etc/passwd"
- Reject parent traversal: "../../../etc/passwd"
- Reject embedded traversal: "templates/../../secret"
- Reject empty paths
- Edge cases: paths with dots in filenames

**SemanticVersion tests:**
- Valid parsing: "1.2.3"
- Tuple property: "1.2.3".tuple == (1, 2, 3)
- Comparison operators: "0.2.2" < "0.3.0", "1.0.0" > "0.9.9"
- Equality: "1.2.3" == "1.2.3"
- Hash consistency for sets/dicts
- Invalid format rejection: "1.2", "1.2.3.4", "v1.2.3", "abc"
- Edge cases: "0.0.0", large numbers

### Task 5: Run validation commands
Execute all validation commands to ensure zero regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- `cd tac_bootstrap_cli && uv run ruff check .`
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

Verify that:
- All existing tests pass unchanged
- All new value object tests pass
- No linting errors
- CLI still runs successfully

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - All tests including new value object tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting passes
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - CLI smoke test

## Notes

### Pydantic v2 Compatibility
The issue example uses Pydantic v1 `__get_validators__` pattern which is deprecated. For Pydantic v2 compatibility while maintaining string subclass behavior:
- Use `__new__` method for string subclass construction
- Validation happens in `__new__` before instance creation
- Can be used with `Annotated` types in Pydantic models for future integration

### No Integration Yet
Per acceptance criteria "Tests existentes siguen pasando sin cambios", we:
- Create value objects as standalone utilities
- Do NOT modify existing domain models (models.py)
- Do NOT integrate into existing Pydantic models yet
- Value objects can be imported and used in new code or integrated in future tasks

### Security Context
TemplatePath validation prevents path traversal attacks. This is critical for a code generator that:
- Reads template files
- Copies files to target directories
- Could be exploited if paths aren't validated

### Version Comparison Use Cases
SemanticVersion will be used for:
- Comparing TAC Bootstrap versions for upgrade detection
- Template compatibility checking
- Dependency version requirements
