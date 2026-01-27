---
doc_type: folder
domain: tac-bootstrap_cli/mypy_cache/3.10/markdown_it/common
owner: UNKNOWN
level: L4
tags:
  - expert:frontend
  - level:L4
  - topic:routing
idk:
  - routing
  - caching
  - performance
  - api
  - frontend
  - cli
related_code:
  - tac_bootstrap_cli/
children:
  - 
source_readmes:
  - README.md
last_reviewed: UNKNOWN
---

# Overview

This folder contains Markdown documentation for the routing system in the Tac Bootstrap CLI.

# Responsibilities

The routing system is responsible for handling incoming requests and dispatching them to the correct handler.

# Key APIs / Components

* `Route`
* `Router`
* `Middleware`

# Invariants & Contracts

* All routes must have a unique path.
* The router must handle all types of HTTP requests (GET, POST, PUT, DELETE).

# Side Effects & IO

* The routing system has no side effects.
* It reads and writes to the file system.

# Operational Notes (perf, scaling, failure)

* The routing system is designed for high performance and scalability.
* In case of a failure, it will log an error message and continue running.

# TODO / Gaps

* Add support for WebSockets