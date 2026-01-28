---
doc_type: folder
domain: tac-bootstrap_cli/mypy_cache/3.10/markdown_it/presets
owner: UNKNOWN
level: L5
tags:
  - expert:backend
  - level:L5
  - topic:caching
idk:
  - mypy-cache
  - type-checking-artifacts
  - markdown-it-library
  - python-3.10
  - presets-module
  - build-cache
  - type-inference
  - metadata-storage
related_code:
  - tac_bootstrap_cli/.mypy_cache/3.10/markdown_it/presets
children: []
source_readmes: []
last_reviewed: UNKNOWN
---

# Overview

This folder contains Markdown presets for the `markdown-it` library.

# Responsibilities

* Generate Markdown presets for `markdown-it`.
* Cache presets for faster rendering.

# Key APIs / Components

* `markdown_it`
* `preset`

# Invariants & Contracts

* Presets are cached in memory.
* Presets are re-generated on every build.

# Side Effects & IO

* Reads from `README.md` for source readme.
* Writes to `README.md` for updated readme.

# Operational Notes (perf, scaling, failure)

* Presets can be re-generated on every build.
* Caching improves rendering performance.

# TODO / Gaps

* Add support for other Markdown formats.
