#!/bin/bash
# Setup an isolated worktree environment with MCP configuration
# Usage: ./scripts/setup_worktree.sh <worktree_path>
#
# This replaces the /install_worktree Claude command with a direct bash script
# to avoid API rate limiting and hanging issues.

set -e

WORKTREE_PATH="$1"

if [ -z "$WORKTREE_PATH" ]; then
    echo "Usage: $0 <worktree_path>"
    exit 1
fi

if [ ! -d "$WORKTREE_PATH" ]; then
    echo "Error: Worktree directory does not exist: $WORKTREE_PATH"
    exit 1
fi

# Get the parent repo root (where this script lives)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PARENT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Convert to absolute path
WORKTREE_PATH="$(cd "$WORKTREE_PATH" && pwd)"

echo "Setting up worktree: $WORKTREE_PATH"
echo "Parent repo: $PARENT_DIR"

# 1. Copy .env if exists in parent
if [ -f "$PARENT_DIR/.env" ]; then
    cp "$PARENT_DIR/.env" "$WORKTREE_PATH/.env"
    echo "  Copied .env"
else
    echo "  No .env in parent (skipping)"
fi

# 2. Create .mcp.json with absolute paths pointing to this worktree
cat > "$WORKTREE_PATH/.mcp.json" << EOF
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--isolated",
        "--config",
        "$WORKTREE_PATH/playwright-mcp-config.json"
      ]
    }
  }
}
EOF
echo "  Created .mcp.json"

# 3. Create playwright-mcp-config.json with absolute video path
mkdir -p "$WORKTREE_PATH/videos"
cat > "$WORKTREE_PATH/playwright-mcp-config.json" << EOF
{
  "browser": {
    "browserName": "chromium",
    "launchOptions": {
      "headless": true
    },
    "contextOptions": {
      "recordVideo": {
        "dir": "$WORKTREE_PATH/videos",
        "size": {
          "width": 1920,
          "height": 1080
        }
      },
      "viewport": {
        "width": 1920,
        "height": 1080
      }
    }
  }
}
EOF
echo "  Created playwright-mcp-config.json"
echo "  Created videos/ directory"

# 4. Copy .claude/ directory so Claude Code recognizes worktree as project root
# CRITICAL: Must COPY not symlink! Symlinks cause Claude to resolve paths to main repo
# which results in files being written to main instead of the worktree
if [ -d "$PARENT_DIR/.claude" ] && [ ! -e "$WORKTREE_PATH/.claude" ]; then
    cp -R "$PARENT_DIR/.claude" "$WORKTREE_PATH/.claude"
    echo "  Copied .claude/ directory"
fi

# 6. Install backend dependencies if applicable
if [ -f "$WORKTREE_PATH/app/server/pyproject.toml" ]; then
    echo "  Installing backend dependencies..."
    (cd "$WORKTREE_PATH/app/server" && uv sync --all-extras)
    echo "  Backend dependencies installed"
fi

# 7. Install frontend dependencies if applicable
if [ -f "$WORKTREE_PATH/app/client/package.json" ]; then
    echo "  Installing frontend dependencies..."
    (cd "$WORKTREE_PATH/app/client" && bun install)
    echo "  Frontend dependencies installed"
fi

echo "Worktree setup complete: $WORKTREE_PATH"
