---
doc_type: folder
domain: tac-bootstrap_cli/mypy_cache/3.10/pydantic/deprecated
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
  - pydantic
  - deprecated
  - cache
  - database
  - type-checking
related_code:
  - tac_bootstrap_cli/
children:
- 
source_readmes:
- README.md
last_reviewed: UNKNOWN
---

# Overview

This folder contains deprecated types and utilities for the Tac Bootstrap CLI.

# Responsibilities

* Maintain compatibility with deprecated APIs.
* Provide fallbacks for users relying on deprecated features.

# Key APIs / Components

* `mypy_cache`
* `pydantic`

# Invariants & Contracts

* All deprecated types conform to the original API contract.
* Fallback implementations are provided for all deprecated functions.

# Side Effects & IO

* This folder has no direct side effects, but users relying on deprecated features may experience unexpected behavior.

# Operational Notes (perf, scaling, failure)

* Performance: No significant performance impact expected due to deprecation.
* Scaling: No scaling implications due to this folder's nature.
* Failure: Deprecation warnings will be logged instead of errors.

# TODO / Gaps

* Investigate alternatives for `mypy_cache` and `pydantic`.