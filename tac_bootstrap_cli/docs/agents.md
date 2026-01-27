# Sub-Agents & Expert Pattern

TAC Bootstrap includes specialized AI agents for autonomous task execution.

## Overview

Agents are specialized AI assistants that can be delegated specific tasks. They provide:
- Domain expertise
- Autonomous execution
- Structured workflows
- Self-improvement capabilities

## Available Agents

### docs-scraper

Fetches and integrates external documentation into project context.

**Location:** `.claude/agents/docs-scraper.md`

**Capabilities:**
- Fetch documentation from URLs
- Process HTML/Markdown/PDF content
- Extract relevant information
- Save to `ai_docs/` directory

**Use cases:**
```
Scrape the FastAPI authentication documentation
Get the React hooks reference
Fetch OpenAPI specification for Stripe API
```

**Output structure:**
```
ai_docs/
├── frameworks/     # Framework documentation
├── libraries/      # Third-party library docs
├── apis/          # API references
└── internal/      # Internal documentation
```

### meta-agent

Generates new sub-agent configuration files from descriptions.

**Location:** `.claude/agents/meta-agent.md`

**Capabilities:**
- Analyze agent requirements
- Design agent architecture
- Generate complete agent files
- Select appropriate tools and model

**Usage:**
```
Create an agent for code review
Create an agent that monitors test coverage
Design an agent for database migration management
```

**Generated structure:**
```markdown
---
name: agent-name
description: Action-oriented description
tools: Tool1, Tool2
model: sonnet
color: cyan
---

# Purpose
Agent role and capabilities.

## Instructions
Step-by-step workflow.

## Report
Output format.
```

### research-docs-fetcher

Discovers and evaluates documentation sources.

**Location:** `.claude/agents/research-docs-fetcher.md`

**Capabilities:**
- Search for official documentation
- Evaluate documentation quality
- Navigate package registries (npm, PyPI, etc.)
- Cross-reference multiple sources

**Research strategies by ecosystem:**

| Ecosystem | Primary Sources |
|-----------|-----------------|
| Python | PyPI, Read the Docs, GitHub |
| JavaScript | npm, GitHub, official sites |
| Go | pkg.go.dev, GitHub |
| Rust | docs.rs, crates.io |
| Java | Maven Central, Javadoc |

**Quality indicators:**
- Official source
- Up-to-date version
- Code examples included
- Well-structured navigation

## Expert Pattern

The expert pattern implements a **Plan-Build-Improve** cycle for specialized domains.

### Concept

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  PLAN   │ ──▶ │  BUILD  │ ──▶ │ IMPROVE │
└─────────┘     └─────────┘     └─────────┘
     │                               │
     └───────────────────────────────┘
              (feedback loop)
```

1. **Plan**: Explore requirements, design architecture, create implementation plan
2. **Build**: Execute plan, implement solution, validate functionality
3. **Improve**: Analyze results, extract learnings, update expertise

### Claude Code Hook Expert

Specialized expert for developing Claude Code hooks.

#### cc_hook_expert_plan

Plans hook implementation with structured methodology.

**Command:** `/experts:cc_hook_expert:cc_hook_expert_plan <requirements>`

**Workflow:**
1. **Understand Requirements**
   - Parse hook requirements
   - Identify hook type (PreToolUse, PostToolUse, etc.)
   - Define success criteria

2. **Explore Codebase**
   - Examine existing hooks
   - Identify patterns in settings.json
   - Find similar implementations

3. **Design Architecture**
   - Hook specification
   - Input/output design
   - Error handling strategy

4. **Create Plan**
   - Write to `specs/hook-{name}-plan.md`
   - Include implementation steps
   - Define testing strategy

**Example:**
```
/experts:cc_hook_expert:cc_hook_expert_plan Create a PreToolUse hook that validates file access patterns
```

#### cc_hook_expert_build

Implements hook based on plan.

**Command:** `/experts:cc_hook_expert:cc_hook_expert_build [plan-path]`

**Workflow:**
1. **Review Plan**
   - Locate plan document
   - Parse implementation decisions
   - Set up task tracking

2. **Implement Hook**
   - Create hook script
   - Implement core logic
   - Add error handling
   - Update settings.json

3. **Validate**
   - Run tests
   - Check linting
   - Manual smoke test

4. **Troubleshoot**
   - Fix any issues
   - Re-validate
   - Update documentation

**Example:**
```
/experts:cc_hook_expert:cc_hook_expert_build specs/hook-file-validator-plan.md
```

#### cc_hook_expert_improve

Self-improvement through analysis of recent changes.

**Command:** `/experts:cc_hook_expert:cc_hook_expert_improve`

**Workflow:**
1. **Establish Expertise**
   - Read current plan and build prompts
   - Understand existing patterns

2. **Analyze Changes**
   - Review recent git commits
   - Identify hook-related modifications

3. **Determine Relevance**
   - Filter for applicable learnings
   - Early return if nothing relevant

4. **Extract Learnings**
   - Identify new patterns
   - Note improvements
   - Update expertise sections

5. **Apply Updates**
   - Modify plan prompt
   - Modify build prompt
   - Document changes

**Self-improvement areas:**
- New hook patterns
- Error handling improvements
- Configuration best practices
- Testing strategies

## Creating Custom Agents

### Agent Structure

```markdown
---
name: agent-name
description: When to use this agent (for delegation)
tools: Read, Write, Bash, etc.
model: haiku | sonnet | opus
color: red | blue | green | yellow | purple | orange | pink | cyan
---

# Purpose

Clear statement of agent's role and capabilities.

## Instructions

### Step 1: First Action
Detailed instructions for first step.

### Step 2: Second Action
Detailed instructions for second step.

## Best Practices
- Domain-specific guidelines
- Quality standards
- Common pitfalls to avoid

## Report

Expected output format and structure.
```

### Agent Location

Place agent files in `.claude/agents/`:

```
.claude/
└── agents/
    ├── docs-scraper.md
    ├── meta-agent.md
    ├── research-docs-fetcher.md
    └── custom-agent.md
```

### Tool Selection

Choose tools based on agent needs:

| Need | Tools |
|------|-------|
| Read code | Read, Grep, Glob |
| Modify code | Read, Write, Edit |
| Execute commands | Bash |
| Web research | WebFetch, WebSearch |
| Complex tasks | Task (sub-agents) |
| User interaction | AskUserQuestion |

### Model Selection

| Model | Use Case |
|-------|----------|
| `haiku` | Quick, simple tasks |
| `sonnet` | Balanced (default) |
| `opus` | Complex reasoning, architecture |

## Agent Invocation

### Direct Delegation

Claude automatically delegates to agents based on task matching:

```
Research the FastAPI security documentation
→ Delegated to research-docs-fetcher

Create an agent for monitoring deployments
→ Delegated to meta-agent
```

### Via Commands

Use slash commands for explicit invocation:

```
/background Refactor authentication module
/parallel_subagents "Analyze codebase" 3
/load_ai_docs React hooks
```

### Via Task Tool

Programmatic invocation in workflows:

```python
# In custom scripts or hooks
from claude import Task

Task(
    agent="docs-scraper",
    prompt="Fetch FastAPI routing documentation"
)
```

## Expert Pattern Best Practices

1. **Start with Plan**: Always plan before building
2. **Iterate**: Use improve phase after significant changes
3. **Document Learnings**: Update expertise sections regularly
4. **Test Thoroughly**: Validate at each phase
5. **Version Plans**: Keep plan files for reference

## Directory Structure

```
project/
├── .claude/
│   ├── agents/
│   │   ├── docs-scraper.md
│   │   ├── meta-agent.md
│   │   └── research-docs-fetcher.md
│   └── commands/
│       └── experts/
│           └── cc_hook_expert/
│               ├── cc_hook_expert_plan.md
│               ├── cc_hook_expert_build.md
│               └── cc_hook_expert_improve.md
├── ai_docs/              # Agent-fetched documentation
└── specs/                # Plan outputs
    └── hook-*-plan.md
```
