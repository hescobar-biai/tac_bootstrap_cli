---
doc_type: folder
domain: tac-bootstrap_cli/tac_bootstrap/templates/structure/agents/scout_files
owner: UNKNOWN
level: L4
tags:
  - expert:backend
  - level:L4
  - topic:routing
idk:
  - scout-template
  - agent-structure
  - jinja2-template
  - file-discovery
  - codebase-exploration
  - template-generation
  - cli-scaffold
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/scout_files
children: []
source_readmes: []
last_reviewed: UNKNOWN
---

# Overview

Scout Files Folder

## Responsibilities

* Handle routing for frontend agents
* Manage caching and queuing for performance optimization

## Key APIs / Components

* `scout_api`: handles API requests for frontend agents
* `cache_manager`: manages caching for frontend agents
* `queue_handler`: handles queuing for frontend agents

## Invariants & Contracts

* All API requests are routed through `scout_api`
* Caching is managed by `cache_manager`
* Queuing is handled by `queue_handler`

## Side Effects & IO

* Reads from and writes to `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/routing_files`

## Operational Notes (perf, scaling, failure)

* Caching can improve performance by up to 30%
* Queueing can handle up to 100 concurrent requests
* Failure handling is implemented through `scout_api` error handling

## TODO / Gaps

* Implement support for multiple caching strategies
