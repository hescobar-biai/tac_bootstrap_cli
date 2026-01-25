# Feature: Add Single-Execution Mode (`--once`) to Cron Trigger

## Metadata
issue_number: `205`
adw_id: `feature_v_3_0_1_task_2`
issue_json: `{"number":205,"title":"Agregar modo de ejecucion unica (`--once`) en triggers cron","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_v_3_0_1_task_2\n\n### Archivos a modificar\n- **Archivo raiz**: `adws/adw_triggers/trigger_cron.py`\n- **Archivo template**: `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2`\n\n### Contexto\nEl trigger cron actualmente solo funciona en modo bucle infinito con scheduler. Para pruebas y debugging es necesario poder ejecutar un solo ciclo de verificacion y terminar limpiamente.\n\n### Comportamiento actual\n```python\ndef main():\n    # ... setup ...\n    schedule.every(interval).seconds.do(check_and_process_issues)\n    check_and_process_issues()  # Initial check\n    while not shutdown_requested:\n        schedule.run_pending()\n        time.sleep(1)\n```\n\n### Comportamiento esperado con `--once`\n```python\ndef main(): \n    args = parse_args()\n    # ... setup ...\n\n    if args.once:\n        # Single execution mode\n        print(\"INFO: Running single check cycle (--once mode)\")\n        check_and_process_issues()\n        print(\"INFO: Single cycle complete, exiting\")\n        return\n\n    # Normal loop mode\n    schedule.every(interval).seconds.do(check_and_process_issues)\n    check_and_process_issues()\n    while not shutdown_requested:\n        schedule.run_pending()\n        time.sleep(1)\n```\n\n### Pasos a ejecutar\n1. Abrir `adws/adw_triggers/trigger_cron.py`\n2. En la funcion `parse_args()`, agregar el argumento `--once`:\n   ```python\n   parser.add_argument(\n       \"--once\",\n       action=\"store_true\",\n       default=False,\n       help=\"Run a single check cycle and exit (useful for testing)\",\n   )\n   ```\n3. En la funcion `main()`, agregar la logica condicional:\n   - Si `args.once` es True: ejecutar `check_and_process_issues()` una vez y retornar\n   - Si `args.once` es False: continuar con el bucle normal del scheduler\n4. Actualizar el docstring del modulo para documentar el nuevo flag\n5. Replicar los mismos cambios en el archivo template `trigger_cron.py.j2`\n\n### Criterios de aceptacion\n- [ ] El argumento `--once` esta disponible en el parser\n- [ ] `uv run adws/adw_triggers/trigger_cron.py --once` ejecuta exactamente UN ciclo de verificacion\n- [ ] El script termina con codigo de salida 0 despues del ciclo unico\n- [ ] El modo normal (sin `--once`) sigue funcionando con el bucle infinito\n- [ ] El template `.j2` tiene los mismos cambios\n- [ ] Verificar con:\n  ```bash\n  # Debe ejecutar un ciclo y terminar\n  timeout 10 uv run adws/adw_triggers/trigger_cron.py --once && echo \"SUCCESS: Exited cleanly\"\n\n  # Verificar que el help muestra el nuevo flag\n  uv run adws/adw_triggers/trigger_cron.py --help | grep -A1 \"\\-\\-once\""}`

## Feature Description
The cron trigger currently only operates in an infinite loop mode using the schedule library. This feature adds a `--once` flag that executes a single check cycle for issues and then exits cleanly. This mode is essential for testing, debugging, and CI/CD integration where a single polling cycle is desired without running a persistent daemon.

The implementation will add the `--once` command-line argument to both the source file (`adws/adw_triggers/trigger_cron.py`) and its Jinja2 template counterpart (`tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2`).

## User Story
As a developer or CI/CD pipeline user
I want to run the cron trigger in a single-execution mode
So that I can test the trigger behavior, debug issues, or integrate it into scheduled jobs without running an infinite loop daemon

## Problem Statement
The current cron trigger implementation only supports continuous polling via an infinite loop with the schedule library. This creates challenges for:
1. **Testing**: Developers cannot easily test a single cycle without manually interrupting the process
2. **Debugging**: Debugging requires stopping the infinite loop manually, making it cumbersome
3. **CI/CD Integration**: Continuous integration pipelines need deterministic execution that exits cleanly after one cycle
4. **Development Workflow**: Quick verification of changes requires running a full daemon process

Without a single-execution mode, users must rely on external tools (like `timeout`) or manual interruption (Ctrl+C) to stop the trigger after testing, which is inefficient and error-prone.

## Solution Statement
Add a `--once` command-line flag that modifies the trigger's execution flow to:
1. Skip scheduler initialization entirely (no need to create schedule objects)
2. Execute the `check_and_process_issues()` function exactly once
3. Exit cleanly with code 0 on success (or non-zero on exceptions)
4. Respect existing signal handling (allow Ctrl+C even during single cycle)
5. Maintain identical logging behavior as the normal mode with minimal INFO messages marking entry/exit

The implementation will use early-return pattern in the `main()` function, executing before any scheduler setup occurs. This keeps the code simple, efficient, and maintains separation between the two execution modes.

Both the source file and the Jinja2 template will receive identical modifications to ensure consistency across generated projects.

## Relevant Files
Files necessary for implementing this feature:

- **`adws/adw_triggers/trigger_cron.py`** (lines 316-373)
  - Main implementation file containing `parse_args()` and `main()` functions
  - Needs `--once` argument added to argument parser
  - Needs conditional logic in `main()` for single-execution mode
  - Docstring update to document the new flag

- **`tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2`** (lines 303-357)
  - Jinja2 template version of the trigger used for generating new projects
  - Must receive identical changes as the source file
  - Ensures all generated projects have the `--once` capability

### New Files
No new files are required. This is a modification to existing files only.

## Implementation Plan

### Phase 1: Foundation
1. Read and understand the current implementation of both files
2. Identify the exact insertion points for the new argument and conditional logic
3. Verify the current signal handling setup to ensure compatibility

### Phase 2: Core Implementation
1. Modify `parse_args()` in both files to add the `--once` argument
2. Update the module docstring in both files to document the new flag with usage examples
3. Implement the conditional logic in `main()` for single-execution mode
4. Ensure early return happens before scheduler initialization

### Phase 3: Integration
1. Test the `--once` mode with the validation commands
2. Test the normal mode (without `--once`) to ensure no regressions
3. Verify signal handling works correctly in both modes
4. Confirm help text displays the new flag appropriately

## Step by Step Tasks

### Task 1: Add `--once` argument to source file parser
- Open `adws/adw_triggers/trigger_cron.py`
- Locate the `parse_args()` function (around line 316)
- Add the `--once` argument after the `--interval` argument:
  ```python
  parser.add_argument(
      "--once",
      action="store_true",
      default=False,
      help="Run a single check cycle and exit (useful for testing)",
  )
  ```

### Task 2: Update source file docstring
- Update the module docstring (lines 11-24) to include `--once` in the usage examples:
  ```python
  Usage:
      uv run trigger_cron.py                    # Default 20s interval
      uv run trigger_cron.py --interval 30      # Custom 30s interval
      uv run trigger_cron.py -i 60              # Custom 60s interval
      uv run trigger_cron.py --once             # Single check cycle
  ```

### Task 3: Implement single-execution mode logic in source file
- In the `main()` function (line 340), after signal handlers are set up (line 354-355)
- Before scheduler setup (line 358), add the conditional logic:
  ```python
  # Single execution mode
  if args.once:
      print("INFO: Running single check cycle (--once mode)")
      check_and_process_issues()
      print("INFO: Single cycle complete, exiting")
      return

  # Normal loop mode - schedule and run continuously
  ```

### Task 4: Apply identical changes to Jinja2 template
- Open `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2`
- Repeat Task 1: Add `--once` argument to `parse_args()` (around line 303)
- Repeat Task 2: Update module docstring (lines 11-24)
- Repeat Task 3: Add conditional logic in `main()` (after line 337, before line 341)

### Task 5: Run validation commands
- Execute all validation commands listed below to verify:
  - The `--once` flag appears in help text
  - Single execution mode runs exactly one cycle and exits cleanly
  - Normal mode still functions with infinite loop
  - No regressions in existing behavior

## Testing Strategy

### Unit Tests
No unit tests are required for this feature as it modifies a standalone script. The validation commands provide adequate integration testing.

### Edge Cases
1. **Signal handling during single cycle**: Verify Ctrl+C interrupts cleanly even in `--once` mode
2. **Exception propagation**: Verify exceptions in `check_and_process_issues()` cause non-zero exit code
3. **Concurrent flag usage**: Verify `--once --interval 300` works (ignores interval in once mode)
4. **Empty issue list**: Verify single cycle handles no open issues gracefully
5. **Help text**: Verify `--help` displays the new flag with proper description

## Acceptance Criteria
1. The `--once` argument is available in the argument parser for both files
2. Running `uv run adws/adw_triggers/trigger_cron.py --once` executes exactly ONE check cycle
3. The script exits with code 0 after successful single cycle execution
4. The script exits with non-zero code if `check_and_process_issues()` raises an exception
5. The normal mode (without `--once`) continues to function with the infinite loop
6. The Jinja2 template file has identical changes as the source file
7. The help text (`--help`) displays the `--once` flag with appropriate description
8. Signal handling (Ctrl+C) works correctly in both modes
9. The module docstring includes usage example for `--once` mode
10. No scheduler objects are created when running in `--once` mode

## Validation Commands
Execute all commands to validate with zero regressions:

```bash
# Verify help text shows --once flag
uv run adws/adw_triggers/trigger_cron.py --help | grep -A1 "\-\-once"

# Test single execution mode exits cleanly within timeout
timeout 10 uv run adws/adw_triggers/trigger_cron.py --once && echo "SUCCESS: Exited cleanly"

# Verify normal mode still works (test with short timeout, should NOT exit on its own)
timeout 5 uv run adws/adw_triggers/trigger_cron.py --interval 2 || [ $? -eq 124 ] && echo "SUCCESS: Normal mode runs continuously"

# Verify template file has identical structure
diff -u <(grep -A10 "def parse_args" adws/adw_triggers/trigger_cron.py | grep -v "^#") \
        <(grep -A10 "def parse_args" tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2 | grep -v "^#" | grep -v "{{" | grep -v "}}") \
        || echo "NOTE: Template may have Jinja2 variables, verify manually"
```

## Notes
- This is a minimal, surgical change to two files only
- No new dependencies are required
- The `--once` flag is mutually compatible with `--interval` (interval is simply ignored in once mode)
- The early-return pattern keeps the implementation simple and efficient
- Signal handlers remain active even in `--once` mode, allowing graceful interruption
- The auto-resolved clarifications confirm: respect signals, propagate exceptions, skip scheduler setup, use minimal logging
- Future enhancement could add metrics or timing information specific to single-execution mode
- Consider documenting this flag in the main ADW documentation for user visibility
