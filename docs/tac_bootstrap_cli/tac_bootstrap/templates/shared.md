---
doc_type: folder
domain: tac-bootstrap_cli/templates/shared/tac_bootstrap_cli/templates/shared
owner: UNKNOWN
level: L3
tags:
  - expert:frontend
  - level:L3
  - topic:routing
idk:
  - routing
  - templating
  - rendering
  - templates
  - cli
  - bootstrap
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/shared/tac_bootstrap_cli/templates/shared/index.ts
children:
  - 
---
# Overview

This folder contains shared routing templates for the Tac Bootstrap CLI.

# Responsibilities

* Handle client-side routing and navigation.
* Provide a consistent templating engine for rendering routes.

# Key APIs / Components

* `index.ts`: Routing configuration and template rendering.
* `router.ts`: Client-side router instance.

# Invariants & Contracts

* All routes must be registered with the router.
* Template rendering must return a valid HTML string.

# Side Effects & IO

* Routes may modify the URL or query parameters.
* Template rendering may access external resources (e.g., APIs).

# Operational Notes (perf, scaling, failure)

* Use caching to improve performance.
* Implement retry mechanisms for failed requests.

# TODO / Gaps

* Add support for server-side routing.