---
doc_type: folder
domain: tac-bootstrap_cli/mypy_cache/3.10/_typeshed
owner: UNKNOWN
level: L4
tags:
  - expert:infra
  - level:L4
  - topic:caching
idk:
  - cache-layer
  - mypy-cache
  - typeshed
  - repo-folder
  - folder-organization
  - cli-integration
  - type-checking
related_code:
  - tac_bootstrap_cli
children:
  - 
---
# Overview

This folder contains the cached typeshed for the tac-bootstrap CLI.

# Responsibilities

The primary responsibility of this folder is to store and manage the cached typeshed, which enables faster type checking for the CLI.

# Key APIs / Components

* `mypy_cache`
* `_typeshed`

# Invariants & Contracts

* The cache is updated periodically.
* The cache is used to speed up type checking.

# Side Effects & IO

* No side effects.
* Input: None.
* Output: Cached typeshed.

# Operational Notes (perf, scaling, failure)

* Performance: The cache can significantly improve performance during type checking.
* Scaling: The cache can be scaled horizontally by adding more machines to the cluster.
* Failure: If the cache is not updated periodically, it may become outdated and cause errors.

# TODO / Gaps

* Investigate ways to improve cache invalidation.