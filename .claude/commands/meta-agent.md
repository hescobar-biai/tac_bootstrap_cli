---
allowed-tools:
  - Write
  - Read
  - Glob
  - Grep
  - AskUserQuestion
description: "Generate new agent definitions from natural language descriptions"
argument-hint: "[agent_description]"
model: sonnet
---

# Meta-Agent Generator

Generate a complete, production-ready agent definition following TAC standards from a natural language description.

## Variables

AGENT_DESCRIPTION: $ARGUMENTS (description of the agent you want to generate)

## Instructions

This meta-agent takes a natural language description and generates a complete agent definition file following TAC Bootstrap standards.

**What is a meta-agent?**
A meta-agent is an agent whose output is another agent. It codifies agent design patterns and standards into a reusable template generator, enabling "agents that create agents."

**How to use:**
1. Invoke with $ARGUMENTS describing the desired agent's purpose and capabilities
2. The meta-agent analyzes your requirements and existing patterns
3. The meta-agent generates a complete agent definition following TAC standards
4. The output is production-ready with proper structure

**Interpretation guidelines:**
- Parse AGENT_DESCRIPTION to understand: purpose, tools needed, personality, model requirements
- Identify what tools the agent should have access to
- Determine appropriate model (sonnet/opus/haiku) based on complexity
- Design agent personality and behavior patterns
- Define clear workflow steps for the agent

## Documentation

Reference these agent files for examples and patterns:

- `.claude/agents/build-agent.md` - File implementation specialist pattern
- `.claude/agents/scout-report-suggest.md` - Read-only analysis pattern
- `.claude/agents/Plan.md` - Planning and design pattern
- `.claude/agents/Explore.md` - Codebase exploration pattern
- `.claude/agents/general-purpose.md` - Multi-tool general agent

These demonstrate TAC's standard agent structure: YAML frontmatter, purpose, workflow, and report sections.

## Workflow

### Step 1: Parse and Validate Description

- Parse AGENT_DESCRIPTION from $ARGUMENTS
- Validate description length (minimum 10 characters)
- Extract key information:
  - Agent's primary purpose
  - Required capabilities (what the agent should do)
  - Expected inputs and outputs
  - Behavioral requirements (proactive vs reactive, cautious vs fast)
- If description is too vague (< 30 chars or lacks context), use AskUserQuestion to clarify:
  - What tasks should the agent perform?
  - What tools will it need?
  - Should it be proactive or reactive?
  - Any personality/behavior requirements?

### Step 2: Infer Agent Configuration

Based on AGENT_DESCRIPTION, intelligently determine:

**A) Tools Required:**
- File operations → Write, Read, Edit
- Code search → Grep, Glob
- Command execution → Bash
- User interaction → AskUserQuestion
- Task management → TodoWrite
- Sub-agents → Task
- Notebooks → NotebookEdit

**B) Model Selection:**
- Simple, repetitive tasks → haiku (fast & cost-effective)
- Standard agent work → sonnet (balanced)
- Complex reasoning, planning, novel tasks → opus (most capable)

**C) Agent Personality:**
- Security/validation tasks → thorough, cautious, detail-oriented
- Build/implementation tasks → methodical, quality-focused
- Research/exploration tasks → curious, comprehensive, pattern-seeking
- Fix/debug tasks → analytical, root-cause focused
- Review tasks → critical, standards-enforcing

**D) Generate kebab-case name:**
- Extract key words from description
- Create descriptive name (e.g., "test-runner", "docs-updater", "api-validator")
- Keep name concise (2-3 words max)

### Step 3: Design Agent Structure

Create complete agent definition with these sections:

**A) YAML Frontmatter:**
```yaml
---
name: [kebab-case-name]
description: [1-2 sentence description from AGENT_DESCRIPTION]
tools: [comma-separated list of tools from Step 2A]
model: [sonnet/opus/haiku from Step 2B]
color: blue
---
```

**B) Purpose Section:**
- Start with "You are a specialized [role]..."
- Explain agent's primary function
- Define scope and constraints
- Mention key behavioral traits (from Step 2C)

**C) Workflow Section:**
- List 4-7 numbered steps the agent should follow
- Each step should be actionable and specific
- Include tool usage guidance where relevant
- Cover: preparation → execution → validation → reporting

**D) Report/Response Section:**
- Define structured output format
- Specify what information to include
- Use clear headings and bullet points
- Provide example format if helpful

### Step 4: Validate and Write Agent

**A) Pre-flight validation:**
- Verify YAML frontmatter is syntactically correct
- Ensure all required sections present (Purpose, Workflow, Report)
- Check that tools list matches workflow requirements
- Validate no placeholder text (e.g., "[TODO]", "[FILL IN]")
- Confirm name is unique (doesn't conflict with existing agents)

**B) Handle existing files:**
- Use Glob to check if `.claude/agents/[name].md` already exists
- If exists, use AskUserQuestion to ask user:
  - Overwrite existing agent?
  - Rename new agent?
  - Abort generation?

**C) Directory creation:**
- Check if `.claude/agents/` directory exists
- If not, inform user and create directory
- Proceed with file creation

**D) Write agent file:**
- Use Write tool to create `.claude/agents/[name].md`
- Write complete agent definition with all sections
- Ensure proper formatting and markdown structure

**E) Post-write validation:**
- Use Read to verify file was written correctly
- Check file size is reasonable (not empty, not truncated)
- Confirm structure matches template

### Step 5: Report Generation

After successful agent creation, provide structured output.

## Report

After generating the agent, provide:

### Generated Agent Summary

- **Agent name**: [kebab-case name]
- **File created**: `.claude/agents/[name].md`
- **Purpose**: [1-sentence description]
- **Tools**: [list of tools the agent can use]
- **Model**: [sonnet/opus/haiku]
- **Personality traits**: [key behavioral characteristics]

### Agent Capabilities

- [Primary capability 1]
- [Primary capability 2]
- [Primary capability 3]

### Usage Instructions

The generated agent can be invoked using the Task tool:

```
Task tool with:
  subagent_type: [agent-name]
  prompt: "[description of what you want the agent to do]"
  description: "[short 3-5 word summary]"
```

Or via agent mention (if supported):
```
@[agent-name] [task description]
```

### Workflow Overview

The agent follows this workflow:
1. [Brief description of step 1]
2. [Brief description of step 2]
3. [Brief description of step 3]
...

### Next Steps

- Test the agent with a sample task to verify it works as expected
- Adjust the agent definition if needed based on test results
- Consider creating template version (`.j2`) if reusable across projects
- Document the agent in your project's agent catalog

### Quality Notes

- ✅ Agent follows TAC Bootstrap standards
- ✅ All required sections present (YAML, Purpose, Workflow, Report)
- ✅ No placeholder text or TODOs
- ✅ Tools match workflow requirements
- ✅ Immediately usable without manual editing
