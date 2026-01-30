---
doc_type: folder
domain: tac-bootstrap_cli/mypy_cache/3.10/pydantic/deprecated
owner: UNKNOWN
level: L5
tags:
  - expert:backend
  - level:L5
  - topic:api
idk:
  - mypy-cache
  - pydantic-deprecated
  - type-checking-artifacts
  - python-3.10
  - static-analysis-cache
  - type-stubs-deprecated
  - pydantic-v1-compat
  - incremental-type-check
  - legacy-pydantic-types
  - backwards-compatibility
  - deprecation-warnings
related_code:
  - tac_bootstrap_cli/.mypy_cache/3.10/pydantic/deprecated
children: []
source_readmes: []
last_reviewed: 2026-01-30
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
