---
doc_type: folder
domain: tac-bootstrap_cli/mypy_cache/3.10/markdown_it/rules_block
owner: UNKNOWN
level: L5
tags:
  - expert:backend
  - level:L5
  - topic:caching
idk:
  - mypy-cache-artifact
  - python-3.10-typecheck
  - markdown-it-parser
  - block-rule-metadata
  - incremental-type-cache
  - ast-cache-storage
  - type-inference-cache
  - markdown-block-grammar
  - parser-rule-stubs
  - cached-module-analysis
related_code:
  - tac_bootstrap_cli/.mypy_cache/3.10/markdown_it/rules_block
children: []
source_readmes: []
last_reviewed: UNKNOWN
---

# Overview

This folder contains routing rules for the frontend.

# Responsibilities

* Handle incoming requests and route them to appropriate components.

# Key APIs / Components

* `rules_block`
* `router`

# Invariants & Contracts

* All routes must be defined in this file.
* The router will only handle GET, POST, PUT, and DELETE requests.

# Side Effects & IO

* This folder has no side effects.
* It reads from the `tac_bootstrap_cli/` repository.

# Operational Notes (perf, scaling, failure)

* This folder is designed to be highly performant.
* It can scale horizontally by adding more instances of the router.

# TODO / Gaps

* Add support for PATCH requests.
