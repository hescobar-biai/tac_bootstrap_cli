#!/bin/bash
# Run tests for TAC Bootstrap CLI development
# Use this for developing the generator itself

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"

echo "TAC Bootstrap CLI - Running Tests"
echo "=================================="

cd "$PROJECT_ROOT/tac_bootstrap_cli"

# Run pytest with coverage
uv run pytest tests/ -v --cov=tac_bootstrap --cov-report=term-missing

echo ""
echo "Tests completed!"
