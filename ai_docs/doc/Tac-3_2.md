# Tactical Agentic Coding (TAC)  
## Lesson 3 – Fresh Agents, Metaprompting, Templates, and Programmatic Execution

### KPI Target: Autonomy at Scale

We want to:
- decrease **attempts**
- increase **streak**
- decrease **presence** to **zero**

To do that, we must take a key step:

> At the right node of the software development life cycle, kick off **new agent instances with no previous context**.

Said another way:

> We must decouple performance from the conversational context window.

“Conversational” means **more than one prompt**.  
We want **one-shot successes**.

One-shot does **not** mean small work:
- **Size goes up**
- agents do more work autonomously

But it does mean our **plans** (prompts scaled up) must contain everything the agent needs to start.

You can pack your plans with details. A “small” plan might be ~100 lines, and still:
- touches many files
- drives real engineering output
- executes cleanly end-to-end

This is why we run fresh agents repeatedly.

---

## Why Fresh Agents Work

By running fresh agents on:
- metaprompting templates
- planning assets
- implementation prompts

…we always know exactly what was in the agent’s context window.

When a new instance starts, you can say:

- We fired `/implement`
- It read **the plan file**
- It read **the implement prompt**
- Then it executed the work

So you know **100%** what the agent’s perspective was at the start.

Ultimately, the goal is:

> **True off-device agentic coding**  
> (agents running without you “present”)

If you do this right, it differentiates your engineering from everyone else.

---

## Compute + Thinking Mode

Use:
- the best available model
- **thinking/reasoning mode**

Why?
- throw more compute at the problem
- maximize capability
- hand off more work safely
- extend size while keeping attempts low

---

## Scaling Prompts: Templates → Plans → Implementation

You can scale:
- the template (encoded best practices)
- the generated plan
- the higher-order prompts that execute the plan

The key is:

> Implement can run **any spec** you generate.

And you can create multiple “implement modes.”

Example: a new higher-order implement prompt could:
1. read the plan
2. implement it
3. **review work completed vs plan**
4. report mismatches and fix them

This is higher-order activity.

---

## Higher-Order Prompts

Just like passing functions into functions, we can pass prompts into prompts:

> **Higher-order prompts** let you shape the work, shape success, and template it into your codebase.

This is where:
- metaprompts
- templates
- plans
- implementation prompts

…combine into repeatable engineering systems.

---

## Self-Validation in Action

A strong template leads to:
- tests created
- README/docs updated
- git diff review
- self-checking behavior

The agent checks its own work.  
It finds issues.  
It fixes them automatically.

This is the power of templating engineering:

> You stop coding.  
> You barely touch the plan.  
> The system does the work.

---

## The Daily Tactical Configuration

This course is designed so you think about three tactics **every day**:

1. **Stop coding**
2. **Adopt your agent’s perspective**
3. **Template engineering**

Agents running loose on a codebase without structure is a plan for failure.

It won’t scale into the true agentic engineering future.

Refreshing your agent each run is essential:
- isolates missions
- improves repeatability
- enables off-device execution

---

## Moving Toward Full SDLC Automation

We’re moving toward automating the full software development life cycle.

So how do we build features end-to-end?

Not by:
- sitting down
- typing code
- manually writing full plans

Instead:
- agents help generate plans by scanning the codebase
- you review templates + plans
- then agents implement
- then agents validate

But to run end-to-end without human presence, we need a key capability:

> Run agents **from the terminal**, programmatically.

Because the terminal is everywhere:
- local
- cloud
- CI/CD environments
- remote machines

This becomes a major topic next lesson.

---

## Feature Example: Query History Side Panel

Example high-level feature prompt:

- Create a new query history side panel in the app  
- Store completed queries in the database  
- Names for each query in the side panel  
- Clicking refocuses the main panel  
- Add a button next to “Upload data”

This becomes input to `/feature`, another template metaprompt.

---

## Validating the Work

After the agent implements a bug fix (e.g., SQL injection prevention):

You validate via:
- manual reproduction steps (from the plan)
- validation commands (from the plan)
- running tests (e.g., `uv run pytest`)

Plans should include:
- steps to reproduce
- validation commands
- self-validation loops

That’s how you close the loop quickly.

---

## Templates as the Core Scaling Mechanism

Plans are prompts scaled.  
Great planning is great prompting.

When plans are saved into the codebase, they become artifacts that:
- your team can reuse
- your future agents can reference
- you can refine over time

Templates matter because:

- writing plans takes time and is error-prone
- templates encode engineering practice
- agents can write first drafts (sometimes final drafts)
- templates improve over time as size KPI increases

And templates can be customized deeply:
- front-end feature templates
- migration templates
- notebook/research templates
- domain-specific bug templates

The more custom the templates, the more unique and differentiated your engineering becomes.

---

## Programmatic Mode: Off-Device Behavior

The path forward is executing templates without a manual IDE session.

Run the agent in programmatic form:
- wrap a slash command prompt in terminal execution
- stream output to a file (e.g., JSONL)
- monitor results asynchronously (by reading output artifacts)

This is uncomfortable at first:
- you don’t “see” the agent
- you’re not manually supervising

But as:
- plans get better
- templates get stronger
- you understand agent perspective

…this becomes the default way to operate across the SDLC.

You’re building:

> **the system that builds the system**

---

## What’s Next: Lesson 4

Lesson 4 leans into:
- programmatic agents
- true off-device agentic coding
- AI developer workflows (ADWs)

ADWs are the highest leverage point:
- prompts + code + triggers
- agents operating across the SDLC
- recovery when things go wrong
- templates to keep future runs on track

The mission remains:

> Stop coding.  
> Adopt your agent’s perspective.  
> Template your engineering.

Lesson 4 is where we start learning to let the product **ship itself**.