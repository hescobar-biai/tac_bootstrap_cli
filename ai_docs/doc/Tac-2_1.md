# Tactical Agentic Coding (TAC)  
## Lesson 2 – Leverage Points (Continued) + KPIs

### Why Tests Are Non-Negotiable

To scale agentic coding, your agents must be able to:

> **Validate their own work.**

Testing is one of the highest leverage points in agentic coding. If you’re not writing tests, this is likely the first leverage point you should prioritize—right alongside **standard output (stdout)**.

We’ll go deeper on testing in future lessons, but the direction is clear:

- **Backend tests** are typically simpler to implement and run.
- We also need **frontend tests**, because we want agents to *see* the results of their work:
  - click buttons
  - validate UI outcomes
  - confirm behavior end-to-end

Throughout Tactical Agentic Coding, we’ll use agents for both backend and frontend testing.

---

## Leverage Point: Plans

Plans are a popular and powerful leverage point.

Example: opening a `specs/` folder might reveal a large “initialize codebase plan” file:
- hundreds of lines
- detailed requirements
- types, frontend/backend structure
- code examples

Most engineers don’t spend enough time communicating what they want done.

### What a plan really is
- Simply: **a plan is a prompt**
- More accurately: **a plan is how you communicate massive work to your agent**

Plans are how we:
- scale up the amount of work we can hand off
- do more in less time
- increase autonomy

And importantly:

> Great planning is great prompting.

We are not typing 700-line plans by hand.

We plan **with our agent**:
- you start with a high-level (often low-information) prompt
- you hand it to the agent
- the agent generates a first draft plan
- you refine it into something reliable

Planning is the first step of the SDLC:
- define what you want
- communicate it clearly

If you nail planning, the rest of the SDLC steps we automate will fall into place.

---

## Leverage Points: Templates + ADWs

After plans, two key leverage points remain:
1. **Templates**
2. **ADWs (AI Developer Workflows)**

### Templates
Templates are essentially:
> **Reusable prompts**

These are not “templates” in the traditional sense—they’re agentic prompts you reuse and pass information into.

In TAC codebases, these often appear as **slash commands**:
- `/command`
- `/command`
- `/command`

The goal:
> You want many commands that let you trigger real engineering work instantly.

These become a core part of daily agentic operation.

### ADWs (AI Developer Workflows)
ADWs are the highest level of abstraction.

An ADW is created when you:
- combine one or more **agentic prompts** (often from a `commands/` directory)
- wrap them in arbitrary code
- kick them off **autonomously** with a **trigger**

This is where programmable agentic tooling matters.

#### Programmable mode example (conceptually)
Instead of iterative back-and-forth prompting, you run:
- “Do this work”
- “Call this command”
- “Return the result”

This is how real engineering work happens autonomously.

> ADWs are prompts + code + trigger → so it runs itself.

This is the leverage point that enables SDLC automation so deeply that your codebase can “run itself”.

Every tactic and concept in TAC pushes toward this.

---

## Measuring Success: Agentic Coding KPIs

We don’t want random vibe coding.
We want measurable improvement.

If you don’t measure it, you can’t improve it.

### The 4 KPIs
There are four numbers that define agentic coding performance:

1. **Size**
2. **Attempts**
3. **Streak**
4. **Presence**

Goal direction:
- Increase **Size**
- Decrease **Attempts**
- Increase **Streak**
- Decrease **Presence**

These four KPIs are enough to track improvement.

---

## KPI 1: Size (Increase)

**Size** = how much work you can hand off to your agent.

If you’re improving, size goes up:
- bigger plans
- longer autonomous runs
- more complex tasks completed in one shot

Example progression:
- 5 minutes → 10 → 20 → 30 → 60 minutes → multiple hours

Don’t underestimate how much work you can hand off autonomously.

---

## KPI 2: Attempts (Decrease)

**Attempts** = how many times you must re-prompt to fix issues after the agent run.

Attempts cost your most valuable engineering resource:

> **Your time.**

If attempts are consistently high (e.g., 5–10, even 3–6), it usually means you’re missing leverage points.

Iteration is sometimes fine in exploratory work, but the goal here is different:

> We want one-shot solutions.  
> We are not aiming to become babysitters for AI agents.

“Tactical agentic coding” is not iterative prompting.

---

## KPI 3: Streak (Increase)

**Streak** = back-to-back one-shot successes.

We want:
- 3 in a row
- 5 in a row
- 10 in a row

An engineer who can run five one-shot prompts that ship real features back-to-back drastically outperforms one who must fix issues after each prompt.

Rule:
> Once you start one-shotting, don’t break the streak.

If you break it:
- identify which leverage point was missing
- fix the system, not just the symptom

---

## KPI 4: Presence (Decrease to Zero)

**Presence** = how much you must sit there guiding and correcting the agent.

Many engineers assume the end game is:
- constant monitoring
- endless prompt back-and-forth

That’s not the end game.

That’s the early game.

The target:
> **Lower presence to zero.**

This doesn’t mean you abandon observability.
It means you let go of hands-on control while maintaining the ability to observe and correct when necessary.

It may feel uncomfortable—engineers love control—but autonomy requires letting go.

---

## How Leverage Points Improve KPIs

Every KPI can be improved using one or more leverage points.

Examples:
- Confusion from dictionaries instead of types → **use types**
- Repo structure inconsistent → **refactor for agent navigation**
- You manually read error messages → **stop** and give them to the agent
- Short iterative prompting → **write plans**
- Agent “succeeds” but bugs exist → **add tests**
- Repeating workflows → **turn them into templates/slash commands**
- Need fully autonomous SDLC automation → **ADWs**

The meta-summary tactic still holds:

> **Adopt your agent’s perspective.**

This drives everything:
- Size up
- Attempts down
- Streak up
- Presence down

---

## Transition: Iterative Mode → Programmable Mode

We’re leaving beginner territory and entering intermediate.

So far, we’ve often used tools in a more iterative “phase 1” way:
- back-and-forth prompting
- frequent interactions (high presence)

That tanks the **Presence** KPI (drives it up).

As TAC progresses, we’ll shift toward:
- **programmable mode**
- autonomous execution
- triggered workflows

This will be uncomfortable, but it’s the direction of Phase 2 engineering.

What stays constant:
- architecture
- direction
- planning
- thinking
- engineering outcomes for users

---

## Looking Ahead: Lesson 3 (Plans)

Some leverage points are so powerful they deserve full lessons.

Lesson 3 focuses on one of the strongest:

> **The Plan**

You’ll learn:
- metaprompting
- higher-order prompts
- reusable plans
- converting high-level intent into low-level, accurate execution details

Plans written from your agent’s perspective make success inevitable.

You’ve got the momentum.

See you in **Lesson 3**.