#!/bin/bash
# Build project - Generic template script
# This serves as a template for generated projects

set -e

echo "Building project..."

# Detect package manager and run build
if [ -f "pyproject.toml" ]; then
    if command -v uv &> /dev/null; then
        uv build
    elif command -v poetry &> /dev/null; then
        poetry build
    else
        python -m build
    fi
elif [ -f "package.json" ]; then
    if command -v pnpm &> /dev/null; then
        pnpm build
    elif command -v bun &> /dev/null; then
        bun run build
    else
        npm run build
    fi
else
    echo "No project configuration found"
    exit 1
fi

echo "Build completed!"
