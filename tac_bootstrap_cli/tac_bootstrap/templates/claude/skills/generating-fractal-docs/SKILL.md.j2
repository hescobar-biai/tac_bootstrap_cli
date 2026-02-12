---
name: generating-fractal-docs
description: Run deterministic documentation generators (docstrings/JSDoc → fractal docs) bundled with this skill. Use to bootstrap or refresh repo documentation safely.
allowed-tools: Read, Grep, Glob, Bash(python:*)
---

# Generating Fractal Docs (Docstrings → Fractal Docs)

## What this skill does
Runs **two deterministic generators**, bundled inside this skill, in the correct order:

1) `scripts/gen_docstring_jsdocs.py`
2) `scripts/gen_docs_fractal.py`

The goal is to:
- enrich code with **information-dense docstrings/JSDoc**
- generate **fractal documentation** under the project's docs directory
- keep token usage minimal and structure stable

## Input

Configuration is read from the invoking spec's frontmatter or project context:

| Field | Description | Example |
|-------|-------------|---------|
| `docs_dir` | Output directory for generated docs | `docs/` |
| `source_dirs` | Source directories to scan | `["src/", "frontend/"]` |
| `include_root` | Root folder to document (passed to `gen_docs_fractal.py --include-root`) | `src` |
| `tag_taxonomy_file` | Path to a JSON file with custom tag taxonomy (array of strings) | `config/tags.json` |

If no spec is provided, the scripts fall back to built-in defaults: current directory for source, `docs/` for output, `src` for include-root, and a general-purpose tag taxonomy.

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
```bash
bash .claude/skills/generating-fractal-docs/scripts/run_generators.sh
