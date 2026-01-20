# Lesson 8 Continuation: Worktrees, Triggers, and Prototyping at Scale

Inside the `trees` directory — which doesn’t exist yet — we’re going to use **dedicated git worktrees**.

Then we have the **review system**.

The review system will be:
- the actual codebase results inside the editor
- plus Highle reviews as tasks progress

Let me kick this off and it’ll make sense.

If you want to understand the agentic layer, open up **`adws`**.

If you want to stay out the loop and find the starting point, open up **`triggers`**.

---

## Trigger: Cron + Notion Tasks

Here we have:

- **`ADW trigger cron notion task`**

Another cron job that executes.

We’ll run `uv run`, fire it off, and monitor/pick up Notion tasks every 15 seconds.

For quick testing, we can reset and do it faster by passing the `--once` flag:
- it runs the workflow one time
- picks up as many tasks as it can

Yet again: another configuration of the agentic layer.

I’m not going to dive deep into this one — you should recognize the pattern by now.

If you ever want to find the prompt, just look for `/`.

And there it is:
- update notion task
- make worktree name
- new worktree
- get notion tasks
- and so on

Then we have composed AI developer workflows that do work for us:
- plan
- update
- etc.

You can see the cron trigger (the trigger in the PETER framework) starting to pick up tasks.

And check that out:
- it agentically picked up and moved that task
- the agent is now starting work

If we open it up, we can monitor and write whatever report/status updates we want.

This is another Outloop system you can wire up to agentic coding:
- build with agentics
- agents operating on your behalf

Example status events:
- generating a worktree name
- worktree created

As always, you can open `do.claude`, go into commands, and see the possible agentic capabilities.

That said: it doesn’t tell the full story.

If you’re balancing deterministic code with non-deterministic agent prompts inside ADWs, you need to read both to get the full picture.

---

## The Atoms: Prompts → Plans → Templates → ADWs

The primitives — the atoms of agentic coding — are your prompts.

Prompts are part of the **core four** and an in-agent leverage point for a reason.

Everything builds on this:
- plans
- prompts
- templates
- ADWs

Then we have auxiliary leverage points:
- types
- tests
- codebase structure

Now we start getting to work:
- multiple agents
- each with their own isolated environment
- operating on arbitrary tasks

---

## Prototyping Value Proposition

What’s the value proposition here?

This codebase specializes in creating prototypes.

We have the classic plan:
- a plan template meta-prompt
- powerful
- useful
- familiar

But you can go further:
- specialize
- solve a real problem class
- offload a real category of engineering work

That’s what your prompts and ADWs should do.

---

## Example: UV + MCP Meta-Template

Let’s look at the **UVM MCP**.

This is another template meta-prompt — but it introduces another variable created on the fly by the agent.

What happens:
- we have a dedicated workflow
- we have additional AI docs (an auxiliary directory)
- we use documentation + a prompt request
- the agent builds an Astral UV Python MCP (Model Context Protocol) server

All it needs:
- the prompt
- the docs
- the workflow

Then it builds an MCP server based on the request.

Template meta-prompt, same structure:
- nothing fundamentally new
- just specialization

You can scale this to any prototype type you want.

This is extremely useful.

---

## Review System: Board Columns and Status

We check the task board:
- in progress
- not started

Looks like we picked up three.

We can see:
- plans successfully created
- JSON formatter (bun script) looks great
- another agent kicked off: UV watch file
- UV plan script

Agents progress.

The board columns look like:
- Done
- Not started
- In progress
- Human-in-the-loop review
- Failed
- Done

This is a review system you can operate outside the loop:
- on mobile
- on another device
- quickly, asynchronously from your main environment

You gather docs, write a quick prompt, fire off a template, and generate a new application at light speed.

This is another category of work you don’t need to do if you invest in the agentic layer.

---

## From In-Loop → Outloop → Zero Touch

We’re on implementation.

Naturally, you want to progress:
- in-loop → outloop
- and the north star from Lesson 7: **target zero-touch engineering**

As you improve the agentic layer, you’ll eventually stop needing to review.

That sounds crazy early on — but it’s where this is going.

Lean forward.

---

## Example Result: MCP System Info Server (Built End-to-End)

We have a completed task: implementation successful.

This is an MCP “system info” server — system information accessible to the agent.

We open the worktree (the isolated environment where the agent completed its work).

The task moved to done.

You can click it and see live updates:
- summary
- notes
- status updates

This is a presentational example — you can put anything you want here.

You should observe and monitor your agentic system well inside your outloop review system.

Now we validate quickly:
- open the generated README
- create the `mcp.json` at the top level
- run a tool call like `get memory info`

And check that out:
- it works perfectly
- memory usage returns correctly

You can also:
- get CPU
- get disk

The agent created this end-to-end.

---

## The Real Point: Solve a Problem Class Once

Not to get lost in this specific tool…

The important part is this:

We created an entire MCP server with a single prompt.

Look at how concise the prompt is:
- “Create a minimal MCP server that provides system information…”

That’s it.

Execute.

You solved the **problem class**:
- building Astral UV MCP services

It’s done.

This is the power of the agentic layer.

This is what happens when you:
- invest in prompts
- invest in templates
- invest in ADWs
- understand leverage points

We solved multiple engineering problems:
- UV watch
- bun script watch app
- MCP server
- and more

Velocity becomes mind-blowing.

Don’t fixate on details.

Focus on the agentic layer.

Prioritize your agentic layer.

---

## Final Example: Agents Inside the App

Now we open the last example.

It looks familiar:
- a natural language SQL interface

But it’s different.

If we open command palette and run `/aa`, we have an agent inside the app.

We talk to Nexus:
- “Hello”

Then we spin up another:
- now we’re talking to Rune too

Two agents operating for us in parallel.

We ask:
- update the “generate random query” button
- rename it to “generate”

They go do the work.

We see a concise summary.

If we glance at the code, we see the same structure:
- ADWs (the agentic layer’s housing unit)
- `do.claude` prompts (the atoms)

We have a dedicated embedded agent application server — so we can access outloop **from inside the application**.

There are many ways to use this.

It’s powerful.

This is where you branch away from code details.

The future of engineering is conceptual:
- beliefs
- leverage
- orchestration of intelligence

The code and prompts matter, but the key is what you now believe is possible.

We’ve shown many permutations of the agentic layer.

This is the place to focus.

---

## Full Recap: What Tactical Agentic Coding Was About

We set out on a single mission:

> become an engineer they can’t replace.

In lesson 8, you now have everything you need.

It starts when you **stop coding**.

The irreplaceable engineer of the future is not writing a single line of code.

### What we now know to be true

- Adopt your agent’s perspective.
- Improve agentic coding KPIs by giving agents what they need:
  - context
  - model
  - prompt
  - tools

Then layer the **12 leverage points** in the right time and place:

**In-agent leverage points**
- context
- model
- prompt
- tools

**Through-agent leverage points**
- stdout
- types
- documentation
- tests
- codebase architecture
- plans
- templates
- ADWs (highest composition)

ADWs = **code + agentics**.

When you combine these:
- you focus on the agentic layer
- you template your engineering
- you encode your practices

Use template meta-prompts:
- prompts that output prompts
- formats, rules, guidelines
- files to read
- conditional docs

This scales to any codebase.

Don’t use toy examples as an excuse.

The focus is the agentic layer.

---

## KPIs and Direction

As you template engineering, you increase agentic coding KPIs:

- fewer attempts to deliver work
- larger tasks you can hand off
- longer successful streaks without mistakes
- lower **presence** (you showing up)

Presence should drop toward zero.

You want to stay out the loop.

In-loop vs outloop agent coding.

As the agentic layer thickens, you want to spend more time out the loop, building the system that builds the system.

---

## Always Add Feedback Loops

How do we stay out the loop safely?

A critical leverage point:

> **Always add feedback loops.**

Add tests and validation commands so agents can confirm success.

SDLC is a fantastic example, but it’s not the only workflow.

It’s not about SDLC.

It’s about composable pieces.

Big labs already do this:
- agents iterating against validation functions

You can do this on your codebase too.

There exists a set of validations that ensures things work.

The question is:
- do you know what they are?

---

## One Agent, One Prompt, One Purpose

There are limits.

Context windows can still be small.

So we sidestep the issue:

> one agent, one prompt, one purpose

Focused agents create focused contexts:
- reproducible
- testable
- improvable

Most of the course uses this pattern.
Only rare exceptions continue conversations via session IDs.

---

## North Star: Zero Touch Engineering

Where does it end?

> **Zero touch engineering.**

As your workflows become reliable, you become the bottleneck.

Review becomes useless.

Eventually you convert PETER to PETE:
- prompt input
- trigger
- environment
- **no review**

This won’t happen overnight.

Engineering is gray.

Progression is one step at a time:
- small chores end-to-end
- then you realize you don’t need validation for those
- because feedback loops cover safety
- review systems (images, videos, multi-agent review) can be embedded if needed

Eventually:
- getting in the loop becomes harmful
- you drop review and ship end-to-end
- your product ships itself

Target zero touch engineering.

---

## The Agentic Layer Defined

The agentic layer is the combination of:

- traditional deterministic code (ADWs as a scriptable layer)
- non-deterministic agentic technology (models, prompts, tool runners)

Old world + new world.

That combination is the agentic layer.

This is the highest leverage point:
- AI developer workflows
- orchestrating intelligence

We prioritize agentics because agents can ship better and faster than us.

Don’t compete with:
- your best engineering practices
- templated into meta-prompts
- executed inside ADWs
- scaling to 5–10 agents per problem

Your competition is now net-new innovation:
- build on the agentic layer
- use compute to solve problems creatively
- teach compute how to build and engineer your way

---

## The Final Guiding Question

Let’s compress everything into one question.

On a day-to-day basis, ask:

> **Am I working on the agentic layer or am I working on the application layer?**

That’s it.

Most of your time should be spent on the agentic layer.

Why?
- because you can teach compute how to build
- because you can teach compute how to engineer your way
- because you can scale compute beyond comprehension
- because you’re orchestrating intelligence

Just like an engineer using AI outperforms one who doesn’t…

An agentic engineer with fleets of agents solving problem classes outperforms classical in-loop AI coding.

You can’t compete without fleets of agents.

So after this course:
- invest in this layer
- prioritize agentics
- ask the question daily
- redirect effort into the agentic layer so agents can do the rest

Once you get your first end-to-end wins:
- bug fix shipped without intervention
- a useful ADW you reuse constantly
- teammates using your ADWs and getting “I didn’t do anything” moments

You’ll realize there’s nothing more important to invest in.

That’s tactic eight:
- prioritize agentics
- prioritize your agentic layer

And by investing in your agentic layer, you’re investing in:
- your users
- your product
- your team
- your company
- yourself

---

## Agentic Engineer: The New Role

Coding has been commoditized.

Implementation is being commoditized.

Early signs: engineering itself begins to commoditize.

This is only negative if you arrive late.

You are early.

Value moves up the stack:
- system design
- architecture
- encoding domain expertise for agents
- quality control
- validation systems
- creative problem decomposition (encoded into ADWs)

This is bigger than a course.

It’s groundwork for a new role:
- agentic engineers
- agentic engineering

Bet on this reality.

Don’t fall behind.

---

## Closing Message

Prioritize agentics.

Spread these ideas to engineers who can handle them.

Your feedback matters — you’ll be asked what you want to see next.

The future is already here.

What matters is that you do something about it.

Imagine your future self looking back, grateful and happier than ever — because you won.

And you say:

> When the agents arrived, something changed.  
> We weren’t just AI coding anymore.  
> We started orchestrating intelligence.

This closes the loop.

Thank you for trusting me with your time, your engineering, your future, and your career.

Put this information to use.

If you do this right, it will change everything.

**Prioritize agentics.**