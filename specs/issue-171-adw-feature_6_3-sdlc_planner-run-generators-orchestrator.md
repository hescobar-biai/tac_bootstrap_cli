# Feature: Documentation Generators Orchestration Script Template

## Metadata
issue_number: `171`
adw_id: `feature_6_3`
issue_json: `{"number":171,"title":"Tarea 6.3: Template run_generators.sh","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_6_3\n\n**Tipo**: feature\n**Ganancia**: Script orquestador que ejecuta los generadores en orden correcto con checks de seguridad (git dirty, paths validos).\n\n**Instrucciones para el agente**:\n\n1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/scripts/run_generators.sh.j2`\n2. Crear renderizado en raiz: `scripts/run_generators.sh` (con permisos de ejecucion)\n2. Contenido del script generado:\n   ```bash\n   #!/usr/bin/env bash\n   set -euo pipefail\n\n   # Configuracion\n   REPO_ROOT=\"{{ config.paths.app_root | default('.') }}\"\n   SCRIPTS_DIR=\"$(dirname \"$0\")\"\n   DOCS_DIR=\"docs\"\n\n   # Preflight checks\n   command -v python3 >/dev/null || { echo \"Error: python3 required\"; exit 1; }\n   command -v uv >/dev/null || { echo \"Error: uv required\"; exit 1; }\n\n   # Parse flags\n   DRY_RUN=\"\"\n   CHANGED_ONLY=\"\"\n   for arg in \"$@\"; do\n       case $arg in\n           --dry-run) DRY_RUN=\"--dry-run\" ;;\n           --changed-only) CHANGED_ONLY=\"--changed-only\" ;;\n       esac\n   done\n\n   # Step 1: Generate/update docstrings\n   echo \"=== Step 1: Enriching docstrings ===\"\n   uv run \"$SCRIPTS_DIR/gen_docstring_jsdocs.py\" \\\n       --root \"$REPO_ROOT\" \\\n       --mode complement \\\n       --languages {{ config.project.language }} \\\n       $CHANGED_ONLY $DRY_RUN\n\n   # Step 2: Generate fractal docs\n   echo \"=== Step 2: Generating fractal documentation ===\"\n   uv run \"$SCRIPTS_DIR/gen_docs_fractal.py\" \\\n       --repo . \\\n       --docs-root \"$DOCS_DIR\" \\\n       --include-root \"$REPO_ROOT\" \\\n       --mode complement \\\n       $DRY_RUN\n\n   echo \"=== Done ===\"\n   ```\n3. El script debe ser ejecutable (chmod +x en scaffold)\n\n**Criterios de aceptacion**:\n- Template renderiza bash valido\n- Script falla limpiamente si faltan dependencias\n- --dry-run se propaga a ambos generadores\n- --changed-only se propaga al generador de docstrings\nFASE 6: Documentacion Fractal como Skill\n\n**Objetivo**: Incluir los generadores de documentacion fractal como parte de los proyectos generados, con slash command para invocacion facil.\n\n**Ganancia de la fase**: Proyectos generados incluyen herramientas de documentacion automatica que mantienen docs sincronizados con el codigo, usando LLM local o remoto.\n\n---\n"}`

## Feature Description
This feature creates a Bash script template that orchestrates the execution of two documentation generators in the correct sequence: `gen_docstring_jsdocs.py` (enriches inline documentation) followed by `gen_docs_fractal.py` (generates folder-level fractal docs). The script includes preflight checks, validates dependencies, propagates command-line flags, and fails fast with clear error messages.

The orchestrator script ensures that:
1. Required dependencies (python3, uv) are available
2. Generator scripts exist before attempting execution
3. The REPO_ROOT directory exists
4. The DOCS_DIR is created if missing
5. Flags like `--dry-run` and `--changed-only` are correctly passed to generators
6. Each generator completes successfully before proceeding to the next (fail-fast with `set -e`)

## User Story
As a developer using a TAC Bootstrap-generated project
I want a single script that orchestrates all documentation generators
So that I can update both inline docstrings and fractal folder docs with one command, with flags for dry-run testing and incremental updates

## Problem Statement
Projects with multiple documentation generators face several challenges:
- Developers must manually run multiple scripts in the correct order
- Flag propagation across scripts is error-prone (forgetting `--dry-run` on one script)
- No validation that dependencies (python3, uv) are installed before execution
- No validation that generator scripts exist before attempting execution
- Partial execution when one generator fails can leave docs in inconsistent state
- Path validation is duplicated across scripts
- Users must remember the correct sequence and flags for each generator

The project needs a single orchestration script that:
- Runs generators in the correct dependency order
- Validates all preconditions before starting
- Propagates flags consistently across generators
- Fails fast with helpful error messages
- Is simple enough for users to understand and customize

## Solution Statement
Create a Jinja2 template (`run_generators.sh.j2`) that renders a Bash orchestration script. The template will:

1. **Use fail-fast mode** (`set -euo pipefail`) to stop on first error
2. **Define configuration variables** from Jinja2 config (REPO_ROOT, SCRIPTS_DIR, DOCS_DIR)
3. **Validate dependencies** (python3, uv) with clear error messages
4. **Validate script existence** for both generators before execution
5. **Validate REPO_ROOT** exists, create DOCS_DIR if missing
6. **Parse command-line flags** (`--dry-run`, `--changed-only`, `--help`)
7. **Handle language configuration defensively** with Jinja2 filters (default to 'python', join lists)
8. **Execute generators in sequence**:
   - Step 1: gen_docstring_jsdocs.py (enriches inline docs)
   - Step 2: gen_docs_fractal.py (generates folder docs from enriched sources)
9. **Propagate flags appropriately**:
   - `--dry-run` → both generators
   - `--changed-only` → docstring generator only (fractal doesn't support it)
10. **Provide minimal help** with `--help` flag
11. **Report progress** with simple echo statements for each step

The template will render to `scripts/run_generators.sh` in generated projects. File permissions (chmod +x) will be handled by future CLI renderer logic.

## Relevant Files

### Similar Script Templates
- `tac_bootstrap_cli/tac_bootstrap/templates/scripts/build.sh.j2` - Example Bash script template with `set -e` and dependency detection
- `tac_bootstrap_cli/tac_bootstrap/templates/scripts/gen_docstring_jsdocs.py.j2` - First generator in pipeline
- `tac_bootstrap_cli/tac_bootstrap/templates/scripts/gen_docs_fractal.py.j2` - Second generator in pipeline

### TAC Bootstrap Infrastructure
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - TACConfig model with paths.app_root, project.language
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Jinja2 rendering service
- `config.yml` - Configuration source (paths.app_root defaults to 'tac_bootstrap_cli', project.language is 'python')

### Existing Scripts for Reference
- `scripts/build.sh` - Shows fail-fast pattern and dependency checking
- `scripts/gen_docstring_jsdocs.py` - Generator 1, supports `--dry-run`, `--changed-only`, `--languages`, `--root`, `--mode`
- `scripts/gen_docs_fractal.py` - Generator 2, supports `--dry-run`, `--repo`, `--docs-root`, `--include-root`, `--mode`

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/scripts/run_generators.sh.j2` - New Jinja2 template
- `scripts/run_generators.sh` - Rendered output in project root (for validation)

## Implementation Plan

### Phase 1: Template Structure & Validation
Create the Jinja2 template with defensive configuration and preflight checks.

1. Create file `tac_bootstrap_cli/tac_bootstrap/templates/scripts/run_generators.sh.j2`
2. Add shebang and fail-fast settings: `#!/usr/bin/env bash` and `set -euo pipefail`
3. Define configuration variables with defensive Jinja2 filters:
   ```bash
   REPO_ROOT="{{ config.paths.app_root | default('.') }}"
   SCRIPTS_DIR="$(dirname "$0")"
   DOCS_DIR="docs"
   ```
4. Add dependency validation (python3, uv) with clear error messages
5. Add generator script existence checks before execution
6. Add REPO_ROOT existence check, create DOCS_DIR if missing

### Phase 2: Flag Parsing & Help
Implement command-line argument parsing with minimal help text.

1. Initialize flag variables (`DRY_RUN=""`, `CHANGED_ONLY=""`)
2. Add `--help` handler that prints usage and exits
3. Parse `--dry-run` and `--changed-only` flags in loop
4. Handle unknown flags gracefully (ignore or warn)

### Phase 3: Generator Execution Pipeline
Orchestrate the two generators in correct sequence with flag propagation.

1. Add Step 1: gen_docstring_jsdocs.py with progress echo
2. Handle `config.project.language` defensively with Jinja2:
   ```jinja2
   {% if config.project.language is iterable and config.project.language is not string %}
   --languages {{ config.project.language | join(' ') }} \
   {% else %}
   --languages {{ config.project.language | default('python') }} \
   {% endif %}
   ```
3. Propagate `$CHANGED_ONLY` and `$DRY_RUN` to Step 1
4. Add Step 2: gen_docs_fractal.py with progress echo
5. Propagate only `$DRY_RUN` to Step 2 (doesn't support --changed-only)
6. Add final "=== Done ===" echo

### Phase 4: Rendered Example & Testing
Create rendered example in `scripts/` directory and validate it works.

1. Render template manually to `scripts/run_generators.sh` using current config.yml
2. Mark as executable conceptually (future CLI will handle chmod +x)
3. Validate template syntax with shellcheck if available
4. Test dry-run mode: `bash scripts/run_generators.sh --dry-run`
5. Test help flag: `bash scripts/run_generators.sh --help`
6. Verify preflight checks fail appropriately (rename uv temporarily)

## Step by Step Tasks

### Task 1: Create template directory structure
- Verify `tac_bootstrap_cli/tac_bootstrap/templates/scripts/` directory exists
- Create directory if missing

### Task 2: Create run_generators.sh.j2 template
- Create file `tac_bootstrap_cli/tac_bootstrap/templates/scripts/run_generators.sh.j2`
- Add shebang: `#!/usr/bin/env bash`
- Add fail-fast settings: `set -euo pipefail`
- Add header comment describing the script's purpose

### Task 3: Add configuration section
- Define `REPO_ROOT` variable using `{{ config.paths.app_root | default('.') }}`
- Define `SCRIPTS_DIR` using `$(dirname "$0")`
- Define `DOCS_DIR` as `docs`
- Add comment explaining each configuration variable

### Task 4: Implement preflight checks
- Check `python3` is available with `command -v python3 >/dev/null`
- Check `uv` is available with `command -v uv >/dev/null`
- Check generator scripts exist:
  ```bash
  [ -f "$SCRIPTS_DIR/gen_docstring_jsdocs.py" ] || { echo "Error: gen_docstring_jsdocs.py not found"; exit 1; }
  [ -f "$SCRIPTS_DIR/gen_docs_fractal.py" ] || { echo "Error: gen_docs_fractal.py not found"; exit 1; }
  ```
- Validate REPO_ROOT directory exists: `[ -d "$REPO_ROOT" ] || { echo "Error: REPO_ROOT not found"; exit 1; }`
- Create DOCS_DIR if missing: `mkdir -p "$DOCS_DIR"`

### Task 5: Add help flag handler
- Add `--help` flag that prints:
  ```
  Usage: run_generators.sh [OPTIONS]

  Options:
    --dry-run       Show what would be done without making changes
    --changed-only  Only process files changed since last commit (docstrings only)
    --help          Show this help message
  ```
- Exit with code 0 after printing help

### Task 6: Implement flag parsing
- Initialize `DRY_RUN=""` and `CHANGED_ONLY=""`
- Parse arguments in for loop:
  ```bash
  for arg in "$@"; do
      case $arg in
          --dry-run) DRY_RUN="--dry-run" ;;
          --changed-only) CHANGED_ONLY="--changed-only" ;;
          --help) show_help; exit 0 ;;
      esac
  done
  ```

### Task 7: Add Step 1 - Docstring generator
- Add progress echo: `echo "=== Step 1: Enriching docstrings ==="`
- Build uv run command for gen_docstring_jsdocs.py with:
  - `--root "$REPO_ROOT"`
  - `--mode complement`
  - `--languages` with defensive Jinja2 handling of list vs string
  - `$CHANGED_ONLY $DRY_RUN` flags

### Task 8: Add Step 2 - Fractal docs generator
- Add progress echo: `echo "=== Step 2: Generating fractal documentation ==="`
- Build uv run command for gen_docs_fractal.py with:
  - `--repo .`
  - `--docs-root "$DOCS_DIR"`
  - `--include-root "$REPO_ROOT"`
  - `--mode complement`
  - `$DRY_RUN` flag only (no --changed-only)

### Task 9: Add completion message
- Add final echo: `echo "=== Done ==="`

### Task 10: Create rendered example
- Render template to `scripts/run_generators.sh` using current config.yml values
- Use consistent formatting with existing scripts in scripts/
- Add note that file permissions will be handled by future CLI

### Task 11: Validate template rendering
- Verify rendered script has valid Bash syntax (manual inspection or shellcheck)
- Check that Jinja2 variables are properly substituted
- Verify no template syntax errors remain in output

### Task 12: Test help flag
- Run `bash scripts/run_generators.sh --help`
- Verify help message displays correctly

### Task 13: Test dry-run mode
- Run `bash scripts/run_generators.sh --dry-run`
- Verify it passes --dry-run to both generators
- Verify no files are modified

### Task 14: Test preflight validation
- Test missing python3 scenario (if safe)
- Test missing uv scenario (if safe)
- Verify error messages are clear and actionable

### Task 15: Run validation commands
- Execute all validation commands to ensure zero regressions
- Verify template is properly integrated
- Check for any linting or type errors

## Testing Strategy

### Unit Tests
Not applicable - this is a Bash script template. Testing focuses on manual validation and integration testing.

### Integration Tests
1. **Template rendering**: Verify template renders without Jinja2 errors
2. **Syntax validation**: Run shellcheck on rendered script if available
3. **Dependency checks**: Verify preflight checks fail when dependencies missing
4. **Flag propagation**: Verify flags are passed correctly to both generators
5. **Dry-run mode**: Verify --dry-run prevents file modifications
6. **Help flag**: Verify --help displays usage and exits cleanly
7. **Sequential execution**: Verify Step 2 only runs if Step 1 succeeds

### Edge Cases
1. **Missing REPO_ROOT**: Script should fail with clear error
2. **Missing generator scripts**: Script should fail before attempting execution
3. **Language as list**: Template should join with spaces
4. **Language undefined**: Template should default to 'python'
5. **Unknown flags**: Script should ignore or warn gracefully
6. **DOCS_DIR missing**: Script should create it automatically
7. **Generator failure**: Script should stop (fail-fast) and not continue to next step

## Acceptance Criteria
1. Template file exists at `tac_bootstrap_cli/tac_bootstrap/templates/scripts/run_generators.sh.j2`
2. Rendered example exists at `scripts/run_generators.sh`
3. Template renders valid Bash (no Jinja2 errors, passes shellcheck)
4. Script fails cleanly if python3 or uv are not installed
5. Script validates generator scripts exist before attempting execution
6. Script validates REPO_ROOT exists and creates DOCS_DIR if missing
7. `--dry-run` flag propagates to both generators
8. `--changed-only` flag propagates only to gen_docstring_jsdocs.py
9. `--help` flag displays usage and exits
10. Script uses `set -euo pipefail` for fail-fast behavior
11. Language configuration handles both string and list values with defensive defaults
12. Progress echoes clearly indicate which step is running
13. Script stops on first generator failure (does not continue to next step)

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `bash scripts/run_generators.sh --help` - Help flag test
- `bash scripts/run_generators.sh --dry-run` - Dry-run smoke test (requires .env with OPENAI_API_KEY)
- `shellcheck scripts/run_generators.sh` - Shell syntax validation (if shellcheck available)

## Notes

### Design Decisions
1. **No git dirty checks**: Omitted per clarifications - generators have --dry-run for safety
2. **Fail-fast with set -e**: Stops on first generator failure for clean error handling
3. **Simple progress output**: Basic echo statements, no verbose mode for MVP
4. **Defensive language handling**: Jinja2 filters handle list/string/undefined cases
5. **Create DOCS_DIR automatically**: Standard behavior for documentation tools
6. **File permissions handled elsewhere**: Future CLI renderer will set executable bit

### Future Enhancements
1. Add `--verbose` flag for detailed logging
2. Add `--skip-docstrings` or `--skip-fractal` flags for selective execution
3. Add timing information for each step
4. Add git dirty check with `--force` override
5. Add support for custom DOCS_DIR location via flag
6. Add validation of OPENAI_API_KEY before running generators
7. Add support for parallel execution (background jobs) if generators are independent

### Dependencies
- Requires bash (standard on macOS/Linux)
- Requires python3 and uv (validated in preflight)
- Requires generator scripts exist (validated before execution)
- Requires .env with OPENAI_API_KEY for actual documentation generation
