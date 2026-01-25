# Advanced Context Engineering Notes (Compact, Bundles, Experts)

## /compact: a well-meaning feature with a big problem

Let’s take our builder and run a very well-meaning feature inside of Cloud Code: **`/compact`**.

You’ve probably used it, but there’s a huge problem:

> After `/compact` runs, do you know *exactly* what’s in your context window every single time?

The answer is: **no**.

- You don’t know.
- I don’t know.
- You have to hit **Ctrl-R** and re-read what compact actually did.

When you get to **advanced agent coding**, it’s time to stop **guessing** and start **knowing**.

### Recommendation: reset + prime instead of compact

I avoid `/compact` and recommend you:

1) **Reset** the context window completely (e.g., `/cle`)  
2) Verify you’re fresh with `/context`  
3) **Prime** again (run your `/prime_*` command)

Then rebuild the exact task context you need and continue forward.

This might sound like “do my work manually,” but the benefit is massive:

- You know exactly what’s in your context window.
- You build the habit of **task-specific context priming prompts**.
- You don’t delegate control of the context window to a tool.

### Why this matters (especially for out-loop)

This prepares you for **out-loop agentic coding**.

At high scale across hundreds of agent executions, you need specialized agents where you can predict context with high confidence.

If `/compact` runs, you **cannot** know the resulting state reliably.

**Rule for out-loop:**  
No single agent should overflow 200k tokens and trigger compaction.

If it does:
- **chop up the task**
- don’t rely on `/compact`
- **reset + prime**

---

## Context Bundles: replayable execution trails (advanced)

You can push in-loop active context management further using **context bundles**.

With **Claude Code hooks**, you can hook into tool calls to create a trail of work that you can use to **re-prime** agents later.

### What is a context bundle?

A context bundle is a simple append-only log of what your Claude Code instances are doing.

Typically stored under an *agentic layer directory*, e.g.:

- `agents/`
  - `background/`
  - `bundles/`

Bundles are often unique per:
- day
- hour
- session ID

A bundle might include:
- the prompt that was run
- read/search operations
- tool inputs
- condensed summaries

### Why bundles matter

A context bundle gives a subsequent agent a **solid understanding (≈60–70%)** of what the previous agent did.

This is valuable because:
- it tells a fuller story for future execution
- it helps remount an agent into a similar state after context “explodes”
- it enables “replay” without all raw details

### Loading a bundle

When a context window blows up:

1) Open a new agent instance  
2) Run something like: **`/load_bundle`**  
3) Paste the bundle path  
4) The new agent:
   - duplicates key reads if needed
   - reconstructs key findings
   - resumes with a better shared understanding

**Important:** record selectively.  
If you log every operation, you’ll overflow the next agent’s context window.

Bundles should be **trimmed**—enough to restore the story, not enough to recreate the entire world.

---

## One agent for one purpose (advanced, beautiful, strict)

There’s no better way to control and manage your context window than:

> **Ship one thing at a time.**

A focused agent is a performant agent.

This forces you to answer:

- What does the pipeline of agents look like for this work?

Once you internalize “one agent for one purpose,” you’ll start solving problems in a clean 2-step workflow:

1) Plan the work **without regard for technology**  
   - solve the user problem first  
2) Plan how to **delegate** across several agents  
   - forming an **agentic pipeline**
   - also known as an **AI Developer Workflow (ADW)**

This is the natural limit of delegation and a dominant pattern in TAC.

---

## Agentic Level: system prompt control (powerful + dangerous)

Once you reach the agentic level, you can start controlling agent behavior at a foundational level: **the system prompt**.

This can change tool behavior even more than output styles.

Many engineers won’t need this level. But if you’re pushing the edge:

- system prompt modifications give fine-grained control over:
  - behavior
  - tool calling discipline
  - read strategies
  - response formatting
  - context flow in/out

### Example: enforce reads in 100-line increments

You can append system instructions like:

- Always read in increments of 100 lines
- If sufficient info is obtained, stop reading and proceed
- If not enough, read the next 100 lines

This can reduce unnecessary reading and context ingestion, and you can see it reflected in context bundles:

- `Read 100`
- `Read 100`
- stop when enough

### Warning: overriding the entire system prompt

Some SDK variables allow a fully custom system prompt, which can wipe the default.

Use with extreme caution:
- Claude Code’s default system prompt is carefully engineered for software work.
- wiping it can degrade behavior quickly.

Recommendation:
- only use this level when needed
- or when building domain-specific agents deployed in your codebase

---

## Primary agent delegation: background agents (out-loop)

A lightweight form of multi-agent delegation is a reusable slash command that spins up a **background** agent.

Example concept:

- `/background`

It can accept:
- prompt
- model
- report file path

### Why it’s useful

Instead of babysitting in-loop, you fire one prompt:

- agent runs out-loop
- does one task
- writes a report file
- finishes

This keeps your primary context window clean and frees your time.

You can track progress via:
- the report file
- the context bundle trail for the background agent

Key idea:
- you’re orchestrating compute
- agents calling agents
- focused tasks with predictable context

---

## Agent Experts: specialized agents that auto-update their knowledge

This pattern pushes everything into something powerful:

> **Agent Experts**

A codebase can contain multiple specialized expert agents, each focused on a particular area (e.g., “Claude Code hooks expert”).

### Structure: a 3-step expert workflow

Experts often run in a consistent flow:

1) **Plan**
2) **Build**
3) **Improve**

The “improve” step is the meta layer:

- analyze the diff / changes made
- update the expert’s own prompts/templates
- keep expertise fresh

This becomes:
- self-documenting
- self-improving
- maintainable institutional memory

### Why experts are powerful

Experts act like:
- the engineer on your team who knows “that one feature better than anyone”
- except encoded as reusable prompt systems
- with the ability to auto-update over time

This is an investment:
- experts must be maintained and monitored

But it beats:
- knowledge stuck in a person’s head
- undocumented tribal context
- repeated relearning across time

---

## Future trends you can bet on (context engineering)

You can expect big labs to push:

1) **Larger context windows**  
2) **Better effective context windows**  
   - models lose capability as context grows (attention degradation)  
3) **Hot-swapped context**  
   - swapping system/tool/context blocks dynamically  
4) **Multi-agent architectures**  
   - better orchestration primitives  
5) **Specialized agents everywhere**  
   - model + prompt + tools tuned per use case  
   - delivered through SDKs, not generic chat loops

---

## Final reminder: it’s not about saving tokens, it’s about spending them properly

We manage context windows to avoid wasting time and tokens fixing agent mistakes.

The goal is:
- one-shot out-loop execution
- massive streams of attempts
- bigger task sizes
- lower human presence

But don’t forget:

> If you write bad prompts, context doesn’t matter.

Stack the big ideas:
- good prompts
- clean context windows
- focused agents
- delegation pipelines (ADWs)

A focused agent is a performant agent.