---
doc_type: folder
domain: tac-bootstrap_cli/mypy_cache/3.10/tac_bootstrap/application
owner: UNKNOWN
level: L4
tags:
  - expert:backend
  - level:L4
  - topic:db
idk:
  - caching
  - db
  - mypy
  - performance
  - python
  - routing
  - typescript
related_code:
  - tac_bootstrap_cli/
  - tac_bootstrap/application/
children:
  - 
children_docs:
  - 
source_readmes:
  - README.md
last_reviewed: UNKNOWN
---

# Overview

This folder contains the application-level cache for the Tac Bootstrap CLI.

# Responsibilities

* Cache application data
* Enforce performance and scalability constraints

# Key APIs / Components

* `mypy_cache`: caching layer for Python code analysis
* `db`: database abstraction layer
* `routing`: routing mechanism for API requests

# Invariants & Contracts

* Cache is updated on every code change
* Cache is invalidated on every deployment

# Side Effects & IO

* Cache writes to disk on every update
* Cache reads from disk on every request

# Operational Notes (perf, scaling, failure)

* Cache size is capped at 100MB to prevent performance degradation
* Cache is periodically cleared to maintain freshness

# TODO / Gaps

* Investigate using a more efficient caching algorithm