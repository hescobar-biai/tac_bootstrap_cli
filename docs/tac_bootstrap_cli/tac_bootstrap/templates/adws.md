---
doc_type: folder
domain: tac-bootstrap-cli-adws
owner: UNKNOWN
level: L3
tags:
  - expert:frontend
  - level:L3
  - topic:routing
idk:
  - adws
  - cli
  - template
  - routing
  - frontend
  - folder
related_code:
  - docs/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules.md
  - docs/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers.md
source_readmes: []
last_reviewed: UNKNOWN
---

# Overview

This is the adws folder in the tac-bootstrap-cli repository.

# Responsibilities

* Handle routing for the frontend application.
* Provide templates for the application.

# Key APIs / Components

* `adw_modules`
* `adw_triggers`

# Invariants & Contracts

* The `adw_modules` component must render the correct template.
* The `adw_triggers` component must handle routing correctly.

# Side Effects & IO

* The `adw_modules` component has no side effects.
* The `adw_triggers` component reads from the `adw_modules` component.

# Operational Notes (perf, scaling, failure)

* This folder is responsible for handling routing in the frontend application. It provides templates and handles triggers.
* Performance: The `adw_modules` component should be optimized for rendering speed.
* Scaling: The `adw_triggers` component should handle a large number of requests.
* Failure: The `adw_modules` component should handle errors correctly.

# TODO / Gaps

* Add support for caching in the `adw_modules` component.