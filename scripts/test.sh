#!/bin/bash
# Run tests - Generic template script
# This serves as a template for generated projects

set -e

echo "Running tests..."

# Detect package manager and run tests
if [ -f "pyproject.toml" ]; then
    if command -v uv &> /dev/null; then
        uv run pytest tests/ -v
    elif command -v poetry &> /dev/null; then
        poetry run pytest tests/ -v
    else
        python -m pytest tests/ -v
    fi
elif [ -f "package.json" ]; then
    if command -v pnpm &> /dev/null; then
        pnpm test
    elif command -v bun &> /dev/null; then
        bun test
    else
        npm test
    fi
else
    echo "No project configuration found"
    exit 1
fi

echo "Tests completed!"
