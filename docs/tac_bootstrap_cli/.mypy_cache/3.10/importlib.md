---
doc_type: folder
domain: tac-bootstrap-cli-mypy-cache-3-10-importlib
owner: UNKNOWN
level: L2
tags:
  - expert:frontend
  - level:L2
  - topic:routing
idk:
  - python
  - mypy
  - cache
  - importlib
  - typing
  - module
  - package
related_code:
  - tac_bootstrap_cli/
  - docs/tac_bootstrap_cli/.mypy_cache/3.10/importlib/metadata.md
source_readmes: []
last_reviewed: UNKNOWN
---

# Overview

Mypy Cache for Tac Bootstrap CLI

## Responsibilities

* Cache imports for Tac Bootstrap CLI
* Enable type checking for Tac Bootstrap CLI

## Key APIs / Components

* `importlib.metadata`
* `mypy`

## Invariants & Contracts

* Cache is updated on import changes
* Type checking is enabled by default

## Side Effects & IO

* Reads import metadata from cache
* Writes import metadata to cache on update

## Operational Notes (perf, scaling, failure)

* Caching can improve performance for large imports
* Cache size can be adjusted for optimal performance

## TODO / Gaps

* Add support for other import types (e.g. `__init__.py`)