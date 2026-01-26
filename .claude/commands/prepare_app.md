# Prepare Application

Prepare the tac-bootstrap development environment for tests or reviews.

## Instructions

### If tac_bootstrap_cli/ exists:

1. **Sync dependencies**
   ```bash
   cd tac_bootstrap_cli && uv sync
   ```


2. **Build Application**
   ```bash
   uv build
   ```

3. **Validate Application Can Start**
   ```bash
   uv run tac-bootstrap --help --help
   ```

4. **Run quick tests**
   ```bash
   uv run pytest -x --tb=short
   ```

### If tac_bootstrap_cli/ does NOT exist:

1. **Inform state**
   - The application has not been created yet
   - Cannot prepare the development environment

2. **Suggest next step**
   - Follow setup instructions in specs/ to create the application

## Report

After running the above steps, report:

1. **Dependencies status**: All dependencies synchronized successfully
2. ****: 3. **Build status**: Application built successfully4. **Application validation**: Application can start (verified with --help)
5. **Test status**: Quick tests passed

## Notes

- This command prepares the environment for application development
- For example app tests (if applicable), use scripts in `scripts/`
- Read documentation in specs/ to understand current project state
