#!/bin/bash
# Run linting - Generic template script
# This serves as a template for generated projects

set -e

echo "Running linter..."

# Detect package manager and run lint
if [ -f "pyproject.toml" ]; then
    if command -v uv &> /dev/null; then
        uv run ruff check .
    elif command -v poetry &> /dev/null; then
        poetry run ruff check .
    else
        ruff check .
    fi
elif [ -f "package.json" ]; then
    if command -v pnpm &> /dev/null; then
        pnpm lint
    elif command -v bun &> /dev/null; then
        bun run lint
    else
        npm run lint
    fi
else
    echo "No project configuration found"
    exit 1
fi

echo "Lint completed!"
