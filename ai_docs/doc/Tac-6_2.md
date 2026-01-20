# Review Proof, Patch Loops, and Agentic Documentation

We can compare **all the changes** made so far against `origin/main`.

You can see:
- there’s our plan
- it created a nice test
- it generated an end-to-end test

This is now just part of our engineering system — we encoded it into templates, so it happens routinely. That’s the path toward a world where we **stay out of the loop**.

These are the tactics you should be thinking about while operating with agents:
- **template your engineering** so you can stay out of the loop
- build systems that are **one agent, one prompt, one purpose**

---

## Review Is Running (And R2 Upload Is Enabled)

If we look at the `agents/ADW` directory, we can see we are now **reviewing the code**.

What comes next is exciting:

- **R2 upload enabled**
- a **public bucket** we can access

Assuming the workflow works as intended — and remembering these are non-deterministic systems — the goal is to build a pipeline of agents that:
- check each other’s work
- verify things look correct
- communicate clearly when something is wrong

Then we improve the composable units.

In this review step, we have roughly three distinct agents running. It’s a good practice to define agent names as constants at the top of the workflow file so it’s obvious:
- which agents run
- which agents control the workflow

We can always search the output logs to see exactly where the agent is.

The review phase includes:
- reviewing against the specification
- writing the review report
- uploading images
- resolving blocking issues (if any)

---

## Review Completed: Proof Reveals a UI Miss

The workflow completes: **plan → build → review**.

Now we see something incredible:

✅ **Images uploaded.**  
We can open the public URL and inspect the screenshot.

And the screenshot shows a problem:

> The export/download icon is not placed correctly.  
> It should not be centered — it should be placed next to the Hide button.

So the agent didn’t obey that requirement fully.

This is a perfect example of why a **concrete review step** matters — and how it helps you continuously improve the workflow.

Even though the agent reports:
- “one-click export implemented”
- “error handling added”
- “all tests passed”

…there’s still work to do in review correctness.

We can see:
- export button appears here
- but we asked for it to appear **next to the Hide button**

So we patch it.

---

## Verify the Feature Manually (Quick Spot Check)

We can start the app and verify behavior:
- click the download icon
- confirm a CSV downloads (works)
- run a query (e.g., “select five users”)
- confirm export works for results (works)

The **feature works**, but the UI placement is wrong:
- export should be just to the left of Hide
- currently misaligned

This is a great showcase for the patch workflow.

---

## Run a Patch: Fix the Placement

We run **ADW patch** — operating as if we’re outside the loop:

Inputs:
- issue number (same issue)
- existing **ADW ID** (because we’re building on existing work)
- patch instruction: place export/download button directly left of Hide

If you pass the wrong ID (PR ID vs Issue ID), rerun with the correct issue number. The workflow finds state from the ADW ID and proceeds.

---

## Why Did This Slip Through?

Two likely reasons:

1) **We skipped the test workflow**
   - UI end-to-end tests likely would have caught this placement issue.

2) **The review step didn’t truly “see” the screenshots**
   - The system captured screenshots, but the screenshots never made it into the agent’s context.
   - The agent operated Playwright, but without pulling screenshots into its reasoning window.

A workflow improvement could be:

> For every screenshot captured, read it into the review agent context during review.

This would likely help the agent catch subtle UI issues like alignment and placement.

---

## Patch Completed: The UI Is Now Correct

Patch completes and produces a patch plan artifact under `specs/patch/`.

We track major work consistently:
- plan files for large work
- patch plans for surgical fixes

The patch plan is concise:
- summary of issue
- targeted fix (e.g., group export + hide into a container on the right side of results header)

After refresh:
✅ Export is now right next to Hide.

---

## “Why Not Just Fix It By Hand?”

You’re missing the point.

The point isn’t whether *you* can fix this fast manually.

The point is building:
> **the system that builds the system**

This isn’t about you anymore. It’s about your agents.

You’re teaching them how to build on your behalf — so it can be about you again.

Remember tactic #1:
> **Stop coding.**

Move up the stack. Become a commander of compute:
- hand off more work to agents
- even small fixes like this
- focus on the high-level work

---

## Documentation: The Final Step

Now we document the feature.

We run `adw/document`:
- against the same issue
- using the same ADW ID
- so it can reference:
  - the `git diff` against `origin/main`
  - the spec/plan file

The documentation workflow:
1) generates new docs (Markdown)
2) updates “conditional documentation” so future agents know what to read

---

## Document Prompt: What It Does

The `/document` prompt generates concise Markdown docs into `app_docs/`.

It:
- diffs against main
- reads the plan/spec
- writes documentation in a consistent template

You can customize the template:
- how you like to document
- what structure you prefer
- what “done” looks like

The output typically includes:
- what was built
- how it works
- what files were changed
- how to use it
- screenshots (if available)

---

## Conditional Documentation: The Magic Layer

Documentation is not only about writing new docs.

It’s also about:
> knowing when and how to pull documentation into future agent runs

The document workflow updates a lower-level prompt: **conditional documentation**.

This prompt says:

- review the conditions
- if your task matches, read the relevant docs before working

This file is referenced across:
- feature
- bug
- chore
- patch
- prime

So documentation becomes part of the planning loop.

This connects:
- planning (beginning of SDLC)
- documenting (end of SDLC)

into a **full feedback cycle**.

---

## Full SDLC Loop Completed

At this point we have:
- a plan
- implementation
- review proof (screenshots)
- patch capability for fixes
- documentation
- conditional docs updated for future work

This is the agentic layer doing more than “just coding.”

Engineering is more than editing files:
- review
- proof
- documentation
- reproducibility

That’s what agents enable when you design the system properly.

---

## Review Proof-of-Value (Even When the Agent Is Wrong)

Review answers the critical question:

> **Is what we built what we asked for?**

Even when the agent is wrong, proof makes it fast to decide:
- yes / no
- patch immediately
- improve workflows

The “proof asset” depends on your domain:
- UI → screenshots/video
- ML/data work → reports, metrics, artifacts, diffs
- analytics/prototyping → outputs, charts, saved runs

Embed the review steps you would personally take into your ADW review workflow.

---

## Why ADWs Matter: The Power Is in Composition

The value isn’t one workflow.

It’s combining isolated workflows:
- plan
- build
- test
- review
- document

They are:
- isolated
- reviewable
- improvable

And they work together cleanly because each runs:
> one agent, one prompt, one purpose

Benefits recap:
- frees context window
- improves focus
- prompts are reusable + improvable
- enables evaluation (explicitly and passively)

---

## KPIs in Practice

In this example:
- We started with **one prompt** (attempt = 1)
- We needed a patch (attempts = 2) → not ideal
- Size shipped was strong (export feature worked)
- Streak was broken because we needed two workflows
- Presence was low: we saw proof, patched, verified

Ideal presence:
1) prompt input at the start
2) final review + merge at the end

In the next lesson, we push this further.

---

## What’s Next: Lesson 7

Lesson 7 reveals the “secret” of tactical agentic coding.

We’ll stop working on toy examples and start showing:
- how fast you can ship with a mature agentic layer
- how workflows compound leverage
- when to use “dangerous/YOLO mode” (carefully)
  - not for big features
  - but potentially for small bugs/chores

Don’t wait to apply this:
- set up basic ADWs
- set up focused agentic prompts
- start compounding your advantage

See you in **Lesson 7**.