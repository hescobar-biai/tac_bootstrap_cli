# Feature: Integrate Fractal Docs in Documentation Workflow

## Metadata
issue_number: `185`
adw_id: `feature_7_2`
issue_json: `{"number":185,"title":"Tarea 7.2: Integrar fractal docs en adw_document_iso.py","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_7_2\n\n**Tipo**: feature\n**Ganancia**: El workflow automatizado de documentacion (ADW) tambien actualiza los docs fractal, manteniendo ambos tipos de docs sincronizados con cada cambio.\n\n**Instrucciones para el agente**:\n\n1. Modificar template: `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_document_iso.py.j2`\n2. Actualizar renderizado en raiz: `adws/adw_document_iso.py`\n2. En la funcion `generate_documentation()`, despues de ejecutar `/document`, agregar:\n   ```python\n   # Step 2: Update fractal documentation for changed files\n   logger.info(\"Updating fractal documentation...\")\n   fractal_result = execute_template(\n       AgentTemplateRequest(\n           command=\"generate_fractal_docs\",\n           args=[\"changed\"],\n           ...\n       )\n   )\n   if fractal_result.success:\n       logger.info(\"Fractal documentation updated successfully\")\n   else:\n       logger.warning(f\"Fractal docs update failed (non-blocking): {fractal_result.error}\")\n   ```\n3. La actualizacion de docs fractal debe ser **non-blocking**: si falla, logea warning pero no falla el workflow completo\n4. Agregar los archivos generados en `docs/` al commit de documentacion\n\n**Criterios de aceptacion**:\n- Template renderiza correctamente\n- Fractal docs se actualizan despues de feature docs\n- Fallo en fractal docs no bloquea el workflow\n- Archivos en docs/ se incluyen en el commit\n\n# FASE 7: Document Workflow Mejorado\n\n**Objetivo**: Mejorar el template existente de /document para incluir frontmatter IDK y integracion con docs fractal.\n\n**Ganancia de la fase**: La documentacion de features generada automaticamente es mas rica, consistente, y encontrable por agentes AI.\n"}`

## Feature Description
This feature enhances the automated documentation workflow (ADW Document Iso) by integrating fractal documentation generation. Currently, the workflow only generates feature-level documentation using the `/document` slash command. After this enhancement, the workflow will also automatically update the fractal documentation tree for all changed files, keeping both documentation types in sync with code changes.

Fractal documentation provides a hierarchical, module-level view of the codebase with IDK (I Don't Know) keywords that help AI agents discover and navigate code. By integrating it into the ADW workflow, every code change will automatically update both:
1. Feature-level documentation (existing `/document` behavior)
2. Module-level fractal documentation (new `/generate_fractal_docs` integration)

## User Story
As a developer using TAC Bootstrap's ADW workflows
I want the documentation workflow to automatically update fractal docs alongside feature docs
So that both types of documentation stay synchronized with code changes without manual intervention

## Problem Statement
The current `adw_document_iso.py` workflow only generates feature-level documentation using the `/document` slash command. When developers make code changes, the fractal documentation tree (which provides module-level overviews and IDK keywords for AI discoverability) becomes outdated. This requires manual execution of `/generate_fractal_docs` to keep the fractal docs in sync, creating an inconsistent documentation experience.

Additionally, the workflow template (`adw_document_iso.py.j2`) used to generate documentation workflows for new projects needs to be updated so that newly generated projects also benefit from this integrated approach.

## Solution Statement
Enhance the `generate_documentation()` function in both the template file and the working file to include a second step that executes `/generate_fractal_docs` with the `changed` scope after successful feature documentation generation. This integration will:

1. Execute the existing `/document` command (Step 1)
2. Validate the documentation file was created
3. Execute `/generate_fractal_docs` with `args=['changed']` (Step 2)
4. Use try-except to make fractal docs non-blocking (log warnings on failure)
5. Include all generated `docs/` files in the existing commit workflow

The existing `git add -A` in `commit_changes()` will automatically stage the fractal docs files, requiring no additional staging logic.

## Relevant Files
Files necessary for implementing the feature:

- `adws/adw_document_iso.py` - The active documentation workflow used in this project
  - Contains `generate_documentation()` function that needs enhancement (lines 100-184)
  - Already has required imports: `execute_template` and `AgentTemplateRequest`

- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_document_iso.py.j2` - Template for generating documentation workflows in new projects
  - Currently does not exist in the file system (needs to be checked)
  - Must mirror the changes made to `adw_document_iso.py`

- `.claude/commands/generate_fractal_docs.md` - The slash command specification
  - Defines the `changed` argument behavior
  - Documents expected output and error handling

- `adws/adw_modules/data_types.py` - Data models
  - Contains `AgentTemplateRequest` (lines 172-181) and `AgentPromptResponse` (lines 163-169)
  - Defines the `success: bool` field used for checking results

- `adws/adw_modules/git_ops.py` - Git operations
  - Contains `commit_changes()` which uses `git add -A` for staging

### New Files
No new files will be created. This is an enhancement to existing files.

## Implementation Plan

### Phase 1: Understand Current Implementation
- Read and analyze the current `generate_documentation()` function in `adws/adw_document_iso.py`
- Verify the template file location and structure in `tac_bootstrap_cli/tac_bootstrap/templates/adws/`
- Review how `execute_template()` and `AgentTemplateRequest` are used in the codebase
- Understand the commit workflow to confirm `git add -A` behavior

### Phase 2: Core Implementation
- Add fractal docs integration to `adws/adw_document_iso.py`
  - Insert code after successful documentation validation (after line ~158)
  - Wrap in try-except for non-blocking behavior
  - Use proper logging for success/warning/error cases
- Mirror identical changes to template file `adw_document_iso.py.j2`

### Phase 3: Integration Testing
- Test the updated workflow on a sample change
- Verify both feature docs and fractal docs are generated
- Confirm fractal docs failure doesn't block the workflow
- Validate that both doc types are included in the commit

## Step by Step Tasks

### Task 1: Analyze Current Implementation
- Read `adws/adw_document_iso.py` focusing on the `generate_documentation()` function
- Read `adws/adw_modules/agent.py` to understand `execute_template()` signature and behavior
- Read `.claude/commands/generate_fractal_docs.md` to understand the slash command interface
- Verify the template file exists at `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_document_iso.py.j2`

### Task 2: Implement Fractal Docs Integration in Working File
- Edit `adws/adw_document_iso.py`
- In the `generate_documentation()` function, after the documentation file validation (after line 158, before the return statement on line 160):
  - Add Step 2 comment: `# Step 2: Update fractal documentation for changed files`
  - Wrap fractal docs execution in try-except block
  - Log info message: "Updating fractal documentation..."
  - Create `AgentTemplateRequest` with:
    - `agent_name='fractal_docs_generator'`
    - `slash_command='/generate_fractal_docs'`
    - `args=['changed']`
    - `adw_id=adw_id`
    - `working_dir=working_dir`
  - Execute using `execute_template()`
  - Check `fractal_result.success` and log appropriate message
  - On exception, log warning but continue execution

### Task 3: Update Template File
- Verify that `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_document_iso.py.j2` exists
- Apply identical changes to the template file as were made to the working file
- Ensure Jinja2 syntax is preserved (if any templating exists in that section)

### Task 4: Manual Testing
- Create a test scenario with code changes
- Run the updated `adw_document_iso.py` workflow
- Verify both documentation types are generated:
  - Feature documentation in `app_docs/`
  - Fractal documentation in `docs/`
- Check logs to confirm fractal docs step executed
- Verify both doc types are included in the git commit

### Task 5: Test Error Handling
- Simulate a fractal docs failure (e.g., temporarily rename `scripts/run_generators.sh`)
- Run the workflow again
- Verify that:
  - A warning is logged for fractal docs failure
  - The workflow continues and completes successfully
  - Feature docs are still committed
  - The workflow does not exit with error

### Task 6: Validation
Execute all validation commands to ensure zero regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- `cd tac_bootstrap_cli && uv run ruff check .`
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests
No new unit tests are required for this feature because:
1. The change is in an ADW workflow script, not in the CLI codebase
2. The integration point (`execute_template()`) is already tested
3. The workflow is integration-level code that would require full environment setup to test

### Manual Testing Scenarios
1. **Happy Path**:
   - Make code changes in the worktree
   - Run `adw_document_iso.py`
   - Verify both `app_docs/` and `docs/` contain updated documentation
   - Verify both are committed together

2. **Fractal Docs Failure**:
   - Temporarily break the fractal docs generator
   - Run workflow
   - Verify warning is logged and workflow completes
   - Verify feature docs are still committed

3. **No Changes**:
   - Run workflow with no git changes
   - Verify early exit (existing behavior)
   - Verify fractal docs step is skipped

### Edge Cases
- **Empty `docs/` directory**: Fractal docs generator creates it if needed
- **Fractal docs script not found**: Logged as warning, workflow continues
- **Working directory is None**: `execute_template()` handles this correctly (defaults to current dir)
- **Both documentation types unchanged**: Commit workflow handles empty commits gracefully

## Acceptance Criteria
1. ✅ Template file `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_document_iso.py.j2` is updated with fractal docs integration
2. ✅ Working file `adws/adw_document_iso.py` is updated with fractal docs integration
3. ✅ Fractal docs generation executes AFTER feature documentation generation and validation
4. ✅ Fractal docs uses `args=['changed']` to only update docs for changed files
5. ✅ Fractal docs execution is wrapped in try-except for non-blocking behavior
6. ✅ Success log message appears when fractal docs succeed
7. ✅ Warning log message appears when fractal docs fail (not error)
8. ✅ Workflow does NOT exit on fractal docs failure
9. ✅ Files in `docs/` are automatically included in the documentation commit (via existing `git add -A`)
10. ✅ Manual testing confirms both doc types are generated and committed together

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests (should have no failures)
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting (should have no errors)
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type checking (should pass)
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test (should display help)

## Notes

### Implementation Details
- The logger parameter is already available in `generate_documentation()` - no import needed
- `AgentTemplateRequest` and `execute_template` are already imported - no new imports needed
- The `args=['changed']` literal string is passed directly to the slash command
- The slash command implementation interprets 'changed' as "analyze git changes and document affected files"

### Design Decisions
- **Non-blocking execution**: Fractal docs are supplementary to feature docs, so failure shouldn't block the workflow
- **Try-except wrapper**: Provides defense-in-depth against unexpected errors in the template execution
- **No explicit staging**: The existing `git add -A` automatically includes all changes
- **Same commit**: Keeps related documentation atomic and avoids polluting git history

### Future Enhancements
- Add telemetry to track fractal docs generation success/failure rates
- Consider adding a configuration option to disable fractal docs integration
- Explore incremental fractal docs generation for large repositories
