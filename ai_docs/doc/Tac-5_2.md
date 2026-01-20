# Lean Into the Future: Scaling Confidence With Closed Loops

Don’t lean into the present.  
Don’t lean into the past.  
**Lean into the future.**

Hand off **more** responsibility to your agents, not less.

With every test we add, with every validation step we encode, we increase confidence — we increase the certainty that our agent actually shipped the work correctly.

At this point we have **six closed-loop tests**. And while `pytest` alone is “a lot more than one test,” we can still treat it as one bucket — because the point is the same:

> More feedback loops = more confidence for the agent.

---

## From Closed-Loop Prompts to the Agentic Layer

Now we know we can write powerful closed-loop prompts that let agents validate their own work:
- run tests
- build
- compile
- verify UI behavior in the browser

We’re handing validation off to the agent — the same way you or I validate work.

So how do we take this further?

How do we embed this into the **agentic layer** we’re building around our codebases?

We teach agents to test by embedding validation into:
- templates
- reusable prompts
- metaprompts

---

## Reusable Prompts: The Growing Toolbelt

If we open `.claude/commands`, we can see a growing list of reusable, natural-language engineering solutions — essentially *agentic tooling* that can solve problems across the codebase.

Example: **the bug prompt**.

Let’s refresh the app: we see new tables appearing. A test deleted a user table and added junk tables like `drop_user`. That’s a bug.

So we resolve it.

And we resolve it without “coding” manually — because we stopped coding as the primary action. Instead, we’re **adding feedback loops into templates** and letting agents execute.

---

## The Bug Metaprompt

The `/bug` prompt is a **metaprompt**: a prompt that creates a prompt.

It generates a structured plan for fixing bugs consistently. This is templated engineering: you encode your process so agents can repeat it reliably.

Key principle:
- use fresh agent instances (avoid context pollution)
- provide the issue context
- let the metaprompt generate a plan

Inputs typically include:
- issue number
- ADW ID (if applicable)
- the bug description (high-level prompt)

In this example, the core problem is:

> tests are writing junk data into the “production” SQLite database.  
> tests should run in memory or isolated DB state.

---

## The Upgrade: Validation Commands Are Now Baked Into Plans

What changed in the plan template?

A huge improvement:

> **Validation commands are included by default in every generated plan.**

So with every:
- bug fix
- feature
- chore

…validation is baked in.

When we say “always add feedback loops,” we mean **always**.

And this isn’t cumbersome: you encode it once into reusable prompts, and your agents repeat it forever.

There’s also an extra rule:

> If you create an end-to-end test, include the additional validation step.

That ensures higher confidence and no regressions.

---

## Multiple Agents, Multiple Issues

While one agent is working, we can fire another issue:

Example UI bug:
- when running queries (e.g., “select five products”), the input field does **not** disable
- users can spam queries
- we want to disable input while running and add a debounce

This is classic low-hanging UI fruit — not something engineers should repeatedly solve manually.

So we spawn another bug request:
- ID: `ADW222`
- request: disable input while query runs + add debounce

---

## Comparing Plans: Backend Bug vs UI Bug

The backend bug plan:
- correctly identifies it doesn’t affect UI
- does **not** trigger end-to-end Playwright work
- includes backend-focused validations (examples):
  - run the specific failing pytest file
  - run SQL checks
  - output before/after state and diff it

These validation commands create multiple closed loops. If the agent makes a mistake, the validators catch it and force correction.

The UI bug plan:
- includes creation of an end-to-end test file
- lists the task explicitly: “Create end-to-end test”
- includes structured test content:
  - intent
  - steps
  - “verify” checkpoints
  - success criteria

This happened because the metaprompt includes the rule:

> If UI/user interaction is affected → add a test.

---

## In-Loop Limitation: One Agent at a Time

While in-loop (on your own device), you can’t safely run multiple agents simultaneously unless you’re extremely careful about file changes.

That’s a limitation of in-loop agentic coding:
- one agent modifying your working tree at a time

Off-device outloop systems avoid this:
- agents run in dedicated sandboxes
- they can take over the environment safely
- work is isolated and traceable

---

## Next Level: Get Out of the Loop With ADWs

After you have:
- reusable prompts
- metaprompts
- baked-in validation

…you move to the next tactic:

> **Stay out of the loop.**

That’s where **ADWs** (AI Developer Workflows) come in.

The ADWs directory becomes the highest-leverage composition layer:
- isolated scripts/workflows
- composable plan/build/test nodes
- run from GitHub issues (Peter framework) or local triggers

---

## ADW Test: Testing as a First-Class Workflow

The test workflow:
- fetches GitHub issue (prompt input)
- runs the application test suite
- reports results
- commits results and opens a PR (review)

Core idea:

> this workflow tests the application and fixes issues — autonomously.

It’s separate from plan/build:
- plan generates spec via `/feature` `/bug` `/chore`
- build implements via `/implement`
- test validates + resolves failures

This separation matters because you can improve each node independently.

---

## Standardized Test Output Enables Automation

The `/test` command:
- runs backend validations (ruff, compile, pytest)
- runs frontend validations (tsc, build)
- reports results in standardized JSON

Why JSON?

So failures can be handed off to **isolated resolver agents**:
- each failure spawns its own agent
- each agent has a fresh context window
- can be parallelized later

Then the workflow:
- parses results
- resolves failed tests
- reruns validations

---

## End-to-End Testing: Playwright as Feedback Loop

End-to-end testing uses:
- a higher-order prompt that takes an E2E test file as input
- preconditions (reset DB, ensure app running)
- screenshots
- structured output formatting

The workflow loops through all E2E tests and retries with resolution if needed.

---

## Observability Matters: Tracing Failures

When failures happen (e.g., cloud tool/API errors), the workflow should be traceable:
- ADW ID
- per-agent logs
- raw output preserved

Example failure mode:
- API error 500 from the model/tool provider
- tests fail because execution is interrupted
- logs reveal the exact cause

Even with failures, you still often get:
- a PR
- a spec
- new E2E tests
- implemented feature artifacts

Then the human reviews at the end:
- “test on top of the test”
- higher confidence than manual-first workflows

---

## Where This Heads Next: Review + Documentation

We’ve embedded testing into:
- daily prompts (bugs/features/chores)
- ADW workflows (plan/build/test)
- outloop execution via the Peter framework
- isolated environments

Next steps:
- **review**
- **documentation**

Codebases grow and evolve:
- features require updated docs
- shipping requires review discipline

In lesson six, we close the loop on the SDLC:
- plan
- build
- test
- review
- document

Start simple:
- one prompt
- one workflow
- then move it out of the loop
- stand up a dedicated agent environment
- keep adding feedback loops

We’re rolling. We’re making progress.

**See you in lesson six — where we close the loop on the software development life cycle.**