# Feature: Expertise File Structure Documentation

## Metadata
issue_number: `564`
adw_id: `feature_Tac_13_Task_2`
issue_json: `{"number": 564, "title": "[TAC-13] Task 2: Create expertise file structure documentation", "body": "**Workflow Metadata:**\n```\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_13_Task_2\n```\n\n**Description:**\nDocument the standard structure for expertise.yaml files used by agent experts.\n\n**Technical Steps:**\n\n1. **Create documentation file**:\n   ```bash\n   /Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/expertise-file-structure.md\n   ```\n\n2. **Define complete YAML schema with examples**:\n\n   **Full Schema Template:**\n   ```yaml\n   overview:\n     description: \"One-sentence description of what this expert covers\"\n     key_files:\n       - \"path/to/main/file1.py\"\n       - \"path/to/main/file2.py\"\n     total_files: 15\n     last_updated: \"2026-02-03\"\n\n   core_implementation:\n     component_name_1:\n       location: \"path/to/component.py\"\n       description: \"What this component does\"\n       key_classes:\n         - name: \"ClassName\"\n           line_start: 10\n           line_end: 150\n           purpose: \"Core responsibility\"\n           key_methods:\n             - name: \"method_name\"\n               line_start: 45\n               line_end: 78\n               signature: \"def method_name(self, arg1: str, arg2: int) -> bool\"\n               logic: \"High-level what it does (not line-by-line)\"\n               dependencies: [\"OtherClass\", \"external_lib\"]\n       key_functions:\n         - name: \"standalone_function\"\n           line_start: 200\n           line_end: 250\n           signature: \"def standalone_function(config: Config) -> Result\"\n           logic: \"What it does and why\"\n\n     component_name_2:\n       # ... same structure ...\n\n   schema_structure:  # Optional: for database/API experts\n     tables:\n       - name: \"table_name\"\n         primary_key: \"id\"\n         columns: [\"col1\", \"col2\", \"col3\"]\n         relationships:\n           - table: \"related_table\"\n             type: \"one_to_many\"\n             foreign_key: \"related_id\"\n     views:\n       - name: \"view_name\"\n         query_logic: \"Aggregates X from Y\"\n\n   key_operations:\n     operation_category_1:\n       descr\n\n[TRUNCATED - body exceeds 2000 chars]"}`

## Feature Description
Create comprehensive documentation for the standard structure of `expertise.yaml` files used by self-improving agent experts in the TAC-13 Agent Experts framework. This documentation will serve as the authoritative reference for agents and developers creating new expertise files, ensuring consistency across all agent expert implementations.

The documentation will define the complete YAML schema, provide annotated examples for different expert types (CLI, database, security, etc.), include line limit constraints (max 1000 lines), validation rules, and best practices for maintaining expertise files as mental models.

## User Story
As an agentic engineer implementing TAC-13 agent experts
I want comprehensive documentation of the expertise.yaml file structure
So that I can create consistent, valid expertise files that agents can effectively use for self-improvement and knowledge retention

## Problem Statement
The TAC-13 Agent Experts framework relies heavily on `expertise.yaml` files as mental models for self-improving agents. Currently, there is no single authoritative documentation that defines:
- The complete YAML schema with all possible fields
- Structural conventions (naming, nesting, organization)
- Validation constraints (max 1000 lines, required fields)
- Best practices for different expert domains
- Examples demonstrating proper usage

Without this documentation, agents and developers must reverse-engineer the structure from existing examples, leading to inconsistent implementations and potential errors in self-improvement workflows.

## Solution Statement
Create a comprehensive markdown documentation file at `ai_docs/doc/expertise-file-structure.md` that:

1. **Defines the complete schema** with all top-level sections (overview, core_implementation, schema_structure, key_operations, best_practices, known_issues)
2. **Provides field-level documentation** including data types, constraints, and purposes
3. **Includes annotated examples** for multiple expert types (CLI, database, security, commands)
4. **Documents validation rules** (YAML syntax, line limits, required fields)
5. **Establishes best practices** for compression, line references, mental model maintenance
6. **Clarifies philosophical principles** (expertise as mental model, not source of truth)

This documentation will be loaded by agents during planning and implementation phases, ensuring all expertise files follow consistent patterns and can be effectively used in the Act → Learn → Reuse loop.

## Relevant Files
Files to reference for understanding existing expertise file patterns:

- `.claude/commands/experts/cli/expertise.yaml` - Example CLI expert mental model
- `.claude/commands/experts/adw/expertise.yaml` - Example ADW expert mental model
- `.claude/commands/experts/commands/expertise.yaml` - Example commands expert mental model
- `ai_docs/doc/Tac-13-agent-experts.md` - Core TAC-13 conceptual documentation
- `ai_docs/doc/TAC-13_implementation_status.md` - Implementation patterns and constraints
- `ai_docs/doc/plan_tasks_tac_13.md` - Task 2 specifications and acceptance criteria

### New Files
- `ai_docs/doc/expertise-file-structure.md` - Complete expertise.yaml schema documentation

## Implementation Plan

### Phase 1: Research
Analyze existing expertise.yaml files to extract common patterns, field structures, and domain-specific variations. Review TAC-13 documentation to understand philosophical principles and technical constraints.

### Phase 2: Schema Definition
Create the complete YAML schema definition with all possible sections, fields, data types, and constraints. Ensure coverage of all use cases (CLI, database, security, API, etc.).

### Phase 3: Documentation Writing
Write comprehensive markdown documentation including schema definition, field-level descriptions, validation rules, examples, best practices, and usage guidelines.

### Phase 4: Validation
Validate documentation against existing expertise.yaml files to ensure completeness and accuracy. Verify all examples are syntactically correct YAML.

## Step by Step Tasks

### Task 1: Analyze Existing Expertise Files
- Read `.claude/commands/experts/cli/expertise.yaml` to understand CLI expert structure
- Read `.claude/commands/experts/adw/expertise.yaml` to understand ADW expert structure
- Read `.claude/commands/experts/commands/expertise.yaml` to understand commands expert structure
- Extract common patterns: field names, nesting levels, data types
- Identify domain-specific variations (schema_structure for databases, key_operations for workflows)

### Task 2: Review TAC-13 Documentation
- Read `ai_docs/doc/Tac-13-agent-experts.md` for philosophical principles
- Read `ai_docs/doc/TAC-13_implementation_status.md` for constraints (1000-line limit)
- Read `ai_docs/doc/plan_tasks_tac_13.md` Task 2 for acceptance criteria
- Extract key principles: expertise as mental model, validation requirements, compression strategies

### Task 3: Define Complete Schema
Create comprehensive YAML schema covering:
- **overview** section: description, key_files, total_files, last_updated
- **core_implementation** section: components with locations, classes, methods, functions, line references
- **schema_structure** section (optional): tables, columns, relationships, views (for database experts)
- **key_operations** section: operation categories with descriptions and patterns
- **best_practices** section: domain-specific guidelines
- **known_issues** section: gotchas, workarounds, technical debt

### Task 4: Create Annotated Examples
Develop 3 complete examples:
1. **CLI Expert example** - Command system with classes and methods
2. **Database Expert example** - Schema with tables, relationships, queries
3. **Security Expert example** - Authentication/authorization patterns

Each example should:
- Be syntactically valid YAML
- Include inline comments explaining field purposes
- Demonstrate proper line references
- Show compression techniques

### Task 5: Document Validation Rules
Define all validation requirements:
- YAML syntax correctness
- Maximum 1000 lines total
- Required fields vs optional fields
- Valid data types for each field
- Naming conventions (snake_case, descriptive)

### Task 6: Write Best Practices Section
Document best practices for:
- Compression strategies (high-level logic, not line-by-line)
- Line reference accuracy (validate against actual code)
- Update frequency (after significant changes)
- Mental model philosophy (abstraction, not duplication)
- Context management (~20% expertise, 80% task work)

### Task 7: Create Usage Guidelines
Write guidelines for:
- When to create new expertise files
- How to structure domain-specific sections
- Integration with question.md and self-improve.md prompts
- Validation workflow (manual and automated)

### Task 8: Write Complete Documentation File
Create `ai_docs/doc/expertise-file-structure.md` with:
- Introduction explaining purpose and philosophy
- Complete schema reference
- Annotated examples for 3+ domains
- Validation rules
- Best practices
- Usage guidelines
- FAQ section

### Task 9: Validate Documentation
- Verify all YAML examples are syntactically correct
- Check that schema covers all fields in existing expertise.yaml files
- Ensure no contradictions with TAC-13 conceptual documentation
- Confirm documentation meets Task 2 acceptance criteria
- Execute validation commands

## Testing Strategy

### Unit Tests
No unit tests required (documentation task).

### Edge Cases
- Expertise files approaching 1000-line limit
- Domain-specific sections (schema_structure, API endpoints)
- Optional vs required fields
- Different compression strategies for verbose implementations

## Acceptance Criteria
- [ ] Documentation file created at `ai_docs/doc/expertise-file-structure.md`
- [ ] Complete YAML schema defined with all possible sections and fields
- [ ] At least 3 annotated examples for different expert domains (CLI, database, security)
- [ ] Validation rules documented (YAML syntax, 1000-line limit, required fields)
- [ ] Best practices section covers compression, line references, mental model philosophy
- [ ] All YAML examples are syntactically valid
- [ ] Documentation is consistent with existing expertise.yaml files
- [ ] Documentation aligns with TAC-13 conceptual principles from `Tac-13-agent-experts.md`
- [ ] File is formatted in clear markdown with proper structure and navigation

## Validation Commands
Execute all commands to validate with zero regressions:

- `uv run python -c "import yaml; yaml.safe_load(open('ai_docs/doc/expertise-file-structure.md').read().split('```yaml')[1].split('```')[0])"` - Validate YAML syntax of first example
- `wc -l ai_docs/doc/expertise-file-structure.md` - Verify documentation is comprehensive (expect 300+ lines)
- `grep -c "^#" ai_docs/doc/expertise-file-structure.md` - Verify structured sections (expect 10+ headings)
- `cat ai_docs/doc/expertise-file-structure.md` - Manual review for completeness

## Notes
- This is a documentation-only task with no code changes
- The documentation will be referenced by agents during planning and implementation of new agent experts
- Expertise files are YAML-based mental models, not source code duplicates
- The 1000-line limit is a hard constraint enforced during self-improvement workflows
- Documentation should emphasize compression strategies to stay within line limits
- Future tasks will reference this documentation when creating new expert domains
- Consider adding validation script in future task to automatically check expertise.yaml files against this schema
