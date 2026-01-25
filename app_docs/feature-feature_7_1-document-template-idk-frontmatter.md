---
doc_type: feature
adw_id: feature_7_1
date: 2026-01-24
idk:
  - frontmatter
  - IDK
  - YAML
  - documentation-template
  - jinja2
  - semantic-search
  - canonical-vocabulary
  - metadata
tags:
  - feature
  - documentation
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/document.md.j2
  - .claude/commands/document.md
---

# Document Template IDK Frontmatter Enhancement

**ADW ID:** feature_7_1
**Date:** 2026-01-24
**Specification:** specs/issue-184-adw-feature_7_1-sdlc_planner-improve-document-template-frontmatter.md

## Overview

Enhanced the `/document` command template to include YAML frontmatter with IDK (Information Dense Keywords) metadata, making generated feature documentation semantically searchable and indexable. The improved template guides agents to extract domain-relevant keywords from implemented code, reference canonical terminology when available, and include executable testing commands.

## What Was Built

- YAML frontmatter structure for feature documentation including doc_type, adw_id, date, IDK keywords, tags, and related_code fields
- New instruction step for IDK keyword extraction (3-8 keywords) with canonical_idk.yml integration
- Enhanced documentation format with Testing section template
- Integration with conditional_docs.md update workflow
- Synchronized changes between Jinja2 template and rendered command file

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/document.md.j2`: Added YAML frontmatter structure to documentation format with Jinja2 variables for adw_id and capability; added instructions for IDK keyword extraction and Testing section
- `.claude/commands/document.md`: Synchronized rendered version of the template with Spanish language preservation, including frontmatter structure and new agent instructions

### Key Changes

- Added frontmatter block at the beginning of Documentation Format section with hardcoded `---` delimiters
- Introduced new instruction step 3 "Extraer Keywords IDK" to guide agents in extracting 3-8 keywords with canonical_idk.yml integration
- Renumbered subsequent instruction steps (4. Generar Documentación, 5. Actualizar Documentación Condicional)
- Enhanced documentation format with standardized Testing section showing executable bash command examples
- Integrated Jinja2 variables `{{ config.adw_id | default('N/A') }}` and `{{ config.capability | default('general') }}` in frontmatter
- Removed conditional test command rendering in favor of freeform executable command placeholders
- Added explicit instruction for agents to update conditional_docs.md after creating documentation

## How to Use

When generating feature documentation using the `/document` command:

1. Run `/document <adw_id> <spec_path>` in a TAC Bootstrap project
2. The agent will analyze git diff, extract 3-8 IDK keywords from code changes
3. If `canonical_idk.yml` exists, keywords will prioritize canonical terms and supplement with feature-specific ones
4. Generated documentation will include YAML frontmatter with metadata
5. Documentation file will be created in `app_docs/` directory
6. Agent will automatically update `.claude/commands/conditional_docs.md` with entry for the new file

Example command:
```bash
/document feature_7_1 specs/issue-184-adw-feature_7_1-sdlc_planner-improve-document-template-frontmatter.md
```

## Configuration

The frontmatter uses the following Jinja2 template variables from `config.yml`:

- `config.adw_id`: ADW workflow identifier (defaults to "N/A")
- `config.capability`: Feature capability category (defaults to "general")
- `config.paths.app_docs_dir`: Documentation output directory (defaults to "app_docs")

No additional configuration is required. The template gracefully handles missing canonical_idk.yml files.

## Testing

Verify template renders correctly with test configuration:

```bash
cd tac_bootstrap_cli && uv run python -c "
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import TACConfig, ProjectSpec, PathsSpec, Language
config = TACConfig(
    project=ProjectSpec(name='test-project', language=Language.PYTHON),
    paths=PathsSpec()
)
repo = TemplateRepository()
output = repo.render('claude/commands/document.md.j2', {'config': config})
print(output[:800])
"
```

Validate YAML frontmatter syntax:

```bash
cd tac_bootstrap_cli && python -c "
import yaml
frontmatter_sample = '''---
doc_type: feature
adw_id: test_123
date: 2026-01-24
idk:
  - keyword1
  - keyword2
tags:
  - feature
  - general
related_code:
  - src/file.py
---'''
parsed = yaml.safe_load(frontmatter_sample.split('---')[1])
assert parsed['doc_type'] == 'feature'
assert isinstance(parsed['idk'], list)
print('Frontmatter YAML is valid ✓')
"
```

Run standard validation suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Verify CLI help renders correctly:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

This enhancement transforms plain feature documentation into structured, metadata-rich documents that integrate with the fractal documentation system. The IDK keywords enable better discoverability and semantic search by AI agents.

The template design prioritizes backward compatibility - projects without canonical_idk.yml files will work correctly, with agents extracting feature-specific keywords directly from code analysis.

The frontmatter structure follows standard YAML syntax and is designed to be both human-readable and machine-parseable for future integration with documentation indexing and search systems.
