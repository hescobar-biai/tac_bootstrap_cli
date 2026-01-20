## Scaling Agent Environments with Isolation

It doesn’t matter that you use **git worktrees**. It doesn’t matter if you want to use individual instances, individual VMs, or Docker containers.

I don’t care *how* you scale up your agent environments.

What matters is that you **can**.

We’ve adjusted all of our workflows to create their own **isolated trees**. In every tree (in every one of these directories), the application exists in a dedicated space for a specific agent to build in.

This is the easiest way to:
- parallelize workflows
- scale agents into your work

You can see we have environment variables and Playwright configuration at the beginning of the workflow.

And we can always search to navigate the agentic layer.

For example, in `plan ISO`, when we plan the work and set up the environment, we run something like:

- `/install worktree`

Then we pass in:
- ports that were created
- the worktree path

You can imagine what this does:

The worktree sets up everything needed to operate the codebase in a dedicated directory.

It’s basically like cloning a fresh version, installing dependencies, and setting up the environment — as if an engineer were operating manually.

This kind of configuration is critical.

A lot of engineers will lean on Docker or agent-based container frameworks. Whatever you use doesn’t matter. Don’t get caught on the tooling.

Get caught on the real goal:

> scaling up the agentic layer so you can multiply your agents.

You want agents operating **in parallel**, in dedicated, isolated, safe environments.

---

## Jump Into Any Agent Environment at Any Time

You want to be able to plug into any environment instantly.

At any moment, you can jump into one of these worktrees and open it:

- `code trees <ID>`

Use a real ID from an active agent. For example, you can copy the ADW ID, open the environment, and watch what’s happening.

Now you’re inside the dedicated environment that agent is operating in.

You can see:
- the branch name
- the issue number (e.g., “Chore task issue 39”)
- the ADW ID

Think in the gray.

We’re not jumping directly to outloop perfection. We’re progressively handing off more and more work to agents.

Things will go wrong.

We’ll need to hop into environments to understand what went wrong — not to fix the issue directly, but to improve the *agentic layer* so the class of issue disappears next time.

That’s the theme:

> build the system that builds the system.

We’re not solving the problem directly anymore.

Your domain-specific problem is still everything — but your ability to solve it scales drastically when you invest in the agentic layer.

The top layer of that is your **AI developer workflows**.

Deeper down, you reach:
- individual prompts
- prompt composition details
- how they ladder back up into workflows

---

## One Agent, One Prompt, One Purpose (Still Holds)

The lesson six tactic has not been broken:

> one agent running one prompt with a single purpose.

To combat state management issues, we track a `state.json` object and pass more meta information through ADWs and individual agents.

Expect to add a state object inside dedicated agent environments.

This frees your agent to do one thing extremely well with all the context it needs — and it lets you jump in and replay exactly what the agent did.

---

## Monitoring Progress Across Parallel Workstreams

We hop back to the top level and check how agents are doing.

Example statuses:
- JSON export agent: in review phase
- drag-and-drop: implementation complete, tests passed, now reviewing
- random data generation: implementing (largest feature), using heavy model set
- update model chore: completed, tests passed, PR created
- CSV text mismatch: patch workflow completed

The key is that the review system stays central:
- you want rich, detailed updates
- so you don’t have to leave the review system to know work shipped end-to-end

In TAC, GitHub Issues are used as the review system:
- workflows post live updates directly back to the issue that triggered them

Many engineers may want to push more into PRs. Either way, a comprehensive review system is a huge edge for review velocity.

---

## Proof-of-Value Review

Here’s what great review looks like:

- review summary
- screenshots
- proof that the feature shipped

Example: drag-and-drop enhancement
- agents uploaded screenshots showing the new overlay
- regression screenshots validating the UI

Remember what review answers:

- Testing: **Does it work?**
- Review: **Is what we built what we asked for?**

The screenshots are proof-of-value.

Agents are operating like you or I would.

---

## In-Loop Review Still Exists (Engineering is Gray)

Even when agents prove the feature shipped, we still do in-loop review sometimes.

Engineering isn’t black-and-white.

It’s gray.

You progress toward outloop one day at a time.

So we do a simple in-loop review:
- pull branch
- reset DB
- restart app
- validate the feature

Example:
- drag-and-drop works in both UI areas
- tables are created correctly from drops

Then we check the artifacts:
- documentation created in `app/docs`
- references original spec
- conditional docs updated so future agents pull the right docs when needed

This is how agents scale with codebase size:
- pull in the right documentation when a condition matches
- operate in isolated worktrees so everything can run in parallel safely

---

## Asymmetric Results From Investing in the Agentic Layer

Investing in the agentic layer produces asymmetric results.

You can’t vibe-code this.

Agents operate as you would:
- engineering is templated
- you stay out of the loop
- one agent, one prompt, one purpose

All tactics stack.

You parallelize yourself across multiple features.

This is scaled agentic impact.

---

## The Next Step: Zero Touch Engineering (ZTE)

Now the next question:

What happens when you get so good at outloop that human review becomes a bottleneck?

Eventually you realize:

> human-in-the-loop review is no longer adding value for a class of problems.

At that point, you move beyond outloop into the next scale:

### ZTE: Zero Touch Engineering

In-loop → Outloop → ZTE

ZTE is like YOLO mode for AI developer workflows:
- maximum confidence mode
- no review
- just ship

You stop reviewing like you stopped coding.

This is the lesson seven tactic:

> target zero engineering.

This is the north star the agentic KPIs lead toward:
- attempts → 1
- size → scales up
- streak → increases
- presence → down to 1

Outloop agents have presence 2:
- show up at prompt
- show up at review

ZTE aims for presence 1:
- show up at prompt
- agents ship end to end

---

## Start Small (ZTE Isn’t For Everything)

You don’t start by shipping a full production feature.

Progress happens one step at a time.

Start with:
1) chores
2) bugs
3) then features

Solve the stupid-simple problems that waste your time.
Scale up gradually.

ZTE runs the same workflow as SDLC — plus one more step:

- ship / approve / merge the PR agentically

If agents consistently pass tests and produce strong proof-of-value reviews across repeated runs, the next step is letting them ship.

---

## Example: Small ZTE Chore

Example prompt:
- update background color (simple styling change)

Run:
- ADW SDLC ZTE (zero-touch engineering)

Workflow:
- plan
- build
- test
- review
- generate docs
- ship

This is primitive in TAC, but it’s the direction everything converges toward.

---

## The Counter Narrative: How You’ll Know When Agents Can Ship Your Work

Real production codebases are complex. Yes.

But this doesn’t happen all at once.

We’re in phase two: the age of agents.

Prepare for agentic coding capabilities to go parabolic.

Here’s the key question:

> If you don’t invest in the agentic layer of your codebase, how will you know when agents can solve your problem class end-to-end?

That’s what all of this is building toward.