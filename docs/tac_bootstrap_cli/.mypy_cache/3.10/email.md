---
doc_type: folder
domain: tac-bootstrap_cli/mypy_cache/3.10/email
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
related_code:
  - tac_bootstrap_cli/
children:
- 
source_readmes:
- README.md
last_reviewed: UNKNOWN
---

# Overview

Email routing in Tac Bootstrap CLI.

## Responsibilities

Route emails to their respective destinations.

## Key APIs / Components

* `email-routing`
* `caching`

## Invariants & Contracts

* All emails are routed correctly.
* Caching is enabled for performance.

## Side Effects & IO

* Email routing: reads from email database, writes to destination folders.
* Caching: reads from cache store, writes to cache store.

## Operational Notes (perf, scaling, failure)

* Use caching for improved performance.
* Scale email routing by increasing worker count.

## TODO / Gaps

- Implement support for multiple email providers.