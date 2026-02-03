---
doc_type: feature
adw_id: feature_Tac_13_Task_2
date: 2026-02-02
idk:
  - expertise-yaml
  - tac-13
  - agent-experts
  - mental-model
  - self-improving-agents
  - yaml-schema
  - act-learn-reuse
tags:
  - feature
  - documentation
  - agent-experts
related_code:
  - ai_docs/doc/expertise-file-structure.md
  - .claude/commands/bug.md
  - .claude/commands/chore.md
  - .claude/commands/feature.md
  - adws/adw_modules/agent.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/bug.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/chore.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/feature.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2
---

# Expertise File Structure Documentation

**ADW ID:** feature_Tac_13_Task_2
**Date:** 2026-02-02
**Specification:** specs/issue-564-adw-feature_Tac_13_Task_2-sdlc_planner-expertise-file-structure-docs.md

## Overview

This feature implements comprehensive documentation for the `expertise.yaml` file structure used by TAC-13 self-improving agent experts. The documentation defines the complete YAML schema, validation rules, best practices, and usage guidelines that enable agents to create and maintain consistent expertise files as mental models for the Act → Learn → Reuse loop.

## What Was Built

- **Complete expertise.yaml schema documentation** at `ai_docs/doc/expertise-file-structure.md` (1301 lines)
- **Improved command prompts** for `/bug`, `/chore`, and `/feature` with clearer output format instructions
- **Updated AI docs context injection** in the ADW agent executor to prepend documentation before command prompts
- **Template updates** for all corresponding Jinja2 templates in `tac_bootstrap_cli/tac_bootstrap/templates/`

## Technical Implementation

### Files Modified

- `ai_docs/doc/expertise-file-structure.md`: **NEW** - Complete 1301-line documentation defining YAML schema, field references, annotated examples (CLI, Database, Security experts), validation rules, best practices, usage guidelines, and FAQ
- `.claude/commands/bug.md`: Simplified output format instructions, removed redundant warnings, clearer machine-parsing guidance
- `.claude/commands/chore.md`: Simplified output format instructions, removed redundant warnings, clearer machine-parsing guidance
- `.claude/commands/feature.md`: Simplified output format instructions, removed redundant warnings, clearer machine-parsing guidance
- `adws/adw_modules/agent.py`: Changed AI docs context injection from appending after command to prepending before command (lines 876-887)
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2`: Template version of agent.py changes
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2`: Updated to align with agent.py context injection pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/bug.md.j2`: Template version of bug.md changes
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/chore.md.j2`: Template version of chore.md changes
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/feature.md.j2`: Template version of feature.md changes

### Key Changes

1. **Expertise Schema Documentation**: Created authoritative 9-section documentation covering:
   - Introduction (what is an expertise file, why YAML, purpose in TAC-13)
   - Philosophy and Principles (mental model, compression, 1000-line limit, self-maintained)
   - Complete YAML Schema (top-level structure with all sections)
   - Field Reference (detailed table of all fields with types and requirements)
   - Annotated Examples (3 complete examples: CLI, Database, Security experts)
   - Validation Rules (YAML syntax, line limits, required fields, data types)
   - Best Practices (compression strategies, line reference accuracy, update frequency)
   - Usage Guidelines (when to create, domain-specific sections, workflow integration)
   - FAQ (20+ common questions with detailed answers)

2. **Command Output Simplification**: Removed excessive warning emojis and redundant instructions from `/bug`, `/chore`, `/feature` commands. Streamlined to focus on critical requirements:
   - Check for existing plan file first
   - Create plan with RELATIVE path only
   - Output ONLY the relative path (machine-parsed)
   - Clear examples of correct vs incorrect output

3. **AI Docs Context Injection**: Changed from appending documentation after command prompts to prepending before command prompts. This ensures:
   - Documentation is available as reference context
   - Command-specific instructions remain primary
   - Better alignment with mental model philosophy

## How to Use

### For Agent Developers

When creating new agent experts with expertise files:

1. **Read the schema documentation**:
   ```bash
   cat ai_docs/doc/expertise-file-structure.md
   ```

2. **Follow the complete YAML schema** defined in section 3 (line 110-162)

3. **Reference annotated examples**:
   - CLI Expert example (lines 353-471): Command system with classes and methods
   - Database Expert example (lines 473-641): PostgreSQL with repositories and schema
   - Security Expert example (lines 643-797): JWT authentication and RBAC

4. **Validate your expertise file**:
   ```bash
   # Check YAML syntax
   python -c "import yaml; yaml.safe_load(open('.claude/commands/experts/cli/expertise.yaml'))"

   # Check line count (must be <= 1000)
   wc -l .claude/commands/experts/cli/expertise.yaml
   ```

5. **Use self-improve workflow** to maintain expertise over time

### For Agent Executors

When running planning commands (`/feature`, `/bug`, `/chore`):

1. **Expertise documentation is auto-loaded** via TAC-9 AI docs mapping
2. **Check command output** - should be EXACTLY one line with relative path
3. **Parse the path** for downstream workflow consumption

Example correct output:
```
specs/issue-564-adw-feature_Tac_13_Task_2-sdlc_planner-expertise-docs.md
```

## Configuration

No additional configuration required. The documentation is loaded automatically when:

- TAC-9 AI docs mappings include keywords: `expertise`, `yaml`, `tac-13`, `agent-experts`, `mental-model`
- Planning commands are executed (`/feature`, `/bug`, `/chore`)

## Testing

### Validate YAML Syntax of Examples

Extract and validate each YAML example from the documentation:

```bash
# Extract first example (CLI Expert) and validate
python -c "
import yaml

with open('ai_docs/doc/expertise-file-structure.md', 'r') as f:
    content = f.read()

# Extract YAML blocks between \`\`\`yaml and \`\`\`
blocks = content.split('```yaml')
for i, block in enumerate(blocks[1:], 1):
    yaml_content = block.split('```')[0]
    try:
        parsed = yaml.safe_load(yaml_content)
        print(f'Example {i}: Valid YAML ✓')
    except yaml.YAMLError as e:
        print(f'Example {i}: Invalid YAML ✗')
        print(e)
"
```

### Verify Documentation Completeness

```bash
# Check documentation length (should be 1300+ lines)
wc -l ai_docs/doc/expertise-file-structure.md

# Check for required sections (should find 9 headings)
grep -c "^## " ai_docs/doc/expertise-file-structure.md

# Verify all examples are present
grep -c "^### Example" ai_docs/doc/expertise-file-structure.md
```

### Test Command Output Format

```bash
# Run feature command and verify output is single line
uv run adws/adw_sdlc_iso.py --issue 999

# Output should be EXACTLY:
# specs/issue-999-adw-{adw_id}-sdlc_planner-{name}.md
# No extra commentary or formatting
```

## Notes

### Design Decisions

1. **1000-line limit**: Hard constraint enforced to keep expertise files at ~20% of agent context window, leaving 80% for actual work

2. **YAML over JSON/Markdown**: YAML provides optimal information density while remaining human-readable and machine-parseable

3. **Mental model philosophy**: Expertise files are abstractions, not source code duplicates. They capture "what" and "why", not line-by-line "how"

4. **Self-maintained by agents**: Humans can manually seed expertise files, but self-improve workflow is responsible for keeping them accurate and up-to-date

5. **Domain-specific sections**: Optional sections (`schema_structure`, `security_constraints`, `performance_patterns`) allow specialization without bloating all expertise files

### Integration with TAC-13 Framework

This documentation is the foundation for:

- **question.md prompts**: Agents read expertise first (Reuse phase)
- **self-improve.md prompts**: Agents update expertise after changes (Learn phase)
- **All expert commands**: Use expertise as mental model during execution (Act phase)

### Future Enhancements

Consider adding in future tasks:

- **Automated validation script**: `validate-expertise` CLI command to check YAML syntax, line count, required fields
- **Expertise file generator**: Scaffold new expertise files with minimal seed structure
- **Version tracking**: Add `version` field to expertise schema for tracking breaking changes
- **Expertise diff tool**: Compare expertise files across versions to track evolution
