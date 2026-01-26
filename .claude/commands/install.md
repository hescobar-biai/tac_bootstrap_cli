# Install & Prime

Install dependencies and prepare the development environment for tac-bootstrap.

## Read
- README.md
- CLAUDE.md
- config.yml

## Check Structure
Verify the application structure exists:
```
tac_bootstrap_cli/
├── (package manifest: pyproject.toml, package.json, Cargo.toml, etc.)
└── (source code)
```

If it doesn't exist, inform the user they need to create the application first.

## Run (if tac_bootstrap_cli exists)

1. Install dependencies:
   ```bash
   cd tac_bootstrap_cli && uv sync
   ```

2. Verify installation:
   ```bash
   uv run tac-bootstrap --help --help
   ```

## Run (if tac_bootstrap_cli does NOT exist)

1. Inform that the application has not been created yet
2. Suggest checking specs/ for setup instructions

## Read and Execute
.claude/commands/prime.md

## Report
- Installation state (successful/pending)
- Installed version (if applicable)
- Next steps
- Available commands:
  - `/prime` - Prepare context
  - `/feature` - Plan feature
  - `/implement <plan>` - Execute plan
  - `/test` - Run tests
