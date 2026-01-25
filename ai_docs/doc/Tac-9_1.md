# Context Engineering (TAC Notes)

A focused engineer is a performant engineer—and a focused agent is a performant agent. **Context engineering** is the name of the game for high-value engineering in the age of agents.

So… how good are your context engineering skills? Do you have a skill issue? Let’s find out and fix it.

There are **three levels of context engineering**, and a **fourth hidden level** if you’re on the bleeding edge pushing into agentic engineering.

## Why context engineering matters

Context engineering techniques are important because they let you manage a **precious and delicate resource**: your agent’s **context window** (e.g., Claude Code).

There are only **two** ways to manage your context window:

- **R** = **Reduce**
- **D** = **Delegate**

We’ll break down techniques at each level using the **R&D framework** to maximize not what *you* can do, but what *your agents* can do for you.

---

## TAC focus: scale intelligence, adopt the agent’s perspective

A huge focus in TAC is scaling the intelligence we can deploy both **in-loop** and **out-loop**. But with every agent we create, we must adopt their perspective to maximize their impact.

**Context** is a critical *in-agent leverage point* that determines how an agent performs for any given task.

There’s a **sweet spot**—a range of context where your agent performs at its maximum possible capability for the task at hand. As you scale to **hundreds or thousands of executions**, hitting this sweet spot consistently becomes even more important.

That’s what context engineering is:

- obsessively managing the context going into agents
- gaining awareness of agent state inside pipelines and ADWs
- aligning **context + model + prompt + tools** (the core four) to hit the bullseye repeatedly

This directly improves your **agentic coding KPIs** (attempts, size of work delegated, streak of success, and your presence).

### The real trick: avoid context rot and context bloat

Adding context is usually the easy part.

The real trick is:
- finding context **agentically**
- removing/delegating context so you don’t create **context rot** and **context bloat**

**Search and destroy** is the real skill.

---

# R&D Framework

When you boil it down, there are only two ways to manage your context window:

- **Reduce**: shrink what enters the primary context window
- **Delegate**: push work/context to sub-agents or other agents, keeping the primary window clean

Every technique below fits into one or both.

---

# Level 1 — Beginner Context Engineering

## 1) Measure the context window (what gets measured gets managed)

Your agent’s context window is a **precious, renewable, but limited temporal resource**.

- It’s **ephemeral** (resets)
- It’s “alive” for only so long
- The **state** inside it determines success

So you must measure it.

### Primary measurement modes

1) **Context already in the agent**
   - Use ` /context `
   - It shows exactly what the agent is carrying and how much is left.

2) **Context you might add**
   - Use IDE token counters / tokenizers (e.g., highlight tokens in a file)
   - Example: if a README is 2,600 tokens, any “read the README” action costs that.

If you aren’t paying attention to context state, you’re just vibe-coding and only tackling the lowest hanging fruit.

✅ **Rule:** Measure your context window.  
- Use ` /context `  
- Install a tokenizer in your IDE  
- Track what you’re feeding agents (and what it costs)

---

## 2) Don’t load MCP servers unless you need them (Reduce)

MCP tools can quietly consume a massive portion of your context.

Example issue:
- Default `mcp.json` auto-loads multiple MCP servers
- That auto-load can cost **~10–12%** of a 200K context window *before doing any work*

That’s wasted compute unless you truly need those servers every time.

### Recommendation

- **Do not ship a default “always-on” `mcp.json`** for the whole codebase.
- Prefer **explicit** MCP loading per task.

Example approach:
- Create specialized MCP configs:
  - `mcp.firecrawl.6k.json`
  - `mcp.github.8k.json`
  - etc.
- Launch with flags (conceptually):
  - run Claude with *only* the MCP server(s) you need for that task

✅ **Rule:** “Default MCP preload” is a beginner mistake.  
Only load MCP servers when explicitly needed because they have a cost.

This is **R** in **R&D**: **reduce** unnecessary default context.

---

## 3) Prefer Context Priming over a huge `claude.md` autoload memory file (Reduce + Control)

This is a bit controversial for beginners, but the recommendation is:

> Prefer **context priming** over relying on large “always-loaded memory files” like `claude.md`.

### What’s the problem with always-on memory?

Even if nothing is inherently “wrong” with `claude.md`, it’s often used poorly:

- It grows over time
- It becomes bloated with irrelevant context
- Worst case: it includes **contradictory information**
- It burns tokens on every boot—even when not needed

### The solution: keep `claude.md` *ultra slim*

Your `claude.md` should contain only **universal essentials** that you are 100% sure you want loaded 100% of the time.

That’s a strict condition—treat it like one.

### Context priming

Context priming is using a reusable slash command (or reusable prompt) like:

- `/prime`
- `/prime_bug`
- `/prime_feature`
- `/prime_chore`
- `/prime_cc` (Claude Code focused prime)

It sets up a **task-specific initial context window** by reading a few key files and producing a short report.

Example structure:

- Purpose
- Run step
- Read step
- Report step

✅ **Rule:** Prime, don’t default.  
Keep always-on memory minimal; use `/prime*` commands for dynamic, controllable setup.

This keeps agents focused and avoids context bloat.

---

# Level 2 — Intermediate Context Engineering

## 4) Control output tokens via output styles (Reduce cost)

Output tokens are typically the most expensive part:

- often **3–5×** the price of input tokens

When running **out-loop agents**, verbose responses burn budget fast—especially at scale.

### Technique: enforce a concise output style

Use a settings file (conceptually `.claude/settings.local.concise`), where you set output style to:

- “one word”
- or minimal “done / failed”
- or tight “status + pointers”

Effect:
- It “hot swaps” the output style block in the system prompt
- Agents stop chatting and only confirm success/failure unless asked

Example impact:
- A normal response might be ~150 output tokens
- A concise “done” might be ~2 tokens

At scale:
- this becomes a huge cost reduction
- especially for trigger-driven workflows and fleets of agents

✅ **Rule:** When you don’t need prose, don’t pay for prose.  
Constrain output styles for out-loop automation.

---

## 5) Use sub-agents properly (Delegate)

Sub-agents are powerful because they create a **partially forked context window**.

Key point:
- Sub-agent instructions are often stored as **system prompts** (not user prompts)
- That means they don’t bloat the primary agent context the same way

### Delegation example: doc scraping / AI docs refresh

Use a reusable command like:
- `/load_ai_docs`

Flow:
- Primary agent triggers the workflow
- Sub-agents do heavy web scraping / document ingestion
- Outputs are written to files
- Primary agent stays clean

Benefit:
- potentially **tens of thousands of tokens** spent in sub-agents instead of your primary context window

✅ **Rule:** Delegate large “token-eating” work (web fetch, doc ingestion, parsing) to sub-agents.

### Sub-agent warning

Sub-agents increase coordination overhead:
- you must track core four across multiple agents
- information flow becomes critical:
  - primary agent prompts sub-agents
  - sub-agents report back to primary agent

If you’re already losing control of a single agent’s context window, clean that up first before going heavy on sub-agents.

---

# Level 3 — Advanced Context Engineering

## 6) Planner + Builder (Delegate across two primary agents)

A classic scalable pattern:

- Agent A: **Planner** (architect)
- Agent B: **Builder** (editor)

Why it matters:
- planning often creates context bloat that isn’t needed during execution
- builder needs a surgical, focused context window for clean code edits

### Workflow

1) Run a planning prompt (e.g., `/quick_plan`)
2) Copy the plan artifact (or file reference)
3) Feed only the plan into the builder agent (e.g., `/build plan.md`)

This keeps:
- the planner’s “exploration tokens” out of the builder
- the builder highly focused
- the resulting work more reliable

✅ **Rule:** Separate responsibilities to reduce rot/bloat.  
Planning tokens are not implementation tokens.

---

## Summary: what to internalize

### Context engineering is core to TAC

You maximize agent performance by:
- adopting the agent’s perspective
- hitting the context sweet spot consistently
- scaling with R&D

### R&D framework recap

- **Reduce**:
  - measure context (`/context`)
  - avoid default MCP preload
  - shrink `claude.md` to universal essentials
  - control output tokens with styles

- **Delegate**:
  - sub-agents for heavy token work
  - planner/builder split for clean execution windows

---

## Next topic (cut point)

Next up: a powerful but risky feature in Claude Code:

- `/compact`

> You probably use it—but it has a huge problem.
> After compaction…

(continue in next note)