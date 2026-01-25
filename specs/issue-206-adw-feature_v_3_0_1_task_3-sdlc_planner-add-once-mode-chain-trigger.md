# Feature: Add Once-Mode Execution to Chain Trigger

## Metadata
issue_number: `206`
adw_id: `feature_v_3_0_1_task_3`
issue_json: `{"number":206,"title":"Agregar modo de ejecucion unica (`--once`) en trigger de cadena","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_v_3_0_1_task_3\n\n#### Archivos a modificar\n- **Archivo raiz**: `adws/adw_triggers/trigger_issue_chain.py`\n- **Archivo template**: `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_issue_chain.py.j2`\n\n### Contexto\nSimilar al trigger cron, el trigger de cadena necesita un modo de ejecucion unica para validar rapidamente el orden de issues sin entrar en un bucle infinito.\n\n### Comportamiento actual\n```python\ndef main():\n    args = parse_args()\n    issue_chain = resolve_issue_chain(args)\n    # ... setup ...\n    schedule.every(interval).seconds.do(check_and_process_issues, issue_chain)\n    check_and_process_issues(issue_chain)\n    while not shutdown_requested:\n        schedule.run_pending()\n        time.sleep(1)\n```\n\n### Comportamiento esperado con `--once`\n```python\ndef main():\n    args = parse_args()\n    issue_chain = resolve_issue_chain(args)\n    # ... setup ...\n\n    if args.once:\n        print(\"INFO: Running single chain check cycle (--once mode)\")\n        check_and_process_issues(issue_chain)\n        print(\"INFO: Single cycle complete, exiting\")\n        return\n\n    # Normal loop mode\n    schedule.every(interval).seconds.do(check_and_process_issues, issue_chain)\n    check_and_process_issues(issue_chain)\n    while not shutdown_requested:\n        schedule.run_pending()\n        time.sleep(1)\n```\n\n### Pasos a ejecutar\n1. Abrir `adws/adw_triggers/trigger_issue_chain.py`\n2. En la funcion `parse_args()`, agregar el argumento `--once`:\n   ```python\n   parser.add_argument(\n       \"--once\",\n       action=\"store_true\",\n       default=False,\n       help=\"Run a single chain check cycle and exit (useful for testing)\",\n   )\n   ```\n3. En la funcion `main()`, agregar la logica condicional despues de `resolve_issue_chain(args)`:\n   - Si `args.once` es True: ejecutar `check_and_process_issues(issue_chain)` una vez y retornar\n   - Si `args.once` es False: continuar con el bucle normal\n4. Actualizar el docstring del modulo para incluir ejemplo con `--once`\n5. Replicar los mismos cambios en el archivo template `trigger_issue_chain.py.j2`\n\n### Criterios de aceptacion\n- [ ] El argumento `--once` esta disponible en el parser\n- [ ] `uv run adws/adw_triggers/trigger_issue_chain.py --issues 1,2,3 --once` ejecuta un ciclo y termina\n- [ ] El script verifica el primer issue abierto de la cadena y sale\n- [ ] El modo normal (sin `--once`) sigue funcionando con el bucle infinito\n- [ ] El template `.j2` tiene los mismos cambios\n- [ ] Verificar con:\n  ```bash\n  # Debe ejecutar un ciclo y terminar (usa issues ficticios para test)\n  timeout 10 uv run adws/adw_triggers/trigger_issue_chain.py --issues 1 --once && echo \"SUCCESS: Exited cleanly\"\n\n  # Verificar que el help muestra el nuevo flag\n  uv run adws/adw_triggers/trigger_issue_chain.py --help | grep -A1 \"\\-\\-once\"\n  ```"}`

## Feature Description
Add a `--once` flag to the chain trigger system that executes a single check cycle and exits. This is similar to the existing `--once` mode in the cron trigger (trigger_cron.py) and provides a way to quickly validate issue chain order without entering an infinite loop, making it ideal for testing and debugging.

## User Story
As a developer or CI/CD pipeline
I want to run the chain trigger once without entering an infinite loop
So that I can quickly test and validate the issue chain processing logic without manual interruption

## Problem Statement
The current chain trigger system (trigger_issue_chain.py) only operates in continuous polling mode, running in an infinite loop that checks the issue chain at regular intervals. This makes it difficult to:
- Test the chain trigger behavior quickly
- Validate issue chain configuration without waiting for manual interruption
- Use the trigger in CI/CD pipelines or one-off validation scripts
- Debug issue processing logic efficiently

The cron trigger already has this capability via the `--once` flag, but the chain trigger lacks this testing-friendly feature.

## Solution Statement
Add a `--once` command-line argument to trigger_issue_chain.py that:
1. Accepts the flag in the argument parser with appropriate help text
2. Executes a single check cycle of the issue chain
3. Processes the first open issue in the chain (if any)
4. Exits cleanly after the cycle completes
5. Updates the module docstring to document the new usage pattern
6. Replicates all changes to the Jinja2 template for consistency

This follows the same pattern already established in trigger_cron.py:364-369, ensuring consistency across trigger systems.

## Relevant Files
Files to be modified for this feature:

- `adws/adw_triggers/trigger_issue_chain.py` - Main implementation file that needs the `--once` flag
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_issue_chain.py.j2` - Template file that must mirror the changes

Reference file (for pattern consistency):
- `adws/adw_triggers/trigger_cron.py` - Contains existing `--once` implementation to follow (lines 339-343, 365-369)

### New Files
None. This feature only modifies existing files.

## Implementation Plan

### Phase 1: Foundation
Read and understand the current implementation structure of both trigger_issue_chain.py and trigger_cron.py to ensure the `--once` pattern is correctly replicated.

### Phase 2: Core Implementation
1. Modify the `parse_args()` function in trigger_issue_chain.py to add the `--once` argument
2. Update the `main()` function to handle the `--once` flag with early return logic
3. Update the module docstring to include the `--once` usage example

### Phase 3: Integration
1. Apply identical changes to the Jinja2 template file
2. Validate that both files have consistent implementation
3. Test the behavior with dummy issue numbers

## Step by Step Tasks

### Task 1: Add `--once` argument to parser
- Open `adws/adw_triggers/trigger_issue_chain.py`
- Locate the `parse_args()` function (around line 330)
- Add the `--once` argument after the `--interval` argument:
  ```python
  parser.add_argument(
      "--once",
      action="store_true",
      default=False,
      help="Run a single chain check cycle and exit (useful for testing)",
  )
  ```

### Task 2: Implement once-mode logic in main()
- In the `main()` function (around line 366), after `resolve_issue_chain(args)` and before the schedule setup
- Add conditional logic to check `args.once`
- If True: print info message, call `check_and_process_issues(issue_chain)` once, print completion message, and return
- Keep the existing loop logic in the else path (no explicit else needed, just continues after the if block)
- The pattern should match trigger_cron.py:365-369

### Task 3: Update module docstring
- Update the module docstring at the top of trigger_issue_chain.py (around lines 11-22)
- Add a new usage example line showing the `--once` flag:
  ```python
  """
  Chain-based ADW trigger system that monitors a specific ordered list of issues.

  This script only processes the first open issue in the list. It will not start
  processing issue N+1 until issue N is closed. Each cycle checks for workflow
  commands in the issue body or latest comment, similar to the cron trigger.

  Usage:
      uv run trigger_issue_chain.py 123 456 789
      uv run trigger_issue_chain.py --issues 123,456,789
      uv run trigger_issue_chain.py --issues 123,456,789 --interval 30
      uv run trigger_issue_chain.py --issues 123,456,789 --once
  """
  ```

### Task 4: Replicate changes to Jinja2 template
- Open `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_issue_chain.py.j2`
- Apply the exact same changes as Tasks 1-3 to the template file
- Ensure the Jinja2 template variables (like `{{ config.project.name }}`) are preserved
- Verify that the `--once` argument, main() logic, and docstring updates are all present

### Task 5: Validation and testing
- Run the help command to verify the flag appears:
  ```bash
  uv run adws/adw_triggers/trigger_issue_chain.py --help | grep -A1 "\-\-once"
  ```
- Test with a timeout to ensure clean exit:
  ```bash
  timeout 10 uv run adws/adw_triggers/trigger_issue_chain.py --issues 1 --once && echo "SUCCESS: Exited cleanly"
  ```
- Test normal mode still works (observe it enters the loop):
  ```bash
  timeout 5 uv run adws/adw_triggers/trigger_issue_chain.py --issues 1
  ```
- Verify the script processes issues correctly in once mode by checking console output

## Testing Strategy

### Unit Tests
No new unit tests are required for this feature as it's a simple CLI argument addition. The existing test suite should continue to pass without modifications.

### Manual Testing
1. **Help text validation**: Verify `--help` shows the new `--once` option
2. **Once-mode execution**: Run with `--once` flag and confirm single cycle execution and clean exit
3. **Normal mode regression**: Run without `--once` flag and confirm infinite loop behavior is unchanged
4. **Issue processing**: Verify that once-mode still correctly identifies and processes the first open issue in the chain
5. **Template consistency**: Generate a new project using the CLI and verify the generated trigger_issue_chain.py has the `--once` flag

### Edge Cases
- Running `--once` with no open issues in the chain (should print "All issues in the chain are closed" and exit cleanly)
- Running `--once` with issues not assigned to current user (should skip and exit cleanly)
- Combining `--once` with different `--interval` values (interval should be ignored in once mode)
- Using `--once` with both positional and `--issues` flag arguments

## Acceptance Criteria
- The `--once` argument is available in the argument parser
- Running `uv run adws/adw_triggers/trigger_issue_chain.py --issues 1,2,3 --once` executes a single cycle and exits
- The script checks the first open issue in the chain and exits cleanly
- Normal mode (without `--once`) continues to work with the infinite loop
- The Jinja2 template file has identical changes
- Help text displays the `--once` option with proper description
- Manual validation commands pass successfully
- No regressions in existing chain trigger functionality

## Validation Commands
Execute all commands to validate with zero regressions:

- `uv run adws/adw_triggers/trigger_issue_chain.py --help | grep -A1 "\-\-once"` - Verify help text
- `timeout 10 uv run adws/adw_triggers/trigger_issue_chain.py --issues 1 --once && echo "SUCCESS: Exited cleanly"` - Test once mode
- `timeout 5 uv run adws/adw_triggers/trigger_issue_chain.py --issues 1` - Verify normal mode still loops
- `diff -u <(grep -A5 "def parse_args" adws/adw_triggers/trigger_issue_chain.py | grep -A3 once) <(grep -A5 "def parse_args" tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_issue_chain.py.j2 | grep -A3 once)` - Verify template consistency

## Notes
- This feature follows the exact same pattern as the `--once` implementation in trigger_cron.py (lines 339-343 for parser, lines 365-369 for main logic)
- The implementation is straightforward and requires no new dependencies
- Both the root file and template must be kept in sync to ensure generated projects have the same capability
- The feature is purely additive and does not change existing behavior when the flag is not used
- Consider documenting this flag in any ADW trigger documentation or README files
