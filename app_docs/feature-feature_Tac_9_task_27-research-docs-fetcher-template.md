---
doc_type: feature
adw_id: feature_Tac_9_task_27
date: 2026-01-26
idk:
  - jinja2-template
  - agent-definition
  - documentation-research
  - template-repository
  - language-agnostic
  - pytest
tags:
  - feature
  - agent-template
  - documentation
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/research-docs-fetcher.md.j2
  - tac_bootstrap_cli/tests/test_template_repo.py
---

# Research-Docs-Fetcher Agent Template

**ADW ID:** feature_Tac_9_task_27
**Date:** 2026-01-26
**Specification:** specs/issue-268-adw-feature_Tac_9_task_27-sdlc_planner-research-docs-fetcher-template.md

## Overview

Added a new Jinja2 agent template for the research-docs-fetcher agent, which specializes in researching and discovering documentation sources. This agent helps projects identify where to find official documentation for libraries, frameworks, and tools, evaluate documentation quality, and fetch relevant content from various sources.

## What Was Built

- **Jinja2 Agent Template**: Created `research-docs-fetcher.md.j2` template following the established minimal templating pattern
- **Comprehensive Agent Definition**: 357-line agent specification covering research workflows, documentation discovery strategies, and ecosystem-specific guidance
- **Language-Agnostic Design**: Agent works across Python, TypeScript, Go, Rust, Java and other ecosystems
- **Unit Tests**: Added 3 comprehensive test methods to verify template rendering and project name substitution
- **Documentation Structures**: Defined recommended file organization and documentation format standards

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/research-docs-fetcher.md.j2`: New Jinja2 template (357 lines)
- `tac_bootstrap_cli/tests/test_template_repo.py`: Added 3 test methods in `TestAgentTemplates` class (lines 629-722)
- `specs/issue-268-adw-feature_Tac_9_task_27-sdlc_planner-research-docs-fetcher-template.md`: Feature specification
- `specs/issue-268-adw-feature_Tac_9_task_27-sdlc_planner-research-docs-fetcher-template-checklist.md`: Implementation checklist

### Key Changes

1. **Template Structure**: Follows the same pattern as `docs-scraper.md.j2` with minimal Jinja2 templating (only `{{ config.project.name }}` substitution)

2. **Agent Capabilities**: The research-docs-fetcher agent provides:
   - Research and discovery workflows for finding documentation
   - Quality evaluation criteria for documentation sources
   - Ecosystem-specific strategies (Python/PyPI, JavaScript/npm, Go/pkg.go.dev, Rust/crates.io, Java/Maven)
   - Structured documentation organization recommendations
   - Example workflows for common research tasks

3. **Key Differences from docs-scraper**:
   - **docs-scraper**: Takes known URLs and scrapes/processes documentation
   - **research-docs-fetcher**: Actively researches WHERE to find documentation, evaluates sources, then fetches

4. **Test Coverage**: Added three unit tests:
   - `test_research_docs_fetcher_template_renders()`: Verifies template renders without errors
   - `test_research_docs_fetcher_template_substitutes_project_name()`: Verifies project name substitution works correctly
   - `test_research_docs_fetcher_template_is_language_agnostic()`: Verifies template works across Python, TypeScript, and Go

## How to Use

### Generate Project with Research-Docs-Fetcher Agent

When using the TAC Bootstrap CLI to generate a new project, the research-docs-fetcher agent will be available in the generated `.claude/agents/` directory:

```bash
# Generate a new project (agent template will be included automatically)
uv run tac-bootstrap generate my-project --language python --package-manager uv
```

### Use the Agent in Generated Projects

Once the project is generated, the research-docs-fetcher agent can be used to research documentation:

```bash
# In the generated project, use the agent to research documentation
# (Specific usage depends on Claude Code integration)
```

### Template Rendering

The template can be rendered programmatically using the TemplateRepository:

```python
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import TACConfig, ProjectSpec, Language, PackageManager

config = TACConfig(
    project=ProjectSpec(
        name="my-project",
        language=Language.PYTHON,
        package_manager=PackageManager.UV,
    ),
    # ... other config
)

repo = TemplateRepository()
content = repo.render("claude/agents/research-docs-fetcher.md.j2", config)
```

## Configuration

No additional configuration is required. The template uses minimal Jinja2 templating:

- `{{ config.project.name }}`: Substituted with the project name from TACConfig

The agent definition is language-agnostic and works across all supported ecosystems without conditional logic.

## Testing

### Run All Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_template_repo.py::TestAgentTemplates::test_research_docs_fetcher_template_renders -v
```

### Run Specific Test Cases

```bash
# Test template rendering
cd tac_bootstrap_cli && uv run pytest tests/test_template_repo.py::TestAgentTemplates::test_research_docs_fetcher_template_renders -v

# Test project name substitution
cd tac_bootstrap_cli && uv run pytest tests/test_template_repo.py::TestAgentTemplates::test_research_docs_fetcher_template_substitutes_project_name -v

# Test language-agnostic design
cd tac_bootstrap_cli && uv run pytest tests/test_template_repo.py::TestAgentTemplates::test_research_docs_fetcher_template_is_language_agnostic -v
```

### Run All Template Repository Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_template_repo.py -v
```

### Validation Commands

```bash
# Run all tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Run linting
cd tac_bootstrap_cli && uv run ruff check .

# Run type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test CLI
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Agent Workflow Sections

The research-docs-fetcher agent includes comprehensive instructions covering:

1. **Research Documentation Sources**: Identification process for what needs documentation
2. **Discover Documentation Locations**: Strategies for libraries/frameworks, APIs, and platforms
3. **Evaluate Documentation Quality**: Quality indicators and warning signs
4. **Fetch Discovered Documentation**: Methods for retrieving documentation from various sources
5. **Structure and Save Documentation**: Recommended directory structure and file format
6. **Navigate Dependency Documentation**: Automatic research of project dependencies

### Ecosystem-Specific Guidance

The agent provides tailored research strategies for:
- **Python**: PyPI, Read the Docs, docs/documentation folders
- **JavaScript/TypeScript**: npm registry, dedicated docs sites, DefinitelyTyped
- **Go**: pkg.go.dev, README docs, examples/ folders
- **Rust**: docs.rs, crates.io, generated documentation
- **Java**: Maven Central, Javadoc, GitHub Pages, Spring guides

### Example Workflows

The agent includes 4 detailed example workflows:
1. Research new library documentation (FastAPI example)
2. Research API documentation (Stripe API example)
3. Research project dependencies (package.json example)
4. Research ecosystem documentation (React ecosystem example)

### Template Discovery

The template is automatically discoverable via `TemplateRepository.list_templates("claude")` and can be rendered using the standard template rendering infrastructure.

### Related Templates

This is the third agent template in TAC Bootstrap:
- `docs-scraper.md.j2`: Scrapes known documentation URLs
- `meta-agent.md.j2`: Meta-agent for orchestrating other agents
- `research-docs-fetcher.md.j2`: Researches and discovers documentation sources (this feature)
