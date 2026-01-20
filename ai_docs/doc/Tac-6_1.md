# TAC — Lesson 6: Review & Document (Advanced Lesson 1 of 3)

Welcome to **Lesson 6** of Tactical Agentic Coding — your first of three advanced lessons.

In this lesson we focus on the **last two steps** of the software developer life cycle:

- **Review**
- **Document**

With these two steps, we get very close to the future where you can run **one prompt** that triggers a **fleet of agents** that ships work **end-to-end**.

So far, with the steps we’ve covered (plan, build, test), you can already outperform many cloud-based agentic coding tools — because you’re encoding *your* expertise and *your* domain knowledge into workflows. But we’re not done.

After this lesson:
- your agents won’t just **plan, build, and test autonomously**
- they’ll also **review their work** to ensure it matches what you actually asked for
- and they’ll **document** it so future agents become more effective

---

## Why Review Matters (And Why It’s Not the Same as Testing)

Some teams group testing and review together. That’s a mistake — especially in the age of agents.

Every SDLC step can be represented as a question + answer:

- **Plan:** “What are we building?”
- **Build:** “Did we make it real?”
- **Test:** “Does it work?”
- **Review:** “Is what we built what we planned?”
- **Document:** “How does it work?”

Testing answers: **Does it work?**  
Review answers: **Is what we built what we asked for? Prove it.**

So review is *not* mainly about code quality or implementation details — we’re handing that to agents and automated checks.

Instead, review is a specification alignment step:
> A dedicated set of agents answers: **Is the work aligned with the plan?**

This is essential to increase **review velocity**, and it addresses a core constraint in agentic coding: planning and reviewing at scale.

---

## Why Documentation Completes the Feedback Loop

After we:
1. confirm the app works (testing workflow)
2. confirm it matches the spec (review workflow)

…we document the work.

Documentation is “simple,” but:
- **what** you document
- **when** you document
- **where** you place it

…is the tricky part.

Why do we document?

Because inside the new **agentic layer** of your codebase, documentation becomes **feedback** for future agents:
- agents can reference what came before
- agents can update docs when it’s appropriate

This creates a complete SDLC feedback loop — and makes agents you run later more performant.

---

## Lesson 6 Tactic: One Agent, One Prompt, One Purpose

This lesson’s tactic solves many real problems engineers face when working with agents.

**Tactic:**  
> **One agent, one prompt, one purpose.**

This is a controversial commitment — but it lets you sidestep a huge list of agentic coding potholes.

Why?

Because “more context” is not always better.

Massive context windows often create:
- distracted agents
- confused reasoning
- **context pollution**
- **context overloading**
- **toxic context**

Big tech may chase the “all-in-one god model” — but that’s not what we’re doing here.

We’re doing real engineering with real constraints.

AI developer workflows exist because they add **compute to the developer**, not magic.

Engineers operate one step at a time:
- planning → building → testing → reviewing → documenting

Each step needs:
- different context
- different tools
- different perspective

So we encode the workflow and hand each step to specialized agents.

Important nuance:
- “one prompt” does not mean “small prompt”
- prompts can be large: metaprompts, templates, higher-order prompts
- the point is **single purpose + focus**

---

## Why This Tactic Works: Advantages of Specialized Agents

### 1) You free up the context window
You give the agent the full window (200k, 500k, 1M tokens, whatever you have) to solve *one problem well*.

As codebases grow, agents need more context to execute work — and specialized agents help manage that.

As agentic engineers, our constraints are:
1. the context window
2. the complexity of the codebase/problem
3. our own ability

Specialized agents bypass **two of the three**.

Model intelligence is not your constraint. Don’t use it as an excuse.

Also: tools like `compact` are band-aids — they reduce context by losing information.

### 2) You let your agent focus
A focused engineer is productive. Agents are the same.

More context adds more variables.
More variables → more confusion → worse agent performance → worse your performance.

So you want **minimum viable context** to solve the problem.

Adopt the agent’s perspective:
- what context does it have?
- what tools does it have?
- what leverage points can it use?

### 3) You can version and improve every prompt
This has a special side effect:

> You can commit every prompt and workflow and continuously improve them.

Instead of massive, one-off context dumps that disappear, you get:
- reproducible steps
- debuggable prompts
- improvable workflows

Search the slash command, open the file, and you know exactly what the agent sees.

Over time you also create “evals” naturally:
- swap models
- add thinking mode
- rerun the prompt
- compare outcomes
- systematically improve agent KPIs

---

## Getting Started: TAC 6 Setup

Business as usual:
- clone the Lesson 6 repo
- `cd` into it
- open your editor
- boot Claude (YOLO mode + Opus, as before)
- run `/install`

New addition in `/install`:
- Cloudflare env vars setup (for uploading image assets)
  - this becomes important in the **review workflow**

Everything else stays consistent:
- copy env vars
- reset DB
- start server in background

Use agents for setup — there’s no reason to do it by hand.

---

## New AI Developer Workflows in TAC 6

In the agentic layer (`adw/`), we now have new low-level workflows:

- **review**
- **patch**
- **document**

And composed workflows like:
- **plan → build → review**
- **plan → build → document**

Plan + build are foundational:
- you need something to review/document *against*
- review/document only exist after work exists on a branch

These workflows are standalone scripts (e.g., uv single-file scripts), which makes them composable and chainable via a shared ADW ID.

---

## Review Workflow: What It Does (At a Glance)

Top-of-file documentation should be clear and concise.

Review workflow in plain language:

1. Find the spec from current branch
2. Review implementation against spec (using git diff)
3. Capture screenshots of critical functionality
4. Report issues
5. If blockers exist: resolve agentically
6. Post results, push updates, update PR

You don’t even need to read the code to know what it does — because the workflow is documented clearly.

---

## Running Plan → Build → Review via GitHub Issue

Create a GitHub issue as the prompt source.

Example feature request:
- one-click table exports
- one-click result export as CSV
- two new endpoints
- UI should use the correct download icon

This is a high-level prompt moving toward mid-level.

Then run:
- `uv run adw/plan_build_review.py <issue_number>`

Agents take over the repo while this runs.
Don’t do parallel work in the same working tree while they operate.

---

## How Review Works Under the Hood

Key mechanics:

### 1) State travels with every ADW
Each workflow uses a shared state file containing:
- ADW ID
- branch name
- plan file
- issue class

Workflows validate state:
- you can’t review if you don’t have a plan + diff + branch

### 2) Review captures screenshots and uploads them
Review initializes an uploader (Cloudflare R2 in this example) to host screenshots publicly so they can be attached to:
- GitHub issues
- PRs
- any review surface

### 3) Review is two phases
- Run review
- If there are blockers → fix them agentically

Goal: reduce human-in-the-loop touchpoints.

If something goes wrong:
- don’t “fix the symptom” manually
- fix the end-to-end workflow so it doesn’t happen again

---

## The Review Prompt (Everything Reduces to Prompts)

The ADW code is mostly deterministic support and reporting.

The real behavior comes from the **review prompt**, which instructs the agent to:

- read the spec file
- compare to `git diff`
- verify critical functionality (screenshots)
- report issues or success

Output is standardized as **JSON** (typed output):
- `success`
- `review_summary`
- `issues[]`
- `screenshots[]` (with URLs after upload)

Issues are categorized into:
- `skippable`
- `tech_debt`
- `blocker`

Only **blockers** should trigger auto-remediation.

This prevents “agents always find something” from derailing progress.

---

## Fixing Review Issues: ADW Patch

If blockers exist, review triggers **patch**.

Patch workflow:
1. create a focused patch plan (surgical fix)
2. run implement on that plan

Patch plan prompt:
- minimal targeted change
- concise plan
- resolves one issue

Then it re-runs review loops (up to a max attempt count).

---

## Why Review Systems & Reporting Matter

A review system (GitHub issue/PR/Jira/etc.) is critical for outloop operations.

Most workflow code is reporting:
- status updates
- logs
- structured outputs
- links to screenshots

That’s not “extra”—it’s what makes outloop workflows usable.

Sometimes you still need to hop in-loop:
- to debug setup problems
- to improve prompts/workflows
- to fix workflow deadlocks

But the goal is always:
> improve the end-to-end system so the loop becomes less necessary over time.

---

## Summary: What Lesson 6 Adds

By the end of Lesson 6, your agentic layer supports:

- plan (metaprompt → spec)
- build (implement plan)
- test (closed-loop validations)
- **review (spec alignment + proof)**
- **document (capture “how it works” for future agents)**

And the tactic that makes it scalable is:

> **One agent, one prompt, one purpose.**