# Lint

Run the linter to check code quality.

## Variables
- $ARGUMENTS: Optional lint arguments or file paths

## Instructions

1. Run the linter:
   ```bash
   uv run ruff check . $ARGUMENTS
   ```

2. If linting fails:
   - Analyze the error output
   - Identify the specific violations and their locations
   - Note if automatic fixes are available
   - Do NOT attempt to fix unless explicitly asked

3. Report results

## Report
- Lint status: passed/failed
- Total issues: X (errors: X, warnings: X)
- Issues found: (list with file:line if any)
- Auto-fixable: X issues
- Suggested fixes: (if applicable and available)
