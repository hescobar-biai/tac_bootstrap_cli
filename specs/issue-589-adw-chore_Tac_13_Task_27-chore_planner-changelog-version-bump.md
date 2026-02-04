# Chore: Update CHANGELOG and bump version to 0.8.0

## Metadata
issue_number: `589`
adw_id: `chore_Tac_13_Task_27`
issue_json: `{"number": 589, "title": "[TAC-13] Task 27: Update CHANGELOG and bump version to 0.8.0", "body": "**Workflow Metadata:**\n```\n/chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_13_Task_27\n```\n\n**Description:**\nUpdate CHANGELOG with all TAC-13 features and bump version to 0.8.0.\n\n**Technical Steps:**\n1. Open `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md`\n2. Add new section at top:\n   ```markdown\n   ## [0.8.0] - 2026-02-03\n\n   ### Added - TAC-13: Agent Experts\n\n   **Core Capabilities:**\n   - Agent experts with self-improving expertise files (Act → Learn → Reuse loop)\n   - Self-improving template metaprompts for domain specialization\n   - Mental model pattern: expertise.yaml files that validate against codebase\n   - Question prompts: Answer domain questions by reading expertise + validating against code\n   - Self-improve prompts: 7-phase workflow (check diff → validate → update → enforce limits)\n\n   **Agent Experts Included:**\n   - CLI Expert: tac-bootstrap CLI, templates, scaffold service\n   - (Optional) ADW Expert: AI Developer Workflows, state management, GitHub integration\n   - (Optional) Commands Expert: Slash command structure, variables, workflows\n\n   **Meta-Agentics:**\n   - `/meta-prompt`: Generate new slash commands from descriptions\n   - `/meta-agent`: Generate new agent definitions from descriptions\n   - Meta-skill pattern documentation (progressive disclosure)\n\n   **Orchestration:**\n   - `/expert-orchestrate`: Plan → Build → Improve workflow for agent experts\n   - `/expert-parallel`: Scale experts in parallel (3-10 instances) for high-confidence results\n\n   **Documentation:**\n   - Comprehensive TAC-13 guide in ai_docs/doc/\n   - Expertise file structure documentation\n   - Meta-skill pattern guide\n   - Auto-detection keywords for TAC-13 docs\n\n   **Templates:**\n   - CLI expert templates (question, self-improve, expertise seed)\n   - Meta-prompt template\n   - Meta-agent template\n   - Expert orchestration templates\n\n   ### Changed\n   - Updated README with Agent Experts section and usage examples\n   - Enhanced AI docs auto-detection with TAC-13 keywords\n   - Extended scaffold service to include expert templates and expertise files\n   ```\n3. Open `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/pyproject.toml`\n4. Update `version = \"0.7.1\"` to `version = \"0.8.0\"`\n5. Commit with message: \"chore: bump version to 0.8.0 and update CHANGELOG with TAC-13 features\"\n\n**Acceptance Criteria:**\n- [ ] CHANGELOG.md has new 0.8.0 section with TAC-13 features\n- [ ] pyproject.toml version bumped to 0.8.0\n- [ ] All validation commands pass\n- [ ] Changes committed with descriptive message"}`

## Chore Description
This is the final task of TAC-13 implementation. We need to:
1. Update CHANGELOG.md with a comprehensive section documenting all TAC-13 features
2. Bump the version from 0.7.1 to 0.8.0 in pyproject.toml
3. Commit the changes with an appropriate message

The CHANGELOG entry should document:
- Agent experts with self-improving expertise files (Act → Learn → Reuse loop)
- Three domain experts: CLI, ADW (optional), Commands (optional)
- Meta-agentic capabilities: /meta-prompt and /meta-agent
- Orchestration commands: /expert-orchestrate and /expert-parallel
- All related documentation and templates

## Relevant Files
Files required to complete this chore:

1. **CHANGELOG.md** - Root of repository
   - Currently at version 0.7.1 (last entry)
   - Need to add new 0.8.0 section at the top
   - Follow established format from 0.7.1 and 0.7.0 entries

2. **tac_bootstrap_cli/pyproject.toml** - Package version definition
   - Line 3: `version = "0.7.1"`
   - Need to update to `version = "0.8.0"`

### New Files
No new files required. This is a documentation and version metadata update.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Add 0.8.0 section to CHANGELOG.md
- Read CHANGELOG.md to understand current structure
- Insert new section at top (after header, before 0.7.1 section)
- Use provided content from issue with proper formatting
- Include all TAC-13 features: agent experts, meta-agentics, orchestration, documentation, templates
- Follow format from previous entries (markdown headings, bullet points, proper indentation)
- Use date 2026-02-03 (today's date based on 0.7.1 entry)

### Task 2: Bump version in pyproject.toml
- Read tac_bootstrap_cli/pyproject.toml
- Update line 3 from `version = "0.7.1"` to `version = "0.8.0"`
- Preserve all other content exactly as is

### Task 3: Validate changes
- Verify CHANGELOG.md has valid markdown structure
- Verify pyproject.toml has valid TOML syntax
- Run all validation commands (see below)

### Task 4: Commit changes
- Stage both files: CHANGELOG.md and tac_bootstrap_cli/pyproject.toml
- Use commit message: "chore: bump version to 0.8.0 and update CHANGELOG with TAC-13 features"
- Include co-author tag as per standard practice

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test CLI functionality

## Notes
- This is the final task (Task 27 of 27) in TAC-13 implementation
- Version 0.8.0 represents completion of Agent Experts milestone
- CHANGELOG content provided in issue body is comprehensive and ready to use
- Follow Keep a Changelog format (https://keepachangelog.com/en/1.1.0/)
- Maintain semantic versioning (0.8.0 = minor version bump for new features)
- This chore requires no code changes, only documentation and metadata updates
