# Task Plan: ADW Triggers Synchronization & Enhancement

**Version Target:** 0.4.1
**Created:** 2026-01-25
**Scope:** Synchronize templates with root files, update documentation

---

## ✅ TAREAS COMPLETADAS (eliminadas del plan)

Las siguientes tareas ya fueron implementadas:

- ~~Task 1: Add `--once` flag to trigger_cron.py~~ ✅ (ROOT + TEMPLATE tienen `--once`)
- ~~Task 2: Add `--once` flag to trigger_issue_chain.py~~ ✅ (ROOT + TEMPLATE tienen `--once`)
- ~~Task 7: Update adw_triggers/__init__.py docstring~~ ✅ (ROOT + TEMPLATE tienen docstring completo)

---

## Task 3

### [CHORE] Create trigger_webhook.py.j2 template (sync from root)

**Description:**
Create the missing Jinja2 template for `trigger_webhook.py`. The root file already exists with user assignment validation logic. Copy content to create the template.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_triggers/trigger_webhook.py` (SOURCE - read only)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_webhook.py.j2` (CREATE)

**Implementation:**
- Copy the full content from the root `trigger_webhook.py` to create `trigger_webhook.py.j2`
- The template will include:
  - `get_current_gh_user()` import
  - `is_issue_assigned_to_me()` import
  - `assign_issue_to_me()` import
  - User assignment validation before workflow execution
  - Startup message showing current user

---

## Task 4

### [CHORE] Synchronize trigger_cron.py.j2 template with root (user validation)

**Description:**
The root `trigger_cron.py` already has user assignment validation. Update the template to match the root file exactly.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_triggers/trigger_cron.py` (SOURCE - read only)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2` (UPDATE)

**Changes required in template:**
- Add imports: `get_current_gh_user`, `is_issue_assigned_to_me`, `assign_issue_to_me`
- Add user validation check in `check_and_process_issues()` before processing each issue
- Add `assign_issue_to_me()` call in `trigger_workflow()`
- Add current user display in `main()` startup messages

---

## Task 5

### [CHORE] Synchronize trigger_issue_chain.py.j2 template with root (user validation)

**Description:**
The root `trigger_issue_chain.py` already has user assignment validation. Update the template to match the root file exactly.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_triggers/trigger_issue_chain.py` (SOURCE - read only)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_issue_chain.py.j2` (UPDATE)

**Changes required in template:**
- Add imports: `get_current_gh_user`, `is_issue_assigned_to_me`, `assign_issue_to_me`
- Modify `get_current_issue()` to check assignment before returning issue
- Add `assign_issue_to_me()` call in `trigger_workflow()`
- Add current user display in `main()` startup messages

---

## Task 6

### [CHORE] Synchronize github.py.j2 template with root (user validation functions)

**Description:**
The root `github.py` already has user validation functions. Update the template to include these three new functions.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/github.py` (SOURCE - read only)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/github.py.j2` (UPDATE)

**Functions to add to template:**
1. `get_current_gh_user() -> Optional[str]` - Returns the authenticated GitHub user login
2. `is_issue_assigned_to_me(issue_number: str, repo_path: Optional[str] = None) -> bool` - Checks if issue is assigned to current user
3. `assign_issue_to_me(issue_id: str) -> bool` - Assigns issue to current user using `@me`

---

## Task 8

### [CHORE] Add polling interval documentation to tac_bootstrap_cli README

**Description:**
Add a dedicated section documenting recommended polling intervals and GitHub API rate limiting considerations for the trigger systems.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md`

**Content to add after "Issue Chain Trigger Setup" section:**

```markdown
#### Trigger Polling Configuration

| Trigger | Default Interval | Recommended Range | Notes |
|---------|------------------|-------------------|-------|
| `trigger_cron.py` | 20s | 15s - 60s | Lower intervals increase API usage |
| `trigger_issue_chain.py` | 20s | 20s - 120s | Sequential processing, less frequent OK |

**GitHub API Rate Limiting:**
- Authenticated requests: 5,000/hour
- Each polling cycle makes 1-3 API calls per open issue
- For repos with many open issues, use longer intervals (30s+)
- Monitor rate limits: `gh api rate_limit`
```

---

## Task 9

### [CHORE] Update CHANGELOG.md with version 0.4.1

**Description:**
Document all changes introduced in this task plan under a new version 0.4.1 entry following Keep a Changelog format and semantic versioning.

**Files affected:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md`

**Content to add between `## [0.4.0]` and `## [0.3.0]` sections:**

```markdown
## [0.4.1] - 2026-01-25

### Added
- User assignment validation in all ADW triggers (cron, webhook, issue_chain)
- Functions `get_current_gh_user()`, `is_issue_assigned_to_me()`, `assign_issue_to_me()` in `github.py`
- Template `trigger_webhook.py.j2` for webhook trigger generation
- Polling interval documentation in README

### Changed
- Triggers now only process issues assigned to the authenticated GitHub user
- Triggers display current user at startup for visibility
- Synchronized `trigger_cron.py.j2` template with root (user validation)
- Synchronized `trigger_issue_chain.py.j2` template with root (user validation)
- Synchronized `github.py.j2` template with root (user validation functions)
```

---

## Execution Checklist

- [ ] Task 3: Create trigger_webhook.py.j2 (from ROOT)
- [ ] Task 4: Sync trigger_cron.py.j2 (user validation from ROOT)
- [ ] Task 5: Sync trigger_issue_chain.py.j2 (user validation from ROOT)
- [ ] Task 6: Sync github.py.j2 (user validation functions from ROOT)
- [ ] Task 8: Add polling docs to README
- [ ] Task 9: Update CHANGELOG.md to v0.4.1

---

## Verification Commands

```bash
# Verify all templates exist and are synced
ls -la tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/

# Verify trigger_webhook.py.j2 was created
ls tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_webhook.py.j2

# Verify user validation functions in templates
grep "get_current_gh_user" tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/github.py.j2
grep "is_issue_assigned_to_me" tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2
grep "is_issue_assigned_to_me" tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_issue_chain.py.j2

# Verify README has polling docs
grep "Trigger Polling Configuration" tac_bootstrap_cli/README.md

# Verify CHANGELOG updated
grep "0.4.1" CHANGELOG.md

# Run tests
uv run pytest tac_bootstrap_cli/tests/ -v
```
