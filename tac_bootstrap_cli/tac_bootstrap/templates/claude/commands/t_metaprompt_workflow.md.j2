---
allowed-tools:
  - Write
  - Edit
  - WebFetch
  - Task
---

# Meta-Prompt Workflow Generator

This is a Level 6 meta-prompt (as defined in TAC-10 abstraction hierarchy) that generates new prompts following the TAC framework's consistent format and structure.

## Variables

HIGH_LEVEL_PROMPT: $ARGUMENTS (description of the prompt you want to generate)

## Instructions

This meta-prompt takes a high-level description of a desired prompt and produces a complete, well-structured prompt following TAC standards.

**What is a meta-prompt?**
A meta-prompt is a prompt whose output is another prompt. It codifies best practices and standards into a reusable template generator.

**How to use:**
1. Invoke this command with $ARGUMENTS describing what kind of prompt you need
2. The agent will analyze your requirements
3. The agent will generate a complete prompt following the Specified Format Template below
4. The generated prompt will be production-ready with proper structure

**Interpretation guidelines:**
- Parse HIGH_LEVEL_PROMPT to understand: purpose, target users, input/output, and desired workflow
- Identify what variables the generated prompt needs to accept
- Determine appropriate tools the generated prompt should allow
- Design a clear workflow with numbered steps
- Define what the report/output should look like

## Documentation

Reference these local command files for examples and patterns:

- `.claude/commands/feature.md` - Feature planning with metadata, variables, and structured format
- `.claude/commands/implement.md` - Implementation workflow with clear instructions
- `.claude/commands/test.md` - Testing workflow with validation steps
- `.claude/commands/review.md` - Review workflow with quality checks
- `.claude/commands/commit.md` - Git commit workflow with conventions
- `.claude/commands/parallel_subagents.md` - Delegation prompt with variable syntax and report format

These files demonstrate TAC's standard structure: frontmatter, variables, instructions, workflow, and report sections.

## Specified Format Template

Generate prompts using this 4-section structure:

### 1. Metadata Section (optional but recommended)

```markdown
---
allowed-tools:
  - ToolName1
  - ToolName2
description: "Brief description of what this prompt does"
argument-hint: "hint for $ARGUMENTS usage"
---

# [Prompt Title]

[Brief introduction explaining the prompt's purpose and when to use it]
```

**Guidelines:**
- Only include frontmatter if the prompt needs specific tool permissions or metadata
- Keep frontmatter minimal - only add what's necessary
- Description should be 1-2 sentences maximum

### 2. Variables Section

```markdown
## Variables

VARIABLE_NAME_1: $1 (description of first positional argument)
VARIABLE_NAME_2: $2 (description of second positional argument, optional: default value)
ANOTHER_VAR: $ARGUMENTS (captures all arguments as single value)
```

**Guidelines:**
- Use SCREAMING_SNAKE_CASE for variable names
- Use `$1`, `$2`, `$3` for positional arguments
- Use `$ARGUMENTS` to capture all arguments as one value
- Include description and default values where appropriate
- Variables can be optional (note this in description)

### 3. Workflow Section

```markdown
## Instructions

[High-level overview of what this prompt does and how to use it]

## Workflow

### Step 1: [Action Name]

- [Specific action or task]
- [Another specific action]
- [Validation or check to perform]

### Step 2: [Next Action Name]

- [Specific action or task]
- [Another specific action]

[Continue with numbered steps as needed]

### Step N: [Final Action Name]

- [Completion actions]
- [Final validations]
```

**Guidelines:**
- Start with Instructions section explaining purpose and usage
- Use numbered steps (Step 1, Step 2, etc.)
- Each step should have a clear action-oriented name
- Include 3-7 steps (fewer for simple prompts, more for complex workflows)
- Each step should have 2-5 bullet points with specific actions
- Include validation or verification steps where appropriate

### 4. Report Section

```markdown
## Report

[Describe the expected output format and structure]

### [Report Subsection 1]

[Details about what to include in this part of the report]

### [Report Subsection 2]

[Details about what to include in this part of the report]

**Format requirements:**
- [Specific formatting requirement 1]
- [Specific formatting requirement 2]

**Do NOT include:**
- [What to avoid in the output]
```

**Guidelines:**
- Clearly specify the expected output format
- Use subsections if the report has multiple parts
- Include both positive requirements (what to include) and negative requirements (what to avoid)
- For machine-parsed outputs, specify exact format (JSON, YAML, etc.)
- For human-readable outputs, describe structure and tone

## Example

**Input (HIGH_LEVEL_PROMPT):**
"Create a prompt for validating that all Python functions have docstrings"

**Generated Output:**

```markdown
---
allowed-tools:
  - Read
  - Grep
  - Bash
---

# Validate Python Docstrings

Check that all Python functions in the codebase have docstrings and report any violations.

## Variables

TARGET_PATH: $1 (path to directory or file to validate, default: current directory)
EXCLUDE_PATTERN: $2 (optional glob pattern to exclude files, e.g., "*/test_*.py")

## Instructions

This prompt validates that all Python function definitions include docstrings. It searches for function definitions and checks if they are followed by docstring declarations.

## Workflow

### Step 1: Identify Python Files

- Use Grep to find all `.py` files in TARGET_PATH
- Apply EXCLUDE_PATTERN if provided to filter out test files or other exclusions
- Create a list of files to validate

### Step 2: Extract Function Definitions

- For each Python file, use Grep to find all function definitions (`def ` pattern)
- Record the file path and line number for each function
- Ignore class methods that start with `_` (private methods can skip docstrings)

### Step 3: Check for Docstrings

- For each function found, Read the file and check if the next non-empty line after the function definition is a docstring (starts with `"""` or `'''`)
- Mark functions as "compliant" or "missing docstring"

### Step 4: Generate Validation Report

- Count total functions found
- Count compliant functions
- List all functions missing docstrings with file paths and line numbers
- Calculate compliance percentage

## Report

Structure your report as follows:

### Summary

- Total Python files scanned: [count]
- Total functions found: [count]
- Functions with docstrings: [count]
- Functions missing docstrings: [count]
- Compliance rate: [percentage]%

### Violations

If violations found, list them:

```
[file_path]:[line_number] - [function_name]
[file_path]:[line_number] - [function_name]
```

If no violations, state: "All functions have docstrings. ✓"

### Recommendations

- [Suggestion for fixing violations]
- [Suggestion for preventing future violations]
```

## Workflow

### Step 1: Analyze HIGH_LEVEL_PROMPT

- Parse the user's description to understand the prompt's purpose
- Identify the target audience and use case
- Determine what inputs (variables) the prompt needs
- Identify what outputs (report) the prompt should produce

### Step 2: Design Prompt Structure

- Decide if frontmatter is needed (does it require specific tools or permissions?)
- Define variables using $1, $2, etc. or $ARGUMENTS syntax
- Sketch out 3-7 workflow steps that accomplish the prompt's goal
- Design the report format based on expected outputs

### Step 3: Generate Complete Prompt

- Use Write tool to create the new prompt file
- Follow the Specified Format Template structure exactly
- Include all 4 sections: Metadata (if needed), Variables, Workflow, Report
- Ensure the prompt is self-contained and clear

### Step 4: Validate Generated Prompt

- Review that the prompt follows TAC standards
- Check that variable syntax is correct ($1, $2, $ARGUMENTS)
- Verify workflow steps are clear and actionable
- Confirm report format is well-specified
- Ensure frontmatter YAML is valid (if included)

## Report

After generating the prompt, provide:

### Generated Prompt Summary

- **File created**: [path to new prompt file]
- **Purpose**: [1-sentence description]
- **Variables**: [list of input variables]
- **Workflow steps**: [count and brief description]
- **Report format**: [description of output structure]

### Key Features

- [Notable feature 1 of the generated prompt]
- [Notable feature 2 of the generated prompt]
- [Notable feature 3 of the generated prompt]

### Usage Example

Show how to invoke the generated prompt:

```bash
/command_name <arg1> <arg2>
```

### Next Steps

- [Suggestion for testing the generated prompt]
- [Suggestion for integrating it into workflows]
