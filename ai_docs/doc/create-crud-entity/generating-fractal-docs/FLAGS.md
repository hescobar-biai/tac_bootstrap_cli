# FLAGS.md — Generator Flags

## gen_docstring_jsdocs.py
Typical options:
- `--root .`
- `--mode augment`
- `--languages python,typescript`
- `--changed-only`
- `--dry-run`

## gen_docs_fractal.py
Typical options:
- `--root .`
- `--docs-dir docs/`
- `--max-depth 5`
- `--merge-existing-readmes`
- `--dry-run`

## Recommended presets
- Local dev: changed-only + dry-run
- CI: full run, deterministic, fail on diff