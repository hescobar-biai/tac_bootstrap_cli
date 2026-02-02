# TAC-13 Dual Strategy - Correction Summary

## Pattern Applied to Tasks 7-17

### Task Structure (All Tasks)

Each task creates **3 components**:

1. **Template (.j2)** in CLI
   - Path: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/{path}.j2`
   - Uses `{{ config.project.name }}` variables

2. **Registration** in scaffold_service.py
   ```python
   plan.add_file(
       action="create",  # or "skip_if_exists" for expertise.yaml
       template="{path}.j2",
       path=".claude/commands/{path}",
       reason="{description}"
   )
   ```

3. **Implementation** in repo root
   - Path: `.claude/commands/{path}`
   - For local testing and use

---

## Tasks 7-12: ADW and Commands Experts

### Task 7: ADW Expert - Question Prompt
- Template: `templates/claude/commands/experts/adw/question.md.j2`
- Repo: `.claude/commands/experts/adw/question.md`
- Registration: "ADW expert question prompt for read-only queries"

### Task 8: ADW Expert - Self-Improve Prompt
- Template: `templates/claude/commands/experts/adw/self-improve.md.j2`
- Repo: `.claude/commands/experts/adw/self-improve.md`
- Registration: "ADW expert 7-phase self-improve workflow"

### Task 9: ADW Expert - Expertise File
- Template: `templates/claude/commands/experts/adw/expertise.yaml.j2` (seed)
- Repo: `.claude/commands/experts/adw/expertise.yaml` (populated)
- Registration: action="skip_if_exists", "ADW expert expertise seed file"

### Task 10: Commands Expert - Question Prompt
- Template: `templates/claude/commands/experts/commands/question.md.j2`
- Repo: `.claude/commands/experts/commands/question.md`
- Registration: "Commands expert question prompt"

### Task 11: Commands Expert - Self-Improve Prompt
- Template: `templates/claude/commands/experts/commands/self-improve.md.j2`
- Repo: `.claude/commands/experts/commands/self-improve.md`
- Registration: "Commands expert 7-phase self-improve workflow"

### Task 12: Commands Expert - Expertise File
- Template: `templates/claude/commands/experts/commands/expertise.yaml.j2` (seed)
- Repo: `.claude/commands/experts/commands/expertise.yaml` (populated)
- Registration: action="skip_if_exists", "Commands expert expertise seed"

---

## Tasks 13-17: Meta-Agentics and Orchestration

### Task 13: Meta-Prompt Generator
- Template: `templates/claude/commands/meta-prompt.md.j2`
- Repo: `.claude/commands/meta-prompt.md`
- Registration: "Meta-prompt generator - prompts that create prompts"

### Task 14: Meta-Agent Generator
- Template: `templates/claude/commands/meta-agent.md.j2`
- Repo: `.claude/commands/meta-agent.md`
- Registration: "Meta-agent generator - agents that create agents"

### Task 15: Meta-Skill Documentation
- **SPECIAL CASE**: Only documentation file, no template
- Path: `ai_docs/doc/meta-skill-pattern.md`
- No registration needed

### Task 16: Expert Orchestrator
- Template: `templates/claude/commands/expert-orchestrate.md.j2`
- Repo: `.claude/commands/expert-orchestrate.md`
- Registration: "Agent expert orchestrator - plan→build→improve workflow"

### Task 17: Parallel Expert Scaling
- Template: `templates/claude/commands/expert-parallel.md.j2`
- Repo: `.claude/commands/expert-parallel.md`
- Registration: "Parallel expert scaling - 3-10 agents for consensus"

---

## Tasks 18-22: Template Consolidation

**IMPORTANT**: Tasks 18-22 originally created templates, but now Tasks 4-17 already create them.

### Required Changes:

**Task 18**: ~~Create CLI expert templates~~ → **REMOVE** (already done in Tasks 4-6)

**Task 19**: Meta-prompt template → **KEEP** (backup/verification task)

**Task 20**: Meta-agent template → **KEEP** (backup/verification task)

**Task 21**: Expert-orchestrate template → **KEEP** (backup/verification task)

**Task 22**: Expert-parallel template → **KEEP** (backup/verification task)

**Task 23**: Register templates → **UPDATE** to verify all registrations from Tasks 4-17

---

## Acceptance Criteria Template (All Tasks)

```markdown
**Acceptance Criteria:**
- ✅ **Template (.j2)** created in CLI templates directory
- ✅ **Template registered** in scaffold_service.py
- ✅ **Implementation file** created in repo root
- ✅ Jinja2 template uses {{ config.project.name }} variables
- ✅ [Task-specific criteria...]

**Validation Commands:**
```bash
# Verify template
test -f tac_bootstrap_cli/tac_bootstrap/templates/{path}.j2 && echo "✓ Template exists"

# Verify registration
grep -A 3 "{path}.j2" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered"

# Verify repo root
test -f .claude/commands/{path} && echo "✓ Repo file exists"
```

**Test Commands:**
```bash
# Test local command
cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap
/{command} [args]

# Test template generation
cd /tmp/test-project
tac-bootstrap add-agentic
test -f .claude/commands/{path} && echo "✓ Generated"
```

**Impacted Paths:**
- `tac_bootstrap_cli/tac_bootstrap/templates/{path}.j2` (template)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` (registration)
- `.claude/commands/{path}` (repo root)
```

---

## scaffold_service.py Registrations

All registrations go in `_add_claude_code_commands()` method:

```python
def _add_claude_code_commands(self, plan: ScaffoldPlan) -> None:
    """Register all command templates."""

    # ... existing registrations ...

    # TAC-13: Agent Experts - CLI
    plan.add_file(
        action="create",
        template="claude/commands/experts/cli/question.md.j2",
        path=".claude/commands/experts/cli/question.md",
        reason="CLI expert question prompt"
    )

    plan.add_file(
        action="create",
        template="claude/commands/experts/cli/self-improve.md.j2",
        path=".claude/commands/experts/cli/self-improve.md",
        reason="CLI expert self-improve workflow"
    )

    plan.add_file(
        action="skip_if_exists",
        template="claude/commands/experts/cli/expertise.yaml.j2",
        path=".claude/commands/experts/cli/expertise.yaml",
        reason="CLI expert expertise seed"
    )

    # TAC-13: Agent Experts - ADW
    plan.add_file(
        action="create",
        template="claude/commands/experts/adw/question.md.j2",
        path=".claude/commands/experts/adw/question.md",
        reason="ADW expert question prompt"
    )

    plan.add_file(
        action="create",
        template="claude/commands/experts/adw/self-improve.md.j2",
        path=".claude/commands/experts/adw/self-improve.md",
        reason="ADW expert self-improve workflow"
    )

    plan.add_file(
        action="skip_if_exists",
        template="claude/commands/experts/adw/expertise.yaml.j2",
        path=".claude/commands/experts/adw/expertise.yaml",
        reason="ADW expert expertise seed"
    )

    # TAC-13: Agent Experts - Commands
    plan.add_file(
        action="create",
        template="claude/commands/experts/commands/question.md.j2",
        path=".claude/commands/experts/commands/question.md",
        reason="Commands expert question prompt"
    )

    plan.add_file(
        action="create",
        template="claude/commands/experts/commands/self-improve.md.j2",
        path=".claude/commands/experts/commands/self-improve.md",
        reason="Commands expert self-improve workflow"
    )

    plan.add_file(
        action="skip_if_exists",
        template="claude/commands/experts/commands/expertise.yaml.j2",
        path=".claude/commands/experts/commands/expertise.yaml",
        reason="Commands expert expertise seed"
    )

    # TAC-13: Meta-Agentics
    plan.add_file(
        action="create",
        template="claude/commands/meta-prompt.md.j2",
        path=".claude/commands/meta-prompt.md",
        reason="Meta-prompt generator"
    )

    plan.add_file(
        action="create",
        template="claude/commands/meta-agent.md.j2",
        path=".claude/commands/meta-agent.md",
        reason="Meta-agent generator"
    )

    # TAC-13: Orchestration
    plan.add_file(
        action="create",
        template="claude/commands/expert-orchestrate.md.j2",
        path=".claude/commands/expert-orchestrate.md",
        reason="Expert orchestrator workflow"
    )

    plan.add_file(
        action="create",
        template="claude/commands/expert-parallel.md.j2",
        path=".claude/commands/expert-parallel.md",
        reason="Parallel expert scaling"
    )
```

---

## Summary

- **Total Tasks**: 27
- **Corrected**: 6 (Tasks 1-6)
- **Remaining**: 21 (Tasks 7-27)
- **Pattern applies to**: Tasks 7-17 (11 tasks)
- **Special cases**: Task 15 (docs only), Tasks 18-22 (consolidation)
- **Already correct**: Tasks 23-27 (integration, docs, version bump)
