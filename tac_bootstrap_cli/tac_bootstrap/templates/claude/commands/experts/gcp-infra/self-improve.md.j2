---
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, TodoWrite
description: Self-improve GCP Infrastructure expertise by validating against codebase implementation
argument-hint: [check_git_diff (true/false)] [focus_area (optional)]
model: sonnet
---

# NOTE: Model "sonnet" uses 3-tier resolution:
#   1. ANTHROPIC_DEFAULT_SONNET_MODEL (env var) - highest priority
#   2. config.yml agentic.model_policy.sonnet_model - project config
#   3. Hardcoded default "claude-sonnet-4-5-20250929" - fallback
# See .claude/MODEL_RESOLUTION.md for details


# Purpose

You maintain the GCP Infrastructure expert system's expertise accuracy by comparing the existing expertise file against the actual codebase implementation. Follow the `Workflow` section to detect and remedy any differences, missing pieces, or outdated information, ensuring the expertise file remains a powerful **mental model** and accurate memory reference for infrastructure tasks.

## Variables

CHECK_GIT_DIFF: $1 default to false if not specified
FOCUS_AREA: $2 default to empty string
EXPERTISE_FILE: .claude/commands/experts/gcp-infra/expertise.yaml
MAX_LINES: 1000

## Instructions

- This is a self-improvement workflow to keep GCP Infrastructure expertise synchronized with the actual codebase
- Think of the expertise file as your **mental model** and memory reference for all infrastructure functionality
- Always validate expertise against real implementation, not assumptions
- Focus exclusively on Infrastructure functionality (GCP, Terraform, IAM, networking, cost)
- If FOCUS_AREA is provided, prioritize validation and updates for that specific area
- Maintain the YAML structure of the expertise file
- Enforce strict line limit of 1000 lines maximum
- Prioritize actionable, high-value expertise over verbose documentation
- When trimming, remove least critical information that won't impact expert performance
- Git diff checking is optional and controlled by the CHECK_GIT_DIFF variable
- Be thorough in validation but concise in documentation
- Write as a principal engineer that writes CLEARLY and CONCISELY for future engineers.
- Keep in mind, after your thorough search, there may be nothing to be done - this is perfectly acceptable.

## Workflow

1. **Check Git Diff (Conditional)**
   - If CHECK_GIT_DIFF is "true", run `git diff` to identify recent changes to infrastructure files
   - If CHECK_GIT_DIFF is "false", skip this step

2. **Read Current Expertise**
   - Read the entire EXPERTISE_FILE
   - Identify key sections: overview, gcp_resources, terraform_patterns, iam, cost_optimization
   - Note any areas that seem outdated or incomplete

3. **Validate Against Codebase**
   - Read documented key implementation files
   - Compare documented expertise against actual Terraform configs, deployment scripts, and infra code

4. **Identify Discrepancies**
   - List all differences found

5. **Update Expertise File**
   - Remedy all identified discrepancies
   - Maintain YAML structure and formatting

6. **Enforce Line Limit**
   - Run: `wc -l .claude/commands/experts/gcp-infra/expertise.yaml`
   - If line count > MAX_LINES: trim least critical sections

7. **Validation Check**
   - Validate YAML syntax: `python3 -c "import yaml; yaml.safe_load(open('.claude/commands/experts/gcp-infra/expertise.yaml'))"`

## Report

### Summary
- Brief overview, discrepancies found/remedied, final line count

### Discrepancies Found
- List each discrepancy

### Updates Made
- Concise list of all updates

### Validation Results
- Confirm expertise is present and YAML is valid

### Codebase References
- List of files validated against
