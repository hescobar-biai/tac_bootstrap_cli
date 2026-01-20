#!/bin/bash
# Run linting for TAC Bootstrap CLI development
# Use this for developing the generator itself

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"

echo "TAC Bootstrap CLI - Running Lint"
echo "================================="

cd "$PROJECT_ROOT/tac_bootstrap_cli"

echo "Running ruff check..."
uv run ruff check .

echo ""
echo "Running ruff format check..."
uv run ruff format --check .

echo ""
echo "Lint completed!"
