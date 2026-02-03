# Feature: Create Expertise File Structure Documentation

## Metadata
issue_number: `564`
adw_id: `feature_Tac_13_Task_2_FINAL`
issue_json: `{"number": 564, "title": "[TAC-13] Task 2: Create expertise file structure documentation", "body": "**Workflow Metadata:**\n```\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_13_Task_2\n```\n\n**Description:**\nDocument the standard structure for expertise.yaml files used by agent experts.\n\n**Technical Steps:**\n\n1. **Create documentation file**:\n   ```bash\n   /Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/expertise-file-structure.md\n   ```\n\n2. **Define complete YAML schema with examples**:\n\n   **Full Schema Template:**\n   ```yaml\n   overview:\n     description: \"One-sentence description of what this expert covers\"\n     key_files:\n       - \"path/to/main/file1.py\"\n       - \"path/to/main/file2.py\"\n     total_files: 15\n     last_updated: \"2026-02-03\"\n\n   core_implementation:\n     component_name_1:\n       location: \"path/to/component.py\"\n       description: \"What this component does\"\n       key_classes:\n         - name: \"ClassName\"\n           line_start: 10\n           line_end: 150\n           purpose: \"Core responsibility\"\n           key_methods:\n             - name: \"method_name\"\n               line_start: 45\n               line_end: 78\n               signature: \"def method_name(self, arg1: str, arg2: int) -> bool\"\n               logic: \"High-level what it does (not line-by-line)\"\n               dependencies: [\"OtherClass\", \"external_lib\"]\n       key_functions:\n         - name: \"standalone_function\"\n           line_start: 200\n           line_end: 250\n           signature: \"def standalone_function(config: Config) -> Result\"\n           logic: \"What it does and why\"\n\n     component_name_2:\n       # ... same structure ...\n\n   schema_structure:  # Optional: for database/API experts\n     tables:\n       - name: \"table_name\"\n         primary_key: \"id\"\n         columns: [\"col1\", \"col2\", \"col3\"]\n         relationships:\n           - table: \"related_table\"\n             type: \"one_to_many\"\n             foreign_key: \"related_id\"\n     views:\n       - name: \"view_name\"\n         query_logic: \"Aggregates X from Y\"\n\n   key_operations:\n     operation_category_1:\n       description: \"What this category handles\"\n       steps:\n         - action: \"Step description\"\n           location: \"file.py:function_name\"\n           key_logic: \"Brief explanation\"\n\n   common_patterns:\n     pattern_name:\n       description: \"When and why this pattern is used\"\n       example_location: \"path/to/example.py:45-78\"\n       key_insight: \"Important thing to know about this pattern\"\n\n   gotchas:\n     - issue: \"Common mistake or edge case\"\n       solution: \"How to handle it\"\n       location: \"where this is handled in code\"\n   ```\n\n3. **Document the three-step workflow**:\n   - **ACT**: Build/modify implementation\n   - **LEARN**: Update expertise file via self-improve loop using git diff\n   - **REUSE**: Reference expertise file for future questions/tasks\n\n4. **Include validation rules**:\n   - Max line count constraints (e.g., 500 lines for expertise files)\n   - Required YAML structure validation\n   - Date format requirements (YYYY-MM-DD)\n   - File path format (relative to project root)\n\n5. **Provide concrete examples**:\n   - Database expert expertise structure\n   - Websocket expert expertise structure\n   - CLI expert expertise structure\n\n6. **Self-improve prompt template**:\n   Include reusable prompt for agents to update expertise files automatically after code changes."}`

## Feature Description
Create comprehensive documentation for the standard structure of `expertise.yaml` files used by Agent Experts in the TAC methodology. This documentation will serve as the canonical reference for building self-improving agents that maintain mental models (expertise files) about specific domains in complex codebases.

The documentation establishes the schema, validation rules, workflows, and examples needed for agents to create, maintain, and use expertise files effectively across different domain types (database, websocket, CLI, etc.).

## User Story
As an AI agent developer implementing Agent Experts for TAC Bootstrap
I want clear documentation on the expertise.yaml file structure and usage patterns
So that I can build consistent, self-improving agents that accumulate domain knowledge correctly

## Problem Statement
The TAC-13 methodology introduces Agent Experts with expertise files as "mental models," but there's no canonical documentation defining:
- The standard YAML schema structure for expertise files
- Required vs. optional sections for different expert types
- Validation rules and constraints (line limits, format requirements)
- The Act → Learn → Reuse workflow integration
- Concrete examples across different domain types
- Self-improve prompt patterns for automatic updates

Without this documentation, developers implementing agent experts will:
- Create inconsistent expertise file structures
- Miss critical sections needed for effective reuse
- Violate size constraints leading to context bloat
- Fail to implement proper self-improve loops
- Duplicate work instead of following established patterns

## Solution Statement
Create a comprehensive documentation file at `ai_docs/doc/expertise-file-structure.md` that defines:

1. **Complete YAML Schema** with all sections:
   - `overview` - Description, key files, metadata
   - `core_implementation` - Classes, functions, methods with line references
   - `schema_structure` - Database tables, views, relationships (optional)
   - `key_operations` - Step-by-step operational workflows
   - `common_patterns` - Reusable patterns with examples
   - `gotchas` - Known issues and solutions

2. **Field Specifications**:
   - Data types, required vs. optional fields
   - Format requirements (dates, file paths, line numbers)
   - Reasonable value ranges and examples

3. **Validation Rules**:
   - Max line count (500 lines recommended)
   - Valid YAML structure checks
   - Required sections per expert type
   - Date format (YYYY-MM-DD)
   - File path format (relative paths only)

4. **Three-Step Workflow Documentation**:
   - **ACT**: Implementation changes with expertise file reference
   - **LEARN**: Self-improve loop triggered by git diff
   - **REUSE**: Question prompts using expertise file as primary source

5. **Concrete Examples**:
   - Database expert: schema, migrations, queries
   - Websocket expert: handlers, session management, events
   - CLI expert: commands, argument parsing, output formatting

6. **Reusable Templates**:
   - Self-improve prompt template
   - Question prompt template
   - Validation script template

## Relevant Files

### New Files
- `ai_docs/doc/expertise-file-structure.md` - Main documentation file to create

### Reference Files
- `ai_docs/doc/Tac-13_1.md` - Agent Experts methodology foundation
- `ai_docs/doc/Tac-13_2.md` - Advanced Agent Experts patterns
- `ai_docs/doc/Tac-13-agent-experts.md` - TAC-13 overview
- `ai_docs/doc/plan_tasks_tac_13.md` - TAC-13 implementation plan

### Example Reference (from TAC-13 docs)
The documentation includes inline examples of database expert and websocket expert structures which should be formalized.

## Implementation Plan

### Phase 1: Research TAC-13 Documentation
Read and synthesize existing TAC-13 documentation to extract:
- Expertise file examples from Tac-13_1.md and Tac-13_2.md
- Agent Expert workflow patterns
- Validation rules and constraints mentioned
- Self-improve loop specifications

### Phase 2: Design Complete Schema
Create the comprehensive YAML schema definition with:
- All required and optional top-level sections
- Nested structure for each section
- Field-level specifications (type, format, examples)
- Comments explaining purpose of each field
- Domain-specific optional sections

### Phase 3: Document Validation Rules
Define clear validation criteria:
- Line count limits and rationale
- YAML structure validation approach
- Required vs. optional section rules per expert type
- Format requirements for dates, paths, line numbers
- Examples of valid and invalid structures

### Phase 4: Create Workflow Integration Guide
Document the three-step loop:
- **ACT**: When and how to reference expertise during implementation
- **LEARN**: Triggering self-improve, analyzing git diff, updating expertise
- **REUSE**: Using expertise to answer questions without searching
- Integration points with existing TAC Bootstrap commands

### Phase 5: Develop Concrete Examples
Create complete, realistic examples for:
- Database expert expertise file
- Websocket expert expertise file
- CLI expert expertise file
Include annotations explaining design choices

### Phase 6: Write Reusable Templates
Provide copy-paste templates for:
- Self-improve prompt (with placeholders)
- Question prompt (with placeholders)
- Validation script (Python/shell)
- Initial expertise file scaffold

## Step by Step Tasks

### Task 1: Read TAC-13 source documentation
- Read `ai_docs/doc/Tac-13_1.md` completely
- Read `ai_docs/doc/Tac-13_2.md` completely
- Read `ai_docs/doc/Tac-13-agent-experts.md` for overview
- Extract all expertise file examples and patterns
- Document validation rules mentioned in the lessons

### Task 2: Design YAML schema structure
- Define `overview` section with all fields
- Define `core_implementation` section for classes and functions
- Define optional `schema_structure` for database experts
- Define `key_operations` workflow section
- Define `common_patterns` reusable patterns section
- Define `gotchas` for edge cases and issues
- Add comprehensive inline YAML comments

### Task 3: Specify validation rules
- Document max line count (500 lines recommended)
- Specify YAML structure validation requirements
- Define required sections per expert type
- Specify date format requirements (YYYY-MM-DD)
- Specify file path format (relative to project root)
- Explain rationale for each constraint

### Task 4: Document Act → Learn → Reuse workflow
- Explain **ACT** phase: implementation referencing expertise
- Explain **LEARN** phase: self-improve loop with git diff
- Explain **REUSE** phase: question answering with expertise
- Provide workflow diagram in Mermaid or ASCII
- Show integration with TAC Bootstrap commands

### Task 5: Create concrete domain examples
- Create complete database expert example with tables, migrations, queries
- Create complete websocket expert example with handlers, sessions, events
- Create complete CLI expert example with commands, args, output
- Annotate each example explaining key decisions
- Show before/after for self-improve loop

### Task 6: Write reusable templates
- Create self-improve prompt template with placeholders
- Create question prompt template with placeholders
- Create validation script (Python preferred)
- Create initial expertise file scaffold template
- Add usage instructions for each template

### Task 7: Review and validate documentation
- Verify all schema sections are documented
- Check YAML syntax in all examples
- Ensure examples follow validation rules
- Test validation script on examples
- Proofread for clarity and completeness

### Task 8: Final validation
- Run through the documentation as if building a new agent expert
- Verify all promised sections exist
- Check cross-references to TAC-13 docs are accurate
- Ensure templates are truly reusable
- Validate that this documentation fulfills issue requirements

## Testing Strategy

### Manual Validation
- Review YAML examples with yamllint
- Verify all code blocks have proper syntax
- Check that schema covers all use cases from TAC-13 docs
- Ensure templates are copy-paste ready

### Integration Validation
- Use this documentation to create a test expert (e.g., "config expert")
- Validate the test expert's expertise file against documented schema
- Run through Act → Learn → Reuse cycle with test expert
- Verify validation rules catch common mistakes

### Documentation Quality
- All sections from schema are explained
- Examples are realistic and complete
- Templates have clear placeholder instructions
- Cross-references to TAC-13 are accurate
- Structure is logical and easy to navigate

## Acceptance Criteria
- [ ] Documentation file exists at `ai_docs/doc/expertise-file-structure.md`
- [ ] Complete YAML schema defined with all required and optional sections
- [ ] Validation rules clearly specified with rationale
- [ ] Three-step workflow (Act → Learn → Reuse) documented with integration points
- [ ] Three concrete domain examples provided (database, websocket, CLI)
- [ ] Reusable templates included for self-improve, question, validation, scaffold
- [ ] All YAML examples are valid and follow validation rules
- [ ] Documentation is comprehensive enough to build agent experts without additional guidance
- [ ] Cross-references to TAC-13 source docs are accurate
- [ ] File is well-structured with clear headings and navigation

## Validation Commands
No code changes, documentation only. Manual validation:

```bash
# Verify file exists
ls -lh ai_docs/doc/expertise-file-structure.md

# Check YAML examples are valid (extract and validate)
grep -A 50 '```yaml' ai_docs/doc/expertise-file-structure.md | yamllint -

# Word count (should be comprehensive, 2000+ words)
wc -w ai_docs/doc/expertise-file-structure.md

# Visual review
cat ai_docs/doc/expertise-file-structure.md
```

## Notes
- This is a documentation-only task with no code implementation
- The expertise file structure documentation will be referenced by future TAC-13 tasks
- Examples should be realistic but simplified for clarity
- Focus on making the documentation immediately actionable for agent developers
- Consider this the "specification" that all expertise files should follow
- The validation script template should be Python for consistency with TAC Bootstrap CLI
- Keep in mind that expertise files are NOT source of truth, but mental models that complement code
- Size limits exist to keep expertise files context-efficient for AI agents
- The self-improve loop is critical to ensure expertise stays synchronized with code changes
