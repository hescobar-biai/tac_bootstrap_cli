---
doc_type: feature
adw_id: feature_Tac_11_task_5
date: 2026-01-27
idk:
  - slash-command
  - read-only
  - qa-mode
  - git-ls-files
  - codebase-exploration
  - agent-instructions
tags:
  - feature
  - slash-command
  - documentation
related_code:
  - .claude/commands/question.md
  - specs/issue-329-adw-feature_Tac_11_task_5-sdlc_planner-question-slash-command.md
---

# Question Slash Command - Read-Only Q&A for Project Structure

**ADW ID:** feature_Tac_11_task_5
**Date:** 2026-01-27
**Specification:** specs/issue-329-adw-feature_Tac_11_task_5-sdlc_planner-question-slash-command.md

## Overview

The `/question` slash command provides a read-only Q&A interface for exploring project structure, architecture, and documentation. It enables developers and AI agents to ask natural language questions about the codebase and receive contextual answers synthesized from git operations and file reading, without making any code modifications.

## What Was Built

- **Read-Only Slash Command**: `.claude/commands/question.md` - A new slash command definition that accepts natural language questions via `$ARGUMENTS`
- **Structured Workflow**: Multi-step instructions for analyzing questions, exploring project structure with git, reading relevant files, and synthesizing answers
- **Safety Constraints**: Explicit read-only constraints leveraging built-in tool safety (Read tool limits, git read-only nature)
- **Flexible Response Format**: Structured output including direct answers, supporting evidence, documentation references, conceptual explanations, and explicit limitations

## Technical Implementation

### Files Modified

- `.claude/commands/question.md`: **NEW** - Main slash command definition file with 91 lines implementing the complete Q&A workflow

### Key Changes

1. **Variable Definition**: Single `QUESTION` variable bound to `$ARGUMENTS` to capture user's natural language query
2. **Five-Step Workflow**:
   - Step 1: Analyze the question to identify relevant areas (structure, implementation, architecture, documentation)
   - Step 2: Use `git ls-files` with variants and piping to explore project structure
   - Step 3: Read project overview files (README.md, CLAUDE.md, PLAN_*.md) with graceful handling of missing files
   - Step 4: Read relevant files based on question context (config, source code, tests, domain docs)
   - Step 5: Synthesize information with direct answers, supporting evidence, and explicit limitations
3. **Guidance Notes**: Explicit instructions for concise responses, structured formatting, partial answers, limitation statements, and stateless operation
4. **Report Format**: Structured output with sections for Answer, Supporting Evidence, Documentation References, Conceptual Explanation, and Limitations
5. **Safety Notes**: Explicit read-only constraint and notes about git operation safety and Read tool built-in limits

## How to Use

1. **Invoke the command with a question**:
   ```bash
   /question How is authentication implemented in this project?
   ```

2. **The agent will**:
   - Use `git ls-files` to explore relevant areas
   - Read README.md and other documentation
   - Read source code files matching the question
   - Synthesize a structured answer

3. **Receive structured response**:
   - Direct answer (2-4 sentences)
   - Supporting evidence with file references
   - Documentation links
   - Conceptual explanations
   - Explicit limitations if information is incomplete

4. **Example questions**:
   - "What is the project structure?"
   - "Where are errors handled?"
   - "How do I configure the database connection?"
   - "What testing framework is used?"
   - "Where is the authentication logic?"

## Configuration

No configuration required. The command works out-of-the-box with any TAC Bootstrap project.

**Optional**: The command automatically reads these files if present:
- `README.md` - Project overview
- `CLAUDE.md` - Agent instructions
- `PLAN_*.md` - Planning documents

## Testing

### Verify Command File Exists

```bash
ls -la .claude/commands/question.md
```

### Check Command Content

```bash
cat .claude/commands/question.md
```

### Test Git Operations (Read-Only)

```bash
# Verify git ls-files works (command used by /question)
git ls-files

# Test filtering (as the command does)
git ls-files '*.py'
git ls-files | grep -E "test_.*\.py"
```

### Manual Testing with Example Question

After invoking `/question`, test with sample questions:
- "What files are in this project?"
- "How is the project structured?"
- "Where is the configuration?"

## Notes

### Design Decisions

1. **Stateless Operation**: Each invocation is independent, matching other slash commands
2. **No Artificial Restrictions**: Command can read any files; safety comes from tool built-in limits
3. **Flexible File Access**: Not restricted to README.md; can read config, source, tests, docs
4. **Graceful Degradation**: States limitations explicitly rather than failing silently

### Implementation Notes

- This is a command *definition* file (markdown), not executable Python code
- Execution happens when an AI agent invokes `/question <query>`
- The markdown serves as instructions/prompt for the agent
- No Python code or CLI integration required
- No pytest tests needed (definition file, not code)

### Safety Considerations

- Read-only constraint prevents modifications
- Git ls-files is inherently safe (only lists files)
- Read tool has built-in limits (2000 lines, character truncation)
- No bash execution beyond git commands
- No network access

### Auto-Resolved Clarifications (from Spec)

All design clarifications were addressed in the implementation:
- ✓ Can read any project files without restrictions
- ✓ Git ls-files variants with flags allowed
- ✓ Piping to grep/awk acceptable
- ✓ Graceful degradation when info unavailable
- ✓ Stateless invocations (no context maintenance)
- ✓ Read tool on all file types
- ✓ Works without README.md
- ✓ Concise, structured responses (bullet points)
- ✓ Conceptual explanations based on actual codebase
