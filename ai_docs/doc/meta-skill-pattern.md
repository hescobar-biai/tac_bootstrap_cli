# Meta-Skill Pattern Documentation

**Version**: 1.0
**Last Updated**: 2026-02-03
**Purpose**: Standard pattern for creating composable, efficient skills using progressive disclosure

---

## Table of Contents

1. [Introduction](#introduction)
2. [Progressive Disclosure Model](#progressive-disclosure-model)
3. [SKILL.md Structure](#skillmd-structure)
4. [Discovery Mechanism](#discovery-mechanism)
5. [Creation Workflow](#creation-workflow)
6. [Concrete Examples](#concrete-examples)
7. [Best Practices](#best-practices)
8. [Comparison: Skills vs Commands vs ADWs](#comparison-skills-vs-commands-vs-adws)
9. [FAQ](#faq)

---

## Introduction

### What are Skills?

**Skills** are composable, reusable agent workflows organized as self-contained directories with a `SKILL.md` entry point and optional supporting resources (templates, scripts, documentation). They represent focused, triggerable capabilities that agents can discover and execute.

**Core Philosophy**: Skills optimize context window usage through **progressive disclosure** - loading only necessary information at each stage of execution.

### Skills vs Other Patterns

| Aspect | Skills | Commands | ADWs |
|--------|--------|----------|------|
| **Purpose** | Reusable workflows with resources | Single-purpose prompts | Complex automation orchestration |
| **Structure** | Directory with SKILL.md + resources | Single .md file | Python scripts |
| **Context Loading** | Progressive (3 levels) | All-at-once | N/A (execution-based) |
| **Resources** | Templates, scripts bundled | None typically | Can invoke external tools |
| **Composability** | High (skills call skills) | Medium | High (ADWs call ADWs) |
| **Typical Size** | <500 lines SKILL.md | <200 lines | Variable |

**When to Use Each**:
- **Skill**: Reusable workflow with templates/scripts (e.g., "create-crud-entity", "generating-fractal-docs")
- **Command**: Simple prompt with no resources (e.g., "/feature", "/commit")
- **ADW**: Multi-step orchestration with branching logic (e.g., SDLC workflow, patch workflow)

### Key Characteristics

1. **Progressive Disclosure**: Load metadata → instructions → resources (only as needed)
2. **Self-Contained**: All dependencies bundled in skill directory
3. **Discoverable**: Triggered by name, keywords, or patterns in user requests
4. **Composable**: Skills can invoke other skills
5. **Resource-Rich**: Can bundle templates, scripts, documentation
6. **Efficient**: Optimize context window through staged loading

---

## Progressive Disclosure Model

### Philosophy

Progressive disclosure is the cornerstone of the skill pattern. Instead of loading all information upfront, skills reveal information in stages based on agent needs.

**Benefits**:
- **Context Window Efficiency**: Load only what's needed for current task
- **Faster Discovery**: Scan metadata without loading full instructions
- **Scalability**: Support hundreds of skills without context bloat
- **Flexibility**: Agents load resources on-demand

### The Three Levels

#### Level 1: Metadata (Always Loaded)

**What**: YAML frontmatter in SKILL.md
**When**: During skill discovery and listing
**Size**: ~50-150 tokens

**Contains**:
- `name`: kebab-case identifier (e.g., `create-crud-entity`)
- `description`: One-line trigger description (50-100 chars)
- Optional: `allowed-tools`, custom fields

**Example**:
```yaml
---
name: create-crud-entity
description: Generate complete CRUD entities following vertical slice architecture. Use when creating new business entities, domain models, or API endpoints. Triggers on requests like "create entity", "add CRUD for", "new domain model", or "generate API for".
---
```

**Purpose**: Enable fast skill discovery without loading full content. Agents scan metadata to find relevant skills.

**Token Usage**: ~50-150 tokens per skill (scannable across 100+ skills)

---

#### Level 2: Instructions (Loaded When Triggered)

**What**: Main body of SKILL.md
**When**: When skill is explicitly triggered or matched
**Size**: ~500-2000 tokens (target <500 lines)

**Contains**:
- Quick Start / Purpose
- When to Use
- Workflow / Instructions
- Architecture Overview
- References to Level 3 resources

**Example**:
```markdown
# Create CRUD Entity

Generate complete CRUD entities following **vertical slice architecture** with FastAPI, SQLAlchemy, and Pydantic.

## Quick Start

1. **Check shared infrastructure**: If `src/shared/` doesn't exist, create it first using templates in [shared/](shared/)
2. **Gather entity info**: Name, fields, business capability name
3. **Decide authorization**: Does entity need access control? (See [WORKFLOW.md](WORKFLOW.md))
4. **Generate vertical slice**: Create all files using templates in [templates/](templates/)
5. **Register router**: Add to `src/main.py`

For detailed steps, see [WORKFLOW.md](WORKFLOW.md).
```

**Purpose**: Provide enough information for agent to execute skill WITHOUT loading all resources.

**Token Usage**: ~500-2000 tokens when skill is selected (focused context for execution)

---

#### Level 3: Resources (Loaded As Needed)

**What**: Linked files in skill directory
**When**: Only when agent needs specific template, script, or detailed docs
**Size**: Variable (can be MB of templates/scripts)

**Contains**:
- Templates (`.md`, `.j2`, code files)
- Scripts (`.sh`, `.py`, executable tools)
- Documentation (`WORKFLOW.md`, `README.md`, reference docs)
- Supporting files (configs, examples)

**Directory Structure**:
```
ai_docs/doc/create-crud-entity/
├── SKILL.md                      # Level 2: Instructions
├── templates/                    # Level 3: Templates
│   ├── domain_entity.py.md
│   ├── schemas.py.md
│   ├── service.py.md
│   └── routes.py.md
├── shared/                       # Level 3: Shared infrastructure
│   ├── base_entity.py.md
│   ├── base_repository.py.md
│   └── database.py.md
└── WORKFLOW.md                   # Level 3: Detailed workflow
```

**Purpose**: Keep bulk resources out of initial context. Load only specific templates/scripts agent needs.

**Token Usage**: 0 tokens initially, load specific files on-demand (5K-50K tokens per resource)

---

### Progressive Disclosure in Action

**Scenario**: User says "Create a Product entity with CRUD endpoints"

**Stage 1 - Discovery** (Level 1 only):
```
Agent scans metadata of all skills
→ Finds: "create-crud-entity" description matches "CRUD entities"
→ Decision: Load this skill
→ Tokens: ~100 (just metadata)
```

**Stage 2 - Planning** (Level 2 loaded):
```
Agent reads SKILL.md main body
→ Understands workflow: check shared → gather info → generate vertical slice
→ Identifies needed resources: templates/domain_entity.py.md, templates/routes.py.md
→ Tokens: ~100 (metadata) + ~1500 (instructions) = ~1600
```

**Stage 3 - Execution** (Level 3 as needed):
```
Agent loads specific templates one-by-one:
→ Read templates/domain_entity.py.md (~500 tokens)
→ Generate domain/product.py
→ Read templates/routes.py.md (~800 tokens)
→ Generate api/routes.py
→ Total: ~1600 + ~1300 = ~2900 tokens (not ~50K if all resources loaded upfront)
```

**Result**: 94% token savings vs loading all resources upfront.

---

### Context Window Optimization

**Without Progressive Disclosure** (anti-pattern):
```
Load all 50 skills entirely = 50 skills × 10K tokens = 500K tokens
→ Context overflow, agent can't load any actual work
```

**With Progressive Disclosure** (skill pattern):
```
Level 1 (discovery): 50 skills × 100 tokens = 5K tokens
Level 2 (selected skill): 1 skill × 1.5K tokens = 1.5K tokens
Level 3 (resources): 3 templates × 500 tokens = 1.5K tokens
→ Total: 8K tokens (98% savings)
```

**The 5/15/80 Rule**:
- 5% of context: Level 1 metadata (all skills)
- 15% of context: Level 2 instructions (selected skill)
- 80% of context: Actual work (code, analysis, generation)

---

## SKILL.md Structure

### YAML Frontmatter Schema

Every SKILL.md starts with YAML frontmatter delimited by `---`.

#### Required Fields

```yaml
---
name: string                      # kebab-case identifier (e.g., "processing-pdfs")
description: string               # One-line trigger description (50-100 chars, keyword-rich)
---
```

**Field Specifications**:

| Field | Type | Format | Purpose |
|-------|------|--------|---------|
| `name` | string | kebab-case, gerund form | Unique skill identifier for discovery |
| `description` | string | 50-100 chars, trigger-rich | Help agents match user requests to skills |

**Naming Convention** (gerund form):
- ✅ `creating-api-endpoints`
- ✅ `processing-pdfs`
- ✅ `generating-fractal-docs`
- ❌ `api-endpoints` (not a verb)
- ❌ `create-api` (imperative, not gerund)
- ❌ `pdf-processor` (noun, not gerund)

**Description Best Practices**:
- Include trigger keywords: "Use when...", "Triggers on..."
- List common request patterns: "create entity", "add CRUD", "new domain model"
- Be specific about what skill does
- Keep under 100 characters for scannability

---

#### Optional Fields

```yaml
---
name: generating-fractal-docs
description: Run deterministic documentation generators (docstrings/JSDoc → fractal docs) bundled with this skill. Use to bootstrap or refresh repo documentation safely.
allowed-tools: Read, Grep, Glob, Bash(python:*)      # OPTIONAL: Restrict tools agent can use
auto-trigger: ["generate docs", "create documentation"]  # OPTIONAL: Keyword triggers
category: documentation           # OPTIONAL: Group skills by category
---
```

**Optional Field Reference**:

| Field | Type | Purpose | Example |
|-------|------|---------|---------|
| `allowed-tools` | string | Restrict agent tool usage | `Read, Grep, Glob, Bash(python:*)` |
| `auto-trigger` | list[string] | Automatic skill invocation keywords | `["generate docs", "fractal"]` |
| `category` | string | Group skills for organization | `documentation`, `code-generation` |
| `version` | string | Track skill evolution | `1.0`, `2.1.3` |
| `author` | string | Skill creator (human or agent) | `TAC-13 Agent`, `developer-name` |

**allowed-tools Format**:
- Comma-separated list of tool names
- Use `*` for wildcards: `Bash(python:*)` allows `python script.py` but not `rm -rf`
- Use tool categories: `Read, Write, Edit` (file operations only)

---

### Standard Markdown Sections

After frontmatter, SKILL.md body follows a standard structure.

#### Section 1: Title and Purpose

```markdown
# Skill Name

One-paragraph description of what this skill does and why it exists.

## Quick Start / Purpose

3-7 step overview of workflow:
1. **Step 1**: Brief description
2. **Step 2**: Brief description
3. **Step 3**: Brief description
```

**Guidelines**:
- Title matches `name` field (but in Title Case)
- Purpose paragraph: 2-3 sentences max
- Quick Start: High-level steps only (details in Level 3 resources)

---

#### Section 2: When to Use

```markdown
## When to Use

Use this skill when:
- Scenario 1 (be specific)
- Scenario 2 (provide context)
- Scenario 3 (include examples)

Do NOT use this skill when:
- Anti-pattern 1
- Anti-pattern 2
```

**Purpose**: Help agents decide if this skill is appropriate for current task.

**Guidelines**:
- Be explicit about use cases
- Include negative cases (when NOT to use)
- Provide concrete examples

---

#### Section 3: Instructions / Workflow

```markdown
## Instructions

### Preconditions
- Requirement 1 (verify before proceeding)
- Requirement 2 (stop if missing)

### Workflow
1) **Phase 1**: Description
   - Substep detail
   - Substep detail
2) **Phase 2**: Description
3) **Phase 3**: Description

### Primary Command
\```bash
bash .claude/skills/skill-name/scripts/main.sh
\```
```

**Guidelines**:
- Include precondition checks
- Break workflow into phases
- Reference Level 3 resources (scripts, templates) rather than inlining
- Provide command examples

---

#### Section 4: Resources / Templates (Optional)

```markdown
## Templates Reference

### Entity Templates (Basic)
- [domain_entity.py.md](templates/domain_entity.py.md) - Domain model
- [schemas.py.md](templates/schemas.py.md) - Request/response DTOs
- [service.py.md](templates/service.py.md) - Application service

### Entity Templates (Authorized)
- [routes_authorized.py.md](templates/routes_authorized.py.md) - Routes with permissions
- [service_authorized.py.md](templates/service_authorized.py.md) - Service with auth
```

**Purpose**: Catalog Level 3 resources with brief descriptions.

**Guidelines**:
- Use relative links from SKILL.md location
- Group resources by category
- Include one-line description per resource
- Don't inline template content (keep SKILL.md under 500 lines)

---

#### Section 5: Best Practices (Optional)

```markdown
## Best Practices

1. **Naming**: Use business language for capability names (e.g., `product_catalog`, not `products`)
2. **Fields**: Keep domain models focused; split large entities into value objects
3. **Validation**: Put business rules in domain layer, input validation in schemas
4. **Testing**: Create tests alongside each capability
```

**Purpose**: Domain-specific guidelines for using skill effectively.

---

### Complete SKILL.md Annotated Example

```yaml
---
name: create-crud-entity
description: Generate complete CRUD entities following vertical slice architecture. Use when creating new business entities, domain models, or API endpoints. Triggers on requests like "create entity", "add CRUD for", "new domain model".
allowed-tools: Read, Write, Edit, Grep, Glob
category: code-generation
version: 1.0
---

# Create CRUD Entity

Generate complete CRUD entities following **vertical slice architecture** with FastAPI, SQLAlchemy, and Pydantic.

## Quick Start

1. **Check shared infrastructure**: If `src/shared/` doesn't exist, create it first using templates in [shared/](shared/)
2. **Gather entity info**: Name, fields, business capability name
3. **Decide authorization**: Does entity need access control? (See [WORKFLOW.md](WORKFLOW.md))
4. **Generate vertical slice**: Create all files using templates in [templates/](templates/)
5. **Register router**: Add to `src/main.py`

For detailed steps, see [WORKFLOW.md](WORKFLOW.md).

## When to Use

Use this skill when:
- Creating new business entities (User, Product, Order)
- Building CRUD APIs following DDD patterns
- Scaffolding vertical slices (domain → application → infrastructure → api)

Do NOT use this skill when:
- Adding single endpoint to existing entity (use manual editing)
- Non-CRUD operations (use custom implementation)
- Simple data models without business logic (use ORM directly)

## Template Variants

| Variant | Use Case |
|---------|----------|
| **Basic** | Public data, no restrictions |
| **Authorized** | Row/column/action level access control |
| **Async** | High concurrency, async/await patterns |

## Architecture Overview

Each entity lives in its own **business capability** directory:

\```
src/
├── {capability_name}/           # e.g., product_catalog, user_management
│   ├── domain/
│   │   └── {entity}.py         # Domain model (extends Entity)
│   ├── application/
│   │   ├── schemas.py          # DTOs: Create, Update, Response
│   │   └── service.py          # Business logic orchestration
│   ├── infrastructure/
│   │   ├── models.py           # SQLAlchemy ORM model
│   │   └── repository.py       # Data access layer
│   └── api/
│       └── routes.py           # FastAPI CRUD endpoints
\```

## Templates Reference

### Entity Templates (Basic)
- [domain_entity.py.md](templates/domain_entity.py.md) - Domain model
- [schemas.py.md](templates/schemas.py.md) - Request/response DTOs (uses BaseSchema)
- [service.py.md](templates/service.py.md) - Application service (uses BaseService)
- [orm_model.py.md](templates/orm_model.py.md) - SQLAlchemy model
- [repository.py.md](templates/repository.py.md) - Data access
- [routes.py.md](templates/routes.py.md) - API endpoints

### Shared Infrastructure
- [base_entity.py.md](shared/base_entity.py.md) - Entity base class with audit fields
- [base_schema.py.md](shared/base_schema.py.md) - Schema base classes
- [base_service.py.md](shared/base_service.py.md) - Service base class with CRUD operations
- [base_repository.py.md](shared/base_repository.py.md) - Generic sync CRUD repository

## Best Practices

1. **Naming**: Use business language for capability names (e.g., `product_catalog`, not `products`)
2. **Fields**: Keep domain models focused; split large entities into value objects
3. **Validation**: Put business rules in domain layer, input validation in schemas
4. **Cross-capability**: Use repository interfaces for cross-slice references
5. **State management**: Use `state` field for soft deletes (0=inactive, 1=active, 2=deleted)
6. **Audit trail**: Always pass `user_id` to service methods for tracking
```

---

## Discovery Mechanism

### How Skills Are Discovered

Skills are discovered through a multi-level search process:

1. **Project-Level Skills** (repo-specific)
2. **Personal-Level Skills** (user-specific across all projects)

#### Project-Level Discovery

**Location**: `ai_docs/doc/*/SKILL.md` or `.claude/skills/*/SKILL.md` (project root)

**Purpose**: Project-specific workflows (e.g., "create-crud-entity" for FastAPI projects)

**Discovery Process**:
```
1. Agent scans project directories for SKILL.md files
2. Parses YAML frontmatter to extract name + description
3. Builds skill registry: {name: {path, description, metadata}}
4. When user request comes in, match keywords from description
```

**Example**:
```
User: "Create a Product entity with CRUD endpoints"
→ Agent scans ai_docs/doc/*/SKILL.md
→ Finds: "create-crud-entity" with description containing "CRUD entities"
→ Loads: ai_docs/doc/create-crud-entity/SKILL.md
```

---

#### Personal-Level Discovery

**Location**: `~/.claude/skills/*/SKILL.md` (user home directory)

**Purpose**: User-specific skills across all projects (e.g., "processing-pdfs" for any project)

**Discovery Process**:
```
1. Agent scans ~/.claude/skills/ for SKILL.md files
2. Merges personal skills with project-level skills
3. Priority: Project-level overrides personal-level (same name)
```

**Use Cases**:
- Generic utilities (PDF processing, image optimization)
- Personal workflows (code review checklist, commit message templates)
- Cross-project patterns (API testing, deployment scripts)

---

### Trigger Patterns

Skills can be triggered by:

1. **Explicit Name**: User says "/create-crud-entity" or "use create-crud-entity"
2. **Keyword Matching**: Description contains keywords from user request
3. **Auto-Trigger**: Frontmatter `auto-trigger` field matches user text
4. **Fuzzy Matching**: Agent infers skill from context

**Keyword Matching Example**:
```yaml
---
name: generating-fractal-docs
description: Run deterministic documentation generators (docstrings/JSDoc → fractal docs) bundled with this skill. Use to bootstrap or refresh repo documentation safely.
---
```

**Triggers**:
- "generate docs" → matches "documentation generators"
- "create fractal documentation" → matches "fractal docs"
- "bootstrap documentation" → matches "bootstrap... documentation"

**Auto-Trigger Example**:
```yaml
---
name: processing-pdfs
description: Extract text, images, and metadata from PDF files
auto-trigger: ["process pdf", "extract from pdf", "parse pdf"]
---
```

**Triggers**:
- "process pdf invoice.pdf" → exact match in auto-trigger
- "extract data from pdf" → fuzzy match in auto-trigger

---

### Skill Name Resolution

When multiple skills match, agent uses priority:

1. **Exact name match** (highest priority)
2. **Auto-trigger exact match**
3. **Keyword match in description** (scored by relevance)
4. **Fuzzy match** (lowest priority)

**Conflict Resolution**:
- Project-level skill overrides personal-level (same name)
- Agent asks user to disambiguate if multiple high-scoring matches

**Example**:
```
User: "Create API documentation"

Matches:
- "generating-fractal-docs" (score: 0.8, keyword: "documentation")
- "create-crud-entity" (score: 0.4, keyword: "create")
- "processing-api-specs" (score: 0.7, keyword: "API")

→ Agent selects "generating-fractal-docs" (highest score)
```

---

### Discovery Algorithm (Simplified)

```python
def discover_skills() -> dict[str, Skill]:
    """Scan project and personal directories for skills"""
    skills = {}

    # 1. Load personal-level skills
    for skill_path in glob("~/.claude/skills/*/SKILL.md"):
        skill = parse_skill(skill_path)
        skills[skill.name] = skill

    # 2. Load project-level skills (override personal)
    for skill_path in glob("ai_docs/doc/*/SKILL.md"):
        skill = parse_skill(skill_path)
        skills[skill.name] = skill  # Overwrites personal if same name

    return skills

def match_skill(user_request: str, skills: dict) -> Skill:
    """Match user request to best skill"""
    scores = {}

    for name, skill in skills.items():
        # Exact name match
        if name in user_request.lower():
            return skill

        # Auto-trigger match
        if skill.auto_trigger:
            for trigger in skill.auto_trigger:
                if trigger in user_request.lower():
                    return skill

        # Keyword scoring
        score = keyword_similarity(user_request, skill.description)
        scores[name] = score

    # Return highest scoring skill
    best_skill = max(scores, key=scores.get)
    if scores[best_skill] > 0.5:  # Threshold
        return skills[best_skill]

    return None  # No good match
```

---

## Creation Workflow

### Step-by-Step Guide for Creating New Skills

#### Step 1: Identify Skill Purpose and Scope

**Questions to Answer**:
- What specific problem does this skill solve?
- Is this a reusable workflow or one-off task?
- Does it need templates, scripts, or documentation?
- Is this project-specific or personal-use?

**Decision Matrix**:

| If... | Then Create... |
|-------|----------------|
| Single prompt, no resources | Command (not a skill) |
| Reusable workflow + templates | Skill |
| Complex multi-step automation | ADW (not a skill) |
| Generic utility (any project) | Personal-level skill |
| Project-specific pattern | Project-level skill |

**Example**:
```
Problem: Need to generate CRUD entities following DDD patterns
→ Reusable workflow: ✅
→ Needs templates: ✅ (domain, service, repository, routes)
→ Project-specific: ✅ (FastAPI + SQLAlchemy specific)
→ Decision: Create project-level skill "create-crud-entity"
```

---

#### Step 2: Choose Skill Name (Gerund Form)

**Naming Rules**:
1. Use gerund form (-ing): `creating-X`, `processing-Y`, `generating-Z`
2. Use kebab-case: `create-crud-entity` not `CreateCRUDEntity`
3. Be descriptive but concise: 2-4 words
4. Use verbs that match user intent

**Good Names**:
- `creating-api-endpoints` (gerund, clear intent)
- `processing-pdfs` (gerund, specific)
- `generating-fractal-docs` (gerund, unique)

**Bad Names**:
- `api` (not a verb, too vague)
- `create-api` (imperative, not gerund)
- `pdf-processor` (noun, not verb)
- `the-thing-that-creates-apis` (too long)

**Validation**:
```bash
# Check if name already exists
grep -r "name: your-skill-name" ai_docs/doc/*/SKILL.md ~/.claude/skills/*/SKILL.md
```

---

#### Step 3: Write Frontmatter

**Template**:
```yaml
---
name: your-skill-name
description: One-line description (50-100 chars) with trigger keywords. Use when [scenario]. Triggers on [patterns].
allowed-tools: Read, Write, Edit, Bash(python:*)  # OPTIONAL
category: code-generation                          # OPTIONAL
---
```

**Description Formula**:
```
[What it does] + [When to use] + [Trigger keywords]

Example:
"Generate CRUD entities following vertical slice architecture. Use when creating new business entities or API endpoints. Triggers on 'create entity', 'add CRUD', 'new domain model'."
```

**Keywords to Include**:
- Action verbs: "generate", "create", "process", "analyze"
- Domain terms: "CRUD", "entity", "API", "documentation"
- Trigger phrases: "Use when...", "Triggers on..."

---

#### Step 4: Structure Main Sections

**Required Sections** (in SKILL.md body):
1. Title + Purpose (1 paragraph)
2. Quick Start (3-7 steps)
3. When to Use (use cases + anti-patterns)
4. Instructions / Workflow

**Optional Sections**:
5. Templates Reference (if Level 3 resources exist)
6. Best Practices
7. Examples
8. Troubleshooting

**Size Target**: 300-500 lines for main SKILL.md

**Template**:
```markdown
# Your Skill Name

One-paragraph description of what this skill does and its value proposition.

## Quick Start

1. **Step 1**: Brief description
2. **Step 2**: Brief description
3. **Step 3**: Brief description

See [WORKFLOW.md](WORKFLOW.md) for detailed steps.

## When to Use

Use this skill when:
- Scenario 1
- Scenario 2

Do NOT use when:
- Anti-pattern 1
- Anti-pattern 2

## Instructions

### Preconditions
- Verify requirement 1
- Check requirement 2

### Workflow
1) Phase 1: Description
2) Phase 2: Description
3) Phase 3: Description

## Templates Reference

- [template1.md](templates/template1.md) - Description
- [template2.md](templates/template2.md) - Description

## Best Practices

1. Guideline 1
2. Guideline 2
```

---

#### Step 5: Create Linked Resources (If Needed)

**Directory Structure** (for skill with resources):
```
ai_docs/doc/your-skill-name/
├── SKILL.md                      # Main entry point
├── WORKFLOW.md                   # Detailed workflow (optional)
├── templates/                    # Code templates
│   ├── template1.py.md
│   ├── template2.py.md
│   └── template3.py.md
├── scripts/                      # Executable scripts
│   ├── main.sh
│   └── helper.py
└── docs/                         # Additional documentation
    ├── architecture.md
    └── examples.md
```

**Resource Organization**:
- `templates/`: Code generation templates (Jinja2, markdown, or plain files)
- `scripts/`: Executable automation (shell scripts, Python)
- `docs/`: Supplementary documentation (not loaded unless referenced)

**Linking from SKILL.md**:
```markdown
## Templates Reference

- [Domain Entity](templates/domain_entity.py.md) - Core business model
- [API Routes](templates/routes.py.md) - FastAPI CRUD endpoints

## Scripts

Run the main generator:
\```bash
bash scripts/generate_entity.sh <entity_name>
\```
```

**Best Practice**: Reference resources by relative path, don't inline content.

---

#### Step 6: Validate Size (<500 Lines for SKILL.md)

**Size Constraints**:
- SKILL.md main file: **<500 lines** (hard limit)
- Templates: No limit (loaded on-demand)
- Scripts: No limit (executed, not loaded as text)
- Total skill directory: No limit

**Check Line Count**:
```bash
wc -l ai_docs/doc/your-skill-name/SKILL.md

# Output should be < 500
```

**If Over Limit**:
1. Move detailed workflows to separate `WORKFLOW.md`
2. Extract examples to `docs/examples.md`
3. Move large code blocks to `templates/`
4. Compress verbose descriptions

**Anti-Pattern** (too large):
```markdown
## Template: Domain Entity

\```python
# 200 lines of template code inlined here...
\```
```

**Correct Pattern**:
```markdown
## Templates Reference

- [domain_entity.py.md](templates/domain_entity.py.md) - Domain model template
```

---

#### Step 7: Test Discovery and Triggering

**Manual Testing**:
```bash
# 1. Test YAML validity
python -c "import yaml; print(yaml.safe_load(open('ai_docs/doc/your-skill-name/SKILL.md').read().split('---')[1]))"

# 2. Test file structure
tree ai_docs/doc/your-skill-name/

# 3. Test line count
wc -l ai_docs/doc/your-skill-name/SKILL.md
```

**Functional Testing** (with agent):
```
1. Start new agent session
2. Use trigger keywords: "I want to [skill purpose]"
3. Verify agent discovers and loads skill
4. Execute workflow
5. Validate outputs
```

**Example**:
```
User: "Create a Product entity with CRUD"
→ Agent should discover "create-crud-entity"
→ Agent should load SKILL.md
→ Agent should reference templates and execute
```

---

### Creation Checklist

Use this checklist when creating a new skill:

- [ ] Purpose identified (not better suited for command or ADW)
- [ ] Name chosen (gerund form, kebab-case, 2-4 words)
- [ ] YAML frontmatter written (name + description required)
- [ ] Description includes trigger keywords
- [ ] Quick Start section (3-7 steps)
- [ ] When to Use section (use cases + anti-patterns)
- [ ] Instructions section (preconditions + workflow)
- [ ] Templates created in `templates/` directory (if needed)
- [ ] Scripts created in `scripts/` directory (if needed)
- [ ] Resources linked from SKILL.md (not inlined)
- [ ] SKILL.md under 500 lines
- [ ] YAML frontmatter valid (test with Python)
- [ ] Skill discoverable (test with keywords)
- [ ] Workflow executable (test end-to-end)

---

## Concrete Examples

### Example 1: create-crud-entity (Complex Skill with Templates)

**Location**: `ai_docs/doc/create-crud-entity/SKILL.md`

**Complexity**: High (12+ templates, shared infrastructure)

**Frontmatter Analysis**:
```yaml
---
name: create-crud-entity
description: Generate complete CRUD entities following vertical slice architecture. Use when creating new business entities, domain models, or API endpoints. Triggers on requests like "create entity", "add CRUD for", "new domain model", or "generate API for".
---
```

**What Makes This a Good Skill**:
1. **Clear Name**: `create-crud-entity` (gerund form, describes action)
2. **Rich Description**:
   - What: "Generate complete CRUD entities"
   - How: "following vertical slice architecture"
   - When: "Use when creating new business entities"
   - Triggers: "create entity", "add CRUD", "new domain model"
3. **Progressive Disclosure**:
   - Level 1: Frontmatter (100 tokens)
   - Level 2: SKILL.md main body (1500 tokens, 151 lines)
   - Level 3: 12+ templates (50K+ tokens, loaded on-demand)
4. **Resource Organization**:
   ```
   create-crud-entity/
   ├── SKILL.md (151 lines)
   ├── templates/ (12 templates)
   │   ├── domain_entity.py.md
   │   ├── schemas.py.md
   │   ├── service.py.md
   │   └── routes.py.md
   └── shared/ (9 shared infrastructure templates)
       ├── base_entity.py.md
       ├── base_repository.py.md
       └── database.py.md
   ```
5. **Well-Structured SKILL.md**:
   - Quick Start (5 steps)
   - Template Variants table
   - Architecture diagram
   - Templates Reference (grouped by variant)
   - Best Practices (8 guidelines)

**Progressive Disclosure In Practice**:

**Discovery Phase** (Level 1 only):
```
User: "Add a User entity with CRUD endpoints"
→ Agent scans 50+ skill descriptions
→ Matches: "create-crud-entity" (contains "CRUD entities")
→ Loaded: ~100 tokens (just frontmatter)
```

**Planning Phase** (Level 2 loaded):
```
→ Agent reads SKILL.md body (151 lines)
→ Understands: vertical slice architecture, need shared infrastructure
→ Identifies: templates/domain_entity.py.md, templates/routes.py.md needed
→ Total: ~100 (L1) + ~1500 (L2) = ~1600 tokens
```

**Execution Phase** (Level 3 as needed):
```
→ Agent reads templates/domain_entity.py.md (~500 tokens)
→ Generates: src/user_management/domain/user.py
→ Agent reads templates/schemas.py.md (~400 tokens)
→ Generates: src/user_management/application/schemas.py
→ Agent reads templates/routes.py.md (~800 tokens)
→ Generates: src/user_management/api/routes.py
→ Total: ~1600 + ~1700 = ~3300 tokens (vs ~50K if all templates loaded upfront)
```

**Result**: 93% token savings through progressive disclosure.

---

### Example 2: generating-fractal-docs (Nested Skill with Scripts)

**Location**: `ai_docs/doc/create-crud-entity/generating-fractal-docs/SKILL.md`

**Complexity**: Medium (2 scripts bundled, deterministic workflow)

**Frontmatter Analysis**:
```yaml
---
name: generating-fractal-docs
description: Run deterministic documentation generators (docstrings/JSDoc → fractal docs) bundled with this skill. Use to bootstrap or refresh repo documentation safely.
allowed-tools: Read, Grep, Glob, Bash(python:*)
---
```

**What Makes This a Good Skill**:
1. **Restricted Tools**: `allowed-tools: Read, Grep, Glob, Bash(python:*)` prevents destructive operations
2. **Bundled Scripts**: Scripts included in skill directory for deterministic execution
3. **Nested Location**: Skill lives inside another skill (`create-crud-entity/generating-fractal-docs/`)
4. **Clear Preconditions**: Lists requirements before execution
5. **Primary Command**: Single entrypoint (`bash scripts/run_generators.sh`)

**Directory Structure**:
```
generating-fractal-docs/
├── SKILL.md (36 lines - very concise)
└── scripts/
    ├── run_generators.sh
    ├── gen_docstring_jsdocs.py
    └── gen_docs_fractal.py
```

**SKILL.md Highlights**:
```markdown
# Generating Fractal Docs (Docstrings → Fractal Docs)

## What this skill does
Runs **two deterministic generators**, bundled inside this skill, in the correct order:

1) `scripts/gen_docstring_jsdocs.py`
2) `scripts/gen_docs_fractal.py`

## Preconditions (must verify)
1) You are in the **repository root**
2) Python 3 is available
3) Repo is in a **clean or reviewable git state** (recommended)

If any precondition fails, stop and explain precisely.

## Default workflow
1) Preflight checks (paths, python, git)
2) Run docstring/JSDoc generator
3) Run fractal docs generator
4) Validate outputs
5) Summarize changes (no large diffs inline)

## Primary command
\```bash
bash .claude/skills/generating-fractal-docs/scripts/run_generators.sh
\```
```

**Key Patterns**:
1. **Conciseness**: Only 36 lines (well under 500-line limit)
2. **Deterministic**: Scripts bundled, reproducible execution
3. **Safety**: Precondition checks prevent errors
4. **Workflow**: Clear 5-step process
5. **Tool Restriction**: `allowed-tools` prevents unsafe operations

**Progressive Disclosure**:
- **Level 1**: Frontmatter (~80 tokens) - "documentation generators"
- **Level 2**: SKILL.md body (~300 tokens) - workflow + preconditions
- **Level 3**: Scripts (~5K tokens) - only loaded if agent inspects them

---

### Example 3: processing-pdfs (Hypothetical Personal Skill)

**Location**: `~/.claude/skills/processing-pdfs/SKILL.md`

**Complexity**: Low (utility skill for personal use)

**Hypothetical Frontmatter**:
```yaml
---
name: processing-pdfs
description: Extract text, images, and metadata from PDF files using PyPDF2 and pdfplumber. Use for invoice parsing, document analysis, or text extraction. Triggers on "process pdf", "extract from pdf", "parse pdf".
allowed-tools: Read, Bash(python:*)
category: utilities
auto-trigger: ["process pdf", "extract pdf", "parse pdf"]
---
```

**Hypothetical SKILL.md**:
```markdown
# Processing PDFs

Extract structured data from PDF files using Python libraries.

## Quick Start

1. **Install dependencies**: `pip install pypdf2 pdfplumber pillow`
2. **Run extractor**: `python scripts/extract_pdf.py <file.pdf>`
3. **Review output**: JSON file with text, images, metadata

## When to Use

Use this skill when:
- Parsing invoices, receipts, or forms
- Extracting text from scanned documents
- Analyzing PDF structure (metadata, fonts, images)

Do NOT use when:
- PDF is encrypted (use decryption first)
- Need OCR for scanned images (use tesseract skill instead)

## Instructions

### Preconditions
- Python 3.7+ installed
- PDF file is readable (not password-protected)

### Workflow
1) **Analyze PDF structure**: Determine if text-based or image-based
2) **Extract text**: Use pdfplumber for text extraction
3) **Extract images**: Use PyPDF2 for embedded images
4) **Extract metadata**: Author, creation date, page count
5) **Output JSON**: Structured data in `<filename>_extracted.json`

### Primary Command
\```bash
python ~/.claude/skills/processing-pdfs/scripts/extract_pdf.py invoice.pdf
\```

## Output Format

\```json
{
  "filename": "invoice.pdf",
  "pages": 3,
  "text": "Full extracted text...",
  "images": ["image1.png", "image2.png"],
  "metadata": {
    "author": "Company Name",
    "created": "2026-01-15",
    "title": "Invoice #12345"
  }
}
\```

## Best Practices

1. **Validation**: Check PDF is readable before processing
2. **Large files**: Process page-by-page to avoid memory issues
3. **OCR**: If text extraction fails, use tesseract for image-based PDFs
```

**What Makes This a Good Personal Skill**:
1. **Generic Utility**: Works across any project (not project-specific)
2. **Auto-Trigger**: Automatically invoked when user says "process pdf invoice.pdf"
3. **Tool Restriction**: Only allows Python scripts (safe for automation)
4. **Output Format**: Clear structure for downstream processing
5. **Personal Location**: `~/.claude/skills/` makes it available everywhere

---

### Example 4: start-orchestrator (Hypothetical Meta-Skill)

**Concept**: Skill that orchestrates other skills (meta-level)

**Hypothetical Frontmatter**:
```yaml
---
name: start-orchestrator
description: Orchestrate complex workflows by chaining multiple skills (plan → build → test → improve). Use for end-to-end feature development. Triggers on "implement feature", "full workflow", "end-to-end".
category: orchestration
allowed-tools: Read, Write, Edit, Bash, Task
---
```

**Hypothetical SKILL.md**:
```markdown
# Start Orchestrator

Chain multiple skills for end-to-end feature development.

## Quick Start

1. **Plan**: Use `/feature` to create implementation plan
2. **Scout**: Use `scout` skill to explore codebase
3. **Build**: Use relevant build skills (e.g., `create-crud-entity`)
4. **Test**: Use `/test` to validate implementation
5. **Improve**: Use expert `self-improve` to update knowledge

## Workflow

### Phase 1: Planning
- Trigger: `/feature <description>`
- Output: Plan file in `specs/`

### Phase 2: Exploration
- Trigger: `scout "<relevant files>"`
- Output: Context bundle with relevant files

### Phase 3: Implementation
- Trigger: Appropriate build skill based on plan
- Output: Generated code

### Phase 4: Validation
- Trigger: `/test`
- Output: Test results

### Phase 5: Learning
- Trigger: Expert `self-improve`
- Output: Updated expertise.yaml

## Example

User: "Implement a Product entity with CRUD endpoints"

Orchestrator executes:
1) `/feature "Product entity CRUD"` → creates plan
2) `scout "entity, repository, routes"` → finds relevant patterns
3) `create-crud-entity` → generates files
4) `/test` → validates implementation
5) `experts/adw/self-improve` → updates ADW expertise
```

**Meta-Pattern**:
- Skill invokes other skills (composability)
- Orchestrates complex workflows
- Bridges planning, implementation, testing, learning

---

## Best Practices

### 1. Size Limit: SKILL.md <500 Lines

**Rationale**: Context window efficiency. SKILL.md is Level 2 (loaded when triggered). Large files bloat context unnecessarily.

**Enforcement**:
```bash
# Check line count
wc -l ai_docs/doc/your-skill-name/SKILL.md

# Must be < 500
```

**Strategies to Stay Under Limit**:

1. **Extract Detailed Workflows**:
   ```markdown
   ## Quick Start

   1. Check prerequisites
   2. Run generator
   3. Validate output

   For detailed steps, see [WORKFLOW.md](WORKFLOW.md).
   ```

2. **Link to Templates, Don't Inline**:
   ```markdown
   ## Templates

   - [domain_entity.py.md](templates/domain_entity.py.md) - Domain model

   <!-- DON'T inline 200 lines of template code -->
   ```

3. **Compress Descriptions**:
   ```markdown
   <!-- BAD: Verbose -->
   This template generates a domain entity class that extends the base Entity class and includes all necessary fields, methods, and validation logic for proper operation within the vertical slice architecture pattern.

   <!-- GOOD: Concise -->
   Generates domain entity extending base Entity class with fields and validation.
   ```

4. **Use Tables for Comparisons**:
   ```markdown
   ## Template Variants

   | Variant | Use Case |
   |---------|----------|
   | Basic | Public data, no restrictions |
   | Authorized | Row/column/action level access control |
   ```

5. **Move Examples to Separate File**:
   ```markdown
   See [docs/examples.md](docs/examples.md) for usage examples.
   ```

**If Approaching 500 Lines**: Audit SKILL.md and aggressively extract to Level 3 resources.

---

### 2. Naming: Use Gerund Form (creating-X, processing-Y, generating-Z)

**Rationale**: Gerund form (-ing) represents ongoing capability, matches user intent ("I want to create...", "I need to process...").

**Convention**:
- ✅ `creating-api-endpoints`
- ✅ `processing-pdfs`
- ✅ `generating-fractal-docs`
- ✅ `analyzing-performance`
- ❌ `create-api` (imperative, not gerund)
- ❌ `api-creator` (noun, not verb)
- ❌ `pdf-processor` (noun, not verb)

**Validation**:
```bash
# Skill name should match pattern: *-ing-*
echo "your-skill-name" | grep -E '.*ing.*'
```

**Why This Matters**:
- Consistency across all skills
- Natural language matching: "I want to create API" → "creating-api-endpoints"
- Avoids confusion with commands (imperative) or nouns (things)

---

### 3. Organization: Group Related Resources in Skill Subdirectory

**Pattern**:
```
skill-name/
├── SKILL.md                      # Entry point
├── templates/                    # Templates grouped by type
│   ├── basic/
│   │   └── template1.md
│   └── advanced/
│       └── template2.md
├── scripts/                      # Scripts grouped by purpose
│   ├── generators/
│   │   └── generate.sh
│   └── validators/
│       └── validate.py
└── docs/                         # Supporting documentation
    ├── WORKFLOW.md
    └── examples.md
```

**Benefits**:
- Self-contained (all dependencies in one directory)
- Easy to relocate or share
- Clear resource organization
- Agents can glob `templates/*.md` or `scripts/*.sh`

**Anti-Pattern** (scattered resources):
```
ai_docs/
├── doc/
│   └── skill-name/
│       └── SKILL.md
├── templates/                    # Templates outside skill directory
│   └── template1.md
└── scripts/                      # Scripts outside skill directory
    └── script.sh
```

**Enforcement**: All skill resources MUST be within skill directory.

---

### 4. Frontmatter: Keep Description Concise but Trigger-Rich

**Formula**: What + When + Triggers (50-100 characters)

**Good Descriptions**:
```yaml
description: Generate CRUD entities following vertical slice architecture. Use when creating new business entities or API endpoints. Triggers on "create entity", "add CRUD", "new domain model".
```
- What: "Generate CRUD entities"
- How: "following vertical slice architecture"
- When: "Use when creating new business entities"
- Triggers: "create entity", "add CRUD", "new domain model"

**Bad Descriptions**:
```yaml
# Too vague
description: Creates entities

# Too verbose
description: This skill provides comprehensive functionality for generating complete CRUD (Create, Read, Update, Delete) entities that strictly follow the vertical slice architectural pattern, which is a design approach that organizes code by feature rather than by technical layer...

# No trigger keywords
description: Entity generator tool
```

**Trigger Keyword Strategy**:
- Include action verbs: "generate", "create", "process", "analyze"
- Include domain terms: "CRUD", "entity", "API", "PDF", "documentation"
- Include common request phrases: "Use when...", "Triggers on..."

**Testing**:
```
If user says: "Create a Product entity"
→ Description should contain: "create", "entity", or "CRUD"
```

---

### 5. Linked Resources: Use Relative Paths, Organize by Type

**Relative Path Convention**:
```markdown
<!-- From SKILL.md, reference resources relatively -->
- [Domain Template](templates/domain_entity.py.md)
- [Workflow Guide](WORKFLOW.md)
- [Generator Script](scripts/generate.sh)
```

**Organization by Type**:
```
skill-name/
├── SKILL.md
├── templates/                    # Code generation templates
│   ├── domain_entity.py.md
│   └── routes.py.md
├── scripts/                      # Executable automation
│   ├── generate.sh
│   └── validate.py
└── docs/                         # Documentation
    ├── WORKFLOW.md
    └── architecture.md
```

**Linking Pattern**:
```markdown
## Templates Reference

### Domain Layer
- [domain_entity.py.md](templates/domain_entity.py.md) - Core business model
- [value_objects.py.md](templates/value_objects.py.md) - Immutable value types

### API Layer
- [routes.py.md](templates/routes.py.md) - FastAPI CRUD endpoints

## Documentation

- [WORKFLOW.md](WORKFLOW.md) - Detailed workflow steps
- [ARCHITECTURE.md](docs/architecture.md) - Architectural decisions
```

**Benefits**:
- Relative paths work regardless of project location
- Clear categorization (templates vs scripts vs docs)
- Agents can scan directories: `glob("templates/*.md")`

---

### 6. Testing: Verify Skill Can Be Discovered and Loads Correctly

**Testing Checklist**:

**1. YAML Syntax Validation**:
```bash
# Extract and validate frontmatter
python -c "
import yaml
content = open('ai_docs/doc/skill-name/SKILL.md').read()
frontmatter = content.split('---')[1]
yaml.safe_load(frontmatter)
print('✅ YAML valid')
"
```

**2. Discovery Test**:
```bash
# Verify skill is discoverable
grep -r "name: your-skill-name" ai_docs/doc/*/SKILL.md
# Should return: ai_docs/doc/your-skill-name/SKILL.md
```

**3. Line Count Validation**:
```bash
# Check SKILL.md size
line_count=$(wc -l < ai_docs/doc/your-skill-name/SKILL.md)
if [ $line_count -lt 500 ]; then
  echo "✅ Size OK ($line_count lines)"
else
  echo "❌ Too large ($line_count lines, max 500)"
fi
```

**4. Link Validation**:
```bash
# Check all linked resources exist
cd ai_docs/doc/your-skill-name/
grep -oP '\[.*?\]\(\K[^)]+' SKILL.md | while read link; do
  if [ -f "$link" ] || [ -d "$link" ]; then
    echo "✅ $link exists"
  else
    echo "❌ $link missing"
  fi
done
```

**5. Functional Test** (with agent):
```
1. Start new agent session (clear context)
2. Use trigger phrase: "I want to [skill purpose]"
3. Verify agent discovers skill
4. Verify agent loads SKILL.md
5. Execute workflow
6. Validate outputs match expectations
```

**Example Functional Test**:
```
User: "Generate a Product entity with CRUD endpoints"

Expected behavior:
→ Agent scans skills
→ Agent matches "create-crud-entity"
→ Agent loads SKILL.md
→ Agent identifies needed templates
→ Agent generates domain/product.py, api/routes.py, etc.
→ All files follow vertical slice architecture

Validation:
✅ Files created in correct locations
✅ Files follow template structure
✅ No missing imports or syntax errors
```

---

## Comparison: Skills vs Commands vs ADWs

### Quick Reference Table

| Aspect | Skills | Commands | ADWs |
|--------|--------|----------|------|
| **Purpose** | Reusable workflows with bundled resources | Single-purpose prompts | Complex multi-step orchestration |
| **File Structure** | Directory: SKILL.md + templates + scripts | Single .md file | Python script (.py) |
| **Location** | `ai_docs/doc/*/SKILL.md` or `~/.claude/skills/*/` | `.claude/commands/*.md` | `adws/adw_*_iso.py` |
| **Context Loading** | Progressive (3 levels) | All-at-once | N/A (execution-based) |
| **Resource Bundling** | Yes (templates, scripts, docs) | No (single file) | Can invoke external tools |
| **Composability** | High (skills invoke skills) | Medium (commands can call skills) | High (ADWs invoke ADWs, skills, commands) |
| **Typical Size** | SKILL.md: <500 lines, resources: unlimited | <200 lines | Variable (100-500 lines) |
| **Discovery** | Keyword matching in description | Slash name (`/feature`) | CLI argument (`--issue <num>`) |
| **Execution Model** | Agent-interpreted (markdown workflow) | Agent-interpreted (prompt) | Python execution (automated) |
| **Use Cases** | Code generation, documentation, utilities | Planning, commits, simple workflows | SDLC automation, multi-agent orchestration |

---

### Detailed Comparison

#### Skills

**Strengths**:
- Resource bundling (templates, scripts)
- Progressive disclosure (efficient context usage)
- Personal + project-level discovery
- Composable (skills call skills)

**Weaknesses**:
- Requires directory structure (more overhead)
- Agent-interpreted (slower than Python execution)
- Complexity in organizing resources

**Best For**:
- Code generation workflows (`create-crud-entity`)
- Documentation generation (`generating-fractal-docs`)
- Personal utilities (`processing-pdfs`)
- Workflows with templates/scripts

**Example**: `create-crud-entity` - generates 6+ files from templates following DDD patterns.

---

#### Commands

**Strengths**:
- Simple (single .md file)
- Fast discovery (slash prefix)
- Easy to create and maintain
- No resource overhead

**Weaknesses**:
- No resource bundling
- All-at-once context loading (inefficient for large commands)
- Limited to project-level (no personal commands)

**Best For**:
- Simple prompts (`/feature`, `/commit`)
- Planning workflows (`/plan`)
- Single-step operations (`/review`)

**Example**: `/feature` - creates implementation plan from issue description (single markdown file, no templates).

---

#### ADWs (AI Developer Workflows)

**Strengths**:
- Python execution (fast, deterministic)
- Complex orchestration (branching, loops)
- Integration with external tools (gh, git, pytest)
- Can invoke skills, commands, other ADWs

**Weaknesses**:
- Requires Python knowledge
- CLI execution (not agent-discovered)
- More complex to maintain

**Best For**:
- SDLC automation (`adw_sdlc_iso.py`)
- Multi-step orchestration (plan → build → test → deploy)
- Integration with CI/CD
- Complex branching logic

**Example**: `adw_sdlc_iso.py` - orchestrates full feature workflow: plan → scout → build → test → commit → PR.

---

### Decision Matrix: When to Use Each

| Scenario | Use This |
|----------|----------|
| Reusable workflow with templates/scripts | **Skill** |
| Simple prompt with no resources | **Command** |
| Complex multi-step automation with branching | **ADW** |
| Personal utility across all projects | **Skill** (personal-level) |
| Project-specific quick action | **Command** |
| SDLC orchestration (plan → build → test → PR) | **ADW** |
| Code generation from templates | **Skill** |
| Git operations (commit, PR creation) | **Command** or **ADW** |
| Documentation generation | **Skill** |
| Feature planning | **Command** |
| Testing + validation loop | **ADW** |

---

### Hybrid Patterns

**Commands Can Trigger Skills**:
```markdown
# In .claude/commands/generate-entity.md
---
allowed-tools: Skill
---

# Generate Entity

Use the `create-crud-entity` skill to generate a new entity:

Instructions for agent: Invoke the create-crud-entity skill with user-provided entity name.
```

**ADWs Can Invoke Skills**:
```python
# In adws/adw_feature_iso.py
def build_phase(feature_name):
    # Invoke skill via agent
    agent.run_skill("create-crud-entity", args={"entity": feature_name})
```

**Skills Can Invoke Other Skills**:
```markdown
# In SKILL.md
## Workflow

1. Use `generating-fractal-docs` skill to create initial documentation
2. Use `create-crud-entity` skill to scaffold entity
3. Use `processing-api-specs` skill to validate API
```

---

## FAQ

### Q: What's the difference between a skill and a command?

**A**:
- **Skill**: Directory with SKILL.md + resources (templates, scripts). Uses progressive disclosure. Can be project or personal-level.
- **Command**: Single .md file in `.claude/commands/`. No resources. All-at-once loading. Project-level only.

**Use skill when**: Workflow needs templates, scripts, or significant resources.
**Use command when**: Simple prompt with no resource dependencies.

---

### Q: Can skills be nested (skill inside skill)?

**A**: Yes. Example: `create-crud-entity/generating-fractal-docs/SKILL.md`

**Benefits**:
- Logical grouping (fractal docs related to CRUD entities)
- Shared context (both skills in same domain)

**Discovery**: Nested skills discovered same as top-level (scan for `*/SKILL.md`).

---

### Q: How do I update an existing skill?

**A**:
1. Read current SKILL.md
2. Edit frontmatter or sections as needed
3. Add/remove/update templates in `templates/`
4. Update version in frontmatter (optional): `version: 1.1`
5. Test discovery and execution

**Best Practice**: Document changes in SKILL.md or separate CHANGELOG.md.

---

### Q: Can I have multiple skills with similar names?

**A**: Avoid. Use unique, descriptive names.

**Conflict Resolution**:
- Project-level overrides personal-level (same name)
- Agent asks user to disambiguate if multiple high-scoring matches

**Example**:
```
Personal: processing-pdfs
Project: processing-project-pdfs

→ User says "process pdf"
→ Agent matches both
→ Agent asks: "Which skill? (1) processing-pdfs (2) processing-project-pdfs"
```

---

### Q: What if skill frontmatter is invalid YAML?

**A**: Agent fails to parse skill, skill not discoverable.

**Validation**:
```bash
python -c "import yaml; yaml.safe_load(open('SKILL.md').read().split('---')[1])"
```

**Common Errors**:
- Missing closing `---`
- Unquoted strings with special characters
- Incorrect indentation

---

### Q: Can skills have dependencies on other skills?

**A**: Yes, implicitly. Skills can reference other skills in workflow.

**Example**:
```markdown
## Workflow

1. **Prerequisite**: Run `generating-fractal-docs` skill first
2. **Main workflow**: Generate entities with templates
3. **Post-processing**: Use `validating-api-schemas` skill
```

**Note**: No formal dependency management. Document prerequisites in SKILL.md.

---

### Q: How do I create a skill template generator (meta-skill)?

**A**: Create a skill that generates other skills.

**Example Frontmatter**:
```yaml
---
name: creating-new-skill
description: Generate a new skill directory with SKILL.md template, templates/ and scripts/ subdirectories. Use when creating new reusable workflows.
---
```

**Workflow**:
1. Ask user for skill name, description, category
2. Create directory: `ai_docs/doc/{skill-name}/`
3. Generate SKILL.md from template with frontmatter
4. Create `templates/` and `scripts/` subdirectories
5. Output: "Skill created at ai_docs/doc/{skill-name}/SKILL.md"

**Meta-Pattern**: Skill that creates skills (meta-meta-agentics).

---

### Q: What's the maximum number of skills before discovery slows down?

**A**: With progressive disclosure (Level 1 only for discovery), scanning 100-500 skills is efficient (~10K-50K tokens).

**Optimization**:
- Use categories to filter: `category: code-generation`
- Use auto-triggers for fast exact matches
- Cache skill registry (read once, reuse)

---

### Q: Can skills work offline?

**A**: Yes, if resources are bundled locally.

**Requirements**:
- All templates in skill directory (no external URLs)
- Scripts executable locally (no API calls)
- No network dependencies

**Validation**:
```bash
# Check for external URLs in skill
grep -r "http://" ai_docs/doc/skill-name/
grep -r "https://" ai_docs/doc/skill-name/
```

---

### Q: How do I version skills?

**A**: Add `version` field to frontmatter.

**Example**:
```yaml
---
name: create-crud-entity
description: Generate CRUD entities...
version: 2.1.0
---
```

**Semantic Versioning**:
- **Major**: Breaking changes (template structure change)
- **Minor**: New features (new template variant)
- **Patch**: Bug fixes (template typo fix)

**Changelog** (optional):
```markdown
## Version History

### 2.1.0 (2026-02-01)
- Added async template variant
- Fixed repository template bug

### 2.0.0 (2026-01-15)
- BREAKING: Renamed domain_model.py to domain_entity.py
- Added authorization templates
```

---

## Conclusion

The **meta-skill pattern** is a powerful abstraction for creating reusable, efficient agent workflows. By following progressive disclosure principles and standardized structure, skills enable:

1. **Context Efficiency**: Load only what's needed (5/15/80 rule)
2. **Composability**: Skills invoke skills (meta-patterns)
3. **Scalability**: Support 100+ skills without context bloat
4. **Discoverability**: Keyword-rich descriptions for fast matching
5. **Maintainability**: Self-contained directories with clear organization

**Key Principles to Remember**:
- Progressive disclosure: metadata → instructions → resources
- SKILL.md <500 lines (use Level 3 for bulk content)
- Gerund naming: `creating-X`, `processing-Y`, `generating-Z`
- Trigger-rich descriptions for discovery
- Self-contained directories with all resources

**Next Steps**:
1. Review existing skills: `create-crud-entity`, `generating-fractal-docs`
2. Create new skills following creation workflow (7 steps)
3. Test discovery and execution
4. Build meta-skills (skills that create/orchestrate skills)

---

**Version**: 1.0
**Last Updated**: 2026-02-03
**Maintained By**: TAC-13 Meta-Agentics Team
