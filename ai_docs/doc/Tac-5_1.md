# TAC — Lesson 5: Closed Loops, Testing, and Self-Validation at Scale

## The Real Asset: User Experience (Not Code)

Welcome to **Tactical Agentic Coding — Lesson 5**.

Let’s be brutally honest: engineers often assume our most valuable output is:
- code
- architecture
- systems
- plans
- features

That’s wrong.

**Our most valuable contribution is the experience we create for users.**

So one of the most valuable things we can do is ensure all the engineering work:
- does what it’s meant to do
- ships correctly
- stays correct as the codebase evolves

How do we do that?

**We test. We validate. We close the loop.**

So we *know* the experience we designed is what ends up in users’ hands.

---

## The Massive Opportunity: Agents Testing For You

Agentic coding gives us an enormous advantage:

> Your agents can test on your behalf at a scale you will never reach manually.

That’s the gift of:
- generative AI
- agent architecture

This lesson is guided by one question — and it’s a major leverage point:

> **Given a unit of valuable work that’s production-ready, how would you (the engineer) test and validate it?**

If you can answer that for every class of work your codebase handles, and then encode it into:
- a command
- a tool call
- an ADW step

…you will move faster than everyone else.

It’s simple in concept, and depending on your staging/production setup, complex in execution.

This is where architecture becomes a major leverage point — and **net-new codebases** have a big advantage.

---

## What Validation Usually Looks Like

When shipping to production, you typically follow a concrete flow to confirm success, such as:

- run a linter
- run unit tests
- run UI tests
- run CI/CD integration tests
- build/compile the app
- check logs (e.g., DataDog) for expected signals
- check error tracking (e.g., Sentry) for absence of errors
- run domain-specific evals (ML/data science evaluation, LLM-as-judge workflows)

And the big one:

> open the browser and click through the feature

This is a feedback loop… and it’s a waste of time.

Not because it’s “bad,” but because it’s work you and I will do less and less as agentic systems scale.

These are feedback loops you can hand off to agents.

---

## Lesson 5 Tactic: Always Add Feedback Loops

Lesson 5 tactic is dead simple:

> **Always add feedback loops.**

Work is useless unless it’s tested.

- The ultimate test: **users**
- The next best test used to be: **you**
- Now the next best test is: **an army of agents** running:
  - regression tests
  - end-to-end tests

This isn’t “stop testing.”
It’s “start teaching your agents to test.”

Why?

Because you can create **closed-loop feedback systems** where agents:
1. execute
2. validate
3. reflect and fix
4. repeat until success

This increases autonomy and strengthens the agentic layer around your codebase.

> This is building the system that builds the system.

---

## Terminology: In-Loop vs Out-Loop vs Closing the Loop

**In-loop agentic coding**  
You’re at the keyboard prompting back and forth.

**Out-loop agentic coding (AFK / off-device)**  
A high-level prompt runs through the **Peter** system:
- prompt input
- trigger
- environment
- review

**Closing the loop**  
The agent:
- does the work
- calls validators/tools
- uses feedback
- keeps iterating until feedback is positive

That’s what it means to close the loop.

---

## A Hard Line: Agents + Testing Win

A debate ends here:

> Engineers who test with agents win. Full stop. Zero exceptions.

Why?

Because test value multiplies by the number of agent executions in your codebase.

Testing is one of the highest leverage points in agentic coding because it enables:
- closed-loop iteration
- self-validation
- confidence scaling

If tests pass:
- you trust the system more
- you stop second-guessing
- you focus on what’s next for users

Same for agents:
- failing tests = cannot ship
- must fix and rerun until green

**Tests make success scale.**

---

## Testing: The Core Question

Testing is simple:

1. **Did it do what you designed it to do?**
2. **Did it break anything else?**

Lesson 5 teaches you to hand off the **test step** of the SDLC to agents so you can improve agentic KPIs:

- attempts ↓
- size ↑
- streak ↑
- presence ↓

We want **end-to-end agents**, not just “good agents.”
And we don’t want them stuck in the loop forever.

---

## Setup: Clone TAC 5 + Agentic Install

We clone the Lesson 5 repo and run `/install`.

Reminder:
- always review slash commands
- they behave like scripts and have real power

What’s new in this install flow:
- resets the SQLite database automatically
- copies env vars (from TAC 4 into TAC 5)
- starts the server
- validates setup
- reports results back

---

## Closed-Loop Prompts: Anatomy

Closed-loop prompting has a consistent structure:

1. **Request** (what to change)
2. **Validate** (commands/tests to run)
3. **Resolve** (if any validation fails, fix and rerun)

> **Request → Validate → Resolve**

This creates a small loop system where the agent tests itself.

---

## Micro Example: One Validator (Ruff)

A simple change:
- comment out validation
- then validate with `ruff`

Ruff catches an error (unused import).
The agent:
- reads stdout feedback
- fixes the issue
- reruns ruff
- completes successfully

That’s the simplest closed loop.

---

## Scaling Up: Multiple Feedback Loops

Next prompt adds multiple validators:

- `ruff` (lint)
- `pytest` (unit tests)
- `python -m compileall` (compile)

The agent:
- makes changes (remove unused endpoint, move env load)
- runs ruff
- hits an error (“load above import”)
- fixes it
- reruns ruff
- runs pytest
- finds a failing test caused by an earlier prompt
- fixes the bug
- reruns pytest
- runs compile step
- finishes

Key principle:

> Tests should be the rule of law in your codebase.

If tests are wrong, fix tests so that test commands carry real weight.

---

## What’s Missing: Front-End + End-to-End Validation

Two major missing categories:
- **front-end tests**
- **end-to-end tests**

We want agents testing the application like a real engineer would.

So we build a reusable validation prompt that includes:

- backend checks (ruff, pytest, compile)
- front-end checks (TypeScript checks, build step)
- end-to-end validation via browser control

---

## Browser-Control E2E: Playwright MCP

We run the Playwright MCP server to validate end-to-end behavior:

- open the app
- take a “before” screenshot
- run a natural-language query (agent types/clicks)
- take an “after” screenshot
- read both screenshots
- verify:
  - query executed correctly
  - expected count (e.g., **7 results**) returned

This validates a precise, observable outcome.

You can point this at:
- local
- staging
- production test accounts

The key is giving agents the ability to validate completion.

---

## Observations: Agents Doing Real Validation Work

The agent produces artifacts:
- before/after screenshots
- logs
- validation outcomes

This is literally what an engineer would do to validate — but automated.

Even if the app is simple, don’t let that deter you:
- the pattern scales
- feedback loops scale autonomy
- validation reduces wasted time

---

## The Point: More Feedback = More Agency

Agents gain agency when you give them self-validating loops.

If you don’t provide testing and closed loops:
- you waste time
- agents fail silently or drift
- you stay stuck babysitting outputs

But if you keep layering feedback loops:
- the agent corrects itself
- you reduce review time
- you scale reliability
- you lean into the future

> Save time. Become agentic. Build closed loops.