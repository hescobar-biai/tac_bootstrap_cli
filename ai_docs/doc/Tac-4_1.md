# Tactical Agentic Coding (TAC)  
## Lesson 4 – AFK Agents, Out-of-Loop Execution, and ADWs (AI Developer Workflows)

### Let Your Product Build Itself

Welcome to **Lesson 4** of Tactical Agentic Coding.

In this lesson, you step **out of the loop** and let your product **build itself**.

How? By adding **four elements of AFK agents**, enabling you to trigger agents to run in their own environment.

By the end of the lesson, you’ll know how to **replace and outperform** modern cloud-based agent coding tools like:
- Copilot
- Devon
- Jules
- Codeex
- and other cloud coding agents

These tools are useful, but they often lack the domain-specific detail needed to ship end-to-end in *your* codebase using *your* engineering practices.

They have natural limits because they’re built for **everyone’s** codebases, not yours.

Just like the prompt, your **agentic pipeline** is too valuable to outsource—especially this early in “Phase 2” of the generative AI era.

> You want to own your agentic pipelines.

You want to slice and dice agents across:
- your codebases
- the software development life cycle (SDLC)
- your own templates and practices

---

## The Compressed Mental Framework So Far

Every tactic is designed to be a simple, compressed framework you can use daily:

1. **Stop coding**  
   Your hands and mind are no longer the best tool for writing code.

2. **Adopt your agent’s perspective**  
   Maximize leverage from your agents.

3. **Template your engineering**  
   Deliver consistent results across complex codebases over hundreds of runs.

4. **Stay out of the loop** (Lesson 4)  
   Let agents run without you.

---

## Staying Out of the Loop

### Two types of agentic coding
There are two types of agentic coding—both powerful:

#### 1) Human-in-the-loop (in-loop)
This is what most engineers do today:
- sit at the device
- prompt back-and-forth
- burn time on chores/bugs/features that don’t require their expertise

Even as the ecosystem celebrates “human in the loop,” it misses a key trend:

> More and more tasks can be fully delegated if you encode them properly.

In-loop agentic coding is real, but it doesn’t scale as well.

#### 2) Out-of-the-loop (outloop)
Outloop agentic coding is **off-device** agentic coding.

You write high → low-level prompts and pass them into an agentic pipeline, then you go **AFK** (away from keyboard).

You might not even be at a keyboard:
- phone
- GitHub
- Slack
- Notion
- Jira
- text message
- any third-party tool

**Stay out of the loop** is a tactic that leverages a fundamental truth:

> Models will improve and tools will change.

Over time, your agents will solve more problems with each improvement.

So instead of doing work yourself, you focus on scaling what your agents can do.

> You build the system that builds the system.

---

## KPIs and Why Outloop Matters

Outloop ties directly to improving agentic coding KPIs:

- Presence **down**
- Size **up**
- Streak **up**
- Attempts **down**

What’s the best way to drive these KPIs?

> Stay out of the loop and build the system that builds the system.

We do this by adding a new **agentic layer** to your codebase.

This will feel different. A bit challenging. But it’s powerful if you act on it.

We’re not playing today’s game.

> We’re playing tomorrow’s.

If you think AI can’t ship your “special snowflake” work end-to-end:

> If you’re not wrong now, you will be. It’s only a matter of time.

Bet on the future. Keep it simple. Lean in.

---

## From Prompt to PR

With what you’ve learned so far in TAC, you can automate nearly half the SDLC:

> **Prompt → PR**

Lesson 3 showed templating engineering. That’s mission-critical for outloop systems because templates encode your solutions into the codebase for agents to reuse.

One size does not fit all—especially as your product becomes unique.

---

## ADWs: The Highest Leverage Point

In Lesson 4, we chain templates together into the highest composition level and leverage point in agentic coding:

> **ADW – AI Developer Workflow**

An ADW is a reusable agentic workflow combining:
- code
- agentic prompts
- agents

…to deliver results autonomously.

Think of ADWs as:
- agentic pipelines
- agentic workflows
- future “scripts” where agentic behavior is expected by default

ADWs synthesize:
- deterministic code (previous-gen systems)
- non-deterministic LLMs (prompt chains + agents)

If you understand and apply ADWs, you’ll fast-track your transition into the future while others are still prompting back-and-forth at their device.

---

## AFK Agents: The Four Elements

To build outloop systems, you need AFK agents: agents that run while you’re away.

There are **four elements** of AFK agents:

1. **Prompt Input**
2. **Trigger**
3. **Environment**
4. **Review System**

Mnemonic: **PETER**
- **P**rompt
- **I**nput
- **T**rigger
- **E**nvironment
- **R**eview

With PETER, your agents can run while you’re AFK.

In this lesson, we run **two ADWs** to automate the **Plan** and **Build** steps of the SDLC:

> Prompt Input → Review

---

## First ADW: A Simple End-to-End Outloop System

We keep it simple but demonstrate the power of a dedicated environment.

### PETER mapping (example setup)

**Prompt Input:** GitHub Issues  
- Create an issue
- Title + description = the prompt the agent executes

**Trigger:** GitHub Webhooks  
- When the issue is created/updated, webhook triggers the workflow

**Environment:** A dedicated machine (example: a Mac mini)  
- Agent has full control in its own environment
- It waits for webhook events and executes workflows

**Review:** GitHub Pull Requests  
- After work is complete, the agent opens a PR for review

---

## Example: Triggering an ADW via GitHub Issue

Create a lightweight issue such as:

**Title:** ADW documentation  
**Body:**  
- `/chore` document the ADW directory  
- read everything in ADW  
- update README with how it works

Chores are the simplest unit of engineering work your agent should take off your plate.

When you create the issue:
- the webhook triggers
- the environment picks it up
- the agent posts progress comments
- it classifies the issue (chore/bug/feature)
- creates a branch
- generates an implementation plan
- implements the plan
- commits changes
- opens a PR

This is the SDLC Plan + Build steps running autonomously.

---

## Why This Works: Micro-Agents and Isolation

By separating agents, you isolate the “Big 3” (context/model/prompt) to solve one problem at a time.

Even in this small workflow, there may be multiple micro-agents:
- classify work
- create branch
- generate plan (planner agent)
- implement plan (implement agent)
- commit
- open PR

A key advantage:
- planner creates a spec
- implement agent has a clean context window
- implementation can use a stronger model
- the plan becomes the prompt for implementation

---

## Reviewing the Outcome

In the PR:
- you see the plan generated by the planner agent
- you see the implementation changes
- you review only the files affected
- you refine templates if clarity or naming is off

Important note:
- if something is wrong, you encode the fix into templates
- future agents stay on track automatically

> Success is planned.  
> You can plan success into your codebase by templating engineering.

---

## Second Run: Local Script Trigger (No Webhook)

To avoid webhook firing while you inspect, you can disable the webhook and run locally.

Then your PETER mapping becomes:

- **Prompt Input:** still GitHub Issues (or local prompt source)
- **Trigger:** local script from TAC 4 codebase
- **Environment:** your local device
- **Review:** GitHub PRs

This makes it easier to follow along and debug.

---

## TAC 4 Setup Notes (High Level)

Workflow setup includes:
- cloning TAC 4 repo
- running `/install`
- checking what install does before running
- unsetting remote origin (so you can push to your own repo)
- copying environment variables (top-level env file)
- installing backend/frontend deps
- copying reusable resources from prior lessons

The AFK agent requires:
- a remote repo (for Issues + PRs)
- environment variables (e.g., API key + tool path)

---

## Next Example Prompt: JSONL Support Feature

Create a new GitHub issue as prompt input:

**Title:** JSONL support  
**Body:**  
- add support for uploading JSONL files  
- standard library only (no new libraries)  
- concat nested fields  
- handle arrays  
- update UI

This is a high → mid-level prompt:
- enough detail to guide the workflow
- still abstract enough for the planner agent to expand into a plan

Then your ADW runs:
- plan generation
- implementation
- validation
- PR review

---

## Key Takeaway

Lesson 4 is about:
- owning your pipeline
- chaining templates into ADWs
- building AFK agents with PETER
- staying out of the loop so your product can ship itself

Once you internalize this, you’re no longer “prompting.”

You’re operating an engineering system where agents deliver work autonomously.