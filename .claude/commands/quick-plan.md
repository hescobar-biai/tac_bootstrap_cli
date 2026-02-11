---
allowed-tools: Task, Read, Write, Edit, Glob, Grep, WebFetch
description: Creates concise engineering implementation plan with parallel scout-based codebase exploration
model: opus
# NOTE: Model "opus" uses 3-tier resolution:
#   1. ANTHROPIC_DEFAULT_OPUS_MODEL (env var) - highest priority
#   2. config.yml agentic.model_policy.opus_model - project config
#   3. Hardcoded default "claude-opus-4-5-20251101" - fallback
# See .claude/MODEL_RESOLUTION.md for details
---

# Purpose

This command creates a concise implementation plan by combining parallel scout-based codebase exploration with intelligent planning. It deploys 3 base scout agents and 5 fast scout agents in parallel to discover relevant files and architectural patterns before generating a plan. The command analyzes task type and complexity to conditionally include plan sections, balancing power with simplicity.

## Variables

USER_PROMPT: $ARGUMENTS
PLAN_OUTPUT_DIRECTORY: specs/
TOTAL_BASE_SCOUT_SUBAGENTS: 3
TOTAL_FAST_SCOUT_SUBAGENTS: 5

## Instructions

### 1. Parse User Requirements
Carefully analyze the USER_PROMPT to understand the task. Extract key concepts and identify the scope of work.

### 2. Determine Task Type and Complexity
Analyze the prompt to classify the task:

**Task Type** (choose one):
- **chore**: Simple housekeeping tasks (dependency updates, minor fixes)
- **feature**: New functionality requiring planning and testing
- **refactor**: Structural improvements with impact analysis
- **fix**: Bug fixes with investigation and testing
- **enhancement**: Improvements to existing features

**Complexity Level** (choose one):
- **simple**: Changes to 1-2 files, straightforward implementation
- **medium**: Changes to 3-5 files, requires some architectural consideration
- **complex**: Changes to 5+ files, architectural impact, needs detailed planning

### 3. Scout Exploration Workflow

Before planning, execute parallel scout exploration to discover relevant files and architectural patterns.

#### Step 1: Launch Parallel Scouts
Use a single message with multiple Task tool invocations to launch ALL scouts in PARALLEL:

**Deploy 3 Base Scout Agents** (scout-report-suggest agents):
1. **Base Scout 1: Architectural Patterns & Domain Logic**
   - Focus: Domain models, service layers, core abstractions, design patterns
   - Thoroughness: medium

2. **Base Scout 2: Infrastructure & Integration Patterns**
   - Focus: Templates, file operations, CLI interfaces, testing utilities
   - Thoroughness: medium

3. **Base Scout 3: Application Services & Workflows**
   - Focus: Service orchestration, application flows, integration points
   - Thoroughness: medium

**Deploy 5 Fast Scout Agents** (scout-report-suggest-fast agents):
1. **Fast Scout 1**: File naming patterns and test files
2. **Fast Scout 2**: Configuration and setup patterns
3. **Fast Scout 3**: Similar feature implementations
4. **Fast Scout 4**: Documentation and examples
5. **Fast Scout 5**: Integration points and extension mechanisms

Each scout receives a targeted prompt based on USER_PROMPT, focusing on different concerns to maximize coverage without redundancy.

#### Step 2: Aggregate Scout Results
- Extract file paths mentioned by each scout
- Build a unified file map with frequency counts
- Identify high-confidence files (found by 2+ scouts)
- Extract architectural patterns and design decisions

#### Step 3: Identify Patterns
Extract from scout findings:
- Existing architectural patterns to follow
- Similar features to reference
- Common abstractions available
- Testing patterns in use

### 4. Conditional Plan Format

Generate plan sections based on task type and complexity:

- **Always include**: Feature Description, User Story, Relevant Files, Implementation Plan, Step by Step Tasks, Validation Commands
- **Include if** (feature OR medium/complex): Problem Statement, Solution Approach, Testing Strategy
- **Include if** (complex): Implementation Phases (breaking down major work)

Reference discovered files and architectural patterns throughout the plan.

### 5. Create Implementation Plan

Structure the plan with:
- Clear metadata and scout exploration summary
- Problem statement (if applicable)
- Solution approach informed by scout findings
- Relevant files section with discovered patterns
- Step-by-step implementation tasks
- Testing strategy (if applicable)
- Acceptance criteria
- Validation commands

Generate a descriptive, kebab-case filename: `PLAN_OUTPUT_DIRECTORY/issue-<number>-adw-<id>-<description>.md`

### 6. Handle Scout Failures Gracefully
If scouts fail:
- Continue planning with successful scouts' results
- Log failures in the plan's Notes section
- Use general knowledge for missing exploration
- Do NOT block plan creation

## Scout Exploration Strategy

Scouts explore the codebase using divide-and-conquer strategies:

**Base Scouts** (3 agents with medium thoroughness):
- Scout 1: Domain layer, business logic, service patterns, core abstractions, design patterns
- Scout 2: Infrastructure layer, integrations, CLI interfaces, file operations, templates
- Scout 3: Service orchestration, workflows, application patterns, extension mechanisms

**Fast Scouts** (5 agents with quick thoroughness):
- Rapid surface-level scans for obvious patterns, naming conventions, test files, examples
- Focus on quick wins and quick pattern detection
- Cost-effective explorers for broader coverage

**File Scoring Algorithm**:
- High Confidence: Found by 2+ scouts (66%+) → Definitely relevant
- Medium Confidence: Found by 1 scout with strong notes → Likely relevant
- Low Confidence: Found by 1 scout with weak notes → Possibly relevant

## Plan Format Template

```markdown
# Feature: <feature name>

## Metadata
task_type: chore|feature|refactor|fix|enhancement
complexity: simple|medium|complex
scouting_status: 3 base + 5 fast scouts deployed

## Scout Exploration Summary

### High-Confidence Files Discovered
<Top 5-10 files found by multiple scouts>

### Key Architectural Patterns Identified
<Patterns discovered through scout exploration>

### Similar Implementations to Reference
<Similar features or modules that can serve as references>

## Feature Description
<Describe the feature in detail>

## User Story
As a <user type>
I want to <action/goal>
So that <benefit/value>

## Problem Statement
<Include this section if (task_type == feature) OR (complexity in [medium, complex])>

## Solution Approach
<Include this section if (task_type == feature) OR (complexity in [medium, complex])>
<Reference discovered architectural patterns and similar implementations>

## Relevant Files
<List relevant files discovered by scouts, prioritizing high-confidence findings>

## Implementation Plan

### Phase 1: Foundation
<Foundational work before implementing the main feature>

### Phase 2: Core Implementation
<Main feature implementation>

### Phase 3: Integration
<Integration with existing functionality>

## Implementation Phases
<Include this section only if (complexity == complex)>
<Break down major work into distinct phases>

## Step by Step Tasks
<Execute each step in order>

## Testing Strategy
<Include this section if (task_type == feature) OR (complexity in [medium, complex])>

## Acceptance Criteria
<Specific, measurable criteria for completion>

## Validation Commands
<Commands to verify implementation>

## Notes
<Scout findings summary, architectural insights, reference files>
```

## Report

After creating and saving the implementation plan, provide output with:

```
✅ Implementation Plan Created

File: <relative path to specs/file.md>
Task Type: chore|feature|refactor|fix|enhancement
Complexity: simple|medium|complex
Scouts Deployed: 3 base + 5 fast (8 parallel agents)
High-Confidence Files: <count>
Plan Sections: <list applicable sections based on task type/complexity>
```
