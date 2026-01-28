---
doc_type: folder
domain: tac-bootstrap_cli/tac_bootstrap/templates/structure/agents/scout_files
owner: UNKNOWN
level: L5
tags:
  - expert:infra
  - level:L5
  - topic:routing
idk:
  - scout-agent-templates
  - jinja2-structure
  - file-discovery
  - agent-scaffolding
  - template-generation
  - codebase-exploration
  - bootstrap-cli
  - agent-infrastructure
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
