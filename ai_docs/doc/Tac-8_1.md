# Tactical Agentic Coding — Lesson 8 (Final)

Welcome to **Tactical Agentic Coding**, lesson 8 — your final lesson.

Everything we’ve done so far has led us here. You now have all the information you need to become an **irreplaceable engineer** in phase two of the generative AI age: **the age of agents**.

In this lesson, we cement critical agentic coding ideas, tactics, and beliefs by revisiting the **atoms** that make up everything we’ll do as agentic engineers moving forward.

These tactics are not bound to the software developer life cycle or any specific engineering workflow.

They exist to serve **your engineering**.

They are **building blocks** you can use to compose repeatable solutions for your agents.

---

## The Agentic Layer: The Ring Around Your Codebase

When I say **“build the system that builds the system,”** I’m talking about the new **agentic layer** of your codebase.

Imagine a ring around your codebase:
- at first it’s thin
- then it becomes thicker as you scale agentics into your system

Machines that operate with your judgment, shipping your way, getting work done autonomously inside your product.

That ring is the agentic layer.

This is where you:
- template your engineering
- teach your product to build itself

This course represents an opportunity to pull the future into the present.

There is engineering work you’re spending time on that you don’t need to be.

As time goes on — as tools improve and models progress — you’ll be able to hand off more and more work to your agentic layer.

The irreplaceable engineer we set out to become operates differently than engineers of today:
- we build the system that builds the system
- we operate on the agentic layer more often than the application layer

At the end of this course, there’s a single guiding question you can use to know whether you’re moving in the right direction or not.

That guiding question is the oil of this course.

All the agentic coding KPIs — every tactic — compress into one question.

But we have important ideas to cover before we get there.

---

## What We’ll Do in Lesson 8

In this lesson, we’ll work through **four unique codebases**, each with their own agentic layer.

The whole point is to give you hands-on quick starts you can use to build:
- a v1
- a proof of concept
- a minimum viable agentic layer

---

## Your Final Tactic: Prioritize Agentics

Let’s cover your final tactic:

> **Prioritize agentics.**

This tactic has been staring us in the face the entire time.

It can drive massive ROI decisions every single day you build with agents.

It’s simple. It’s everything:

> **Prioritize your agentic layer.**

Agentics refer to systems or entities capable of autonomous action and decision-making.

This tactic represents all others:
- from target zero-touch engineering  
- all the way back to stop coding

All tactics compress into this:
> prioritize your agentic layer.

The trick is that this will fluctuate, but as a general rule:

> the more time you invest into your agentic layer, the thicker you make that ring around your codebase, the more problem classes your agentic layer can solve on your behalf.

As a starting point, I recommend:
- **at least half** of your engineering time spent on the agentic layer

When you’re starting out, building it initially, you’ll likely invest even more upfront.

---

## Two Layers: Agentic vs Application

Let’s make it absolutely clear:

- **Agentic layer**
- **Application layer**

Inside “application layer” I’m being broad:
- DevOps
- infrastructure
- database
- raw application code

All of that is application layer.

Your agentic layer is separate — and should remain separate.

I recommend more than half your time should focus on the agentic layer.

As we work through the final codebases, keep your eyes on the **primitives**:
- the composable units of agentic coding
- from individual prompts
- up to multi-step AI developer workflows

That’s what matters.

Not the SDLC.  
Not a model.  
Not a tool.  
Not Cloud Code.

The primitives.

Claude Code is the first viable engineering tool that unlocks agentic engineering — but it won’t be the last.

Tools will change. Models will improve.

That’s why we fixate on primitives.

This is not a Claude Code course.

This is a course on tactical agentic coding: ideas you can bring to the battleground of engineering with agents every day.

In this final lesson, we close the loop.

---

## Minimum Viable Agentic Layer: The Primitives Codebase

We start by pushing you toward the minimum viable agentic layer.

We’ll work through different examples — different shapes of what an agentic layer can look like.

You’ll see similarities.

I’ve repurposed much of the work from earlier lessons, but keep your eyes on the primitives.

We open the terminal, clone the lesson 8 codebase, and you’ll see five distinct codebases.

We’ll work through three to four.

The **agentic layer primitives** codebase is a simple empty codebase meant to help you build your agentic layer from scratch.

Start with the README.

For your minimum viable agentic layer, you only need:

- an **AI developer workflows** directory (ADWs)
- **prompts** (stored as slash commands / markdown prompts)
- **plans / specs** (markdown artifacts)

You need some type of scripting layer (ADWs). It doesn’t matter what you use:
- TypeScript with Bun
- Python with UV
- old-school shell scripts

The only thing that matters is:
- you can compose code
- reference other files
- keep it isolated from your application layer

That separation is critical.

Apps and agents are distinct.

Your app lives in its own directory.

Your agentic ring operates around it.

None of this works without prompts.

Prompts + ADWs let you combine:
- deterministic, guaranteed code execution  
with
- the non-deterministic world of agents

If you only operate with prompts, you miss capabilities and workflows.

---

## Core Prompts: Prime, Start, Implement, Templates

A minimum agentic layer usually starts with something like:

### `/prime`
A reusable priming prompt that sets the agent up to understand your codebase quickly.

Different codebases may require different priming commands:
- prime the whole codebase
- prime specific subsystems
- prime a single domain

### `/start`
A prompt to start your application:
- boot services
- run commands
- restart processes

This can be simple or complex.

The point: agents handle running your codebase the way you would.

### `/implement`
A higher-order prompt:
- a prompt that takes another prompt (or a plan) as input
- executes implementation based on that plan

### Templates (Meta Prompts)
Templates are a core component of the agentic layer.

They define your engineering workflows.

They are prompts that generate prompts:
- chore templates
- feature templates
- bug templates

Key idea:
- agents research the codebase
- produce a plan
- encode your practices
- solve problem classes (not one-off fixes)

Think from the agent’s perspective:

> Is this the workflow you would use to solve the problem class?

---

## The Highest Abstraction: AI Developer Workflows

Once you start collecting prompts and using them in-loop, move out-loop.

Scale up by chaining prompts with deterministic code.

That’s the role of ADWs.

A great starting point is the minimal “ADW prompt” script:
- it calls an agent
- wraps state and logging
- produces a concise output

It’s the thinnest viable gateway into agentic coding.

From there, you scale:
- call slash commands from scripts (`/start`, etc.)
- stop “chatting” with the agent
- fire-and-forget execution
- isolate runs
- track logs

In-loop is a great place to start and do deep work on the agentic layer.

It’s a terrible place to stay.

If you have a successful product, the value of building an agentic layer is parabolic:
- put 10 minutes in
- get hours of value out

Because the layer compounds as it thickens:
- more ADWs
- better templates
- more feedback loops
- more autonomy

---

## A Simple Workflow Example: Chore → Implement

After you can run a prompt out-loop, you chain them into workflows.

Example: **`chore_implement`**
- run `/chore` (template produces plan path)
- then run `/implement` with that plan path

Nothing complicated is happening:
- two prompts back-to-back
- glue code for state + logging
- deterministic execution around non-deterministic reasoning

This unlocks infinite combinations:
- chainable ADWs
- 1→2 handoff workflows
- architect/editor patterns
- upgrade paths to full SDLC or ZTE workflows

The point is control:
- you control which prompts run
- how they chain
- what gets validated
- what gets committed
- what gets shipped

---

## Thicker Layer Example: Multi-Agent Task System with Worktrees

Next, we move into a thicker layer: a multi-agent system driven by a task list.

Example: a data science / notebook scenario (`todone` style workflow).

The application code is not the point.

The point is the agentic layer around it:
- a shared `tasks.md`
- a trigger that checks tasks every few seconds
- multiple git worktrees (isolated environments)
- multiple agents operating in parallel

This is powerful for:
- data engineering
- experiments
- model variants
- iterative pipelines

Tasks can include tags:
- model selection (e.g., “Opus”)
- workflow selection (e.g., plan+implement vs quick patch)
- any metadata that changes execution behavior

This is how you push beyond the chat UI:
- prompts become tasks
- tasks become triggers
- triggers kick off ADWs
- ADWs operate in isolated worktrees
- results roll in continuously

And the system marks work:
- done / blocked
- commit hashes
- agent IDs
- traceable execution history

This is still just one possible shape of an agentic layer.

Build it however you want.

---

## Don’t Do the Work Yourself

Remember the final tactic:

> prioritize agentics.

Don’t do the work by yourself.

Teach your agents to solve the problem class.

Build the system that builds the system.

Prompts compose into workflows.

Workflows operate on tasks.

Triggers keep you out-loop.

---

## Validating Agent Work by Entering a Worktree

When something completes, you can open the worktree for that agent and validate quickly.

You’ll see:
- the generated artifacts (datasets, scripts, notebooks)
- commits
- changes stacked on top of previous agent work

This is the pattern:
- isolate work
- parallelize agents
- validate outcomes
- compound progress

---

## Next: Agentic Prototyping

We then move to agentic prototyping — fully out-loop — where prompt input comes from a board (e.g., Notion database in board view).

This maps directly to the Peter framework:
- prompt input
- trigger environment
- review system

And it enables rapid prototyping at the pace modern innovation demands.

*(Continuing from here, we’ll break down how the prototyping board drives agents end-to-end and how you can adapt it to your stack.)*