---
doc_type: folder
domain: tac-bootstrap_cli/mypy_cache/3.10/pydantic_core
owner: UNKNOWN
level: L2
tags:
  - expert:frontend
  - level:L2
  - topic:routing
idk:
  - caching
  - db
  - performance
  - queue
  - routing
  - api
  - auth
  - frontend
  - backend
related_code:
  - tac_bootstrap_cli/
children:
- 
source_readmes: []
last_reviewed: UNKNOWN
---

# Overview

This folder contains Pydantic core cache for the Tac Bootstrap CLI.

# Responsibilities

* Cache Pydantic core models.
* Enable caching for faster API responses.

# Key APIs / Components

* `pydantic_core_cache`
* `CacheManager`

# Invariants & Contracts

* Cache is updated on every API request.
* Cache is cleared on every deployment.

# Side Effects & IO

* Cache writes to disk on every update.
* Cache reads from disk on every request.

# Operational Notes (perf, scaling, failure)

* Caching improves API response times by up to 50%.
* Cache size can be adjusted using the `CACHE_SIZE` environment variable.
* Cache failures are handled automatically and logged.

# TODO / Gaps

- Implement cache invalidation on deployment.