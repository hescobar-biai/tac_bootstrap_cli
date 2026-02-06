# TAC-14: Skills System Guide

**Version**: 1.0
**Baseline**: TAC-14 (v0.8.x)
**Component**: Component 1 -- Skills System (Class 1 Grade 7)

This guide provides a comprehensive reference for the Skills System introduced in TAC-14. It covers how Skills differ from Commands, the progressive disclosure architecture, the anatomy of a Skill, five complete examples, creation workflows, troubleshooting, and integration with other TAC-14 components.

---

## Table of Contents

1. [Skills vs Commands](#skills-vs-commands)
2. [Progressive Disclosure](#progressive-disclosure)
3. [Skill Anatomy](#skill-anatomy)
4. [Complete Examples](#complete-examples)
5. [Creating Your Own Skills](#creating-your-own-skills)
6. [Troubleshooting](#troubleshooting)
7. [Integration with TAC-14](#integration-with-tac-14)

---

## Skills vs Commands

TAC-14 supports two primary mechanisms for extending Claude's behavior: **Commands** and **Skills**. While they serve complementary purposes, they differ fundamentally in structure, invocation model, and capability.

### Commands (`.claude/commands/*.md`)

Commands are static prompt templates invoked explicitly by the user with `/command-name`. They consist of a single markdown file containing a text template with `$ARGUMENTS` placeholders. When invoked, the template text is injected directly into the conversation. Commands are ideal for repetitive, well-scoped tasks that always follow the same structure.

**Example command** (`/commit`):
```markdown
# Generate Git Commit

## Variables
agent_name: $ARGUMENT
issue_class: $ARGUMENT
issue: $ARGUMENT

## Instructions
- Generate a concise commit message in the format: `<agent_name>: <issue_class>: <commit message>`
...
```

### Skills (`.claude/skills/{name}/SKILL.md`)

Skills are rich, self-contained modules stored as directories. Each Skill has a `SKILL.md` file with YAML frontmatter (`name` and `description`) and a markdown body containing instructions. Skills can bundle additional resources -- documentation, scripts, templates -- in subdirectories alongside `SKILL.md`. Unlike Commands, Skills are **model-invoked**: Claude autonomously decides when to load and use a Skill based on the user's request and the Skill's description. This means Skills are triggered contextually rather than explicitly.

**Example skill** (`meta-skill`):
```yaml
---
name: creating-new-skills
description: Creates new Agent Skills for AI Agents following best practices and documentation. Use when the user wants prompts 'create a new skill ...' or 'use your meta skill to ...'.
---

# Purpose
Create new Agent Skills by following a structured workflow...
```

### Comparison Table

| Aspect | Commands | Skills |
|--------|----------|--------|
| **Invocation** | User-invoked with `/command-name` | Model-invoked (Claude decides automatically) |
| **Structure** | Single `.md` file | Directory with `SKILL.md` + optional `docs/`, `scripts/`, `templates/` |
| **Parameterization** | `$ARGUMENTS` placeholder substitution | Description-based matching; no explicit parameters |
| **Documentation** | Self-contained in the file | Progressive disclosure: metadata, instructions, resources |
| **Context Loading** | Entire file loaded at once | Three-level progressive disclosure (metadata always, body on trigger, resources on demand) |
| **Complexity** | Low -- simple text templates | Medium to High -- structured workflows with bundled resources |
| **Resource Bundling** | None (single file only) | Templates, scripts, reference docs in subdirectories |
| **Composability** | Limited -- one command at a time | High -- Skills can reference other Skills |
| **Best For** | Repetitive tasks: commit, lint, build, review | Reusable domain workflows: code review, test generation, documentation |
| **Token Overhead** | Full template loaded every time | ~100 tokens for metadata; body loaded only when relevant |

### When to Use Each

- **Use a Command** when: You need a quick, user-triggered action with a fixed structure. Examples: `/commit`, `/lint`, `/build`, `/implement`.
- **Use a Skill** when: You need a reusable workflow with bundled resources that Claude should trigger contextually. Examples: code review with checklists, test generation with templates, documentation with style guides.
- **Use an ADW** when: You need multi-step orchestration with branching logic, external tool invocations, and programmatic control. Examples: SDLC workflow, patch workflow, ship workflow.

---

## Progressive Disclosure

Progressive disclosure is the core design principle of the Skills System. Instead of loading all information into the context window at once, Skills reveal information in stages based on what the agent actually needs at each point.

### Why Progressive Disclosure Matters

- **Context window efficiency**: Only relevant content occupies the context window at any given time.
- **Scalability**: You can install dozens or hundreds of Skills without context bloat. Each Skill costs only ~100 tokens of metadata at startup.
- **Faster discovery**: Claude scans lightweight metadata to find the right Skill without reading all instructions.
- **Flexibility**: Resources load on-demand, meaning a Skill can bundle megabytes of templates and scripts with zero cost until they are actually needed.

### The Three Levels

#### Level 1: Metadata (Always Loaded)

The YAML frontmatter of every installed Skill is pre-loaded into Claude's system prompt at startup. This includes only the `name` and `description` fields.

**When**: At session startup, for every installed Skill.
**Token cost**: ~50-150 tokens per Skill.
**Purpose**: Enables Claude to know what Skills exist and when to trigger them.

```yaml
---
name: creating-new-skills
description: Creates new Agent Skills for AI Agents following best practices and documentation. Use when the user wants prompts 'create a new skill ...' or 'use your meta skill to ...'.
---
```

#### Level 2: Instructions (Loaded When Triggered)

When a user's request matches a Skill's description, Claude reads the full body of `SKILL.md` into the context window. This contains the workflow, step-by-step instructions, and references to Level 3 resources.

**When**: When Claude determines the Skill is relevant to the current task.
**Token cost**: ~500-2000 tokens (target: SKILL.md body under 500 lines).
**Purpose**: Provides the agent with enough procedural knowledge to execute the Skill.

```markdown
# Purpose
Create new Agent Skills by following a structured workflow based on best practices.

## Instructions
### Prerequisites
**Required Reading** - Read these files in order before creating a skill:
1. [docs/claude_code_agent_skills.md](docs/claude_code_agent_skills.md)
2. [docs/claude_code_agent_skills_overview.md](docs/claude_code_agent_skills_overview.md)
...
```

#### Level 3: Resources (Loaded As Needed)

Additional files bundled in the Skill directory -- documentation, templates, scripts, examples -- are loaded only when the instructions explicitly reference them and the agent determines they are needed for the current task.

**When**: Only when the agent navigates to a referenced file.
**Token cost**: Variable (effectively unbounded total, but only loaded portions consume tokens).
**Purpose**: Provides deep reference material, executable scripts, or templates without upfront cost.

```
meta-skill/
├── SKILL.md                                    # Level 2
└── docs/                                       # Level 3
    ├── claude_code_agent_skills.md
    ├── claude_code_agent_skills_overview.md
    └── blog_equipping_agents_with_skills.md
```

### How Users Graduate Through Levels

The progressive disclosure model also describes how users naturally adopt Skills:

1. **Basic invocation**: A user asks Claude a question that happens to match a Skill. Claude loads the Skill automatically and follows its instructions. The user may not even know a Skill was involved.
   ```
   "Help me review this Python code for security issues"
   → Claude triggers the code-review Skill, follows its checklist
   ```

2. **Intentional use**: The user learns which Skills are available and crafts requests to trigger them deliberately. They may combine requests to invoke multiple Skills.
   ```
   "Use your meta-skill to create a deployment Skill for AWS"
   → Claude triggers the meta-skill, follows its creation workflow
   ```

3. **Advanced composition**: The user creates new Skills that reference other Skills, builds orchestrator commands that leverage Skills, or chains Skill outputs as inputs to subsequent requests.
   ```
   "Create a Skill that first runs code-review, then generates tests for any issues found"
   → Uses meta-skill to compose code-review + test-generator Skills
   ```

---

## Skill Anatomy

### Directory Structure

Every Skill lives in a directory under one of three locations:

| Location | Scope | Sharing |
|----------|-------|---------|
| `~/.claude/skills/{skill-name}/` | Personal (all your projects) | Not shared |
| `.claude/skills/{skill-name}/` | Project (team via git) | Shared via git |
| Plugin-bundled | Plugin-scoped | Shared via plugin installation |

The minimal structure requires only a `SKILL.md` file:

```
.claude/skills/{skill-name}/
└── SKILL.md          # Required: main definition with YAML frontmatter
```

A more complete Skill includes supporting files:

```
.claude/skills/{skill-name}/
├── SKILL.md          # Main definition with YAML frontmatter
├── docs/             # Supporting documentation
│   ├── reference.md
│   └── examples.md
├── scripts/          # Executable utilities
│   └── helper.py
└── templates/        # Output templates
    └── template.md
```

### SKILL.md Format

The `SKILL.md` file must begin with YAML frontmatter delimited by `---` lines, followed by a markdown body.

#### YAML Frontmatter

```yaml
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it.
---
```

**Required fields**:

| Field | Constraints |
|-------|-------------|
| `name` | Max 64 characters. **Lowercase letters, numbers, and hyphens only**. Use gerund form (verb + -ing): `processing-pdfs`, `analyzing-data`, `generating-tests`. Cannot contain XML tags or reserved words ("anthropic", "claude"). |
| `description` | Max 1024 characters. **Must be written in third person** (critical for discovery). Include both what the Skill does AND when to use it. Mention key trigger words/phrases. Cannot contain XML tags. |

**Optional fields (Claude Code only)**:

| Field | Purpose |
|-------|---------|
| `allowed-tools` | Comma-separated list restricting which tools Claude can use when this Skill is active. Example: `Read, Grep, Glob` |

#### Description Best Practices

The `description` is the single most important field for Skill discovery. Claude uses it to decide whether to trigger the Skill.

Good descriptions (third person, specific, include triggers):
```yaml
description: Reviews Python code for PEP 8 compliance, security issues, and performance bottlenecks. Use when reviewing Python code, checking code quality, or analyzing Python files for best practices.
```

```yaml
description: Generates comprehensive unit tests for Python services using pytest. Use when user asks to create tests, generate test suites, or add test coverage for existing code.
```

Bad descriptions (first person, vague, no triggers):
```yaml
description: Helps with code
description: I can review your files
description: For testing
```

#### Markdown Body

The body follows the frontmatter and typically includes these sections:

```markdown
# Skill Name

## Purpose
One-paragraph description of what this Skill accomplishes.

## Instructions
### Prerequisites
- Required dependencies, tools, environment setup

### Workflow
1. **Step one**: Description with code examples
2. **Step two**: Description with details
3. **Step three**: Expected outcomes

## Examples
### Example 1: Descriptive Title
User request: "..."
Actions taken: ...
Expected outcome: ...
```

**Key guidelines for the body**:
- Keep the body under 500 lines for optimal performance.
- Use clear, actionable, numbered steps.
- Reference supporting files with relative links: `[reference.md](docs/reference.md)`.
- Avoid deeply nested references -- keep references one level deep from `SKILL.md`.
- For files over 100 lines, include a table of contents at the top.
- Always use forward slashes for file paths: `scripts/helper.py` (not backslashes).

---

## Complete Examples

### Example 1: meta-skill -- Creates New Skills from Descriptions

The `meta-skill` is the only Skill currently shipped with the TAC-14 agentic layer. It is a self-referential Skill that teaches Claude how to create new Skills following best practices.

**Invocation**:
```
"Use your meta-skill to create a deployment skill for AWS"
"Create a new skill for analyzing log files"
```

**What it does**:
1. Reads comprehensive documentation on Skill architecture from its `docs/` directory.
2. Asks clarifying questions about the desired Skill's purpose, triggers, and resources.
3. Creates the Skill directory structure under `.claude/skills/`.
4. Writes the `SKILL.md` file with proper YAML frontmatter and markdown body.
5. Adds supporting files (scripts, templates, documentation) as needed.
6. Tests the Skill by verifying file structure and YAML validity.

**Expected output**: A complete Skill directory ready for use, committed to the project repository.

**SKILL.md frontmatter**:
```yaml
---
name: creating-new-skills
description: Creates new Agent Skills for AI Agents following best practices and documentation. Use when the user wants prompts 'create a new skill ...' or 'use your meta skill to ...'.
---
```

**Directory structure**:
```
.claude/skills/meta-skill/
├── SKILL.md
└── docs/
    ├── claude_code_agent_skills.md
    ├── claude_code_agent_skills_overview.md
    └── blog_equipping_agents_with_skills.md
```

---

### Example 2: code-review -- Security and Quality Analysis

A code review Skill that provides structured analysis of code for security vulnerabilities, best practices, and quality issues.

**Invocation**:
```
"Check security vulnerabilities in the auth module"
"Review the payment service for code quality issues"
"Analyze src/api/ for potential bugs"
```

**What it does**:
1. Reads the target files using `Read`, `Grep`, and `Glob` tools.
2. Follows a structured review checklist (security, error handling, performance, style).
3. Identifies specific issues with file paths and line numbers.
4. Categorizes findings by severity (critical, warning, info).
5. Produces a structured markdown report with actionable recommendations.

**Expected output**: A categorized review report with severity levels, specific file/line references, and concrete fix suggestions.

**SKILL.md frontmatter**:
```yaml
---
name: reviewing-code-quality
description: Reviews code for security vulnerabilities, performance issues, error handling gaps, and style violations. Use when reviewing code, checking PRs, auditing security, or analyzing code quality. Triggers on requests like "review code", "check security", "audit this module", or "find bugs".
allowed-tools: Read, Grep, Glob
---
```

**Directory structure**:
```
.claude/skills/reviewing-code-quality/
├── SKILL.md
└── docs/
    ├── security_checklist.md       # OWASP-based security review items
    ├── performance_patterns.md     # Common performance anti-patterns
    └── report_template.md          # Structured output format
```

**SKILL.md body (abbreviated)**:
```markdown
# Code Quality Review

Performs structured code review following established security and quality checklists.

## Instructions

### Prerequisites
- No external dependencies required (uses built-in Read, Grep, Glob tools)

### Workflow

1. **Identify scope**: Determine which files/directories to review
   - If user specifies files, use those directly
   - If user specifies a module or feature, use Glob to find all relevant files

2. **Security review**: Check against [security_checklist.md](docs/security_checklist.md)
   - Input validation and sanitization
   - Authentication and authorization patterns
   - SQL injection, XSS, CSRF vulnerabilities
   - Secrets or credentials in source code

3. **Quality review**: Analyze code structure
   - Error handling completeness
   - Resource management (file handles, connections)
   - Naming conventions and readability
   - DRY violations and code duplication

4. **Performance review**: Check [performance_patterns.md](docs/performance_patterns.md)
   - N+1 query patterns
   - Unnecessary computations in loops
   - Missing caching opportunities

5. **Generate report**: Use [report_template.md](docs/report_template.md) format
   - Group findings by severity
   - Include file path and line number for each finding
   - Provide specific fix recommendations

## Examples

### Example 1: Module Security Audit
User request: "Check the auth module for security issues"
...
```

---

### Example 3: test-generator -- Unit Test Suite Generation

A Skill that generates comprehensive unit test suites for existing code using pytest conventions.

**Invocation**:
```
"Generate unit tests for UserService"
"Add test coverage for the payment processing module"
"Create tests for all functions in src/utils/validators.py"
```

**What it does**:
1. Reads the target source files and identifies all public functions/methods/classes.
2. Analyzes function signatures, return types, and dependencies.
3. Identifies edge cases (null inputs, boundary values, error conditions).
4. Generates pytest test files following project conventions (conftest fixtures, parametrize decorators).
5. Includes both positive (happy path) and negative (error handling) test cases.

**Expected output**: One or more `test_*.py` files with comprehensive test cases, fixtures, and parametrized tests.

**SKILL.md frontmatter**:
```yaml
---
name: generating-unit-tests
description: Generates comprehensive pytest unit test suites for Python modules and services. Use when user asks to create tests, generate test suites, add test coverage, or write unit tests. Triggers on requests like "generate tests for", "add test coverage", "create unit tests", or "test this module".
---
```

**Directory structure**:
```
.claude/skills/generating-unit-tests/
├── SKILL.md
├── docs/
│   ├── pytest_conventions.md       # Project-specific pytest patterns
│   └── fixture_patterns.md         # Common fixture templates
└── templates/
    ├── test_service_template.md    # Template for service tests
    └── test_api_template.md        # Template for API endpoint tests
```

**SKILL.md body (abbreviated)**:
```markdown
# Unit Test Generation

Generate comprehensive pytest test suites that follow project conventions and achieve high coverage.

## Instructions

### Prerequisites
- Target project uses pytest as the test framework
- Review [pytest_conventions.md](docs/pytest_conventions.md) for project-specific patterns

### Workflow

1. **Analyze target code**: Read source files to identify:
   - All public functions, methods, and classes
   - Function signatures and type hints
   - External dependencies (for mocking)
   - Error handling paths

2. **Plan test cases**: For each function/method, identify:
   - Happy path scenarios
   - Edge cases (empty inputs, boundary values, None)
   - Error conditions (invalid inputs, exceptions)
   - Integration points requiring mocks

3. **Select template**: Choose from [templates/](templates/):
   - `test_service_template.md` for business logic services
   - `test_api_template.md` for FastAPI/Flask endpoints

4. **Generate test file**:
   - Follow naming convention: `test_{module_name}.py`
   - Place in corresponding `tests/` directory mirroring source structure
   - Use `@pytest.mark.parametrize` for multiple input scenarios
   - Use fixtures from [fixture_patterns.md](docs/fixture_patterns.md)

5. **Validate**: Run `pytest {test_file} -v` to confirm tests pass

## Examples

### Example 1: Service Test Generation
User request: "Generate unit tests for UserService"
...
```

---

### Example 4: refactor -- Code Restructuring with Safety Checks

A Skill that guides safe code refactoring operations with pre/post validation.

**Invocation**:
```
"Extract payment logic into a separate module"
"Refactor the monolithic handler into separate services"
"Move database queries from the controller into a repository layer"
```

**What it does**:
1. Analyzes the target code to understand current dependencies and call chains.
2. Creates a refactoring plan with specific file-level changes.
3. Runs existing tests before making changes (baseline).
4. Performs the refactoring in incremental steps.
5. Updates all import statements and references across the codebase.
6. Runs tests after each step to verify nothing broke.
7. Produces a summary of all changes with before/after comparisons.

**Expected output**: Refactored code with updated imports, passing tests, and a change summary.

**SKILL.md frontmatter**:
```yaml
---
name: refactoring-code
description: Performs safe code refactoring operations including extract module, move function, rename across codebase, and restructure layers. Use when user asks to refactor, extract, restructure, or reorganize code. Triggers on requests like "extract into module", "refactor this", "move logic to", or "restructure".
---
```

**Directory structure**:
```
.claude/skills/refactoring-code/
├── SKILL.md
└── docs/
    ├── refactoring_patterns.md     # Extract Method, Extract Class, Move Module, etc.
    ├── safety_checklist.md         # Pre/post validation steps
    └── import_resolution.md        # How to trace and update imports
```

**SKILL.md body (abbreviated)**:
```markdown
# Code Refactoring

Perform safe, incremental code refactoring with automated validation at each step.

## Instructions

### Prerequisites
- Working test suite (run `pytest` or equivalent to verify baseline)
- Version control (uncommitted changes will be stashed)

### Workflow

1. **Understand scope**: Read the target code and all callers
   - Use Grep to find all references to the target code
   - Map the dependency graph (who calls what)

2. **Create refactoring plan**: Based on [refactoring_patterns.md](docs/refactoring_patterns.md)
   - Extract Module: Move code to new file, update imports
   - Extract Class: Group related functions into a class
   - Move Function: Relocate between modules
   - Rename: Update all references across codebase

3. **Baseline validation**: Run existing tests to confirm green state
   - If tests fail before refactoring, stop and report

4. **Execute incrementally**: One logical change at a time
   - Make change
   - Update imports using [import_resolution.md](docs/import_resolution.md)
   - Run tests
   - If tests fail, revert and try a different approach

5. **Post-refactoring validation**: Follow [safety_checklist.md](docs/safety_checklist.md)
   - All tests pass
   - No unused imports
   - No circular dependencies
   - Linter passes

## Examples

### Example 1: Extract Payment Logic
User request: "Extract payment logic into a separate module"
...
```

---

### Example 5: doc-generator -- API Documentation Generation

A Skill that generates structured API documentation from source code analysis.

**Invocation**:
```
"Create API documentation for the user endpoints"
"Generate documentation for all REST endpoints in src/api/"
"Document the authentication API with request/response examples"
```

**What it does**:
1. Scans source files to identify all API endpoints (routes, handlers).
2. Extracts endpoint metadata: HTTP method, path, parameters, request/response schemas.
3. Identifies authentication requirements and middleware.
4. Generates structured markdown documentation following a consistent template.
5. Includes request/response examples with sample payloads.

**Expected output**: Markdown API documentation with endpoint tables, parameter descriptions, example requests/responses, and authentication requirements.

**SKILL.md frontmatter**:
```yaml
---
name: generating-api-docs
description: Generates structured API documentation from source code analysis including endpoint tables, parameter descriptions, and request/response examples. Use when user asks to document APIs, create endpoint documentation, or generate API reference. Triggers on requests like "document API", "create API docs", "generate endpoint documentation".
allowed-tools: Read, Grep, Glob
---
```

**Directory structure**:
```
.claude/skills/generating-api-docs/
├── SKILL.md
├── docs/
│   └── framework_patterns.md      # FastAPI, Flask, Express detection patterns
└── templates/
    ├── api_overview_template.md    # Top-level API documentation template
    ├── endpoint_template.md        # Per-endpoint documentation template
    └── schema_template.md          # Request/response schema template
```

**SKILL.md body (abbreviated)**:
```markdown
# API Documentation Generator

Generate comprehensive API reference documentation from source code analysis.

## Instructions

### Prerequisites
- No external dependencies required (read-only analysis)
- Review [framework_patterns.md](docs/framework_patterns.md) to identify the API framework

### Workflow

1. **Detect framework**: Analyze project structure to identify:
   - FastAPI (look for `@app.get`, `@router.post`, `APIRouter`)
   - Flask (look for `@app.route`, `Blueprint`)
   - Express (look for `router.get`, `app.use`)

2. **Discover endpoints**: Use Grep to find all route decorators
   - Extract HTTP method, path, handler function
   - Identify path parameters, query parameters
   - Find request body schema (Pydantic models, marshmallow schemas)

3. **Extract metadata**: For each endpoint:
   - Read the handler function
   - Identify response model/schema
   - Check for authentication decorators
   - Find middleware or dependency injection

4. **Generate documentation**: Using [templates/](templates/)
   - Start with [api_overview_template.md](templates/api_overview_template.md)
   - Generate each endpoint using [endpoint_template.md](templates/endpoint_template.md)
   - Document schemas using [schema_template.md](templates/schema_template.md)

5. **Write output**: Create documentation file(s) at project's docs location

## Examples

### Example 1: FastAPI Endpoint Documentation
User request: "Create API documentation for the user endpoints"
...
```

---

## Creating Your Own Skills

### Step-by-Step Guide

#### Step 1: Define Purpose and Triggers

Before writing any files, answer these questions:

1. **What task or domain does this Skill cover?** (e.g., "generating database migration scripts")
2. **When should Claude use this Skill?** List trigger phrases users might say (e.g., "create migration", "add database column", "generate schema change").
3. **What expertise or workflows need to be captured?** (e.g., specific migration tool conventions, naming patterns, rollback procedures).
4. **Does the Skill need scripts, templates, or other resources?** (e.g., migration templates, validation scripts).

#### Step 2: Create the Directory

```bash
# For team-shared Skills (committed to git):
mkdir -p .claude/skills/your-skill-name

# For personal Skills (available across all your projects):
mkdir -p ~/.claude/skills/your-skill-name
```

**Naming conventions**:
- Use gerund form (verb + -ing): `generating-migrations`, `processing-pdfs`, `analyzing-logs`
- Lowercase letters, numbers, and hyphens only
- Maximum 64 characters
- Cannot contain reserved words ("anthropic", "claude")
- Avoid generic names like `helper`, `utils`, `tools`

#### Step 3: Write the SKILL.md

Create the `SKILL.md` file with YAML frontmatter and markdown body:

```yaml
---
name: generating-migrations
description: Generates database migration scripts following project conventions with up/down methods, naming patterns, and rollback procedures. Use when user asks to create migrations, add database columns, modify schema, or generate migration files. Triggers on "create migration", "add column", "change schema".
---

# Database Migration Generator

## Purpose
Generate safe, reversible database migration scripts following project conventions.

## Instructions

### Prerequisites
- Project uses Alembic (Python) or Knex (Node.js) for migrations
- Database schema files are in `src/database/` or `alembic/versions/`

### Workflow
1. **Identify change**: What schema modification is needed?
2. **Check existing migrations**: Read recent migrations to understand conventions
3. **Generate migration**: Create migration file with:
   - Descriptive name: `{timestamp}_{description}.py`
   - `upgrade()` function with the change
   - `downgrade()` function to reverse the change
4. **Validate**: Check for syntax errors and dependency ordering

## Examples

### Example 1: Add Column
User request: "Add an email_verified boolean column to the users table"
...
```

#### Step 4: Add Supporting Files (Optional)

If your Skill needs additional context, create supporting files:

```bash
mkdir -p .claude/skills/your-skill-name/docs
mkdir -p .claude/skills/your-skill-name/templates
mkdir -p .claude/skills/your-skill-name/scripts
```

Reference them from `SKILL.md` using relative links:
```markdown
For naming conventions, see [docs/conventions.md](docs/conventions.md).
Use the template in [templates/migration_template.md](templates/migration_template.md).
Run validation with [scripts/validate_migration.py](scripts/validate_migration.py).
```

**Guidelines for supporting files**:
- Keep references one level deep from `SKILL.md` (avoid `docs/subfolder/another/file.md`)
- For files over 100 lines, include a table of contents at the top
- Make scripts executable: `chmod +x scripts/*.py`
- Use forward slashes in all paths: `scripts/helper.py`

#### Step 5: Test the Skill

1. **Verify structure**:
   ```bash
   ls -la .claude/skills/your-skill-name/
   ```

2. **Validate YAML frontmatter**:
   ```bash
   head -10 .claude/skills/your-skill-name/SKILL.md
   ```
   Ensure: opening `---` on line 1, closing `---` before markdown content, valid YAML syntax (no tabs, correct indentation).

3. **Test with relevant queries**: Ask Claude questions that should trigger the Skill:
   ```
   "Create a migration to add email_verified column to users"
   ```

4. **Iterate**: If Claude does not trigger the Skill, refine the `description` to include more specific trigger words. If Claude's execution is unclear, improve the workflow instructions.

#### Step 6: Commit and Share

```bash
git add .claude/skills/your-skill-name/
git commit -m "feat: add generating-migrations skill"
git push
```

Team members get the Skill automatically when they pull.

### Using meta-skill to Generate Skills Automatically

The fastest way to create a new Skill is to use the existing `meta-skill`:

```
"Use your meta-skill to create a skill for generating database migrations"
```

The meta-skill will:
1. Read its comprehensive documentation on Skill architecture.
2. Ask you clarifying questions about the Skill's purpose and triggers.
3. Create the complete directory structure.
4. Write `SKILL.md` with proper frontmatter and instructions.
5. Add supporting files as needed.
6. Verify the structure and provide testing guidance.

This approach ensures your new Skill follows all best practices from the official documentation.

### YAML Frontmatter Quick Reference

| Field | Required | Constraints | Example |
|-------|----------|-------------|---------|
| `name` | Yes | Max 64 chars; lowercase, numbers, hyphens; gerund form; no reserved words | `generating-migrations` |
| `description` | Yes | Max 1024 chars; third person; include what + when + triggers; no XML tags | `Generates database migration scripts... Use when user asks to create migrations...` |
| `allowed-tools` | No | Comma-separated tool names (Claude Code only) | `Read, Grep, Glob, Bash` |

---

## Troubleshooting

### Skill Not Found / Not Triggering

**Symptom**: You ask a relevant question but Claude does not use your Skill.

**Checks**:

1. **Is the Skill in the correct location?**
   ```bash
   # Personal Skills
   ls ~/.claude/skills/your-skill-name/SKILL.md

   # Project Skills
   ls .claude/skills/your-skill-name/SKILL.md
   ```

2. **Is the description specific enough?**
   Vague descriptions prevent discovery. Include specific trigger words that users would naturally use.

   Too generic:
   ```yaml
   description: Helps with databases
   ```

   Specific:
   ```yaml
   description: Generates database migration scripts with up/down methods. Use when creating migrations, adding columns, or modifying database schema.
   ```

3. **Is the description written in third person?**
   Descriptions are injected into the system prompt. First/second person phrasing breaks discovery.

   Wrong:
   ```yaml
   description: I can help you create migrations
   ```

   Correct:
   ```yaml
   description: Creates database migration scripts following project conventions. Use when...
   ```

4. **Are there conflicting Skills?**
   If multiple Skills have similar descriptions, Claude may choose the wrong one or become confused. Make descriptions distinct with unique trigger terms.

### YAML Frontmatter Parsing Errors

**Symptom**: The Skill fails to load or Claude reports errors.

**Checks**:

1. **Is the frontmatter delimited correctly?**
   The file must start with `---` on line 1, and the frontmatter must end with `---` before the markdown body. No blank lines before the opening delimiter.

   Correct:
   ```
   ---
   name: my-skill
   description: My skill description.
   ---

   # My Skill
   ```

   Wrong (blank line before opening):
   ```

   ---
   name: my-skill
   ...
   ```

2. **Are there syntax errors in the YAML?**
   - No tabs (use spaces only)
   - Strings with special characters (colons, quotes) must be quoted
   - No trailing whitespace after field names

   ```yaml
   # This will break:
   description: Use when: user asks for help

   # This is correct:
   description: "Use when: user asks for help"
   ```

3. **Validate by inspection**:
   ```bash
   head -15 .claude/skills/your-skill-name/SKILL.md
   ```

### Skill Docs Not Loading (Level 3 Resources)

**Symptom**: The Skill triggers, but Claude does not read supporting files.

**Checks**:

1. **Are file references correct?** Use relative paths from `SKILL.md`:
   ```markdown
   # Correct:
   See [docs/reference.md](docs/reference.md)

   # Wrong (absolute path):
   See [/Users/me/.claude/skills/my-skill/docs/reference.md](...)
   ```

2. **Do the referenced files exist?**
   ```bash
   ls -la .claude/skills/your-skill-name/docs/
   ```

3. **Are paths using forward slashes?**
   ```markdown
   # Correct:
   See [scripts/helper.py](scripts/helper.py)

   # Wrong (Windows-style backslashes):
   See [scripts\helper.py](scripts\helper.py)
   ```

4. **Are references too deeply nested?**
   Keep references one level deep from `SKILL.md`. Avoid chains like `SKILL.md -> docs/guide.md -> docs/subfolder/detail.md`.

### Permission Issues

**Symptom**: Claude cannot read or execute Skill files.

**Checks**:

1. **Are scripts executable?**
   ```bash
   chmod +x .claude/skills/your-skill-name/scripts/*.py
   chmod +x .claude/skills/your-skill-name/scripts/*.sh
   ```

2. **Are file permissions readable?**
   ```bash
   ls -la .claude/skills/your-skill-name/SKILL.md
   # Should show at least -rw-r--r--
   ```

3. **Is the `allowed-tools` field too restrictive?**
   If you specified `allowed-tools: Read, Grep, Glob` but the Skill needs to write files or run scripts, Claude will be unable to execute those operations.

### How to Debug Skill Execution

1. **Run Claude Code in debug mode**:
   ```bash
   claude --debug
   ```
   This shows Skill loading and matching decisions.

2. **Ask Claude directly**:
   ```
   "What Skills are available?"
   "List all available Skills"
   ```
   This reveals which Skills Claude can see and their descriptions.

3. **Test incrementally**:
   - First verify the Skill triggers (check description matching)
   - Then verify Level 2 instructions are clear (check workflow execution)
   - Finally verify Level 3 resources load correctly (check file references)

---

## Integration with TAC-14

The Skills System (Component 1) integrates with other TAC-14 components to form a comprehensive agentic layer.

### Skills + Agent Definitions (Component 2)

Agent Definitions (`.claude/agents/*.md`) are specialized agent profiles invoked as sub-agents by orchestrator commands. While Skills and Agents are both markdown-based, they serve different purposes:

| Aspect | Skills | Agent Definitions |
|--------|--------|-------------------|
| **Purpose** | Reusable domain workflows | Specialized execution profiles |
| **Invoked by** | Claude (model-invoked) | Orchestrator commands via `Task` tool |
| **Location** | `.claude/skills/` | `.claude/agents/` |
| **Frontmatter** | `name`, `description` | `name`, `description`, `tools`, `model`, `color` |
| **Contains** | Workflows + bundled resources | Agent persona + system prompt |

**How they work together**: An Agent Definition can leverage Skills during its execution. For example, the `build-agent` (which implements single files) might trigger the `generating-unit-tests` Skill if it determines that the file it is implementing needs accompanying tests. The agent does not explicitly invoke the Skill -- Claude's model-invoked discovery handles it automatically based on the task context.

**Example integration flow**:
```
User: /orch_scout_and_build "Add payment processing with tests"
  └─> Orchestrator Command spawns scout-report-suggest agent
  └─> Orchestrator Command spawns build-agent
       └─> build-agent writes payment module
       └─> Claude's Skill discovery triggers generating-unit-tests
            └─> Tests are generated alongside the implementation
```

### Skills + Orchestrator Commands (Component 3)

Orchestrator Commands (`.claude/commands/orch_*.md`) coordinate multi-agent workflows by spawning sub-agents through the `Task` tool. Skills enhance orchestrator workflows by providing domain expertise that any agent in the pipeline can leverage.

**Key orchestrator commands**:

| Command | Description | How Skills Help |
|---------|-------------|-----------------|
| `orch_plan_w_scouts_build_review.md` | Full pipeline: scout, plan, build, review | Review agents can use code-review Skill |
| `orch_scout_and_build.md` | Discover files, then build | Build agents can use doc-generator or test-generator Skills |
| `orch_one_shot_agent.md` | Single-agent task execution | Any Skill matching the task triggers automatically |
| `build_in_parallel.md` | Parallel file implementation | Each parallel builder can use relevant Skills independently |
| `parallel_subagents.md` | Coordinate multiple sub-agents | Sub-agents share access to project Skills |

**Example**: When running `/orch_plan_w_scouts_build_review "Implement user authentication"`:
1. The **scout** agent analyzes the codebase (may trigger read-only Skills).
2. The **planner** agent creates an implementation plan.
3. The **build** agents implement files (may trigger test-generator or doc-generator Skills).
4. The **review** agent checks the implementation (may trigger code-review Skill).

Skills add a layer of domain expertise on top of the agent pipeline without requiring explicit orchestration. Each agent in the pipeline independently discovers and uses relevant Skills.

### Skills in ADW Workflows (adws/)

ADW (AI Developer Workflows) are Python-based automation scripts that run outside the terminal (outloop). While ADWs and Skills operate at different levels -- ADWs are Python scripts, Skills are markdown-based -- they can complement each other:

1. **ADWs invoke Claude Code sessions** that have access to project Skills. When an ADW spawns a Claude agent (via `adw_modules/agent.py`), that agent session has access to all installed Skills in the project.

2. **ADWs can create Skills** as part of their workflow. For example, an SDLC workflow could generate a project-specific Skill during the planning phase.

3. **Skills inform ADW design**: Patterns discovered through Skill usage can be formalized into ADW automation. If a Skill is used frequently enough, it may warrant being promoted to a full ADW workflow with programmatic control.

**Integration architecture**:
```
ADW Workflow (Python, outloop)
  └─> Spawns Claude Agent (via Agent SDK)
       └─> Agent has access to .claude/skills/
       └─> Agent can use /commands
       └─> Agent can invoke Task tool for sub-agents (.claude/agents/)
            └─> Sub-agents also have access to Skills
```

### Summary: TAC-14 Component Interaction

```
Class 1: Agentic Layer
├── Skills (.claude/skills/)          ← Domain expertise, model-invoked
├── Commands (.claude/commands/)      ← User-triggered actions
└── Hooks (.claude/hooks/)            ← Automated validations

Class 2: Outloop Systems
├── Agent Definitions (.claude/agents/)  ← Sub-agent profiles
├── Orchestrator Commands (orch_*)       ← Multi-agent coordination
└── Agent SDK (adw_agent_sdk.py)         ← Programmatic control

Class 3: Orchestrator Agent
├── Database (SQLite)                    ← State persistence
├── WebSockets                           ← Real-time events
├── Workflows (adws/)                    ← Python automation
└── Web UI (FastAPI + Vue 3)             ← Visual orchestration
```

Skills operate at Class 1 but are accessible from Class 2 (via agent sub-processes) and Class 3 (via ADW-spawned agents). They provide the foundational domain expertise that all higher-level components can leverage automatically.

---

## References

- [meta-skill SKILL.md](/.claude/skills/meta-skill/SKILL.md) -- The actual meta-skill implementation
- [meta-skill-pattern.md](meta-skill-pattern.md) -- Detailed meta-skill pattern documentation
- [Tac-14_complete_guide.md](Tac-14_complete_guide.md) -- Full TAC-14 component reference
- [Tac-14_1.md](Tac-14_1.md) / [Tac-14_2.md](Tac-14_2.md) -- TAC-14 course material
- [Anthropic Blog: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
