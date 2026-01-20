# Tactical Agentic Coding (TAC)  
## Lesson 3 – Plans, Templates, and Metaprompting

### The Prompt Is Everything

Welcome to **Lesson 3** of Tactical Agentic Coding.

What used to be a joke is now one of the most valuable skills an engineer can have:

> **The prompt is everything.**

Why? Because the prompt is the medium through which you communicate with:
- agentic tools
- generative AI systems
- autonomous workflows

At the heart of TAC is learning how to communicate properly with agents so they can get work done **autonomously**.

Adopting your agent’s perspective is like empathizing with a friend or coworker:
- to connect
- to solve problems
- you must take their perspective

---

## AI Coding vs Agentic Engineering

With AI coding and the **Big 3**:
- Context
- Model
- Prompt

…you can push LLMs hard and generate massive amounts of code.

But:

> AI coding is not enough.

Coding is only one element of engineering.

That’s why they’re called **vibe coders**, not **vibe engineers**.

Agentic coding (and the **Core 4**) takes it to the next level:

### Core 4
- Context
- Model
- Prompt
- Tools

With tools added, prompts become exponentially more powerful.

Prompting is how we enable this.
To maximize it, we must **scale prompts**.

---

## Scaling Prompts: Plans

What does a “scaled prompt” look like?

> A plan.  
> A specification.  
> A PRD.

Plans are prompts scaled up for high impact.

### Core principle
> **The plan is the prompt.**  
> And that means: **great planning is great prompting.**

Full circle.

Planning is how we communicate better than the rest.

---

## Lesson 3 Goal

In Lesson 3, we will:
- scale your prompts into plans
- scale your plans into something even more powerful
- unlock your ability to augment **and automate** the full SDLC

Those who plan the future tend to create it.

> Success is planned.

This lesson moves us deeper into the **Plan + Build** phases of the Agentic SDLC.

---

## The 80/20 of Agentic Engineering (3 Tactics)

With just three tactics you learn the Pareto 80/20 of agentic engineering:

1. **Stop coding**  
   - your hands and mind are no longer the best tool for writing code

2. **Adopt your agent’s perspective**  
   - maximize leverage from your agents

3. **Template your engineering**  
   - deliver consistent results across hundreds of agent executions  
   - regardless of codebase size or complexity

This is one solution to the “my codebase is too big” problem.

When you template engineering, you encode problem-solving into reusable units that:
- you
- your team
- and your agents

…can see, use, and improve.

Plans are often the end result of templates.

But planning alone is expensive:
- time-consuming
- easy to miss details
- scales in cost with complexity and codebase size

So we need a better approach.

---

## The Strategy: Convert Successful Plans into Templates

We need a solution that works for:
- chores
- bugs
- small features
- large features
- new codebases
- massive refactors

We do this by taking successful plans and converting them into **templates**  
(one of the 12 leverage points of agentic coding).

This creates a suite of templates that gives you control over how your agent solves problems.

Agentic tools (Codeex, Copilot, Devon, Jules, Gemini CLI, and whatever comes next) are powerful—but limited by nature:

- they don’t understand your codebase like you do
- out-of-the-box, they don’t give you the control you need to ship end-to-end across the SDLC

Templates fix that.

---

## TAC 3 Codebase Walkthrough

### Setup
- open terminal
- clone the Lesson 3 repo (link in loot box)
- `cd` into it
- open in VS Code

Boot up the agent tool and run:
- `/install`

Important: `/install` now runs a new script that copies an env file from the TAC 2 codebase (resource reuse).

The agent:
- installs backend deps
- installs frontend deps
- copies env file
- reports the completed work

### Run the app
Run the start script:
- `scripts start`

Open the browser:
- natural language → SQL interface
- upload data
- run a query like: “Show users with age between 20 and 40”
- verify results

Stdout is visible in terminal output, and the agent can read it if needed.

---

## First Template: `/chore` (Metaprompt → Plan)

Now we run a template:

- `/chore "<your task>"`

Example argument:
- “Replace all server print statements with proper Python logging log levels. Make sure all output is written to standard out.”

This triggers a special custom slash command that produces a unique outcome:

> A template + a metaprompt.

### What is a metaprompt?
> A prompt that builds a prompt.  
More specifically: an agentic prompt that generates a **plan** based on a template.

The agent:
- searches the codebase
- gathers context
- reasons through the change
- writes a full plan into `specs/`

### Result: a generated plan
The plan includes:
- chore title
- description
- relevant files
- step-by-step tasks
- validation commands
- final notes

In other words:
> One sentence → full plan.

---

## Understanding the Template Prompt

If you open `.claude/commands/chore` you’ll see:
- **Purpose**
- **Relevant files**
- **Plan format**
- **Instructions**
- **Argument injection** (the string you passed becomes the chore description)

This is why templates are powerful:

> You are templating your engineering.

---

## Implementing the Plan: `/implement <plan_path>`

Generating a plan is not enough.
Now we execute it.

Workflow:
1. create plan via `/chore`
2. implement plan via `/implement <path>`

`/implement` is a reusable prompt that basically says:
- read the plan
- think hard
- implement it
- report completed work

Key detail:
- “Think hard” activates the tool’s reasoning mode (a leverage point)

This is a higher-order pattern:
> **plans passed into prompts** (higher-order prompts)

The agent:
- aligns the to-do list to the plan steps
- makes changes
- runs validation commands
- reports:
  - what changed
  - which files were modified

### Validation loop
The plan includes validation commands (tests + execution), enabling self-validation and regression prevention.

Result:
> A full chore completed agentically with **two prompts**:
- planning prompt
- implementation prompt

---

## Scaling the Pattern: `/bug` (Templated Bug Fixing)

Next: apply the same strategy to bugs.

Run:
- `/bug "<bug description>"`

This is also:
> a metaprompt template that generates a plan

Example bug:
- “Resolve major issue: SQL statements not escaping user input into SQL.”

The generated bug plan may include:
- problem statement
- solution outline
- steps to reproduce
- root cause analysis
- relevant files
- new files (if needed)
- step-by-step tasks
- validation
- notes

Then execute it:
- `/implement <bug_plan_path>`

---

## Why Fresh Agent Instances Every Time?

You’ll notice a pattern:
- new terminal
- new agent instance
- no memory of prior steps

This is intentional.

We do **not** want one long-running agent stretched across the SDLC.

There are three reasons:

### 1) Focus the context window
One agent per task keeps every available token focused on one mission.

This matters more as:
- tasks get longer
- codebases get larger
- execution becomes more autonomous

### 2) Force assets to be isolated + reusable
Fresh instances force your:
- prompts
- plans
- templates

…to be:
- isolated
- reusable
- improvable
- dependency-free

This creates a trail of:
- repeatable success
- measurable failures you can improve

Large codebases benefit massively from specialized templates:
- “classes of bugs”
- “front-end specific problems”
- “refactor templates”
- “performance templates”
- etc.

### 3) Prepare for off-device agentic coding
Fresh-agent workflows prepare you for true autonomous operation.

We are not here to babysit one agent.

We are here to improve KPIs:
- increase **size**
- decrease **attempts**
- increase **streak**
- decrease **presence** toward zero

---

## Closing Direction

Templates are how you encode engineering.
Metaprompts are how you turn high-level intent into detailed plans.
Plans are how you drive predictable execution.

This is where agentic coding becomes engineering.

Next steps continue building toward:
- reusable planning systems
- higher-order prompting
- reliable one-shot execution at scale
- autonomous SDLC workflows