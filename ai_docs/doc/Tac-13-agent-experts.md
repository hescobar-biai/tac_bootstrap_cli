# TAC-13: Agent Experts - Self-Improving Agents

**Learn once. Apply forever.**

---

## Table of Contents

1. [The Problem TAC-13 Solves](#the-problem-tac-13-solves)
2. [Agent Experts: Self-Improving Agents](#agent-experts-self-improving-agents)
3. [Expertise Files as Mental Models](#expertise-files-as-mental-models)
4. [The 3-Step Agent Expert Loop](#the-3-step-agent-expert-loop)
5. [Implementation Patterns](#implementation-patterns)
6. [Meta-Agentics Building Blocks](#meta-agentics-building-blocks)
7. [Self-Improve Workflow](#self-improve-workflow)
8. [When to Use Agent Experts](#when-to-use-agent-experts)
9. [When NOT to Use Agent Experts](#when-not-to-use-agent-experts)
10. [Challenges & Tradeoffs](#challenges--tradeoffs)
11. [Real-World Examples](#real-world-examples)

---

## The Problem TAC-13 Solves

**Agents forget and don't learn.**

Modern agents have a fundamental flaw that persists regardless of how good your context engineering or agentic prompt engineering becomes:

- **TAC-9/10/12** improved workflows, but each execution starts from zero
- **Memory files** require manual updates and consume developer time
- **Generic agents** rebuild understanding every time they run
- **No learning between executions** means repeated work and lost knowledge

Traditional software improves as it's used—storing user analytics, usage data, and patterns. **Agents of today don't.**

### The Solution

TAC-13 introduces: **Agents that learn automatically from each execution**

Agent experts embody three critical behaviors:
1. **Act** - Take useful actions (build, modify, query)
2. **Learn** - Store new information automatically
3. **Reuse** - Use accumulated knowledge on next execution

---

## Agent Experts: Self-Improving Agents

### What is an Agent Expert?

An agent expert is a concrete form of a **self-improving template metaprompt**.

Let's break this down:

- **Metaprompts**: Prompts that build other prompts
- **Template metaprompts**: Prompts that build other prompts with a specific purpose and structure
- **Self-improving prompts**: Prompts that update themselves, related prompts, or isolated files with new information

**Self-improving + template + metaprompt = Self-improving template metaprompt**

### The Key Difference

| Generic Agent | Agent Expert |
|--------------|--------------|
| Search codebase every time | Reads expertise first |
| No memory between runs | Maintains mental model |
| Manual knowledge transfer | Automatic learning |
| 100% context window usage | 20% expertise + 80% specific task |
| Executes and forgets | Executes and learns |
| Starts from zero | Starts with accumulated knowledge |

### Why This Matters

Without agent expertise:
- You have to track changes manually
- Rebuild understanding each time
- Lose speed and trust at scale
- Agents consume full context windows repeatedly

With agent experts:
- The agent keeps track of its mental model
- Updates expertise as code changes
- Reuses knowledge automatically
- Stays focused: one agent, one prompt, one purpose
- Protects context windows through delegation

---

## Expertise Files as Mental Models

### What is an Expertise File?

The expertise file is the **mental model** of the problem space for your agent expert.

**Critical Understanding**: This is NOT a source of truth.

It's like your own mental model:
- Not the code
- Not comments
- Not PRDs
- A working memory structure that evolves

**The true source of truth is always the code.**

But auxiliary memory and mental models are still ultra valuable.

### Example Structure (expertise.yaml)

```yaml
overview:
  description: "Brief system description"
  key_files:
    - "path/to/file1.py"
    - "path/to/file2.py"
  last_updated: "2026-01-15"
  total_lines: 450

core_implementation:
  component_name:
    location: "path/to/component.py"
    key_functions:
      - name: "function_name"
        line_start: 42
        line_end: 87
        purpose: "What this function does"
        dependencies:
          - "other_module.function"
    patterns:
      - "Design pattern or approach used"

integration_points:
  external_systems:
    - name: "database"
      connection_file: "shared/database.py"
      session_management: "context manager pattern"

  internal_modules:
    - name: "auth_module"
      interaction: "Validates tokens before queries"

known_patterns:
  - pattern: "Repository pattern for data access"
    files: ["repositories/*.py"]

  - pattern: "Dependency injection via FastAPI"
    implementation: "dependencies.py"

recent_changes:
  - date: "2026-01-15"
    description: "Added async repository support"
    affected_files:
      - "shared/base_repository_async.py"

  - date: "2026-01-10"
    description: "Implemented soft delete pattern"
    details: "All entities now use state=2 for deletion"
```

### Key Principles

1. **Compressed representation** - Use YAML/JSON/TOML to maximize information density
2. **Finite size** - Enforce max lines (e.g., 1000 lines) to prevent bloat
3. **Actionable information** - Prioritize what helps agents make decisions
4. **Self-maintained** - Agents update this, not humans
5. **Validated against code** - Self-improve step keeps it accurate

---

## The 3-Step Agent Expert Loop

Agent experts have three concrete steps that form a continuous loop:

### 1. Act (Take Useful Action)

The agent performs meaningful work against the codebase:
- Build new features
- Modify existing code
- Fix bugs
- Refactor components
- Query and analyze

**Example**: Add a session-based counter to display total websocket events

### 2. Learn (Store New Information)

After acting, the agent automatically updates its expertise:
- Compare git diff against current mental model
- Identify new patterns or changes
- Update expertise file with validated information
- Maintain accuracy through validation checks

**Example**: Self-improve step detects new websocket event types and updates expertise.yaml

### 3. Reuse (Use Accumulated Knowledge)

On the next execution, the agent starts with its mental model:
- Read expertise file first (20% of context)
- Validate assumptions against code
- Use accumulated knowledge to work faster
- Avoid redundant searching and re-discovery

**Example**: Question prompt reads expertise, then validates specific details in code

### The Loop in Action

```
┌─────────────────────────────────────────┐
│  REUSE                                  │
│  - Read expertise.yaml                  │
│  - Start with accumulated knowledge     │
│  - Validate against current code        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  ACT                                    │
│  - Execute task based on expertise      │
│  - Make code changes                    │
│  - Build, modify, query                 │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  LEARN                                  │
│  - Run self-improve with git diff       │
│  - Update expertise automatically       │
│  - Validate and enforce constraints     │
└──────────────┬──────────────────────────┘
               │
               └──────────► Back to REUSE
```

---

## Implementation Patterns

### File Structure

```
.claude/commands/experts/
├── cli/
│   ├── question.md          # Reuse step (query expertise)
│   ├── self-improve.md      # Learn step (update expertise)
│   └── expertise.yaml       # Mental model data structure
├── adw/
│   ├── question.md
│   ├── self-improve.md
│   └── expertise.yaml
├── database/
│   ├── question.md
│   ├── self-improve.md
│   └── expertise.yaml
└── websocket/
    ├── question.md
    ├── self-improve.md
    └── expertise.yaml
```

### Question Prompt Pattern (Reuse)

```markdown
# Expert Question Prompt

You are a [DOMAIN] expert with accumulated knowledge about this system.

## Process

1. **Read expertise file**
   - Location: `.claude/commands/experts/[domain]/expertise.yaml`
   - This is your mental model - use it as a starting point

2. **Validate assumptions**
   - Compare expertise against current codebase
   - Note any discrepancies
   - Identify outdated information

3. **Answer the question**
   - Use expertise to guide your investigation
   - Validate critical details in actual code
   - Report findings with file references

4. **Note gaps**
   - What information was missing from expertise?
   - What has changed since last update?
   - Include in your response for future learning

## Input

**User Question**: {{ user_question }}

## Output Format

### Answer
[Your answer based on expertise + code validation]

### References
- `file.py:line` - Specific locations

### Expertise Gaps Identified
- [What was missing or outdated]
```

### Self-Improve Prompt Pattern (Learn)

```markdown
# Expert Self-Improve Prompt

Automatically update expertise based on recent changes.

## Process

1. **Analyze changes**
   - Input: git diff or change description
   - Identify what's new, modified, or removed

2. **Read current expertise**
   - Load `.claude/commands/experts/[domain]/expertise.yaml`
   - Understand existing mental model

3. **Validate against code**
   - Check if expertise matches reality
   - Find discrepancies
   - Identify missing information

4. **Update expertise**
   - Add new patterns, files, functions
   - Update changed information
   - Remove obsolete entries
   - Maintain compressed format

5. **Enforce constraints**
   - Max lines: {{ max_lines }}
   - Valid YAML syntax
   - Prioritize actionable information
   - Remove low-value details if needed

6. **Validate update**
   - Verify YAML is valid
   - Check line count
   - Ensure critical information preserved

## Input

**Changes**: {{ git_diff or change_description }}

## Output

Updated expertise.yaml file
```

### Orchestrator Pattern (Plan → Build → Improve)

```markdown
# Expert Orchestrator

Coordinate the full Act → Learn → Reuse workflow.

## Workflow

### Phase 1: PLAN (Reuse)
- Read expertise file
- Validate against current code
- Create implementation plan
- Delegate to builder (protect context)

### Phase 2: BUILD (Act)
- Execute plan via sub-agent
- Make code changes
- Capture git diff

### Phase 3: IMPROVE (Learn)
- Pass git diff to self-improve
- Update expertise automatically
- Validate changes

## Input

**Task**: {{ user_task }}

## Context Management

- Planning uses expertise (20%) + code validation (80K tokens)
- Building delegates to sub-agent (protect main context)
- Improving processes only the diff (efficient)
```

---

## Meta-Agentics Building Blocks

Meta-agentics help you build **the system that builds the system**.

These building blocks greatly increase your output as an agentic engineer—with or without agent experts.

### Meta-Prompts

**Prompts that build other prompts.**

**Example Use Case**: Create a new version of question prompt with mermaid diagrams

```markdown
# Meta-Prompt Generator

Create a new agentic prompt based on specifications.

## Input
- Base prompt (optional)
- Purpose
- Variables needed
- Output format

## Process
1. Analyze requirements
2. Structure prompt with clear sections
3. Add variable placeholders
4. Define output format
5. Include validation steps

## Output
Complete markdown prompt file ready to use
```

**When to use**:
- Scaling prompts across domains (database expert → API expert → billing expert)
- Creating variants (question with diagrams, question with code snippets)
- Standardizing prompt structures across team

### Meta-Agents

**Agents that build other agents.**

**Example Use Case**: Create a planner agent that reads and executes plan prompts in parallel

```markdown
# Meta-Agent Generator

Generate specialized agents from templates or specifications.

## Input
- Agent purpose
- Required tools
- Context needs
- Prompts to execute

## Process
1. Define agent structure (.md file)
2. Specify tool permissions
3. Configure context loading
4. Set up prompt execution flow
5. Add validation and error handling

## Output
Fully functional agent definition file
```

**When to use**:
- Scaling agents across similar tasks (frontend planner, backend planner, DB planner)
- Creating specialized variants (fast agent with haiku, thorough agent with opus)
- Building agent swarms for parallel work

### Meta-Skills

**Processes transformed into reusable skills with progressive disclosure.**

**Example Use Case**: Transform "start orchestrator" process into concrete skill

```markdown
# Meta-Skill Generator

Convert manual processes into documented, executable skills.

## Progressive Disclosure Levels

### Level 1: Metadata
- Name
- Purpose (3-5 words)
- Category
- When to use

### Level 2: Instructions
- Step-by-step execution
- Required inputs
- Expected outputs
- Common flags/options

### Level 3: Resources
- Related files
- Dependencies
- Configuration needs
- Troubleshooting

## Input
- Process description
- Execution steps
- Resources needed

## Output
Structured skill definition with 3-level disclosure
```

**When to use**:
- Codifying repeated workflows (start app, run tests, deploy)
- Team knowledge sharing
- Onboarding automation

---

## Self-Improve Workflow

The 7-phase self-improve workflow ensures expertise stays accurate and valuable.

### Phase 1: Analyze Changes

```yaml
# Input: git diff or change description
changes_detected:
  new_files:
    - "path/to/new_file.py"
  modified_files:
    - "path/to/changed_file.py"
  deleted_files:
    - "path/to/removed_file.py"
  key_changes:
    - "Added async repository support"
    - "Implemented soft delete pattern"
```

### Phase 2: Read Current Expertise

Load and parse existing expertise.yaml to understand current mental model.

### Phase 3: Validate Against Code

Compare expertise claims against actual code:
- Do referenced files exist?
- Are line numbers accurate?
- Do functions match signatures?
- Are patterns still used?

### Phase 4: Identify Discrepancies

```yaml
discrepancies:
  outdated:
    - item: "Connection pool in database.py:42"
      reality: "Moved to database.py:156"

  missing:
    - "Async repository pattern in base_repository_async.py"

  incorrect:
    - item: "Delete uses CASCADE"
      reality: "Delete uses soft delete (state=2)"
```

### Phase 5: Update Expertise

Apply updates while maintaining structure:
- Add new information
- Correct outdated entries
- Remove obsolete items
- Preserve critical historical context

### Phase 6: Enforce Constraints

```yaml
constraints:
  max_lines: 1000
  format: "yaml"
  required_sections:
    - overview
    - core_implementation
    - integration_points

validation:
  current_lines: 687
  valid_yaml: true
  all_sections_present: true
```

### Phase 7: Final Validation

- Parse YAML to ensure valid syntax
- Count lines and trim if needed
- Verify all critical information preserved
- Write updated expertise.yaml

---

## When to Use Agent Experts

Agent experts shine in specific scenarios. Use them when:

### 1. High-Risk, High-Complexity Areas

- **Billing systems** - Revenue-critical code where mistakes cost money
- **Security systems** - Authentication, authorization, encryption
- **Complex niche systems** - Domain-specific logic that requires deep understanding
- **Large interconnected codebases** - Systems spanning many files far apart

### 2. High Error Rates

- Generic agents keep making mistakes in an area
- Need to enforce specific constraints or patterns
- Tune self-improve to force attention to critical details

### 3. Product-Focused Use Cases

- **User-specific personalization** - Maintain per-user mental models
- **Adaptive UI/UX** - Agents that learn user preferences
- **Generative interfaces** - Context-aware component generation

### 4. Evolving Systems

- Codebase grows and changes frequently
- New patterns emerge over time
- Need to maintain understanding across refactors

### 5. Specialized Domains

- **Database operations** - Schema, migrations, query patterns
- **API integrations** - Multi-way sync between systems
- **DevOps** - Infrastructure as code, deployment patterns
- **ML/Data Science** - Model training, feature engineering
- **Data types** - Keep types synced across monorepo/microservices

### Red Flags That Signal Need for Expert

- "The agent keeps getting this wrong"
- "This is too important to mess up"
- "It takes forever to explain the context every time"
- "The code is spread across 10+ files"
- "There are critical constraints that must be followed"

---

## When NOT to Use Agent Experts

Avoid agent experts when:

### 1. Problem Doesn't Evolve

- One-time migration tasks
- Static configuration that rarely changes
- Simple scripts with no growth expected

### 2. Brand-New, Generic Codebases

- Just starting a project with standard patterns
- No unique value or complexity yet
- Better to wait until patterns emerge

### 3. You Don't Have a Mental Model Yet

**Critical point**: If you don't understand the problem space, you can't judge expert performance.

- You'll build an expert that makes things worse
- Can't validate if updates are correct
- Better to explore first, then create expert

### 4. Low-Value, Low-Risk Areas

- Simple CRUD operations
- Standard boilerplate
- Temporary code or prototypes

### 5. Fresh Perspectives Needed

Sometimes a generic agent's "beginner's mind" catches issues an expert would miss.

### Alternative: Memory Files vs Experts

**Memory files**:
- Global, always-loaded context
- Good for universal rules
- Must be manually updated

**Agent experts**:
- Explicitly invoked
- Domain-specific knowledge
- Self-updating

Use memory files for project-wide standards. Use experts for specialized domains.

---

## Challenges & Tradeoffs

### 1. Seeding

**Challenge**: How to create the first version of expertise?

**Solution**:
- Start simple - don't over-engineer initial seed
- Run self-improve from blank or minimal seed
- Let agent create expertise structure
- Tweak self-improve prompt and rerun
- Repeat until agent stops finding new things

**Like joining a new job**:
- Get rough rundown of codebase, tools, processes
- Review process, branches, docs
- Agent builds expertise from there

### 2. "Another Source of Truth?"

**Challenge**: Isn't this creating duplicate information?

**Answer**: No.
- Expertise is NOT source of truth
- It's a mental model that references code
- Self-improve keeps it synced for you
- Code is always the source of truth

**Key trend**: Teach agents how to do things, don't do things for agents.

### 3. Finite Context

**Challenge**: Expertise could grow indefinitely

**Solution**:
- Enforce max lines (e.g., 1000)
- Use compressed representations (YAML, JSON, TOML)
- Prioritize high-value information
- Prune low-value details when space needed

```yaml
constraints:
  max_lines: 1000

pruning_strategy:
  remove_first:
    - "Old comments"
    - "Obvious patterns"
    - "Redundant information"

  keep_always:
    - "Integration points"
    - "Critical constraints"
    - "Non-obvious patterns"
```

### 4. False Expertise

**Challenge**: Agents can update something incorrectly

**Reality**:
- This error rate will decrease but won't hit zero
- Humans also have false expertise
- Expect and plan for it

**Mitigation**:
- Validation steps in self-improve
- Compare against actual code
- Review expertise periodically
- Git track changes to expertise files

### 5. Too Granular

**Challenge**: Expertise becomes verbose documentation

**Solution**:
- Prompt engineering: specify detail level
- Prioritize actionable high-value expertise
- Let agents decide what's important (it's their mental model)
- Avoid over-documentation

**Bad**:
```yaml
# 200 lines documenting every function signature
```

**Good**:
```yaml
# 50 lines highlighting patterns, integration points, critical constraints
```

### 6. Too Many Experts

**Challenge**: When to use expert vs generic agent?

**Solution** (develop processes):
- Router systems
- Reminders in prompts
- Auto-pick based on file paths or keywords
- Team habit: check experts directory first

**For now**: If you're building many experts, that's good. Make it a habit to check before starting work.

---

## Real-World Examples

### Example 1: Database Expert

**Mental model (650 lines)**:

```yaml
overview:
  description: "PostgreSQL database layer with sync/async support"
  key_files:
    - "shared/database.py"
    - "shared/base_repository.py"
    - "shared/base_repository_async.py"
  patterns:
    - "Repository pattern for data access"
    - "Soft delete with state=2"
    - "Connection pooling with SQLAlchemy"

database_module:
  connection_pool:
    location: "shared/database.py:156-187"
    engine_config:
      pool_size: 5
      max_overflow: 10
      pool_pre_ping: true
    context_manager: "get_db() yields session"

query_patterns:
  filtering:
    active_only: "filter(Entity.state == 1)"
    with_deleted: "No state filter"
    soft_delete: "update state=2, preserve data"

  pagination:
    pattern: "offset/limit with total count"
    helper: "paginate_query() in base_repository.py"

data_models:
  base_entity:
    location: "shared/base_entity.py:15-89"
    fields:
      - id (UUID, primary key)
      - created_at (UTC)
      - created_by (user reference)
      - state (EntityState enum)
      - version (optimistic locking)

    state_transitions:
      - "activate() -> state=1"
      - "deactivate() -> state=0"
      - "soft_delete() -> state=2"

migration_patterns:
  tool: "Alembic"
  location: "shared/alembic.py"
  workflow:
    - "Auto-generate: alembic revision --autogenerate"
    - "Review and refine SQL"
    - "Test in dev"
    - "Apply: alembic upgrade head"

  naming: "YYYYMMDD_HHMM_description"

sync_distribution:
  utilities:
    - "sync_to_dev.py - Replicate prod to dev"
    - "anonymize_pii.py - Strip sensitive data"
```

**Workflow**:
1. **Reuse**: `/experts/database/question "How do soft deletes work?"`
   - Agent reads expertise.yaml
   - Knows to check base_entity.py and repository patterns
   - Validates in code
   - Reports findings with line references

2. **Act**: Add new async repository method
   - Uses expertise to understand patterns
   - Implements following established conventions
   - Creates git diff

3. **Learn**: `/experts/database/self-improve` with diff
   - Detects new async method
   - Updates expertise.yaml automatically
   - Validates YAML and line count

### Example 2: WebSocket Expert

**Task**: Add session-based counter to app navbar showing total websocket events

**Workflow**:

```bash
# Plan step (Reuse + Validate)
# - Read websocket expertise (20% context)
# - Validate against current code (80K tokens)
# - Create detailed plan
# - Pass plan to builder

# Build step (Act)
# - Sub-agent executes plan (61K tokens, 41 tool uses)
# - Protects main agent context
# - Generates git diff

# Self-improve step (Learn)
# - Analyze git diff
# - Update expertise with new patterns
# - Surgical changes: 5, 9, 17, 4 lines
```

**Mental model updates**:

```yaml
session_state:
  websocket_counter:
    location: "frontend/stores/websocket.ts:42-67"
    purpose: "Track total websocket messages per session"
    integration: "Displayed in navbar component"

websocket_events:
  total_types: 21
  categories:
    - agent_lifecycle
    - agent_communication
    - orchestrator
    - chat
    - system

recent_changes:
  - date: "2026-01-15"
    description: "Added session-based event counter"
    files:
      - "frontend/stores/websocket.ts"
      - "frontend/components/navbar.tsx"
```

**Result**:
- 3 expert agents completed task
- 1 failed (non-determinism is okay with parallel scaling)
- Expertise automatically updated
- Next task starts with this knowledge

### Example 3: Billing Expert (Saved Money)

**Why expert**: Billing mistakes directly cost money. High risk = need expert.

```yaml
overview:
  description: "Stripe billing integration with webhook handling"
  critical_constraints:
    - "NEVER charge twice for same event"
    - "ALWAYS verify webhook signatures"
    - "Log all billing events for audit"

webhook_handling:
  location: "api/webhooks/billing.py"
  events:
    - "customer.subscription.created"
    - "customer.subscription.updated"
    - "invoice.payment_succeeded"
    - "invoice.payment_failed"

  idempotency:
    pattern: "Check event_id in processed_events table"
    location: "api/webhooks/billing.py:89-102"
    critical: "Prevents double-charging"

  signature_verification:
    location: "api/webhooks/billing.py:45-58"
    algorithm: "HMAC SHA256"
    critical: "Security - verify Stripe sent it"

billing_flow:
  frontend:
    - "Checkout component -> Stripe hosted page"
    - "Success callback -> update user state"

  backend:
    - "Webhook receives payment confirmation"
    - "Verify signature and idempotency"
    - "Update subscription status"
    - "Send confirmation email"
    - "Log to audit table"

common_gotchas:
  - "Test mode vs live mode API keys"
  - "Webhook endpoint must be publicly accessible"
  - "Handle failed payments gracefully"
  - "Subscription updates can trigger multiple webhooks"
```

**Impact**: Expert prevented double-charging bug that would have cost real money.

### Example 4: Product Expert - Personalized Shopping

**Concept**: Per-user agent experts for adaptive UI/UX

```yaml
# expertise/users/user_12345.yaml
user_preferences:
  viewed_products:
    - id: "nvidia-dgx-spark"
      category: "AI Hardware"
      price_range: "$10,000+"
      viewed_at: "2026-01-15T14:23:00Z"

  added_to_cart:
    - id: "enterprise-gpu-cluster"
      category: "AI Hardware"
    - id: "ml-optimization-course"
      category: "Education"

  purchased:
    - id: "startup-ai-bundle"
      category: "Bundles"
      price: "$4,999"
      date: "2026-01-10"

inferred_interests:
  primary: "AI/ML Infrastructure"
  secondary: "Education/Training"
  price_sensitivity: "High (enterprise level)"

recommendation_strategy:
  priority_categories:
    - "AI Hardware"
    - "ML Software"
    - "Professional Services"

  avoid_categories:
    - "Consumer Electronics"
    - "Budget Options"
```

**UI Generation**:
- System prompt loads user expertise
- Generates personalized product sections
- Adapts recommendations based on behavior
- Learns from each interaction

**Scale**: One expertise file per user = ultimate personalization

---

## Closing Perspective

### The Core Question

Do you want:
- **A generalist that forgets every time**, or
- **An expert that remembers and learns** so next time it starts with powerful working understanding?

### Key Takeaways

1. **Agent experts solve forgetting** - The fundamental problem of modern agents
2. **Act → Learn → Reuse loop** - Continuous improvement without human intervention
3. **Expertise as mental model** - Not source of truth, but working memory
4. **Meta-agentics** - Build the system that builds the system
5. **Self-improve workflow** - 7 phases ensure accuracy and value
6. **Use for high-risk areas** - Billing, security, complex systems
7. **Avoid premature optimization** - Wait for patterns to emerge

### The Bigger Picture

Agent experts represent a shift in how we think about AI systems:

- Traditional software stores data
- Modern software learns from usage patterns
- **Agent experts learn from their own actions**

This is the seed of:
- Self-improving systems
- Autonomous engineering
- Adaptive user experiences

### Build the System That Builds the System

Focus on the **agentic layer** - the ring around your codebase that can operate it:
- For you
- With you
- Without you

**Don't directly update expertise files.**
**Teach your agents how to update them.**

That's the essence of agentic engineering.

---

## Next Steps

1. **Identify your first expert** - Billing? Database? API integration?
2. **Start with question + self-improve** - Build the loop
3. **Let it run** - Watch expertise accumulate
4. **Add orchestration** - Plan → Build → Improve workflow
5. **Scale with parallel experts** - 3-10 agents for critical tasks

**Remember**: Experts grow. They update their knowledge. They never stop learning.

Build agents that do the same.

---

*Part of the Tactical Agent Coding (TAC) course series. See also: TAC-1 (Foundations), TAC-9 (Workflows), TAC-10 (Context), TAC-12 (Scale).*
