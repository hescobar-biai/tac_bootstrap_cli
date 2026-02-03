# Feature: Create expertise file structure documentation

## Metadata
issue_number: `564`
adw_id: `feature_Tac_13_Task_2_sin_docs`
issue_json: `{"number": 564, "title": "[TAC-13] Task 2: Create expertise file structure documentation", "body": "**Workflow Metadata:**\n```\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_13_Task_2\n```\n\n**Description:**\nDocument the standard structure for expertise.yaml files used by agent experts.\n\n**Technical Steps:**\n\n1. **Create documentation file**:\n   ```bash\n   /Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/expertise-file-structure.md\n   ```\n\n2. **Define complete YAML schema with examples**..."}`

## Feature Description
Create comprehensive documentation for the standard structure of expertise.yaml files used by agent experts. This documentation will serve as a reference for both humans and AI agents when creating, updating, or understanding expertise files that power self-improving agents in the TAC-13 agent expert system.

## User Story
As an agentic engineer using TAC-13 agent experts
I want to have clear documentation on the structure of expertise.yaml files
So that I can create consistent, well-structured expertise files and understand how agents should maintain their mental models

## Problem Statement
The TAC-13 agent expert system relies on expertise.yaml files as mental models for specialized agents. Currently, the expertise file structure is demonstrated through examples in TAC-13-agent-experts.md, but there is no dedicated reference documentation that:
- Defines the complete YAML schema with all available sections
- Explains when to use each section and field
- Provides detailed examples for different domain types (database, API, CLI, etc.)
- Documents best practices for maintaining finite, actionable expertise
- Guides both humans and agents in creating effective mental models

This documentation gap makes it harder to onboard new agent experts and maintain consistency across expertise files.

## Solution Statement
Create a dedicated documentation file `ai_docs/doc/expertise-file-structure.md` that serves as the authoritative reference for expertise.yaml schema and structure. This document will include:
1. Complete YAML schema template with all sections
2. Field-by-field explanations with purpose and usage guidelines
3. Domain-specific examples (database, API, CLI, WebSocket, billing)
4. Best practices for maintaining expertise files
5. Validation criteria and constraints
6. Anti-patterns to avoid

This documentation will be structured for progressive disclosure - starting with the overview schema, then detailed field descriptions, then comprehensive examples.

## Relevant Files
Files needed to understand expertise structure:

- `ai_docs/doc/TAC-13-agent-experts.md` - Main TAC-13 documentation with expertise examples (lines 89-157 show basic structure)
- `.claude/commands/experts/cc_hook_expert/` - Existing expert directory structure to understand organization
- `.claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md` - Example expert command that references expertise
- `.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md` - Self-improve pattern that updates expertise

### New Files
- `ai_docs/doc/expertise-file-structure.md` - The new comprehensive documentation file

## Implementation Plan

### Phase 1: Foundation
1. Read TAC-13-agent-experts.md to extract existing expertise examples and patterns
2. Analyze the cc_hook_expert directory structure to understand real-world usage
3. Review self-improve prompts to understand how agents update expertise
4. Identify all sections and fields used across examples

### Phase 2: Core Implementation
1. Create the documentation file at `ai_docs/doc/expertise-file-structure.md`
2. Define the complete YAML schema template with all sections
3. Document each section with purpose, when to use, and examples
4. Add domain-specific complete examples (database, API, CLI, WebSocket, billing)
5. Include best practices and validation criteria

### Phase 3: Integration
1. Ensure the documentation aligns with examples in TAC-13-agent-experts.md
2. Verify the schema matches patterns used in expert commands
3. Add cross-references to related documentation
4. Ensure the document is discoverable via conditional_docs system

## Step by Step Tasks

### Task 1: Analyze Existing Expertise Patterns
- Read TAC-13-agent-experts.md lines 89-900 to extract all expertise examples
- Identify all sections used: overview, core_implementation, schema_structure, key_operations, integration_points, known_patterns, recent_changes
- Document field types, purposes, and usage patterns
- Note different domain examples (database lines 796-859, websocket lines 878-926, billing lines 935-983)

### Task 2: Define Complete YAML Schema
- Create the full schema template with all possible sections
- Document required vs optional sections
- Define field types and constraints for each section
- Include inline comments explaining each field's purpose
- Add validation rules (max_lines: 1000, valid YAML, required sections)

### Task 3: Create Domain-Specific Examples
- Database expert example with tables, relationships, query patterns, migration patterns
- API expert example with endpoints, authentication, rate limiting, error handling
- CLI expert example with commands, arguments, workflows, configuration
- WebSocket expert example with event types, connection handling, state management
- Billing expert example with payment flows, webhooks, idempotency, critical constraints

### Task 4: Document Best Practices
- Compressed representation principles (YAML/JSON/TOML)
- Finite size enforcement (1000 line max)
- Actionable information priority (what helps agents decide)
- Self-maintained through self-improve workflow
- Validation against code as source of truth
- When to prune low-value details

### Task 5: Add Validation and Anti-Patterns
- YAML syntax validation requirements
- Line count enforcement mechanisms
- Required vs optional section guidelines
- Anti-patterns to avoid (over-documentation, line-by-line logic, obsolete information)
- How to handle constraint violations during self-improve

### Task 6: Write Progressive Disclosure Structure
- Start with overview and quick reference schema
- Follow with detailed section-by-section documentation
- Include comprehensive domain examples
- End with best practices and troubleshooting
- Add table of contents for easy navigation

### Task 7: Create and Validate Documentation File
- Write the complete documentation to `ai_docs/doc/expertise-file-structure.md`
- Ensure markdown formatting is correct
- Verify all code blocks use proper syntax highlighting
- Add cross-references to TAC-13-agent-experts.md
- Include date and version information

### Task 8: Final Validation
- Read the created file to verify completeness
- Check that all sections from the issue body are included
- Verify examples are accurate and comprehensive
- Ensure the document is self-contained and useful for both humans and agents
- Run validation commands (no specific tests needed, but file should exist and be readable)

## Testing Strategy

### Unit Tests
No unit tests required - this is documentation only.

### Edge Cases
- Verify documentation covers all expertise sections found in examples
- Ensure schema is complete enough for different domain types
- Check that best practices align with self-improve workflow
- Validate that examples are realistic and match real-world usage

## Acceptance Criteria
1. Documentation file exists at `ai_docs/doc/expertise-file-structure.md`
2. Complete YAML schema template is defined with all sections
3. Each section has clear explanation of purpose and usage
4. At least 5 domain-specific complete examples are provided (database, API, CLI, WebSocket, billing)
5. Best practices for maintaining expertise files are documented
6. Validation criteria and constraints are clearly specified
7. Document includes table of contents and is well-organized
8. Cross-references to TAC-13-agent-experts.md are included
9. The documentation is usable by both humans and AI agents
10. File is formatted in proper markdown with syntax highlighting

## Validation Commands
No specific validation commands needed for documentation. Visual inspection will verify:

- File exists and is readable: `cat ai_docs/doc/expertise-file-structure.md`
- Markdown is properly formatted (manual review)
- Schema examples are valid YAML (manual review)
- Content is comprehensive and accurate (manual review)

## Notes
- This documentation builds on the examples in TAC-13-agent-experts.md but provides a focused reference
- The schema should be flexible enough to accommodate different domain types while maintaining consistency
- Expertise files are mental models, not source of truth - this should be emphasized throughout
- The 1000 line constraint is critical for context efficiency and should be prominently documented
- Examples should show realistic, non-trivial expertise that demonstrates value
- The documentation should help guide self-improve prompts in maintaining expertise quality
