# GitHub Check

Verify GitHub connection and configuration for the project.

## Instructions

Run GitHub checks in sequence and report results.

### 1. Verify GitHub CLI installed
```bash
gh --version
```
- If fails: Report that `gh` CLI is not installed
- Suggest: `brew install gh` (macOS) or see https://cli.github.com/

### 2. Verify GitHub authentication
```bash
gh auth status
```
- Should show authenticated account
- If fails: Suggest `gh auth login`

### 3. Verify Git remote configured
```bash
git remote -v
```
- Should show `origin` pointing to GitHub
- If no remote: Report that it's not configured

### 4. Verify repository access
```bash
gh repo view --json name,owner,url
```
- If works: Show repo info
- If fails: Verify permissions or that the repo exists

### 5. Verify current branch
```bash
git branch --show-current
```
- Show current branch

### 6. Verify sync status with remote
```bash
git fetch origin --dry-run 2>&1
```
- Verify connection to remote works

### 7. Verify issues and PRs (optional)
```bash
gh issue list --limit 5
gh pr list --limit 5
```
- Show recent issues and PRs if they exist

## Report

Report results as JSON:

```json
{
  "status": "ready|warning|error",
  "checks": [
    {
      "name": "gh_cli_installed",
      "passed": boolean,
      "message": "string"
    },
    {
      "name": "gh_authenticated",
      "passed": boolean,
      "message": "string",
      "account": "string (if passed)"
    },
    {
      "name": "git_remote_configured",
      "passed": boolean,
      "message": "string",
      "remote_url": "string (if passed)"
    },
    {
      "name": "repo_access",
      "passed": boolean,
      "message": "string",
      "repo_name": "string (if passed)"
    },
    {
      "name": "remote_sync",
      "passed": boolean,
      "message": "string"
    }
  ],
  "summary": {
    "current_branch": "string",
    "open_issues": number,
    "open_prs": number
  },
  "next_steps": ["string"]
}
```

### Example Output

```json
{
  "status": "ready",
  "checks": [
    {"name": "gh_cli_installed", "passed": true, "message": "gh version 2.40.0"},
    {"name": "gh_authenticated", "passed": true, "message": "Logged in", "account": "user"},
    {"name": "git_remote_configured", "passed": true, "message": "Remote configured", "remote_url": "git@github.com:org/repo.git"},
    {"name": "repo_access", "passed": true, "message": "Access verified", "repo_name": "tac-bootstrap"},
    {"name": "remote_sync", "passed": true, "message": "Connection successful"}
  ],
  "summary": {
    "current_branch": "main",
    "open_issues": 3,
    "open_prs": 1
  },
  "next_steps": []
}
```
