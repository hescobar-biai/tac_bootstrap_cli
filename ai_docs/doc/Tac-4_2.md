# TAC Lesson 4 – Running an ADW Locally (Issue #33) and Breaking Down the Workflow

## Local Trigger + Webhook Disabled

A brand new feature is coming in. We’ve disabled the agent’s sandbox run:
- the webhook event is **off**
- it’s **not listening**
- nothing will auto-run

So we’ll kick this off **on our device** using a **local trigger**.

We create the GitHub issue and reference it by issue number **33**.

---

## Health Check Before Running the ADW

Before running any complex (or even simple) workflow, validate the environment with a **health check**.

This should be built into your ADWs so you always know:
- env vars are correct
- paths are correct
- repo access is correct
- the agent can run

Run the health check on issue **33**:
- environment path is set
- GitHub repository looks good
- Cloud Code runs properly
- it posts a health check comment to the issue
- **green light to proceed**

You may see a warning if you’re still pointing to the original TAC 4 repo:
- you must update it to your own repo to use your own Issues + PRs

---

## ADWs Directory = Agentic Layer

The ADW directory operates as a unit **around** your codebase.

Notice:
- `app/` is completely untouched
- we do not conflate `app/` with `ADWs/`

The **ADWs** plus your **prompts** (reusable prompts, templates, metaprompts) form the **agentic layer** around the codebase.

---

## Running the Plan+Build ADW Locally

This codebase has **one** ADW:
- **Plan + Build**
- automates the first two SDLC steps

Kickoff is intentionally simple:
- `uv run <script> <issue_number>`

These scripts are single-file scripts. They can be:
- Python with `uv`
- bun scripts
- shell scripts
- anything you want

The point is: they are an orchestration layer above the codebase.

Run it for issue **33** from within the ADWs directory:

- it starts the workflow
- generates an ADW ID (if you don’t pass one)
- creates a branch like `jsonl-support`
- the agent takes over
- you are now **out of the loop**

You focus on **what**, not **how**.

The “how” has already been encoded into:
- templates
- reusable prompts
- metaprompts
- the ADW itself

---

## Live Updates in the GitHub Issue

Back in the issue, you see live updates:
- it classifies the issue as a **feature**
- so it runs the **feature** template, not the chore template

This matters because different classes of work require different templates:
- chore
- bug
- feature
- (and any other domain-specific classes you want)

This “classification switch” is a core pattern:
> We must target specific classes of problems.

---

## How the ADW Works (Plan Build)

The workflow is readable right at the top:

1. **Fetch GitHub issue details**  
   Pulls in the prompt source (title + body).

2. **Create a feature branch**  
   (could also be a chore/bug branch depending on classification).

3. **Run the plan agent**  
   Uses Cloud Code with a plan prompt:
   - runs `/feature` (the reusable prompt)

4. **Run the build agent**  
   Takes the plan and implements it:
   - passes the plan as an argument
   - pulls correct context
   - executes (like `/implement` from Lesson 3)

5. **Create a PR**  
   Ships back into the review system.

This is the first two SDLC steps automated:
> Plan + Build (Plan + Code)

---

## Composition: Deterministic Code + Non-Deterministic Intelligence

The ADW is a composition of:
- deterministic orchestration code (scripts, GitHub API, branching, PR creation)
- non-deterministic intelligence (LLMs via Cloud Code programmable mode)

And critically:
- logging
- reporting
- observability

Because it doesn’t matter if the agent solved the problem if you can’t verify it.

So the ADW ensures:
- it’s observable
- it’s reportable
- it’s monitorable

---

## Core Execution Flow (Simplified)

- parse args → issue number (e.g., **33**)
- generate ADW ID (optional input)
- set up logger
- validate environment variables
- load GitHub repo
- fetch issue (title + body)
- post progress comments or errors
- run steps:
  - classify issue
  - create branch
  - build plan
  - commit plan
  - implement
  - commit implementation
  - create PR

Between each step:
- logs
- error checks
- issue comments (progress)
- continued flow

---

## Prompt Isolation Pattern (No Ad Hoc Strings)

The ADW isolates prompts as slash commands:
- no random prompt strings inside the orchestration code
- prompts are stored as reusable assets
- each prompt can be improved independently

Example: `classify_issue` uses a slash-command prompt, then maps result:
- chore / bug / feature / etc.

If you add new classes:
- update the mapping
- update datatypes
- add a prompt

---

## Plan Step Example: Building a Template Request

The plan builder constructs:
- agent name
- slash command (`/feature`)
- prompt args
- model selection

Recommendation:
> Use the most powerful model for the most complex steps (plan + build).

For speed, you might demo with a faster model (e.g., Sonnet), but serious builds should use top models.

---

## Programmable Mode: The Key Primitive

The execute step:
- builds the prompt
- logs the prompt
- runs Cloud Code in **programmable mode**

It runs “dangerously,” but because it’s in a **dedicated environment**, it can still be safe.

Programmable mode is the unlock:
> It lets Cloud Code become a programmable primitive you can call in any step of any workflow.

---

## Workflow Observability and Logs

Two critical observability layers:
1. per Cloud Code session ID logs
2. per ADW workflow logs (the whole run)

You can inspect micro-agents within one ADW run:
- branch generator
- issue classifier
- planner
- implementer
- PR creator
- committer(s)

---

## Result: PR Created + JSONL Support Shipped

The workflow completes:
- PR created
- issue shows timeline (~17 minutes)

PR includes:
- files changed
- comprehensive tests
- updated UI
- sample data in test assets
- the generated plan (planner output)

The plan is crucial:
- it’s a concrete artifact
- you can improve the system
- agents can learn from it
- avoids “ad hoc prompt magic”

Example scale:
- ~170-line plan
- implement agent expands it into working code

---

## Manual Regression Test (Fast Validation)

After merging/checkout:
- run server/client
- refresh UI
- confirm:
  - normal queries still work
  - upload now supports **CSV / JSON / JSONL**
  - JSONL upload works using sample data
  - queries run over uploaded data

This showcases a key idea:
> Many features an engineer would pick up are completely unnecessary to do manually.

---

## The Real Pattern: Fix the System, Not the Issue

When something goes wrong:
- don’t just patch the output
- fix the **templates**
- fix the **ADW**
- improve the **system that caused it**

This trend will continue and will apply to large codebases too.

---

## Tools Don’t Matter; The 4 Elements Do

It doesn’t matter if you use:
- GitHub Issues
- Jira
- Notion
- anything else

The four elements are always there:
- prompt input
- trigger
- environment
- review

Build systems that build the system for you.

---

## Dedicated Environment + Remote Trigger

Set up a dedicated environment where the agent runs on its own.

Then you can:
- create an issue anywhere
- hit a trigger
- kick off workflows remotely
- ship PRs back for review

This has massive ROI.

Start now:
- configure it
- fire off a small chore
- build trust
- then scale to bugs
- then full features

Cloud tools may “do something similar,” but they aren’t running:
- your templates
- your prompts
- your domain-specific best practices

---

## Pivotal Lesson: Build the Agentic Layer

Focus on the two essential directories:

- Prompt storage (e.g., `.claude/commands`)
- `ADWs/` (agentic workflows / pipelines)

Add:
- logging
- observability
- clear reporting
- review hooks

So you can stay out of the loop.

---

## The Next Level: Reliability via Closed Loops (Lesson 5)

These workflows still require review.

Next goal:
> increase review velocity while scaling plan/build velocity

In Lesson 5, you close loops by teaching agents to validate their own work:
- multiple tests
- multiple dimensions of validation
- backend + frontend + scripts + everything

That drastically reduces review time and fixes.

---

## Summary Call to Action

- Template your engineering
- Build ADWs
- Stay out of the loop
- Let your product ship itself

You’re halfway through Tactical Agentic Coding.

Lesson 5 is where reliability and self-validation accelerate everything.