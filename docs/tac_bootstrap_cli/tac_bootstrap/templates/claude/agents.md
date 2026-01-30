---
doc_type: folder
domain: agents/claude/templates/tac_bootstrap_cli
owner: UNKNOWN
level: L3
tags:
  - expert:backend
  - level:L3
  - topic:api
idk:
  - agent-templates
  - context-bundles
  - hook-logs
  - security-logs
  - template-infrastructure
  - cli-generation
  - jinja2-templates
  - agent-scaffolding
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/agents
children: []
source_readmes: []
last_reviewed: 2026-01-30
---

# Overview

The agents folder contains the template for the Claude agent, which is used to manage routes in the frontend.

# Responsibilities

* Manage route configuration and routing logic.
* Handle incoming requests and send responses.
* Maintain state and session data.

# Key APIs / Components

* `AgentTemplate`: responsible for rendering the agent template.
* `RouteConfigurator`: configures routes for the agent.
* `FrontendRouting`: handles frontend routing logic.

# Invariants & Contracts

* The agent must always be in a valid state.
* Route configuration must be consistent with the agent's state.

# Side Effects & IO

* Reads and writes to file system (template files).
* Handles incoming requests and sends responses.

# Operational Notes (perf, scaling, failure)

* Use caching to improve performance.
* Implement failover mechanisms for route configuration.
* Monitor agent performance and adjust as needed.

# TODO / Gaps

* Implement support for multiple routes per agent.
