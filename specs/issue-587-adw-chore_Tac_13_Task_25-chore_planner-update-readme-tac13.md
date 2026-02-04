# Chore: Update main README with TAC-13 features

## Metadata
issue_number: `587`
adw_id: `chore_Tac_13_Task_25`
issue_json: `{"number": 587, "title": "[TAC-13] Task 25: Update main README with TAC-13 features", "body": "**Workflow Metadata:**\n```\n/chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_13_Task_25\n```\n\n**Description:**\nAdd TAC-13 reference to main tac_bootstrap README.\n\n**Technical Steps:**\n1. Open `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/README.md`\n2. Update feature list to include:\n   ```markdown\n   - **Agent Experts (TAC-13)**: Self-improving agents with expertise files\n   ```\n3. Add to `.claude/commands/` description:\n   ```markdown\n   - **Agent Experts**: Self-improving domain experts with mental models\n   ```\n4. Update course reference section to mention TAC-13\n\n**Acceptance Criteria:**\n- TAC-13 is clearly mentioned\n- Links to documentation are correct\n- Integrates with existing content\n\n**Impacted Paths:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/README.md`\n"}`

## Chore Description
Update the main README.md file in the tac_bootstrap repository to document the TAC-13 Agent Experts feature. This includes adding TAC-13 to the feature list, updating command descriptions, and adding a reference in the TAC course table.

TAC-13 introduces the Agent Experts framework - self-improving agents that build and evolve expertise files through an ACT → LEARN → REUSE loop. The documentation should reflect this capability as a core feature of the agentic layer.

## Relevant Files
Files needed to complete this chore:

- **README.md** - Main repository README at `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/README.md`
  - Currently documents TAC-1 through TAC-12 features
  - Contains a "TAC Bootstrap generates automatically" section describing the agentic layer structure
  - Has a "Referencia: Curso TAC" table mapping TAC lessons (1-8) to implementations
  - Needs TAC-13 additions in multiple strategic locations

- **ai_docs/doc/** - TAC-13 documentation for reference
  - Contains TAC-13 implementation details and patterns
  - Used to ensure accurate descriptions

### New Files
No new files required - this is documentation update only.

## Step by Step Tasks

### Task 1: Add TAC-13 to Agentic Layer Structure Description
In the "Solucion" section where the project structure is shown, add documentation for the `.claude/commands/experts/` directory:
```markdown
├── .claude/                    # Configuracion Claude Code
│   ├── settings.json           # Permisos y hooks
│   ├── commands/               # 25+ comandos slash
│   │   ├── prime.md            # Priming del agente
│   │   ├── feature.md          # Planificacion features
│   │   ├── implement.md        # Ejecucion de planes
│   │   ├── experts/            # Agent Experts (TAC-13)
│   │   └── ...
```

Add a brief note explaining the experts directory:
```markdown
- **Agent Experts**: Self-improving domain experts with expertise files
```

### Task 2: Update TAC-12 Integration Section with TAC-13
Add TAC-13 to the "TAC-12 Integration" section as a fourth pillar:

```markdown
**Agent Experts (TAC-13)** - Self-improving agents that evolve domain-specific mental models through an ACT → LEARN → REUSE loop. Expert agents maintain expertise files (max 1000 lines YAML) that capture patterns, decisions, and institutional knowledge for high-risk domains like security, billing, and complex architectures.
```

### Task 3: Add TAC-13 Entry to Course Reference Table
Update the "Referencia: Curso TAC" table to include TAC-13:

```markdown
| TAC-13 | Agent Experts | .claude/commands/experts/ |
```

Add this row after TAC-8 (or in proper numerical order if TAC-9 through TAC-12 are already documented).

### Task 4: Validate All Changes
- Ensure TAC-13 is mentioned in at least 3 locations in the README
- Verify that all paths are correct and consistent with the repository structure
- Confirm Markdown formatting is valid
- Check that the descriptions accurately reflect TAC-13's ACT → LEARN → REUSE pattern
- Ensure links to documentation are correct (if any are added)

### Task 5: Execute Validation Commands
Run validation commands to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- TAC-13 is part of the ongoing effort to document advanced agentic capabilities
- The Agent Experts framework is already implemented in `.claude/commands/experts/` in the repo
- This task focuses on making TAC-13 discoverable and understandable from the main README
- Keep descriptions concise but accurate - focus on the ACT → LEARN → REUSE loop concept
- This is purely documentation work - no code changes required
