# FLAGS.md — Generator Flags

## gen_docstring_jsdocs.py
Typical options:
- `--root .`
- `--mode augment`
- `--languages python,typescript`
- `--changed-only`
- `--dry-run`
- `--docs-dir <docs-dir>`
- `--tag-taxonomy-file <path-to-json>`

## gen_docs_fractal.py
Typical options:
- `--root .`
- `--docs-dir <docs-dir>`
- `--include-root <source-dir>`
- `--max-depth 5`
- `--merge-existing-readmes`
- `--dry-run`
- `--tag-taxonomy-file <path-to-json>`

## Recommended presets
- Local dev: changed-only + dry-run
- CI: full run, deterministic, fail on diff