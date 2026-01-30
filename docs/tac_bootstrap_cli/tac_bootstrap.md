---
doc_type: folder
domain: tac-bootstrap-cli-core
owner: UNKNOWN
level: L3
tags:
  - expert:frontend
  - level:L3
  - topic:routing
idk:
  - cli
  - api
  - routing
  - frontend
  - performance
  - scalability
  - caching
related_code:
  - tac_bootstrap_cli/tac_bootstrap
children:
  - docs/tac_bootstrap_cli/tac_bootstrap/application.md
  - docs/tac_bootstrap_cli/tac_bootstrap/domain.md
  - docs/tac_bootstrap_cli/tac_bootstrap/infrastructure.md
  - docs/tac_bootstrap_cli/tac_bootstrap/interfaces.md
  - docs/tac_bootstrap_cli/tac_bootstrap/templates.md
source_readmes:[]
last_reviewed: 2026-01-30
---

# Overview

The `tac-bootstrap` CLI folder provides a routing system for the frontend application.

# Responsibilities

* Handle HTTP requests and responses.
* Provide routing configuration for the application.

# Key APIs / Components

* `cli`: The main CLI entry point.
* `api`: The API gateway for the application.
* `routing`: The routing configuration for the frontend application.

# Invariants & Contracts

* All routes must be defined in the `routes` file.
* The `cli` component must handle all HTTP requests.

# Side Effects & IO

* The `cli` component reads and writes data to the database.
* The `api` component handles API requests and responses.

# Operational Notes (perf, scaling, failure)

* The application uses a caching mechanism to improve performance.
* The routing configuration can be scaled horizontally using multiple instances of the `routing` component.

# TODO / Gaps

* Implement support for WebSocket connections.
