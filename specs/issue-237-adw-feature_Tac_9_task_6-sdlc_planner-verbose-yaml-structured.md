# Feature: Add verbose-yaml-structured.md.j2 output style template

## Metadata
issue_number: `237`
adw_id: `feature_Tac_9_task_6`
issue_json: `{"number":237,"title":"Add verbose-yaml-structured.md.j2 output style template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_6\n\n**Description:**\nCreate Jinja2 template for the \"verbose-yaml-structured\" output style. This style produces YAML-structured output for machine parsing.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/output-styles/verbose-yaml-structured.md`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/verbose-yaml-structured.md.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/output-styles/verbose-yaml-structured.md` (CREATE - rendered)"}`

## Feature Description

Add a new output style template called "verbose-yaml-structured" that converts the comprehensive guidance from "verbose-bullet-points" into YAML format for machine parsing. This style provides the same detailed, comprehensive response guidelines as verbose-bullet-points but serialized in YAML format instead of Markdown, enabling programmatic consumption and parsing of Claude's behavioral directives.

The template will be created in two locations following the established pattern:
1. **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/verbose-yaml-structured.md.j2`
2. **Rendered Source**: `.claude/output-styles/verbose-yaml-structured.md`

## User Story

As a system integrator building agentic workflows
I want output style definitions in machine-parseable YAML format
So that I can programmatically parse and apply Claude's behavioral directives in automated systems

## Problem Statement

The existing output style templates (verbose-bullet-points, concise-tts, concise-done, concise-ultra) are all in Markdown format, which is optimized for human readability but not for machine parsing. While the verbose-bullet-points style provides excellent comprehensive guidance, there's no structured format for programmatic consumption. Adding a YAML-formatted version enables:

- Programmatic parsing of response guidelines
- Integration with configuration management systems
- Machine-readable structured data for agentic workflows
- Consistency with PyYAML-based infrastructure already in the project

## Solution Statement

Create a `verbose-yaml-structured` output style template that:

1. Converts all content from verbose-bullet-points into valid YAML 1.1 format
2. Uses top-level keys for major sections: `style_name`, `description`, `response_guidelines`, `when_to_use`, `examples`, `important_notes`
3. Preserves all semantic meaning and content from the original verbose-bullet-points style
4. Maintains compatibility with standard YAML parsers (PyYAML)
5. Follows the established naming convention: `{style-name}.md.j2` for templates and `{style-name}.md` for rendered files
6. Contains no Jinja2 template variables, matching the pattern of existing static output-style templates

## Relevant Files

### Existing Templates (Reference)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/verbose-bullet-points.md.j2` - Source template to convert
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-tts.md.j2` - Pattern reference
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2` - Pattern reference
- `.claude/output-styles/verbose-bullet-points.md` - Source content to convert

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/verbose-yaml-structured.md.j2` - Jinja2 template (CREATE)
- `.claude/output-styles/verbose-yaml-structured.md` - Rendered YAML source file (CREATE)

## Implementation Plan

### Phase 1: Content Analysis
Analyze the verbose-bullet-points template to understand all sections and information hierarchy that needs to be preserved in YAML format.

### Phase 2: YAML Structure Design
Design the YAML structure that mirrors the content organization of verbose-bullet-points while ensuring PyYAML compatibility and readability.

### Phase 3: Template Creation
Create both the Jinja2 template and rendered source files with complete YAML content.

### Phase 4: Validation
Validate the YAML files against PyYAML parser and ensure content completeness.

## Step by Step Tasks

### Task 1: Create verbose-yaml-structured.md.j2 Jinja2 template
- Convert verbose-bullet-points content to YAML 1.1 format
- Use appropriate YAML data types (strings, lists, nested maps)
- Ensure the file is valid YAML parseable by PyYAML
- Place at: `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/verbose-yaml-structured.md.j2`
- Content structure:
  - `style_name`: "verbose-yaml-structured"
  - `description`: Brief 1-2 sentence description
  - `response_guidelines`: List of bullet points
  - `when_to_use`: List of use cases
  - `examples`: Map with "good" and "avoid" sections
  - `important_notes`: List of key callouts

### Task 2: Create .claude/output-styles/verbose-yaml-structured.md rendered file
- Copy content from Task 1's Jinja2 template
- Verify YAML syntax and formatting
- Ensure all content from verbose-bullet-points is present and correctly formatted
- Place at: `.claude/output-styles/verbose-yaml-structured.md`

### Task 3: Validate YAML format
- Run PyYAML parser on both files to confirm they're valid YAML
- Verify no content loss or corruption
- Test round-trip parsing: load and dump to ensure consistency

### Task 4: Verify integration and completeness
- Check that the template follows naming conventions: `{style-name}.md.j2`
- Confirm file locations match established pattern
- Ensure no Jinja2 variables are needed (static content)
- Run final smoke test of YAML validity

## Testing Strategy

### Unit Tests
- Validate YAML structure using PyYAML parser
- Verify all required top-level keys exist: `style_name`, `description`, `response_guidelines`, `when_to_use`, `examples`, `important_notes`
- Test parsing of nested structures (lists, maps)
- Confirm the file can be loaded and re-dumped without errors

### Edge Cases
- Test YAML special characters handling (colons, quotes, hyphens in values)
- Verify multiline strings are properly formatted
- Ensure list items and nested maps render correctly
- Check that URLs and code examples within YAML are properly escaped

### Validation
```bash
python3 -c "import yaml; yaml.safe_load(open('.claude/output-styles/verbose-yaml-structured.md'))"
python3 -c "import yaml; yaml.safe_load(open('tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/verbose-yaml-structured.md.j2'))"
```

## Acceptance Criteria

1. **File Creation**: Both files exist at correct locations
   - `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/verbose-yaml-structured.md.j2` ✓
   - `.claude/output-styles/verbose-yaml-structured.md` ✓

2. **YAML Validity**: Files are valid YAML 1.1 format
   - Parseable by PyYAML without errors ✓
   - All special characters properly escaped ✓
   - No syntax errors or formatting issues ✓

3. **Content Completeness**: All verbose-bullet-points content preserved
   - `style_name` section present ✓
   - `response_guidelines` with all 9 guidelines ✓
   - `when_to_use` with all 7 use cases ✓
   - `examples` with good and avoid patterns ✓
   - `important_notes` with all 7 callouts ✓

4. **Semantic Equivalence**: YAML version conveys same meaning as Markdown
   - Response guidelines semantically identical ✓
   - Use cases preserved with full context ✓
   - Examples demonstrate same concepts ✓
   - Important notes maintain emphasis and significance ✓

5. **Naming and Convention Compliance**:
   - Filename follows pattern: `verbose-yaml-structured` (hyphen-separated, lowercase) ✓
   - Extension is `.md.j2` for template and `.md` for rendered ✓
   - No Jinja2 template variables used (static content) ✓
   - Located in correct directory alongside other output-style templates ✓

6. **No Breaking Changes**:
   - Existing output-style templates unchanged ✓
   - Directory structure maintained ✓
   - Project dependencies unchanged ✓

## Validation Commands

Execute these commands in sequence to validate with zero regressions:

```bash
# 1. Validate YAML syntax for Jinja2 template
python3 -c "import yaml; yaml.safe_load(open('tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/verbose-yaml-structured.md.j2')); print('✓ Template YAML valid')"

# 2. Validate YAML syntax for rendered file
python3 -c "import yaml; yaml.safe_load(open('.claude/output-styles/verbose-yaml-structured.md')); print('✓ Rendered YAML valid')"

# 3. Verify file existence and permissions
ls -lah tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/verbose-yaml-structured.md.j2
ls -lah .claude/output-styles/verbose-yaml-structured.md

# 4. Compare content structure (ensure both files have same structure)
python3 << 'EOF'
import yaml

template = yaml.safe_load(open('tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/verbose-yaml-structured.md.j2'))
rendered = yaml.safe_load(open('.claude/output-styles/verbose-yaml-structured.md'))

print(f"Template keys: {sorted(template.keys())}")
print(f"Rendered keys: {sorted(rendered.keys())}")
assert template.keys() == rendered.keys(), "Key mismatch!"
print("✓ Structure matches between files")
EOF

# 5. Smoke test - verify no regression in other output styles
python3 -c "
import os
import yaml
output_styles_dir = 'tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/'
for f in os.listdir(output_styles_dir):
    if f.endswith('.md.j2'):
        try:
            yaml.safe_load(open(os.path.join(output_styles_dir, f)))
            print(f'✓ {f} valid')
        except Exception as e:
            print(f'✗ {f} invalid: {e}')
"
```

## Notes

### Design Decisions

1. **YAML 1.1 Standard**: Using YAML 1.1 for maximum compatibility with PyYAML, which is already in project dependencies
2. **No Jinja2 Variables**: Following the established pattern where output-style templates are static instructional files with no dynamic variables
3. **Markdown Wrapper**: The YAML content is wrapped in a markdown code block for documentation purposes (similar to other output-style templates)
4. **Static Content**: No configuration variability needed—output styles are fixed guidelines for Claude's behavior

### Future Considerations

- If YAML 1.2 support is needed in future, can upgrade once PyYAML adds full YAML 1.2 support
- Additional output styles can follow the same YAML pattern (e.g., concise-yaml-ultra)
- The YAML structure can serve as basis for programmatic configuration in agentic workflows

### Quality Assurance

- Test YAML parsing with real-world PyYAML usage patterns
- Verify no content loss or semantic changes during Markdown-to-YAML conversion
- Ensure consistency with established naming conventions and directory structure
- Confirm integration with existing output-style ecosystem (no conflicts or dependencies)
