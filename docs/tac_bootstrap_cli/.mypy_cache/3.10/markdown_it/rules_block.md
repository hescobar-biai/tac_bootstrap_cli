---
doc_type: folder
domain: tac-bootstrap_cli/mypy_cache/3.10/markdown_it/rules_block
owner: UNKNOWN
level: L2
tags:
  - expert:frontend
  - level:L2
  - topic:routing
idk:
  - routing
  - caching
  - performance
  - api
  - queue
  - db
  - auth
  - logging
related_code:
  - tac_bootstrap_cli/
children:
  - 
source_readmes:
  - README.md
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