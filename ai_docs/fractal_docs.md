# Fractal Documentation System

This document describes the fractal documentation approach used in this repository, including the generators, patterns, and best practices.

## Overview

The fractal docs system maintains a hierarchical documentation tree under `docs/` that mirrors the source code structure. Documentation is generated from:

1. **Python docstrings** - Module, class, and function documentation
2. **TypeScript/TSX JSDoc** - Exported symbols documentation
3. **Existing README files** - Authoritative context for each folder

## Generators

### 1. Docstring/JSDoc Generator (`gen_docstring_jsdocs.py`)

Adds information-dense docstrings to Python and JSDoc to TypeScript code.

**Modes:**
- `add` - Add docs only where missing
- `overwrite` - Replace all docs (dangerous)
- `complement` - Append missing sections without deleting existing content

**Required Docstring Sections (Python):**
- `Purpose:` - One-line description
- `Tags:` - Comma-separated allowed tags
- `Ownership:` - Layer + MUST NOTs
- `Invariants:` - MUST/MUST NOT rules
- `Side effects:` - External impacts
- `Inputs:` - Parameters
- `Outputs:` - Return values
- `Failure modes:` - Error conditions
- `IDK:` - Information Dense Keywords (5-12 keywords)

**Required JSDoc Sections (TypeScript):**
- Purpose, Tags, Ownership, Invariants, Side effects, Failure modes, IDK

### 2. Fractal Docs Generator (`gen_docs_fractal.py`)

Generates markdown documentation per folder under `docs/`.

**Output Structure:**
```
src/backend/shared/domain  -> docs/src/backend/shared/domain.md
src/backend/shared         -> docs/src/backend/shared.md
src/backend                -> docs/src/backend.md
src                        -> docs/src.md
```

**Generation Order:** Bottom-up (deepest folders first, then parents)

**Merge Strategy (complement mode):**
- Frontmatter is normalized/updated
- Existing body is preserved
- Missing sections are appended

## Frontmatter Schema

All generated docs include YAML frontmatter:

```yaml
---
doc_type: folder
domain: src.backend.shared
owner: UNKNOWN
level: L3
tags:
  - expert:backend
  - topic:api
idk:
  - cqrs
  - domain-events
  - repository-pattern
related_code:
  - src/backend/shared
children:
  - docs/src/backend/shared/domain.md
source_readmes:
  - src/backend/shared/README.md
last_reviewed: UNKNOWN
---
```

## Tag Taxonomy

Allowed tags for classification:

**Expert Tags:**
- `expert:backend`, `expert:frontend`, `expert:data`, `expert:infra`, `expert:observability`

**Level Tags:**
- `level:L1` through `level:L5` (depth-based, deeper = higher L)

**Topic Tags:**
- `topic:auth`, `topic:routing`, `topic:logging`, `topic:db`, `topic:caching`
- `topic:queue`, `topic:api`, `topic:performance`

## IDK (Information Dense Keywords)

IDK lines provide rapid context retrieval for AI agents and search.

**Rules:**
- 5-12 keywords per symbol/folder
- NO sentences, NO verbs, NO filler words
- Use canonical technical nouns
- kebab-case format (allow `-` and `/`)
- Prefer terms from existing canonical IDK lists

**Examples:**
```
IDK: cqrs, outbox, idempotency, transactions, correlation-id
IDK: routing, api, validation, structured-logging, health-check
```

## Required Document Sections

Each folder doc must include:

1. **Overview** - Brief purpose statement
2. **Responsibilities** - What this module owns
3. **Key APIs / Components** - Bulleted list of main exports
4. **Invariants & Contracts** - MUST/MUST NOT rules
5. **Side Effects & IO** - External interactions
6. **Operational Notes** - Performance, scaling, failure behavior
7. **TODO / Gaps** - Only if gaps exist

## Running the Generators

### Standard Run
```bash
bash .claude/skills/generating-fractal-docs/scripts/run_generators.sh --repo .
```

### With Dry Run
```bash
bash .claude/skills/generating-fractal-docs/scripts/run_generators.sh --repo . --dry-run
```

### Auto-Branch (Safe for CI)
```bash
bash .claude/skills/generating-fractal-docs/scripts/run_generators.sh --repo . --auto-branch
```

## Generator Flags

### gen_docstring_jsdocs.py

| Flag | Description |
|------|-------------|
| `--repo` | Repository root path |
| `--include-glob` | Glob pattern to filter files |
| `--mode` | `add`, `overwrite`, or `complement` |
| `--dry-run` | Preview changes without writing |
| `--no-backup` | Skip creating .bak files |
| `--snippet-lines` | Lines of context for LLM (default: 220) |
| `--base-url` | OpenAI-compatible API base URL |
| `--api-key` | API key |
| `--model` | Model name |

### gen_docs_fractal.py

| Flag | Description |
|------|-------------|
| `--repo` | Repository root path |
| `--docs-root` | Output directory (default: `docs`) |
| `--include-root` | Source folder to document (default: `src`) |
| `--mode` | `overwrite` or `complement` |
| `--dry-run` | Preview changes without writing |
| `--max-tokens` | LLM max tokens (default: 1200) |

## Recommended Presets

### Local Development
```bash
--mode complement --dry-run
```
Preview changes, complement existing docs.

### CI Pipeline
```bash
--mode complement --auto-branch
```
Full run, deterministic, fail on unexpected diff.

## When to Regenerate

Run fractal docs generators:
- After refactors or file moves
- Before creating new AI experts
- When docs drift from code reality
- After significant feature additions

## Ignored Directories

The generators skip:
- `.git`, `node_modules`, `.venv`, `venv`
- `__pycache__`, `dist`, `build`
- `.next`, `.turbo`, `.cache`
- `target`, `vendor`, `.idea`, `.vscode`

## OpenAI-Compatible API Support

Both generators support any OpenAI-compatible API:

```bash
# OpenAI
--base-url https://api.openai.com/v1 --api-key $OPENAI_API_KEY --model gpt-4.1-mini

# Ollama (local)
--base-url http://localhost:11434/v1 --api-key ollama --model cogito:8b

# LM Studio
--base-url http://localhost:1234/v1 --api-key lm-studio --model local-model
```

## Best Practices

1. **Conservative by default** - Always use `complement` mode unless explicitly rebuilding
2. **Review before commit** - Check `git diff` after generation
3. **Preserve human context** - Generators merge, not replace
4. **Keep IDK focused** - Quality over quantity in keywords
5. **Document invariants** - MUST/MUST NOT rules prevent regressions
6. **Clean git state** - Commit or stash changes before running generators
