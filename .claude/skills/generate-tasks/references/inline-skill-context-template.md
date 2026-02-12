# Inline Skill Context Template

Reference for assembling context when creating skills inline during `generate-tasks` gap resolution (Step 6b).

---

## Context Payload

Gather the following before calling `init_skill.py` and editing the generated SKILL.md:

| Field | Source | Example |
|-------|--------|---------|
| **Skill name** | Gap name from Step 6 mapping (`gap:<name>`) | `create-notification-handler` |
| **Purpose** | ROADMAP step descriptions that map to this gap | "Handles Slack notification dispatch and formatting" |
| **Target file paths** | `File` column of all ROADMAP steps using this skill | `backend/app/infrastructure/notification.py` |
| **Architecture context** | TDD sections relevant to the skill's domain | Data flow, service layer patterns |
| **Conventions** | STANDARDS file constraints (naming, testing, DI) | Snake-case modules, pytest, dependency injection |
| **Similar installed skills** | Closest existing skill by category or pattern | `create-domain-service`, `scaffold-backend-service` |

---

## SKILL.md Generation Rules

After running `init_skill.py`, replace the TODO template with synthesized content:

### Frontmatter

```yaml
---
name: {skill-name}
description: |
  {1-2 sentence description derived from ROADMAP step descriptions}.
  Triggers: "{trigger phrase 1}", "{trigger phrase 2}"
---
```

### Body Structure

Use a **workflow-based** structure (most common for domain skills):

1. **Title** — `# {Skill Title}` (title-cased from kebab name)
2. **Overview** — 1-2 sentences: what it creates and when to use it
3. **Input** — Table of required context (file paths, config, domain models)
4. **Workflow** — 3-5 numbered steps covering:
   - File creation / scaffolding
   - Core implementation pattern
   - Wiring (DI, routing, imports)
   - Tests
5. **Conventions** — Project-specific rules from STANDARDS (keep concise)
6. **References** — Links to reference files if any were created

### Line Targets

- **Total SKILL.md**: Under 80 lines (starter quality)
- **Frontmatter**: 4-6 lines
- **Overview + Input**: 10-15 lines
- **Workflow**: 30-40 lines
- **Conventions + References**: 10-15 lines

---

## Skill Category Patterns

Choose the naming prefix based on what the skill produces:

| Prefix | Use When | Examples |
|--------|----------|---------|
| `create-*` | Produces a single domain concept (model, service, handler, event) | `create-notification-handler`, `create-webhook-processor` |
| `scaffold-*` | Produces multiple related files (page + components, service + config) | `scaffold-auth-flow`, `scaffold-form-builder` |

### Naming Rules
- Kebab-case, max 3 words after prefix
- Use domain language from the ROADMAP descriptions
- Avoid generic names — be specific to the project context

---

## Cleanup Checklist

After editing the generated SKILL.md, delete the example files that `init_skill.py` creates:

- `scripts/example.py`
- `references/api_reference.md`
- `assets/example_asset.txt`

If the skill needs no scripts, references, or assets directories, delete those empty directories too.

---

## Quality Notes

Inline-created skills are **starter quality** — they provide enough structure to unblock task generation and initial implementation. They may benefit from iteration after the first implementation pass. The goal is a functional skill that captures the right workflow, not a polished production skill.
