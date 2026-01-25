# Feature: Slash Command /generate_fractal_docs

## Metadata
issue_number: `179`
adw_id: `feature_6_4`
issue_json: `{"number":179,"title":"Tarea 6.4: Slash command /generate_fractal_docs","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_6_4\n\n**Tipo**: feature\n**Ganancia**: Los usuarios pueden invocar la generacion de docs fractal como slash command de Claude Code, integrandolo en su workflow de desarrollo.\n\n**Instrucciones para el agente**:\n\n1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/generate_fractal_docs.md.j2`\n2. Crear renderizado en raiz: `.claude/commands/generate_fractal_docs.md`\n2. Contenido del command:\n   ```markdown\n   # Generate Fractal Documentation\n\n   Generate or update the fractal documentation tree for this project.\n\n   ## Arguments\n   - $SCOPE: Scope of generation. Options: \"full\" (all files), \"changed\" (only git-changed files). Default: \"changed\"\n\n   ## Instructions\n\n   1. Run the fractal documentation generator:\n      ```bash\n      {% if SCOPE == \"full\" %}\n      bash scripts/run_generators.sh\n      {% else %}\n      bash scripts/run_generators.sh --changed-only\n      {% endif %}\n      ```\n\n   2. Review the generated documentation in `docs/` directory\n\n   3. If new files were created, verify:\n      - Frontmatter has valid YAML\n      - IDK keywords are relevant to the module\n      - Overview section accurately describes the folder contents\n\n   4. Commit the documentation changes:\n      ```bash\n      git add docs/ && git commit -m \"docs: update fractal documentation\"\n      ```\n\n   ## Expected Output\n   - Updated/created markdown files in `docs/` directory\n   - One file per folder in `{{ config.paths.app_root | default(\"src\") }}/`\n   - Each file has frontmatter with IDK keywords and structured body sections\n   ```\n\n**Criterios de aceptacion**:\n- Template renderiza markdown valido\n- Comando es invocable como `/generate_fractal_docs` en Claude Code\n- Soporta argumento SCOPE (full/changed)\nFASE 6: Documentacion Fractal como Skill\n\n**Objetivo**: Incluir los generadores de documentacion fractal como parte de los proyectos generados, con slash command para invocacion facil.\n\n**Ganancia de la fase**: Proyectos generados incluyen herramientas de documentacion automatica que mantienen docs sincronizados con el codigo, usando LLM local o remoto.\n\n---\n"}`

## Feature Description
This feature creates a Claude Code slash command template (`/generate_fractal_docs`) that allows developers to invoke fractal documentation generation directly from their development workflow. The command acts as a thin, defensive wrapper around the `scripts/run_generators.sh` orchestrator script created in Task 6.3.

The command provides:
1. Simple invocation: `/generate_fractal_docs` or `/generate_fractal_docs full`
2. Prerequisite validation: Checks that `scripts/run_generators.sh` exists
3. Error handling: Only proceeds to review/commit steps if generation succeeds
4. Intelligent commit behavior: Only prompts to commit if changes were actually made
5. User guidance: Clear instructions and helpful error messages

The command integrates seamlessly into Claude Code's workflow, making documentation generation as easy as typing a slash command.

## User Story
As a developer using a TAC Bootstrap-generated project
I want to generate/update fractal documentation with a slash command
So that I can keep docs synchronized with code changes without leaving my Claude Code workflow

## Problem Statement
Developers using TAC Bootstrap-generated projects need to:
- Remember the exact path and flags for the documentation orchestrator script
- Manually check if the script exists before running it
- Remember to review generated documentation for correctness
- Decide whether to commit changes (avoiding empty commits)
- Context-switch out of their Claude Code workflow to run bash commands

Without a slash command:
- Documentation updates are friction-heavy (requiring bash knowledge)
- Developers forget to update docs because the process is manual
- No guidance on what to verify after generation
- Risk of committing broken documentation if generator fails silently
- Poor integration with Claude Code's conversational workflow

The project needs a slash command that:
- Makes doc generation a single, memorable command
- Validates prerequisites with helpful error messages
- Guides users through the review process
- Only commits when changes actually exist
- Feels native to Claude Code's workflow

## Solution Statement
Create a Jinja2 template (`generate_fractal_docs.md.j2`) that renders a Claude Code slash command. The command will:

1. **Accept a SCOPE argument** (default: "changed")
   - "changed" → run with `--changed-only` flag (incremental updates)
   - "full" → run without flags (regenerate all docs)

2. **Validate prerequisites** before execution
   - Check that `scripts/run_generators.sh` exists
   - If missing, show helpful error with setup instructions
   - This prevents cryptic bash errors for users

3. **Execute the orchestrator script**
   - Use Jinja2 conditional to pass correct flags based on SCOPE
   - Let the script handle all heavy lifting (dependency checks, git fallback, etc.)

4. **Verify script success** before proceeding
   - Check exit code of run_generators.sh
   - Only proceed to review/commit if generation succeeded
   - Show error output if failed

5. **Guide user through review**
   - Prompt to review generated files in `docs/` directory
   - Instruct to verify frontmatter YAML, IDK keywords, overview accuracy
   - Note that script output shows generation summary

6. **Handle commits intelligently**
   - Check if docs/ has changes with `git diff --quiet docs/`
   - Only prompt to commit if changes exist
   - Inform user "No documentation changes to commit" if nothing changed
   - Use conventional commit message format: `docs: update fractal documentation`

7. **Reference config values** safely
   - Use `{{ config.paths.app_root | default("src") }}` pattern
   - Document expected directory structure

The template will be committed both as:
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/generate_fractal_docs.md.j2` (for generation)
- `.claude/commands/generate_fractal_docs.md` (for use in tac_bootstrap repo itself)

This follows the existing pattern in the repo where templates and rendered versions coexist.

## Relevant Files

### Similar Command Templates
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/test.md.j2` - Example command with bash execution and result handling
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/commit.md.j2` - Example with git operations
- `.claude/commands/test.md` - Rendered version showing actual format

### Related Infrastructure
- `scripts/run_generators.sh` - Orchestrator script that this command wraps (created in Task 6.3)
- `scripts/gen_docstring_jsdocs.py` - First generator in pipeline
- `scripts/gen_docs_fractal.py` - Second generator in pipeline
- `config.yml` - Contains config.paths.app_root value

### TAC Bootstrap CLI
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - TACConfig model
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Template rendering service

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/generate_fractal_docs.md.j2` - Command template
- `.claude/commands/generate_fractal_docs.md` - Rendered command for tac_bootstrap repo

## Implementation Plan

### Phase 1: Template Creation
Create the Jinja2 template with:
- Argument definition (SCOPE parameter)
- Prerequisites validation section
- Conditional bash execution based on SCOPE
- Success checking logic
- Review instructions
- Smart commit logic

### Phase 2: Rendering for TAC Bootstrap Repo
Render the template for the tac_bootstrap repo itself:
- Use actual config values from config.yml
- Create `.claude/commands/generate_fractal_docs.md`
- Verify that SCOPE interpolation works correctly

### Phase 3: Documentation and Testing
- Verify template syntax is valid Jinja2
- Verify rendered markdown is valid
- Verify bash commands are correct
- Test the command manually in Claude Code

## Step by Step Tasks

### Task 1: Create Command Template
Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/generate_fractal_docs.md.j2` with:

1. Header and description:
   ```markdown
   # Generate Fractal Documentation

   Generate or update the fractal documentation tree for this project.
   ```

2. Arguments section:
   ```markdown
   ## Arguments
   - $SCOPE: Scope of generation. Options: "full" (all files), "changed" (only git-changed files). Default: "changed"
   ```

3. Instructions section with prerequisite check:
   ```markdown
   ## Instructions

   1. Verify that the documentation generator script exists:
      ```bash
      if [ ! -f scripts/run_generators.sh ]; then
        echo "Error: scripts/run_generators.sh not found."
        echo "This script should be generated with the TAC Bootstrap Agentic Layer."
        echo "Run: tac-bootstrap init"
        exit 1
      fi
      ```
   ```

4. Execute generator with conditional flags:
   ```markdown
   2. Run the fractal documentation generator:
      ```bash
      {% if SCOPE == "full" %}
      bash scripts/run_generators.sh
      {% else %}
      bash scripts/run_generators.sh --changed-only
      {% endif %}

      if [ $? -ne 0 ]; then
        echo "Error: Documentation generation failed. See output above for details."
        exit 1
      fi
      ```
   ```

5. Review instructions:
   ```markdown
   3. Review the generated documentation:
      - Check the output above for generation summary
      - Examine files in `docs/` directory

   4. If new files were created or existing files were updated, verify:
      - Frontmatter has valid YAML
      - IDK keywords are relevant to the module
      - Overview section accurately describes the folder contents
   ```

6. Smart commit logic:
   ```markdown
   5. Commit the documentation changes (if any):
      ```bash
      if ! git diff --quiet docs/; then
        git add docs/
        git commit -m "docs: update fractal documentation"
        echo "Documentation changes committed."
      else
        echo "No documentation changes to commit."
      fi
      ```
   ```

7. Expected output section:
   ```markdown
   ## Expected Output
   - Updated/created markdown files in `docs/` directory
   - One file per folder in `{{ config.paths.app_root | default("src") }}/`
   - Each file has frontmatter with IDK keywords and structured body sections

   ## Notes
   - The `docs/` directory is created automatically if it doesn't exist
   - If git is not initialized and `--changed-only` is used, the script falls back to full generation
   - Run with `SCOPE=full` to regenerate all documentation from scratch
   ```

### Task 2: Render Command for TAC Bootstrap Repo
Create `.claude/commands/generate_fractal_docs.md`:

1. Read the config.yml to get actual values:
   - config.paths.app_root (should be "tac_bootstrap_cli")
   - Verify what the actual value is

2. Manually render the template with these values:
   - Replace `{{ config.paths.app_root | default("src") }}` with "tac_bootstrap_cli"
   - Replace `{% if SCOPE == "full" %}` with literal Jinja2 (since this is a template for Claude Code, not for Jinja2)
   - Actually, keep the SCOPE conditionals as-is since Claude Code will interpolate them

3. Create the file with proper markdown formatting

### Task 3: Verification and Testing
1. Verify template syntax:
   - Check that Jinja2 syntax is correct
   - Verify that bash syntax is correct
   - Ensure markdown formatting is valid

2. Test the rendered command:
   - Manually invoke `/generate_fractal_docs` in Claude Code
   - Verify it shows the right instructions
   - Check that SCOPE argument works (try both "changed" and "full")

3. Run validation commands (final step)

## Testing Strategy

### Manual Testing
1. **Test prerequisite validation**:
   - Temporarily rename scripts/run_generators.sh
   - Run `/generate_fractal_docs`
   - Verify error message is helpful
   - Rename script back

2. **Test SCOPE argument**:
   - Run `/generate_fractal_docs` (default, should use --changed-only)
   - Run `/generate_fractal_docs full` (should run without flags)
   - Verify correct flags are passed to script

3. **Test success/failure handling**:
   - Verify that failed script execution shows error
   - Verify that successful execution proceeds to review

4. **Test smart commit**:
   - Run when no changes exist → should say "No changes"
   - Make a change, run again → should commit
   - Verify commit message format

### Template Validation
1. Verify Jinja2 syntax is correct
2. Verify bash syntax is correct (shellcheck if available)
3. Verify markdown renders correctly

## Acceptance Criteria
- ✅ Template file exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/generate_fractal_docs.md.j2`
- ✅ Rendered file exists at `.claude/commands/generate_fractal_docs.md`
- ✅ Template renders valid markdown
- ✅ Command is invocable as `/generate_fractal_docs` in Claude Code
- ✅ SCOPE argument works (both "full" and "changed")
- ✅ Prerequisite check validates script existence
- ✅ Error handling prevents committing failed generation
- ✅ Smart commit only commits when changes exist
- ✅ Instructions guide user through review process
- ✅ Uses `config.paths.app_root` with "src" as default
- ✅ Both template and rendered versions are committed to repo

## Validation Commands
Run all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- Manually test `/generate_fractal_docs` command in Claude Code

## Notes

### Design Decisions
1. **Minimal validation in command**: The slash command is a thin wrapper. Complex validation belongs in `run_generators.sh`, not here.

2. **SCOPE default is "changed"**: Most developers want incremental updates. Full regeneration is opt-in.

3. **Git fallback is transparent**: If git isn't initialized, `run_generators.sh` handles fallback to full mode. The command doesn't need to know.

4. **No YAML schema validation**: The generator creates valid YAML. Manual review (step 4) catches issues. Adding schema validation would add complexity without proportional benefit.

5. **Commit both template and rendered**: Follows existing repo pattern. The rendered version makes the command immediately usable in tac_bootstrap repo and serves as reference documentation.

6. **Error messages over silent failures**: Better to fail with clear error than proceed with wrong assumptions.

### Future Enhancements
- Could add a `--dry-run` SCOPE option to preview changes
- Could add output parsing to show file count/summary
- Could integrate with `/document` command for full doc workflow

### Dependencies
- Requires Task 6.3 to be complete (`scripts/run_generators.sh` must exist)
- Requires `scripts/gen_docstring_jsdocs.py` (Task 6.1)
- Requires `scripts/gen_docs_fractal.py` (Task 6.2)
