# Expertise File Structure Documentation

**Version**: 1.0
**Last Updated**: 2026-02-02
**Purpose**: Standard structure for `expertise.yaml` files used by TAC-13 self-improving agent experts

---

## Table of Contents

1. [Introduction](#introduction)
2. [Philosophy and Principles](#philosophy-and-principles)
3. [Complete YAML Schema](#complete-yaml-schema)
4. [Field Reference](#field-reference)
5. [Annotated Examples](#annotated-examples)
6. [Validation Rules](#validation-rules)
7. [Best Practices](#best-practices)
8. [Usage Guidelines](#usage-guidelines)
9. [FAQ](#faq)

---

## Introduction

### What is an Expertise File?

An expertise file (`expertise.yaml`) is the **mental model** maintained by a TAC-13 agent expert. It represents accumulated knowledge about a specific domain within a codebase, stored in a compressed, structured format.

**Critical Understanding**: This is NOT a source of truth. The code is always the source of truth.

An expertise file is like your own mental model:
- Not the code itself
- Not documentation or comments
- Not PRDs or specs
- A working memory structure that evolves with the codebase

### Why YAML Format?

YAML provides optimal information density for agent context windows:
- **Compressed**: More information per line than JSON or markdown
- **Readable**: Agents parse it easily, humans can review it
- **Structured**: Enforces consistent organization across domains
- **Validatable**: YAML parsers ensure syntactic correctness

### Purpose in TAC-13 Workflow

Expertise files enable the **Act → Learn → Reuse** loop:

1. **Reuse** (`question.md`): Agent reads expertise first (20% of context) before validating against code
2. **Act**: Agent performs work using expertise as mental model
3. **Learn** (`self-improve.md`): Agent automatically updates expertise based on changes

---

## Philosophy and Principles

### Core Principles

1. **Expertise as Mental Model**
   - Represents the agent's understanding, not objective truth
   - Must be validated against actual code when used
   - Evolves as the codebase changes

2. **Compressed Representation**
   - Use YAML for maximum information density
   - Prioritize high-level patterns over implementation details
   - Store "what" and "why", not line-by-line "how"

3. **Finite Size**
   - **Hard limit**: 1000 lines maximum
   - Prevents context window bloat
   - Forces prioritization of valuable information

4. **Actionable Information**
   - Include what helps agents make decisions
   - File locations, line ranges, patterns, constraints
   - Remove obvious or redundant information

5. **Self-Maintained**
   - Agents update expertise, not humans
   - Self-improve workflow keeps it accurate
   - Validated against code on every update

6. **Domain-Specific**
   - One expertise file per expert domain
   - Separate concerns (CLI vs ADW vs Database vs Security)
   - Enable focused, specialized agent experts

### What NOT to Include

- Line-by-line code explanations
- Full function implementations
- Obvious patterns (e.g., "functions have parameters")
- Information easily inferred from code
- Redundant documentation
- Personal opinions or preferences

### What TO Include

- **Integration points**: How components connect
- **Non-obvious patterns**: Design decisions and rationale
- **Critical constraints**: Must-follow rules (e.g., "NEVER charge twice")
- **File locations**: Where to find key components
- **Line ranges**: Boundaries of classes, methods, sections
- **Dependencies**: What relies on what
- **Gotchas**: Common pitfalls and workarounds

---

## Complete YAML Schema

### Top-Level Structure

```yaml
# All expertise.yaml files follow this structure

overview:
  description: string                    # One-sentence system description
  key_files: [string]                    # 3-10 most important files
  total_files: integer                   # Total files in domain
  last_updated: string                   # ISO 8601 date (YYYY-MM-DD)

core_implementation:
  component_name_1:                      # Repeat for each major component
    location: string                     # File path
    description: string                  # What this component does
    key_classes: [Class]                 # Main classes (optional)
    key_functions: [Function]            # Main functions (optional)
    patterns: [string]                   # Design patterns used (optional)

  component_name_2:
    # ... same structure ...

schema_structure:                        # OPTIONAL - for database/API experts
  tables: [Table]                        # Database tables
  views: [View]                          # Database views (optional)
  endpoints: [Endpoint]                  # API endpoints (optional)

key_operations:
  operation_category_1:                  # Group by logical category
    description: string                  # What this category handles
    files: [string]                      # Relevant files
    patterns: [string]                   # Common patterns
    examples: [string]                   # Usage examples (optional)

  operation_category_2:
    # ... same structure ...

best_practices:
  [string]                               # List of domain-specific guidelines

known_issues:
  - issue: string                        # Description of problem
    workaround: string                   # How to avoid/fix
    affected_files: [string]             # Where it appears (optional)

recent_changes:                          # OPTIONAL - track evolution
  - date: string                         # ISO 8601 date
    description: string                  # What changed
    affected_files: [string]             # Files modified
    details: string                      # Additional context (optional)
```

### Optional Sections

Add these sections only when relevant to the expert domain:

```yaml
integration_points:                      # For multi-system experts
  external_systems: [ExternalSystem]
  internal_modules: [InternalModule]

security_constraints:                    # For security-critical experts
  authentication: object
  authorization: object
  encryption: object

performance_patterns:                    # For performance-critical experts
  caching: object
  connection_pooling: object
  async_patterns: object
```

---

## Field Reference

### Overview Section

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | string | ✅ | One-sentence description of domain (max 100 chars) |
| `key_files` | list[string] | ✅ | 3-10 most important file paths |
| `total_files` | integer | ✅ | Total number of files in domain |
| `last_updated` | string | ✅ | ISO 8601 date when expertise last updated |

**Example**:
```yaml
overview:
  description: "CLI system with 50+ slash commands and hook integration"
  key_files:
    - "tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py"
    - "tac_bootstrap_cli/tac_bootstrap/application/command_service.py"
  total_files: 12
  last_updated: "2026-02-02"
```

### Core Implementation Section

#### Component Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `location` | string | ✅ | File path where component is defined |
| `description` | string | ✅ | What this component does (1-2 sentences) |
| `key_classes` | list[Class] | ❌ | Main classes in component |
| `key_functions` | list[Function] | ❌ | Main standalone functions |
| `patterns` | list[string] | ❌ | Design patterns used |

**Example**:
```yaml
core_implementation:
  command_parser:
    location: "tac_bootstrap_cli/tac_bootstrap/application/command_service.py"
    description: "Parses and executes slash commands from .claude/commands/"
    key_classes:
      - name: "CommandService"
        line_start: 15
        line_end: 150
        purpose: "Coordinates command discovery and execution"
        key_methods:
          - name: "execute_command"
            line_start: 45
            line_end: 78
            signature: "def execute_command(self, name: str, args: list[str]) -> Result"
            logic: "Loads command file, validates permissions, executes"
            dependencies: ["PermissionService", "FileLoader"]
    patterns:
      - "Command pattern for extensible CLI"
      - "Service layer with dependency injection"
```

#### Class Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Class name |
| `line_start` | integer | ✅ | First line of class definition |
| `line_end` | integer | ✅ | Last line of class definition |
| `purpose` | string | ✅ | Core responsibility of class |
| `key_methods` | list[Method] | ❌ | Important methods |

#### Method/Function Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Method/function name |
| `line_start` | integer | ✅ | First line of definition |
| `line_end` | integer | ✅ | Last line of definition |
| `signature` | string | ✅ | Full signature with types |
| `logic` | string | ✅ | High-level what it does (NOT line-by-line) |
| `dependencies` | list[string] | ❌ | Classes/modules it depends on |

### Schema Structure Section (Optional)

Use for database experts, API experts, or data-heavy systems.

#### Table Object

```yaml
tables:
  - name: string                         # Table name
    primary_key: string                  # Primary key column
    columns: [string]                    # List of column names
    relationships: [Relationship]        # Foreign key relationships
    indexes: [string]                    # Index definitions (optional)
```

#### Relationship Object

```yaml
relationships:
  - table: string                        # Related table name
    type: string                         # one_to_many, many_to_one, many_to_many
    foreign_key: string                  # Foreign key column
```

#### Endpoint Object (for API experts)

```yaml
endpoints:
  - path: string                         # URL path (e.g., /api/users/{id})
    method: string                       # HTTP method (GET, POST, etc.)
    handler: string                      # File:line where handler is defined
    description: string                  # What endpoint does
    parameters: [Parameter]              # Request parameters (optional)
```

### Key Operations Section

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | string | ✅ | What this operation category handles |
| `files` | list[string] | ✅ | Relevant file paths |
| `patterns` | list[string] | ✅ | Common patterns used |
| `examples` | list[string] | ❌ | Usage examples |

**Example**:
```yaml
key_operations:
  command_execution:
    description: "Loading and executing slash commands from markdown files"
    files:
      - "tac_bootstrap_cli/tac_bootstrap/application/command_service.py"
      - "tac_bootstrap_cli/tac_bootstrap/infrastructure/file_loader.py"
    patterns:
      - "Commands stored as markdown with YAML frontmatter"
      - "Lazy loading for performance"
      - "Permission validation before execution"
    examples:
      - "/prime loads ai_docs based on mappings"
      - "/feature creates planning workflow"
```

### Best Practices Section

Simple list of domain-specific guidelines.

```yaml
best_practices:
  - "Always validate command permissions before execution"
  - "Use lazy loading for command discovery to improve startup time"
  - "Include argument hints in command frontmatter for better UX"
  - "Log all command executions for debugging"
```

### Known Issues Section

```yaml
known_issues:
  - issue: "Command execution fails silently if markdown has invalid YAML frontmatter"
    workaround: "Validate YAML syntax with yamllint before committing"
    affected_files:
      - ".claude/commands/*.md"

  - issue: "Permission hooks can block legitimate operations if too strict"
    workaround: "Test hooks thoroughly before enabling in production"
```

---

## Annotated Examples

### Example 1: CLI Expert

**Domain**: Command-line interface system with slash commands

```yaml
# CLI Expert Expertise File
# Domain: Slash command system for tac_bootstrap CLI
# Last validated: 2026-02-02

overview:
  description: "CLI system with 50+ slash commands and hook integration"
  key_files:
    - "tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py"
    - "tac_bootstrap_cli/tac_bootstrap/application/command_service.py"
    - ".claude/commands/"  # Directory with 50+ command files
  total_files: 12
  last_updated: "2026-02-02"

core_implementation:
  cli_entrypoint:
    location: "tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py"
    description: "Typer-based CLI entrypoint with subcommands"
    key_functions:
      - name: "main"
        line_start: 25
        line_end: 45
        signature: "def main() -> None"
        logic: "Initializes Typer app, registers commands, runs CLI"
        dependencies: ["typer", "CommandService"]
    patterns:
      - "Typer for CLI framework"
      - "Rich for terminal formatting"

  command_service:
    location: "tac_bootstrap_cli/tac_bootstrap/application/command_service.py"
    description: "Discovers, loads, and executes slash commands"
    key_classes:
      - name: "CommandService"
        line_start: 15
        line_end: 180
        purpose: "Manage command lifecycle and execution"
        key_methods:
          - name: "discover_commands"
            line_start: 30
            line_end: 55
            signature: "def discover_commands(self, directory: Path) -> list[Command]"
            logic: "Scans .claude/commands/ for .md files, parses frontmatter"
            dependencies: ["FileLoader", "YAMLParser"]

          - name: "execute_command"
            line_start: 80
            line_end: 120
            signature: "def execute_command(self, name: str, args: list[str]) -> Result"
            logic: "Validates permissions, loads command, executes with args"
            dependencies: ["PermissionService", "Logger"]

  permission_system:
    location: "tac_bootstrap_cli/tac_bootstrap/application/permission_service.py"
    description: "Validates command permissions and runs hooks"
    key_classes:
      - name: "PermissionService"
        line_start: 10
        line_end: 95
        purpose: "Check if command is allowed based on settings.json and hooks"
        key_methods:
          - name: "check_permission"
            line_start: 25
            line_end: 60
            signature: "def check_permission(self, command: Command, context: Context) -> bool"
            logic: "Checks allowed-tools, runs pre-execution hooks, returns allow/deny"

key_operations:
  command_execution:
    description: "Loading and executing slash commands"
    files:
      - "tac_bootstrap_cli/tac_bootstrap/application/command_service.py"
      - ".claude/commands/*.md"
    patterns:
      - "Commands are markdown files with YAML frontmatter"
      - "Frontmatter defines: allowed-tools, description, argument-hint"
      - "Command body is Jinja2 template rendered with args"
    examples:
      - "/prime: loads AI docs based on keyword mappings"
      - "/feature <desc>: creates feature planning workflow"

  hook_integration:
    description: "Running shell hooks before/after command execution"
    files:
      - ".claude/hooks/user-prompt-submit.sh"
      - "tac_bootstrap_cli/tac_bootstrap/infrastructure/hook_runner.py"
    patterns:
      - "Hooks are shell scripts that can approve/block actions"
      - "Pre-hooks run before command execution"
      - "Post-hooks run after command completion"

best_practices:
  - "Always include argument-hint in command frontmatter for better UX"
  - "Use allowed-tools to restrict command capabilities"
  - "Validate command args before rendering Jinja2 template"
  - "Log command execution for debugging and audit trails"
  - "Keep command files under 200 lines for readability"

known_issues:
  - issue: "Command fails silently if YAML frontmatter is invalid"
    workaround: "Validate YAML with yamllint before committing"
    affected_files: [".claude/commands/*.md"]

  - issue: "Hooks can block legitimate operations if too strict"
    workaround: "Test hooks in isolated environment first"
    affected_files: [".claude/hooks/*.sh"]

recent_changes:
  - date: "2026-02-01"
    description: "Added permission service for hook integration"
    affected_files:
      - "tac_bootstrap_cli/tac_bootstrap/application/permission_service.py"
      - "tac_bootstrap_cli/tac_bootstrap/application/command_service.py"
```

### Example 2: Database Expert

**Domain**: PostgreSQL database with async support

```yaml
# Database Expert Expertise File
# Domain: PostgreSQL database layer with sync/async repositories
# Last validated: 2026-02-02

overview:
  description: "PostgreSQL database with SQLAlchemy, async support, soft deletes"
  key_files:
    - "shared/database.py"
    - "shared/base_repository.py"
    - "shared/base_repository_async.py"
    - "shared/base_entity.py"
  total_files: 8
  last_updated: "2026-02-02"

core_implementation:
  connection_management:
    location: "shared/database.py"
    description: "Database connection pooling and session management"
    key_functions:
      - name: "get_db"
        line_start: 156
        line_end: 187
        signature: "def get_db() -> Generator[Session, None, None]"
        logic: "Context manager that yields SQLAlchemy session with auto-commit/rollback"
        dependencies: ["SQLAlchemy", "engine"]

    patterns:
      - "Connection pooling with pool_size=5, max_overflow=10"
      - "Context manager pattern for automatic session cleanup"
      - "Pool pre-ping to detect stale connections"

  base_entity:
    location: "shared/base_entity.py"
    description: "Base class for all database entities with common fields"
    key_classes:
      - name: "BaseEntity"
        line_start: 15
        line_end: 89
        purpose: "Provides id, created_at, state, version for all entities"
        key_methods:
          - name: "soft_delete"
            line_start: 65
            line_end: 70
            signature: "def soft_delete(self) -> None"
            logic: "Sets state=2 instead of deleting record"

          - name: "activate"
            line_start: 72
            line_end: 75
            signature: "def activate(self) -> None"
            logic: "Sets state=1 for active record"

  repository_pattern:
    location: "shared/base_repository.py"
    description: "Generic repository for CRUD operations"
    key_classes:
      - name: "BaseRepository"
        line_start: 10
        line_end: 200
        purpose: "Generic CRUD with filtering, pagination, soft delete support"
        key_methods:
          - name: "get_active"
            line_start: 45
            line_end: 60
            signature: "def get_active(self, id: UUID) -> Optional[T]"
            logic: "Fetches entity with state=1 only"

          - name: "paginate"
            line_start: 120
            line_end: 145
            signature: "def paginate(self, offset: int, limit: int) -> tuple[list[T], int]"
            logic: "Returns (entities, total_count) for pagination"

schema_structure:
  tables:
    - name: "users"
      primary_key: "id"
      columns: ["id", "email", "name", "state", "created_at", "version"]
      relationships:
        - table: "roles"
          type: "many_to_many"
          foreign_key: "user_roles.user_id"

    - name: "projects"
      primary_key: "id"
      columns: ["id", "name", "owner_id", "state", "created_at"]
      relationships:
        - table: "users"
          type: "many_to_one"
          foreign_key: "owner_id"

  views:
    - name: "active_users_view"
      query_logic: "SELECT * FROM users WHERE state = 1"

key_operations:
  querying:
    description: "Fetching entities with filtering and pagination"
    files:
      - "shared/base_repository.py"
      - "shared/base_repository_async.py"
    patterns:
      - "Active only: filter(Entity.state == 1)"
      - "Include deleted: no state filter"
      - "Pagination: offset/limit with total count"
    examples:
      - "repo.get_active(id) - fetch single active entity"
      - "repo.paginate(0, 20) - first 20 active entities"

  soft_delete:
    description: "Marking records as deleted without removing data"
    files:
      - "shared/base_entity.py"
      - "shared/base_repository.py"
    patterns:
      - "state=2 means soft deleted"
      - "state=1 means active"
      - "state=0 means inactive (not deleted)"
    examples:
      - "entity.soft_delete() - mark as deleted"
      - "repo.get_active(id) - excludes soft deleted"

  migrations:
    description: "Database schema migrations with Alembic"
    files:
      - "shared/alembic.py"
      - "alembic/versions/*.py"
    patterns:
      - "Auto-generate: alembic revision --autogenerate"
      - "Manual review required before applying"
      - "Naming: YYYYMMDD_HHMM_description.py"
    examples:
      - "alembic revision --autogenerate -m 'add user roles'"
      - "alembic upgrade head"

best_practices:
  - "Always use get_active() to exclude soft deleted records"
  - "Use context manager (with get_db()) for automatic session cleanup"
  - "Test migrations in dev environment before production"
  - "Use soft delete (state=2) instead of CASCADE for data preservation"
  - "Validate version field for optimistic locking on updates"

known_issues:
  - issue: "Connection pool exhaustion under high load"
    workaround: "Increase pool_size and max_overflow in database.py config"
    affected_files: ["shared/database.py"]

  - issue: "Soft deleted records appear in counts if not filtered"
    workaround: "Always use .filter(Entity.state == 1) in queries"

recent_changes:
  - date: "2026-01-15"
    description: "Added async repository support"
    affected_files:
      - "shared/base_repository_async.py"
    details: "Parallel async operations for better performance"

  - date: "2026-01-10"
    description: "Implemented soft delete pattern"
    affected_files:
      - "shared/base_entity.py"
      - "shared/base_repository.py"
    details: "All entities now use state=2 for deletion instead of CASCADE"
```

### Example 3: Security Expert

**Domain**: Authentication and authorization system

```yaml
# Security Expert Expertise File
# Domain: Authentication, authorization, and encryption
# Last validated: 2026-02-02

overview:
  description: "JWT-based auth with role-based access control and encryption"
  key_files:
    - "api/auth/jwt_service.py"
    - "api/auth/permission_service.py"
    - "api/middleware/auth_middleware.py"
    - "shared/encryption.py"
  total_files: 6
  last_updated: "2026-02-02"

core_implementation:
  jwt_authentication:
    location: "api/auth/jwt_service.py"
    description: "JWT token generation and validation"
    key_classes:
      - name: "JWTService"
        line_start: 20
        line_end: 150
        purpose: "Create and verify JWT tokens with expiration"
        key_methods:
          - name: "create_token"
            line_start: 45
            line_end: 75
            signature: "def create_token(self, user_id: UUID, roles: list[str]) -> str"
            logic: "Generates JWT with user_id, roles, expiration in payload"
            dependencies: ["PyJWT", "SECRET_KEY"]

          - name: "verify_token"
            line_start: 90
            line_end: 120
            signature: "def verify_token(self, token: str) -> dict"
            logic: "Validates signature, checks expiration, returns payload"

    patterns:
      - "HS256 algorithm with rotating secrets"
      - "Token expiration: 24 hours"
      - "Refresh tokens stored in database for revocation"

  authorization:
    location: "api/auth/permission_service.py"
    description: "Role-based access control (RBAC)"
    key_classes:
      - name: "PermissionService"
        line_start: 15
        line_end: 100
        purpose: "Check if user has required role/permission"
        key_methods:
          - name: "check_permission"
            line_start: 35
            line_end: 65
            signature: "def check_permission(self, user: User, resource: str, action: str) -> bool"
            logic: "Validates user roles against resource permissions matrix"

  encryption:
    location: "shared/encryption.py"
    description: "Field-level encryption for sensitive data"
    key_functions:
      - name: "encrypt_field"
        line_start: 25
        line_end: 45
        signature: "def encrypt_field(value: str, key: bytes) -> str"
        logic: "AES-256-GCM encryption with authenticated encryption"
        dependencies: ["cryptography.Fernet"]

      - name: "decrypt_field"
        line_start: 50
        line_end: 70
        signature: "def decrypt_field(encrypted: str, key: bytes) -> str"
        logic: "Decrypts AES-256-GCM, verifies authentication tag"

security_constraints:
  authentication:
    token_expiration: "24 hours"
    refresh_token_rotation: "Required on every refresh"
    failed_login_limit: "5 attempts before lockout"

  authorization:
    default_policy: "deny"  # Explicit allow required
    role_hierarchy:
      - "admin > manager > user > guest"

  encryption:
    algorithm: "AES-256-GCM"
    key_rotation: "Every 90 days"
    sensitive_fields: ["email", "phone", "ssn", "credit_card"]

key_operations:
  login_flow:
    description: "User authentication and token issuance"
    files:
      - "api/auth/login_handler.py"
      - "api/auth/jwt_service.py"
    patterns:
      - "Validate credentials against hashed password"
      - "Generate JWT with user_id and roles"
      - "Return access_token + refresh_token"
      - "Log login event for audit"
    examples:
      - "POST /api/auth/login with email+password"
      - "Returns: {access_token, refresh_token, expires_in}"

  protected_endpoint_access:
    description: "Validating JWT on protected routes"
    files:
      - "api/middleware/auth_middleware.py"
    patterns:
      - "Extract JWT from Authorization header"
      - "Verify signature and expiration"
      - "Attach user to request context"
      - "Check permissions for requested resource"
    examples:
      - "GET /api/users requires 'read:users' permission"
      - "POST /api/admin requires 'admin' role"

best_practices:
  - "NEVER log JWT tokens or encryption keys"
  - "ALWAYS use HTTPS in production for token transmission"
  - "Rotate encryption keys every 90 days"
  - "Store passwords with bcrypt (min 12 rounds)"
  - "Validate JWT signature before checking expiration"
  - "Use refresh tokens for long-lived sessions"
  - "Implement rate limiting on login endpoints"

known_issues:
  - issue: "JWT tokens cannot be revoked before expiration"
    workaround: "Use short expiration (24h) + refresh token pattern, store refresh tokens in DB for revocation"
    affected_files: ["api/auth/jwt_service.py"]

  - issue: "Admin role has unrestricted access to all resources"
    workaround: "Implement granular permissions for admin actions"

recent_changes:
  - date: "2026-01-20"
    description: "Added refresh token rotation"
    affected_files:
      - "api/auth/jwt_service.py"
      - "api/auth/refresh_handler.py"
    details: "Old refresh token invalidated when new one issued"

  - date: "2026-01-15"
    description: "Implemented field-level encryption"
    affected_files:
      - "shared/encryption.py"
      - "shared/base_entity.py"
    details: "PII fields now encrypted at rest with AES-256-GCM"
```

---

## Validation Rules

### YAML Syntax

All expertise files MUST be valid YAML:

```bash
# Validate syntax
python -c "import yaml; yaml.safe_load(open('expertise.yaml'))"
```

**Common YAML Errors**:
- Inconsistent indentation (use 2 spaces)
- Missing colons after keys
- Incorrect list syntax
- Unescaped special characters in strings

### Line Limit Constraint

**Hard limit**: 1000 lines maximum

```bash
# Check line count
wc -l expertise.yaml

# Should return <= 1000
```

**Enforcement**: Self-improve workflow MUST prune low-value information when approaching limit.

**Pruning Priority** (remove first):
1. Old entries in `recent_changes` (keep last 5)
2. Obvious patterns in `best_practices`
3. Redundant information across sections
4. Verbose descriptions (compress to 1-2 sentences)

### Required Fields

All expertise files MUST include:

```yaml
# Required top-level sections
overview:
  description: "..."      # REQUIRED
  key_files: [...]        # REQUIRED
  total_files: N          # REQUIRED
  last_updated: "..."     # REQUIRED

core_implementation:      # REQUIRED - at least 1 component
  component_name:
    location: "..."       # REQUIRED
    description: "..."    # REQUIRED

key_operations:           # REQUIRED - at least 1 category
  category_name:
    description: "..."    # REQUIRED
    files: [...]          # REQUIRED
    patterns: [...]       # REQUIRED

best_practices: [...]     # REQUIRED - at least 3 items
```

**Optional sections**: `schema_structure`, `known_issues`, `recent_changes`, `integration_points`, etc.

### Data Type Validation

| Field | Type | Format |
|-------|------|--------|
| `description` | string | 1-200 characters |
| `key_files` | list[string] | File paths, 3-10 items |
| `total_files` | integer | Positive number |
| `last_updated` | string | ISO 8601: YYYY-MM-DD |
| `line_start` | integer | Positive number |
| `line_end` | integer | > line_start |

### Naming Conventions

- **Component names**: `snake_case`, descriptive (e.g., `command_service`, `jwt_authentication`)
- **Operation categories**: `snake_case`, verb-based (e.g., `querying`, `soft_delete`, `login_flow`)
- **File paths**: Absolute or relative from repo root
- **Dates**: ISO 8601 format (YYYY-MM-DD)

---

## Best Practices

### Compression Strategies

1. **Use High-Level Logic Descriptions**
   ```yaml
   # BAD - too detailed
   logic: |
     Line 1: Check if user is None
     Line 2: If None, raise ValueError
     Line 3: Hash password with bcrypt
     Line 4: Compare with stored hash
     Line 5: Return True if match

   # GOOD - high-level
   logic: "Validates password by comparing bcrypt hash with stored value"
   ```

2. **Avoid Redundant Information**
   ```yaml
   # BAD - obvious
   patterns:
     - "Functions take parameters"
     - "Classes have methods"
     - "Files end with .py"

   # GOOD - non-obvious patterns
   patterns:
     - "Command pattern for extensible CLI"
     - "Repository pattern with soft deletes"
     - "JWT rotation on every refresh"
   ```

3. **Prioritize Line Ranges Over Full Code**
   ```yaml
   # Include line ranges, not full implementations
   key_methods:
     - name: "execute_command"
       line_start: 80
       line_end: 120
       # Agents can read the code if needed
   ```

### Line Reference Accuracy

**Critical**: Line numbers MUST be accurate when expertise is created/updated.

```yaml
# VALIDATION in self-improve workflow
# 1. Read file at location
# 2. Verify line_start and line_end are correct
# 3. Confirm class/method name matches
# 4. Update if code has moved
```

**Handling Code Changes**:
- Self-improve detects moved code via git diff
- Updates line ranges automatically
- Removes references to deleted code

### Update Frequency

**When to run self-improve**:
- ✅ After significant feature implementation
- ✅ After refactoring that moves code
- ✅ When expertise feels outdated (manual trigger)
- ✅ Weekly for high-churn domains
- ❌ After every minor change (too frequent)
- ❌ Never (expertise becomes stale)

**Git-Diff-Driven Updates**:
```bash
# Run self-improve with git diff context
/experts/cli/self-improve true

# Agent analyzes recent changes and updates expertise
```

### Mental Model Philosophy

**Remember**: Expertise is an abstraction, not duplication.

**Good Mental Model**:
```yaml
# Captures "what" and "why"
command_execution:
  description: "Commands are markdown files with Jinja2 templates"
  patterns:
    - "Lazy loading for performance"
    - "Permission validation before execution"
```

**Bad Mental Model**:
```yaml
# Duplicates code
command_execution:
  code: |
    def execute_command(self, name, args):
        cmd = self.load_command(name)
        if not self.check_permission(cmd):
            raise PermissionError
        return cmd.execute(args)
```

### Context Management

**The 20/80 Rule**: Expertise should consume ~20% of context, leaving 80% for specific task work.

```
┌─────────────────────────────┐
│ Agent Context Window        │
│                             │
│ ┌─────────────────────────┐ │
│ │ Expertise (20%)         │ │  ← Mental model
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │                         │ │
│ │ Task-Specific Work      │ │  ← Actual code, validation
│ │ (80%)                   │ │
│ │                         │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘
```

**If expertise exceeds 20%**: Compress or split into multiple expert domains.

---

## Usage Guidelines

### When to Create New Expertise Files

✅ **Create expertise file when**:
- Domain has 5+ interconnected files
- High complexity or non-obvious patterns
- High error rate with generic agents
- Security or revenue-critical code
- Frequent changes requiring accumulated knowledge

❌ **Don't create expertise file when**:
- Simple 1-2 file domains
- Self-explanatory code
- Brand-new codebase (wait for patterns to emerge)
- You don't understand the domain yet

### How to Structure Domain-Specific Sections

**Database Expert**: Add `schema_structure` section
```yaml
schema_structure:
  tables: [...]
  views: [...]
  relationships: [...]
```

**API Expert**: Add `endpoints` in `schema_structure`
```yaml
schema_structure:
  endpoints:
    - path: "/api/users/{id}"
      method: "GET"
      handler: "api/users.py:45"
```

**Security Expert**: Add `security_constraints` section
```yaml
security_constraints:
  authentication: {...}
  authorization: {...}
  encryption: {...}
```

**Performance Expert**: Add `performance_patterns` section
```yaml
performance_patterns:
  caching: {...}
  async_patterns: {...}
```

### Integration with Agent Workflows

#### Question Prompt (Reuse)

```markdown
# In .claude/commands/experts/cli/question.md

## Process

1. **Read expertise file**
   - Location: `.claude/commands/experts/cli/expertise.yaml`
   - Parse YAML structure
   - Use as mental model

2. **Validate against code**
   - Check line references
   - Confirm patterns still apply
   - Note discrepancies

3. **Answer question**
   - Use expertise to guide investigation
   - Validate details in actual code
   - Report findings with references
```

#### Self-Improve Prompt (Learn)

```markdown
# In .claude/commands/experts/cli/self-improve.md

## Workflow

### Phase 1: Analyze Git Diff (Optional)
- If $1 == "true": Run git diff HEAD
- Identify changed files in domain
- Focus update on changes

### Phase 2: Read Current Expertise
- Load expertise.yaml
- Parse YAML structure

### Phase 3: Validate Against Code
- Check file paths exist
- Verify line ranges are accurate
- Confirm patterns match reality

### Phase 4: Identify Discrepancies
- Outdated line numbers
- Removed code
- New patterns

### Phase 5: Update Expertise
- Add new information
- Correct outdated entries
- Remove obsolete items

### Phase 6: Enforce Constraints
- Check line count <= 1000
- Prune if needed
- Validate YAML syntax

### Phase 7: Write Updated File
- Backup old version
- Write new expertise.yaml
```

#### Orchestrator Pattern (Plan → Build → Improve)

```markdown
# Plan step: Read expertise + validate
# Build step: Execute with mental model
# Improve step: Update expertise with changes
```

### Validation Workflow

**Manual Validation**:
```bash
# 1. Check YAML syntax
python -c "import yaml; yaml.safe_load(open('.claude/commands/experts/cli/expertise.yaml'))"

# 2. Check line count
wc -l .claude/commands/experts/cli/expertise.yaml

# 3. Manual review
cat .claude/commands/experts/cli/expertise.yaml
```

**Automated Validation** (future):
```bash
# Validate against schema
validate-expertise .claude/commands/experts/cli/expertise.yaml

# Output:
# ✓ Valid YAML
# ✓ Line count: 687/1000
# ✓ Required fields present
# ⚠ Line reference outdated: command_service.py:80 (moved to :85)
```

---

## FAQ

### Q: Why 1000 lines maximum?

**A**: Context window efficiency. Expertise should be ~20% of agent context, leaving 80% for actual work. 1000 lines of compressed YAML fits this constraint for most domains.

### Q: What if my domain needs more than 1000 lines?

**A**: Split into multiple expert domains:
- `database_schema` (tables, relationships)
- `database_queries` (query patterns, repositories)
- `database_migrations` (Alembic, version history)

### Q: How often should self-improve run?

**A**:
- After significant changes (new feature, refactor)
- Weekly for high-churn domains
- When expertise feels outdated
- NOT after every minor change

### Q: What if line references become outdated?

**A**: Self-improve validates line references against actual code and updates automatically. This is Phase 3 of the workflow.

### Q: Can I manually edit expertise.yaml?

**A**: Yes, but prefer using self-improve. Manual edits should be for:
- Initial seeding
- Correcting major errors
- Emergency fixes

Let agents maintain it over time.

### Q: How do I seed a new expertise file?

**A**: Two approaches:

1. **Minimal seed** (recommended):
   ```yaml
   overview:
     description: "Brief description"
     key_files: []
     total_files: 0
     last_updated: "2026-02-02"

   core_implementation: {}
   key_operations: {}
   best_practices: []
   ```
   Then run self-improve to populate.

2. **Pre-populated seed**:
   Manually create complete initial version, then let self-improve refine.

### Q: What's the difference between expertise and documentation?

**A**:

| Aspect | Expertise | Documentation |
|--------|-----------|---------------|
| Audience | Agents | Humans |
| Format | YAML (compressed) | Markdown (verbose) |
| Maintenance | Automated (self-improve) | Manual |
| Purpose | Mental model for tasks | Reference for understanding |
| Validation | Against code | Against requirements |
| Line limit | 1000 lines | No limit |

### Q: Can expertise files contain secrets?

**A**: NO. Never include:
- API keys
- Passwords
- Database credentials
- Encryption keys
- PII

Store configuration in `.env`, reference it in expertise:
```yaml
encryption:
  key_location: "env.ENCRYPTION_KEY"  # Reference, not value
```

### Q: How do I handle breaking changes?

**A**: Self-improve detects breaking changes via git diff:

```yaml
recent_changes:
  - date: "2026-02-02"
    description: "BREAKING: Renamed execute_command to run_command"
    affected_files:
      - "command_service.py"
    details: "Updated all callers to use new name"
```

Agents read `recent_changes` first to understand evolution.

### Q: What if two agents update expertise simultaneously?

**A**: Git merge conflict resolution:
- Prefer most recent update
- Manually merge both changes
- Re-run self-improve to reconcile

**Prevention**: Use orchestrator pattern to serialize updates.

---

## Conclusion

Expertise files are the foundation of TAC-13 self-improving agents. By following this structure and validation process, you ensure agents can:

1. **Reuse** accumulated knowledge efficiently
2. **Act** with confidence based on mental models
3. **Learn** automatically from their actions

**Key Principles to Remember**:
- Expertise is a mental model, not source of truth
- Validate against code on every use
- Keep under 1000 lines through compression
- Let agents maintain it via self-improve
- Prioritize actionable, non-obvious information

**Next Steps**:
1. Review existing expertise files for your domains
2. Create new expertise for high-complexity areas
3. Set up self-improve workflows
4. Let the agents learn and evolve their expertise

---

**Version**: 1.0
**Last Updated**: 2026-02-02
**Maintained By**: TAC-13 Self-Improving Agents
