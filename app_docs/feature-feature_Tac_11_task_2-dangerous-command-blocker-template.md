---
doc_type: feature
adw_id: feature_Tac_11_task_2
date: 2026-01-27
idk:
  - jinja2-template
  - security-hook
  - package-manager
  - code-generation
  - dangerous-command-blocker
  - cli-generator
tags:
  - feature
  - security
  - templates
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/dangerous_command_blocker.py.j2
  - tac_bootstrap_cli/tac_bootstrap/domain/models.py
---

# Dangerous Command Blocker Template

**ADW ID:** feature_Tac_11_task_2
**Date:** 2026-01-27
**Specification:** specs/issue-339-adw-feature_Tac_11_task_2-sdlc_planner-dangerous-command-blocker-template.md

## Overview

Created a Jinja2 template version of the dangerous command blocker security hook that adapts to different Python package managers (uv, pip, poetry, pipenv). This template enables TAC Bootstrap CLI to generate customized hook files for new projects with the appropriate shebang and package manager configuration.

## What Was Built

- **Jinja2 Template File**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/dangerous_command_blocker.py.j2`
- **Package Manager Adaptation**: Conditional shebang logic based on `config.project.package_manager.value`
- **Security Logic Preservation**: Complete dangerous command patterns, critical paths, and safety checks maintained unchanged
- **Specification Documentation**: Detailed spec and checklist files created

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/dangerous_command_blocker.py.j2`: New Jinja2 template with conditional shebang rendering
- `specs/issue-339-adw-feature_Tac_11_task_2-sdlc_planner-dangerous-command-blocker-template.md`: Feature specification
- `specs/issue-339-adw-feature_Tac_11_task_2-sdlc_planner-dangerous-command-blocker-template-checklist.md`: Implementation checklist

### Key Changes

- **Conditional Shebang**: Template renders different shebangs based on package manager:
  - UV: `#!/usr/bin/env -S uv run --script` with PEP 723 inline script metadata
  - Others (pip, poetry, pipenv): `#!/usr/bin/env python3`
- **Template Variable**: Uses `{{ config.project.package_manager.value }}` for package manager detection
- **Security Preservation**: All dangerous patterns (rm -rf, dd, mkfs, chmod 777, etc.) remain hardcoded and unchanged
- **Complete Implementation**: Full 292-line hook implementation with logging, validation, and safer alternatives

## How to Use

### When Generating Projects

The template is automatically used by TAC Bootstrap CLI when generating new projects:

1. CLI reads project configuration including package manager choice
2. Jinja2 renderer processes the template with project config
3. Generated hook file contains appropriate shebang for chosen package manager
4. Hook is placed in `.claude/hooks/dangerous_command_blocker.py` in target project

### Manual Template Rendering

For testing or manual use:

```python
from jinja2 import Template

# Load template
with open('tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/dangerous_command_blocker.py.j2') as f:
    template = Template(f.read())

# Render with config (example: UV package manager)
config = {
    'project': {
        'package_manager': {
            'value': 'uv'
        }
    }
}
rendered = template.render(config=config)
```

## Configuration

### Template Variables

- `config.project.package_manager.value`: Package manager identifier (`"uv"`, `"pip"`, `"poetry"`, `"pipenv"`)

### Supported Package Managers

| Package Manager | Shebang Line | PEP 723 Metadata |
|----------------|--------------|------------------|
| uv | `#!/usr/bin/env -S uv run --script` | Yes |
| pip | `#!/usr/bin/env python3` | No |
| poetry | `#!/usr/bin/env python3` | No |
| pipenv | `#!/usr/bin/env python3` | No |

### Security Features (Hardcoded)

All security logic remains constant across package managers:
- Dangerous command patterns (rm -rf, dd, mkfs, chmod 777, etc.)
- Critical path protections (/, /etc, /usr, /home, etc.)
- Safer alternative suggestions
- Security audit logging to `agents/security_logs/blocked_commands.jsonl`

## Testing

### Validate Template Syntax

Verify Jinja2 syntax is correct:

```bash
cd tac_bootstrap_cli && uv run python -c "from jinja2 import Template; Template(open('tac_bootstrap/templates/claude/hooks/dangerous_command_blocker.py.j2').read())"
```

### Run Unit Tests

Execute all tests to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Lint and Type Check

Verify code quality:

```bash
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### CLI Smoke Test

Ensure CLI still works:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Manual Rendering Test

Test template rendering for each package manager:

```python
from jinja2 import Template

template_path = 'tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/dangerous_command_blocker.py.j2'
with open(template_path) as f:
    template = Template(f.read())

# Test UV
config_uv = {'project': {'package_manager': {'value': 'uv'}}}
rendered_uv = template.render(config=config_uv)
assert '#!/usr/bin/env -S uv run --script' in rendered_uv

# Test pip
config_pip = {'project': {'package_manager': {'value': 'pip'}}}
rendered_pip = template.render(config=config_pip)
assert '#!/usr/bin/env python3' in rendered_pip
```

## Notes

### Security-First Design
The dangerous command patterns list is intentionally hardcoded and not configurable. Security policies should be consistent across all generated projects regardless of package manager choice.

### Simple Templating
Only the shebang line requires templating. The rest of the 292-line implementation remains identical across all package managers, ensuring consistent security behavior.

### Future Enhancements
- Add comprehensive template rendering tests to test suite
- Consider extending template to support additional package managers
- Add validation to ensure package manager value is supported

### Template Pattern Consistency
This template follows the same patterns as other hook templates in the directory:
- Uses `config.project.package_manager.value` for package manager detection
- Conditional blocks with `{% if %}...{% else %}...{% endif %}`
- Preserves complete implementation without modification to core logic
