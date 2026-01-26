# Start

Start tac-bootstrap in development mode.

## Variables
- PORT: Not applicable (CLI or library)

## Check
Verify application exists:
```bash
ls tac_bootstrap_cli/
```

## Workflow

### If application exists:

1. Verify dependencies:
   ```bash
   cd tac_bootstrap_cli && uv sync
   ```

2. Start application:
   ```bash
   uv run tac-bootstrap --help
   ```

3. Verify running:
   - Check for successful startup messages
   - Verify no errors in output

### If application does NOT exist:

1. Inform user that the application has not been created yet
2. Show instructions:
   ```
   The application for tac-bootstrap does not exist yet.

   To create it, check the specs directory for setup instructions:
   1. Read specs/
   2. Follow the setup guide
   ```

## Report
- Application state (running/pending)
- Available commands (if running)
- Next steps
