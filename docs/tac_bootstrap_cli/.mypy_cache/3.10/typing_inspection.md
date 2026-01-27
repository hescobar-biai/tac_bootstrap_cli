---
doc_type: folder
domain: tac-bootstrap_cli/mypy_cache/3.10/typing_inspection
owner: UNKNOWN
level: L4
tags:
  - expert:infra
  - level:L4
  - topic:caching
idk:
  - caching-layer
  - type-checking
  - mypy-cache
  - python-3.10
  - typing-inspection
  - cache-management
  - static-type-checking
related_code:
  - tac_bootstrap_cli/
children:
  -
    path: tac_bootstrap_cli/tac-bootstrap-cli/
  -
    path: tac_bootstrap_cli/tac-bootstrap-cli/docs/
source_readmes:
  - README.md
last_reviewed: UNKNOWN
---

# Overview

Caching layer for Python type checking.

# Responsibilities

Manage caching for Python type checking.

# Key APIs / Components

* `mypy_cache`
* `typing_inspection`

# Invariants & Contracts

* Cache contents are valid for the duration of the cache.
* Cache is updated periodically to reflect changes in dependencies.

# Side Effects & IO

* Reads/writes to cache directory.
* Updates cache on dependency changes.

# Operational Notes (perf, scaling, failure)

* Cache size can be adjusted via configuration options.
* Cache updates occur asynchronously.

# TODO / Gaps

* Investigate cache eviction strategies.