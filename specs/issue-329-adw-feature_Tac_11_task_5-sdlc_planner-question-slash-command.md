# Feature: Create /question Slash Command for Read-Only Q&A

## Metadata
issue_number: `329`
adw_id: `feature_Tac_11_task_5`
issue_json: `{"number":329,"title":"Create /question slash command in base repository","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_11_task_5\n\nCreate a read-only Q&A command for answering questions about project structure without making code changes.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/question.md`\n\n**Implementation details:**\n- Allowed tools: Bash(git ls-files:*), Read only\n- Purpose: Answer questions about project structure and documentation\n- Variables: QUESTION ($ARGUMENTS)\n- Workflow:\n  - Use `git ls-files` to understand project structure\n  - Read README.md for project overview\n- Response format:\n  - Direct answer to question\n  - Supporting evidence from project structure\n  - References to relevant documentation\n  - Conceptual explanations where applicable\n- IMPORTANT: No code changes allowed"}`

## Feature Description
Create a read-only slash command `/question` that allows users to ask questions about the project structure, architecture, and documentation without making any code changes. This command will use git operations and file reading to explore the codebase and provide informed, contextual answers. The command is designed to be stateless, flexible, and comprehensive while maintaining strict read-only constraints.

## User Story
As a developer or AI agent working with a TAC Bootstrap project
I want to ask questions about the project structure and get immediate, contextual answers
So that I can understand the codebase architecture, locate specific functionality, and make informed development decisions without needing to manually explore multiple files

## Problem Statement
When working with TAC Bootstrap projects (or any project using this Agentic Layer), developers and AI agents frequently need to:
- Understand project structure and organization
- Locate specific functionality or components
- Learn about architectural patterns and conventions
- Discover relationships between modules
- Find relevant documentation

Currently, this requires manually executing multiple commands (git ls-files, reading files, grepping for patterns) and synthesizing the results. There's no unified, conversational way to query the project structure.

## Solution Statement
Implement a `/question` slash command that:
1. Accepts a natural language question as input (via $ARGUMENTS)
2. Uses git operations (ls-files with variants) to explore project structure
3. Reads relevant files (README, code files, documentation) based on the question
4. Synthesizes information from multiple sources
5. Returns a structured, concise answer with:
   - Direct answer to the question
   - Supporting evidence from the codebase
   - References to specific files/locations
   - Conceptual explanations where applicable

The command relies on existing tool safety mechanisms (Read tool limits, git read-only nature) rather than artificial restrictions, allowing maximum utility while maintaining safety.

## Relevant Files
Files necessary for implementing this feature:

- `.claude/commands/question.md` - NEW - Main command implementation file
- `.claude/commands/prime.md` - REFERENCE - Example of read-only command structure
- `.claude/commands/review.md` - REFERENCE - Example of git integration and workflow
- `.claude/settings.json` - REFERENCE - May need to verify command registration (if applicable)
- `README.md` - REFERENCE - Will be mentioned in command workflow
- `CLAUDE.md` - REFERENCE - Will be mentioned as documentation source

### New Files
- `.claude/commands/question.md` - The main slash command definition following the established format used by other commands in `.claude/commands/`

## Implementation Plan

### Phase 1: Research Existing Patterns
Understand the structure and conventions used by existing slash commands in the repository to ensure consistency.

**Tasks:**
1. Read 3-5 existing command files to identify common patterns:
   - Variable declaration syntax
   - Instructions section structure
   - Report/output format conventions
   - How read-only constraints are expressed
   - Use of git commands vs other tools
2. Identify any special formatting or sections required
3. Note any integration points with settings.json or hooks

### Phase 2: Core Implementation
Create the `/question` command following established patterns and the requirements from the issue.

**Tasks:**
1. Create `.claude/commands/question.md` with proper frontmatter and structure
2. Implement Variables section:
   - QUESTION ($ARGUMENTS) - the user's question
3. Implement Instructions section:
   - Step 1: Use git ls-files (with variants) to explore project structure
   - Step 2: Identify relevant files based on the question
   - Step 3: Read README.md for project overview
   - Step 4: Read additional relevant files as needed (code, docs, config)
   - Step 5: Synthesize information to answer the question
   - Include guidance on:
     - Being concise but comprehensive
     - Using structured formatting (bullet points)
     - Graceful degradation when information is unavailable
     - Providing partial answers with explicit limitations
     - Each invocation is stateless (no context maintenance)
4. Implement Report section:
   - Direct answer format
   - Supporting evidence structure
   - References to files with line numbers where applicable
   - Conceptual explanations when needed
5. Add explicit note about read-only constraints (no code changes)

### Phase 3: Validation and Documentation
Test the command format and ensure it integrates properly with the existing system.

**Tasks:**
1. Verify markdown syntax is correct
2. Check that the command follows the same structure as other commands
3. Ensure git commands are properly formatted and safe (read-only)
4. Verify that variable references use correct syntax ($ARGUMENTS, etc.)
5. Add any necessary comments or clarifications in the file

## Step by Step Tasks
IMPORTANT: Execute each step in order.

### Task 1: Research Existing Command Patterns
- Read `.claude/commands/prime.md` to understand read-only command structure
- Read `.claude/commands/review.md` to see git integration patterns
- Read `.claude/commands/feature.md` or another complex command to see workflow patterns
- Document key patterns: variable syntax, section headers, git command usage, output format

### Task 2: Create question.md File Structure
- Create `.claude/commands/question.md`
- Add title header: `# Question`
- Add description paragraph explaining the command purpose
- Create `## Variables` section with QUESTION ($ARGUMENTS)

### Task 3: Implement Instructions Section
- Create `## Instructions` section
- Add step-by-step workflow:
  - Step 1: Analyze the question to identify relevant areas
  - Step 2: Use git ls-files (with flags like -o, -m if needed) to explore structure
  - Step 3: Read README.md for project overview
  - Step 4: Read additional files based on question context
  - Step 5: Synthesize information to answer
- Add guidance notes:
  - Be concise but comprehensive
  - Use bullet points and structured formatting
  - Provide partial answers when full answer unavailable
  - State limitations explicitly
  - Each invocation is stateless
  - No code changes allowed (read-only constraint)

### Task 4: Implement Report Section
- Create `## Report` section
- Define output format:
  - Direct answer to the question (2-4 sentences)
  - Supporting evidence (bullet points)
    - Files referenced (with paths and line numbers if applicable)
    - Relevant code/config snippets (if helpful)
  - References to documentation (links or file paths)
  - Conceptual explanations (if applicable)
  - Limitations (if any information is unavailable)
- Include example format structure

### Task 5: Add Safety and Constraint Notes
- Add explicit note about read-only operation
- Emphasize no code modifications allowed
- Note that git operations are inherently safe (read-only)
- Mention Read tool handles binary/large files automatically
- Clarify that the command can read any project files without restrictions

### Task 6: Review and Polish
- Check markdown syntax and formatting
- Ensure consistency with other command files
- Verify all sections are complete
- Check that git commands are properly formatted
- Validate variable references ($ARGUMENTS)

### Task 7: Manual Validation
- Verify file exists at `.claude/commands/question.md`
- Check file content matches requirements
- Ensure formatting is correct
- Confirm all auto-resolved clarifications are addressed:
  - ✓ Can read any project files
  - ✓ Git ls-files variants allowed
  - ✓ Graceful degradation when info unavailable
  - ✓ Stateless invocations
  - ✓ All file types allowed (Read tool handles)
  - ✓ Works without README.md
  - ✓ Concise, structured responses
  - ✓ Conceptual explanations based on codebase

## Testing Strategy

### Manual Validation Tests
Since this is a command definition file (not executable code), testing involves:

1. **File Format Validation**
   - Verify markdown syntax is valid
   - Check all sections are present and properly formatted
   - Ensure variable references use correct syntax

2. **Content Validation**
   - Instructions are clear and actionable
   - Git commands are safe (read-only)
   - Report format is well-defined
   - Guidance covers all clarified requirements

3. **Integration Validation**
   - File follows same structure as other commands
   - Compatible with how slash commands are invoked
   - No conflicts with existing commands

### Edge Cases
1. **Missing README.md** - Instructions handle gracefully (try to read, continue if missing)
2. **Binary/Large Files** - Rely on Read tool's built-in handling
3. **Complex Questions** - Guidance on structured responses helps manage complexity
4. **No Matching Files** - Instructions include guidance on stating limitations
5. **Ambiguous Questions** - Agent uses judgment to explore relevant areas

## Acceptance Criteria
- [ ] File `.claude/commands/question.md` exists
- [ ] File contains all required sections: title, description, Variables, Instructions, Report
- [ ] Variables section defines QUESTION ($ARGUMENTS)
- [ ] Instructions section includes:
  - [ ] Step-by-step workflow using git ls-files and Read
  - [ ] Guidance on being concise but comprehensive
  - [ ] Note about stateless operation
  - [ ] Read-only constraint explicitly stated
- [ ] Report section defines clear output format:
  - [ ] Direct answer structure
  - [ ] Supporting evidence format
  - [ ] References to documentation
  - [ ] Conceptual explanations
  - [ ] Limitations statement
- [ ] Git commands use safe, read-only operations (ls-files)
- [ ] File follows markdown formatting conventions of other commands
- [ ] All auto-resolved clarifications are addressed in the implementation:
  - [ ] No restrictions on which files can be read
  - [ ] Git ls-files variants (with flags) are allowed
  - [ ] Piping to grep/awk is acceptable
  - [ ] Partial answers with explicit limitations
  - [ ] Stateless invocations (no context maintenance)
  - [ ] Read tool on all file types
  - [ ] Graceful handling of missing README.md
  - [ ] Concise, structured responses (bullet points)
  - [ ] Conceptual explanations based on actual codebase

## Validation Commands
Since this is a command definition file (not code), validation is primarily manual:

```bash
# Verify file exists
ls -la .claude/commands/question.md

# Check file content
cat .claude/commands/question.md

# Validate markdown syntax (if markdownlint is available)
# markdownlint .claude/commands/question.md

# Verify it follows same pattern as other commands
ls -la .claude/commands/*.md | wc -l  # Should show question.md is added

# Check git status shows the new file
git status .claude/commands/question.md
```

## Notes

### Design Decisions
1. **Stateless Operation**: Each invocation is independent. This matches the design of other slash commands and keeps implementation simple.
2. **No Artificial Restrictions**: Unlike some command definitions, this one allows reading any files and using git ls-files variants. The safety comes from:
   - Read tool's built-in limits (2000 lines, character truncation)
   - Git commands being inherently read-only
   - No Write, Edit, or Bash execution capabilities
3. **Flexible File Access**: The command can read any project files, not just README.md. This maximizes utility for answering diverse questions.
4. **Graceful Degradation**: If information isn't available, the command should state limitations rather than fail silently.

### Implementation Notes
- This is a command *definition* file, not executable code
- The actual execution happens when an AI agent invokes `/question <query>`
- The markdown file serves as instructions/prompt for the agent
- No Python code or CLI integration required for this task
- No tests in the traditional sense (no pytest needed)

### Future Enhancements (Out of Scope)
- Integration with embeddings or semantic search
- Caching of frequently asked questions
- Suggested follow-up questions
- Context maintenance across invocations (would require significant architecture changes)

### Security Considerations
- Read-only constraint prevents any modifications
- Git ls-files is safe (only lists files)
- Read tool has built-in safety (line/character limits)
- No bash execution beyond git commands
- No network access
