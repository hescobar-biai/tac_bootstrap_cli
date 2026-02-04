# Chore: Update CLI README with TAC-13 Agent Experts Documentation

## Metadata
issue_number: `586`
adw_id: `chore_Tac_13_Task_24`
issue_json: `{"number": 586, "title": "[TAC-13] Task 24: Update CLI README with TAC-13 features", "body": "**Workflow Metadata:**\n```\n/chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_13_Task_24\n```\n\n**Description:**\nAdd comprehensive documentation for Agent Experts (TAC-13) to the CLI README.\n\n**Technical Steps:**\n1. Open `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md`\n2. Add new section after \"Intelligent Documentation Loading (TAC-9)\":\n   ```markdown\n   ### Agent Experts (TAC-13)\n   ```\n3. Document:\n   - What are agent experts (Act \u2192 Learn \u2192 Reuse loop)\n   - Self-improving template metaprompts concept\n   - Expertise files as mental models\n   - When to use agent experts vs generic agents\n4. Include usage examples:\n   ```bash\n   # Query CLI expert\n   /experts:cli:question \"How does template registration work?\"\n\n   # Self-improve CLI expert after code changes\n   /experts:cli:self-improve true\n\n   # Orchestrate expert through full workflow\n   /expert-orchestrate cli \"Add new template for hooks\"\n\n   # Scale experts in parallel for high-confidence results\n   /expert-parallel cli \"Review scaffold service logic\" 5\n   ```\n5. Add table of included experts:\n\n| Expert Domain | Expertise Coverage | Commands |\n|---------------|-------------------|----------|\n| `cli` | tac-bootstrap CLI, templates, scaffold service | `/experts:cli:question`, `/experts:cli:self-improve` |\n| `adw` (optional) | AI Developer Workflows, state management | `/experts:adw:question`, `/experts:adw:self-improve` |\n| `commands` (optional) | Slash command structure, variables | `/experts:commands:question`, `/experts:commands:self-improve` |\n\n6. Document meta-agentics:\n   - `/meta-prompt` - Generate new slash commands\n   - `/meta-agent` - Generate new agent definitions\n   - Progressive disclosure for skills\n\n**Acceptance Criteria:**\n- Section is clear and actionable\n- Examples are concrete and copy-pasteable\n- Table is properly formatted\n- Integrates seamlessly with existing README structure\n- Matches style of other feature sections\n\n**Impacted Paths:**\n- `/Users/hernandoescobar/Doc\n\n[TRUNCATED - body exceeds 2000 chars]"}`

## Chore Description

Add comprehensive documentation section for Agent Experts (TAC-13) to the CLI README at `tac_bootstrap_cli/README.md`. This section will explain the self-improving agent expert pattern, including the Act → Learn → Reuse loop, expertise files as mental models, and when to use specialized experts versus generic agents.

The new section must be inserted after the existing "Intelligent Documentation Loading (TAC-9)" section (around line 248) and before "TAC-12 Multi-Agent Orchestration" (line 390).

## Relevant Files

Files to complete this chore:

- `tac_bootstrap_cli/README.md` - Target file for documentation update. Currently has TAC-9 section ending at ~line 389 and TAC-12 section starting at ~line 390. New TAC-13 section will be inserted between these.
- `ai_docs/doc/plan_tasks_tac_13.md` - Source specification for Task 24 with complete requirements (lines 3231-3290)
- `ai_docs/doc/TAC-13_dual_strategy_summary.md` - Context on TAC-13 architecture and expert system design
- `ai_docs/doc/TAC-13_implementation_status.md` - Current implementation status showing 3 expert domains implemented (CLI, ADW, Commands)
- `.claude/commands/experts/*` - Existing expert command implementations for reference examples

### New Files
None - only editing existing README.md

## Step by Step Tasks

IMPORTANTE: Execute each step in order.

### Task 1: Read current README structure
- Read `tac_bootstrap_cli/README.md` to identify exact insertion point
- Locate the end of "Intelligent Documentation Loading (TAC-9)" section (~line 389)
- Verify TAC-12 section starts immediately after (~line 390)
- Note the formatting style and section structure to match

### Task 2: Draft TAC-13 Agent Experts section content
- Create new section header: `### Agent Experts (TAC-13)`
- Write introduction explaining:
  - Act → Learn → Reuse loop concept
  - Self-improving template metaprompts
  - Expertise files as mental models (YAML-based knowledge)
  - Decision criteria: when to use experts vs generic agents
- Follow the tone and style of existing TAC-9 and TAC-12 sections
- Keep explanations concise but actionable

### Task 3: Add usage examples subsection
- Create subsection with concrete, copy-pasteable examples:
  ```bash
  # Query CLI expert
  /experts:cli:question "How does template registration work?"

  # Self-improve CLI expert after code changes
  /experts:cli:self-improve true

  # Orchestrate expert through full workflow
  /expert-orchestrate cli "Add new template for hooks"

  # Scale experts in parallel for high-confidence results
  /expert-parallel cli "Review scaffold service logic" 5
  ```
- Add brief explanations for each command category
- Ensure commands match actual implementations in `.claude/commands/experts/`

### Task 4: Add expert domains table
- Create properly formatted markdown table:

| Expert Domain | Expertise Coverage | Commands |
|---------------|-------------------|----------|
| `cli` | tac-bootstrap CLI, templates, scaffold service | `/experts:cli:question`, `/experts:cli:self-improve` |
| `adw` (optional) | AI Developer Workflows, state management | `/experts:adw:question`, `/experts:adw:self-improve` |
| `commands` (optional) | Slash command structure, variables | `/experts:commands:question`, `/experts:commands:self-improve` |

- Note: Mark ADW and Commands as "(optional)" since they may not be in all installations

### Task 5: Document meta-agentic capabilities
- Add subsection for meta-agentic commands:
  - `/meta-prompt` - Generate new slash commands from natural language
  - `/meta-agent` - Generate new agent definitions (.md + .j2 files)
  - Progressive disclosure for skills (beginner → advanced patterns)
- Explain how these enable extensibility and self-evolution of the agentic layer
- Link conceptually to the "self-improving" aspect of experts

### Task 6: Insert section into README
- Use Edit tool to insert the complete TAC-13 section
- Insert after line ~389 (end of TAC-9) and before line 390 (start of TAC-12)
- Ensure proper spacing (2 blank lines between sections)
- Maintain consistent markdown formatting with surrounding sections

### Task 7: Verify integration and formatting
- Re-read the updated README to confirm:
  - Section is placed correctly between TAC-9 and TAC-12
  - Markdown table renders properly (aligned columns)
  - Code blocks have correct syntax highlighting (bash)
  - Examples are copy-pasteable without modification
  - Style matches existing sections (headers, tone, structure)
  - No broken links or references

### Task 8: Run validation commands
- Execute all validation commands to ensure zero regressions
- Verify README structure integrity
- Confirm no unintended changes to other sections

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test CLI still works

## Notes

**Integration Points:**
- This section builds on TAC-9 (intelligent doc loading) by introducing expert-specific documentation (expertise files)
- Complements TAC-12 (orchestration) by providing specialized expert agents for orchestration workflows
- Enables progressive disclosure: users start with `/experts:cli:question` and graduate to `/expert-orchestrate` and `/expert-parallel`

**Formatting Guidelines:**
- Match the style of TAC-9 section (lines 248-389): clear hierarchy, concrete examples, hybrid detection system explanation
- Match the style of TAC-12 section (line 390+): command tables, usage patterns, parameter descriptions
- Use consistent header levels: `###` for main section, `####` for subsections if needed
- Maintain the README's progressive disclosure pattern: simpler concepts first, advanced patterns later

**Content Constraints:**
- Keep explanations concise (2-3 sentences per concept)
- Prioritize actionable examples over theory
- Use the exact commands that exist in `.claude/commands/experts/`
- Avoid duplicating content from other sections
- Cross-reference related sections (TAC-9, TAC-12) where appropriate

**Quality Checklist:**
- [ ] Section header follows naming convention
- [ ] Act → Learn → Reuse loop explained clearly
- [ ] Expertise files concept introduced
- [ ] Decision criteria for experts vs generic agents
- [ ] All 4 usage examples are copy-pasteable
- [ ] Expert domains table has 3 rows (CLI, ADW, Commands)
- [ ] Meta-agentic commands documented (meta-prompt, meta-agent)
- [ ] Progressive disclosure mentioned
- [ ] Proper placement between TAC-9 and TAC-12
- [ ] Formatting matches surrounding sections
