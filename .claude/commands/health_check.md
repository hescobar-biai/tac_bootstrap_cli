# Health Check

Verify the development environment state for tac-bootstrap.

## Variables

TEST_COMMAND_TIMEOUT: 2 minutes

## Instructions

Execute development environment verifications for tac-bootstrap.

### If tac_bootstrap_cli/ exists:

1. **Verify application structure**
   - Command: `ls -la tac_bootstrap_cli/`
   - Must exist: source files, configuration

2. **Verify dependencies installed**
   - Command: `cd tac_bootstrap_cli && uv sync --dry-run`
   - If missing dependencies, report

3. **Verify application works**
   - Command: `uv run tac-bootstrap --help --help`
   - Must show help or respond

4. **Verify syntax**
   - Command: `cd tac_bootstrap_cli && uv run python -m py_compile **/*.py`
   - No syntax errors

5. **Verify config.yml**
   - Read config.yml and validate it's valid YAML
   - Verify required fields: project.name, project.language

### If tac_bootstrap_cli/ does NOT exist:

1. **Verify base configuration files**
   - Command: `ls config.yml CLAUDE.md`
   - These files must exist

2. **Inform state**
   - The application has not been created yet
   - Next step: Follow setup instructions in specs/

## Report

Report results as JSON:

```json
{
  "status": "healthy|warning|error",
  "app_exists": boolean,
  "checks": [
    {
      "name": "string",
      "passed": boolean,
      "message": "string"
    }
  ],
  "next_steps": ["string"]
}
```
