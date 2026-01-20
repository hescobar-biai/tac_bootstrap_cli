# Lesson 7: Approaching the Edge of Agentic Coding

Welcome to **Lesson 7**, your second-to-last Tactical Agentic Coding lesson.

Here, we approach the **edge of agentic coding**.

We ship **end-to-end** with our **outloop system**, delivering more engineering value than we ever could before. In the next hour, you’ll witness something most engineers dismiss as impossible:

> A codebase that nearly runs itself.

This lesson flows differently from the rest.

---

## What We’ll Do in This Lesson

First, we’re going to hand off **five net new pieces of work** to the agentic layer that now ships end to end:

- Plan
- Build
- Test
- Review
- Document

You’ll see the **order-of-magnitude improvement** in engineering velocity and what it looks like to fully invest in the agentic layer.

Next, we’ll work through a few additions that increase engineering velocity with agents.

Then we’ll break down how we’ve parallelized AI developer workflows using **git worktrees**. This enables multiple agent pipelines to execute simultaneously in **isolated environments** on a single device.

You can tweak this however you like:
- set up containers
- use Docker
- use multiple machines

We’ll keep it simple and focus on the key idea:

> scaling beyond what in-loop agentic coding can offer.

Midway through the lesson, we’ll introduce the **third level of agentic coding**.

On the agentic engineering velocity scale, there are three levels:
1) **In-loop**
2) **Outloop**
3) **(A third level beyond outloop)**

Most engineers are operating in the loop.

Throughout TAC, you’ve learned how to construct powerful outloop systems that outperform out-of-the-box agent coding tools because they contain **your engineering practices** and **your engineering workflows**.

But there’s a level beyond outloop systems.

We’ll understand a critical moment in the future where **human-in-the-loop review becomes a bottleneck**, not a safety net. This tactic will lead us to the secret of tactical agentic coding.

---

## Collect the Dividends of the Outloop System

Let’s collect the dividends from our complete end-to-end outloop agentic system.

Once you’ve invested in your outloop system — once you’ve built **the system that builds the system** — it pays you back massively.

We’ll prompt, let agents cook, review the codebase, and then review their work.

As we go, we’ll address:
- shortcomings
- trade-offs
- improvements for this version of the system
- how to move toward the next scale of agentic coding

We are approaching the edge. These are the advanced lessons.

Some ideas haven’t fully arrived yet, but the goal is to give you the greatest edge possible.

So let’s get started and hand off more work than ever with the new agentic layer of our codebase.

---

## Dedicated Agent Environment and Trigger System

We have our dedicated agent environment up and running.

- The webhook trigger is ready for prompts coming in from GitHub issues.
- GitHub issues are our prompt input from the **PETA framework**.
- We’ve templated our engineering.
- We’re operating out of the loop.

So we can scale impact as easily as copying a file.

Open the agent environment:
- refresh the app
- see the codebase (a natural language SQL interface)

Now we rapidly enhance the application.

Our agents know how to operate the codebase — let’s put them to work.

We open:
- the editor
- the webhook runner
- GitHub Issues (prompt source)

Remember the PETA framework:
- Prompt input
- Trigger
- Environment
- Review system

Our prompt input is GitHub Issues.

---

## Hand Off 5 Pieces of Work (End-to-End)

We’ll fire off **five issues**, back-to-back, that run end to end.

We’ll intentionally mix difficulty levels.

### 1) Feature: Increase drag-and-drop surface area

We want to increase the drop zone surface area so we can drag and drop over any element.

### 2) Feature: JSON export

Simple high-level prompt:
> “I want JSON export.”

Agents handle the rest.

### 3) Feature: Generate synthetic random data from schema

We want the ability to click a table and generate additional random data based on the existing schema and table patterns.

This is the kind of mid-level prompt you might get from a PM or build into your product.

Now you can have agents do this in parallel at scale.

### 4) Chore: Improve model for query generation

We want better models for query generation.

Example:
- update model to use `o4-mini`
- currently set to GPT-4.1

This is representative of work you don’t need to do manually anymore — hand it to agents.

### 5) Bug: UI mismatch in product export label

Example bug:
- product CSV export shows chart icon + “CSV”
- selecting a product shows mismatched text

We want to align it.

This is small — we won’t run the full SDLC flow.
We’ll use a **patch workflow**.

---

## Fire Them All Off in Parallel

Five issues. Fired back-to-back.

Our outloop agent system picks up events and starts work.

We’ve learned to stay out of the loop.

We verify the agent is picking up events:
- open code/editor
- see events coming in
- agents have full control over the device
- issues update live with workflow logs (review system feedback)

We keep going.

This is what it looks like to scale:
- feature after feature
- in parallel
- with rich workflows

It’s absurd levels of scale.

We now have:
- not one issue
- not two
- but **three, four, five** issues getting tackled by agentic pipelines (AI developer workflows)

This happens because we encoded engineering into the agent layer.

Now it operates for us.

---

## While Agents Work: Understand the Agentic Layer

There will be waiting and reviewing, so we use the time to break down what changed in the codebase and how the agentic layer works.

This isn’t about the toy app.

The ideas scale to your real codebases.

We’re wrapping the codebase in a new agentic layer that operates the codebase on your behalf.

We open the terminal:
- clone the lesson 7 codebase
- run the usual workflow:
  - start Claude in YOLO mode
  - run `/install`

We don’t do simple hands-on work anymore — agents do it.

If something is missing from your usual developer workflow:
> embed it into the agentic layer.

---

## The Highest Leverage Unit: ADWs

Recap: the top-level unit of the agentic layer is **ADWs**.

In Lesson 7, we have additional workflows — the most important being:

- **ADW SDLC ISO** (Software Development Life Cycle — isolated)
- **SDLC ZTE ISO** (we’ll break down later)
- **ADW Ship ISO**

We focus on the key idea:

> end-to-end agents shipping work on our behalf the way we would.

The ADW directory is a scripting layer to construct pipelines of agents that solve classes of problems back-to-back-to-back.

Not all workflows will work perfectly end to end — and that’s fine.

We’re leaning toward the future:
- moving from in-loop → toward outloop
- improving workflows one day at a time
- improving down to the prompt level

---

## SDLC in Isolation: Plan → Build → Test → Review → Document

This is the SDLC workflow in isolation:

- Plan
- Build
- Test
- Review
- Document

This is what we fired off for most of the issues.

For the small UI mismatch bug, we used patch:
- simple cleanup
- no need to run full SDLC for small text alignment (though you could)

This SDLC workflow is what we’ve been building up to:

> full automation across the software developer lifecycle.

There are many flavors. You’ll tweak it and make it your own — but it’s an incredible starting point for the agentic layer of a codebase.

At a high level, it’s composed of smaller building blocks:
- plan
- build
- test (sometimes skipping e2e to save time)
- review
- document

---

## The Scaling Leap: Parallelism with Git Worktrees

Now the interesting part:

Before, the agent box was limited to operating in the base directory.

Now we use **git worktrees**.

It doesn’t matter if you use:
- git worktrees
- multiple VMs
- Docker containers
- separate machines

What matters is:

> you can scale the agent environments.

We’ve adjusted workflows to create isolated environments so multiple pipelines can run simultaneously on a single device.

*(This is where we start breaking beyond what in-loop agent coding can offer.)*