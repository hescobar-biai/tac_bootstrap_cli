---
doc_type: folder
domain: tac-bootstrap-cli-claude
owner: UNKNOWN
level: L3
tags:
  - expert:frontend
  - level:L3
  - topic:routing
idk:
  - routing-engine
  - request-response
  - route-mapping
  - url-normalization
  - path-parsing
related_code: ['tac_bootstrap_cli/tac_bootstrap/templates/claude']
children:
  - docs/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents.md
  - docs/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands.md
  - docs/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks.md
  - docs/tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles.md
source_readmes:
  - README.md
last_reviewed: UNKNOWN
---

# Overview

The Claude routing folder contains the routing engine and related components.

# Responsibilities

* Handle incoming requests and route them to appropriate handlers.
* Manage URL normalization, path parsing, and request-response handling.

# Key APIs / Components

* Routing Engine
* Request-Response Handler
* Route Mapping System
* URL Normalization Service
* Path Parsing Component

# Invariants & Contracts

* All routes must be defined in the route mapping system.
* The routing engine must handle all types of requests (GET, POST, PUT, DELETE).

# Side Effects & IO

* The routing engine performs I/O operations on the request-response handler.
* The route mapping system updates the routing table.

# Operational Notes (perf, scaling, failure)

* The routing engine is designed for high performance and scalability.
* In case of failure, the routing engine will retry failed requests.

# TODO / Gaps

* Implement support for WebSockets.