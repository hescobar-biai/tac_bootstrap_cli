#!/usr/bin/env bash
# batch_adw_workflow.sh - Execute ADW workflow for multiple features
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo "Usage: $0 \"feature-001,feature-002,feature-003\" \"owner/repo\""
    echo ""
    echo "Arguments:"
    echo "  features    Comma-separated list of feature names"
    echo "  repo        GitHub repository in format owner/repo"
    echo ""
    echo "Example:"
    echo "  $0 \"feature-auth,feature-api,feature-ui\" \"myorg/myrepo\""
    exit 1
}

# Function to send macOS notification
notify() {
    local message="$1"
    osascript -e "display notification \"$message\" with title \"ADW Workflow\""
}

# Function to log with timestamp
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

# Validate arguments
if [ $# -ne 2 ]; then
    log_error "Invalid number of arguments"
    usage
fi

FEATURES_INPUT="$1"
REPO="$2"

# Validate repo format
if [[ ! "$REPO" =~ ^[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+$ ]]; then
    log_error "Invalid repository format. Expected: owner/repo"
    usage
fi

# Parse features into array
IFS=',' read -ra FEATURES <<< "$FEATURES_INPUT"

if [ ${#FEATURES[@]} -eq 0 ]; then
    log_error "No features provided"
    usage
fi

log "Starting batch ADW workflow"
log "Repository: $REPO"
log "Features to process: ${#FEATURES[@]}"
echo ""

# Track results
SUCCESSFUL=()
FAILED=()

# Process each feature
for feature in "${FEATURES[@]}"; do
    # Trim whitespace
    feature=$(echo "$feature" | xargs)

    if [ -z "$feature" ]; then
        continue
    fi

    echo "=============================================="
    log "Processing feature: $feature"
    echo "=============================================="

    # Step 1: Create GitHub issue using claude
    log "Creating GitHub issue for $feature..."

    # Use script to provide a pseudo-TTY for claude CLI
    ISSUE_OUTPUT=$(script -q /dev/null claude --dangerously-skip-permissions -p "/create-gh-issue $feature $REPO" 2>&1) || {
        log_error "Failed to create issue for $feature"
        FAILED+=("$feature")
        notify "$feature failed - issue creation error"
        continue
    }

    # Step 2: Extract issue number (without #)
    # Expected output format: "issue number: #123"
    ISSUE_NUMBER=$(echo "$ISSUE_OUTPUT" | grep -oE 'issue number: #[0-9]+' | grep -oE '[0-9]+$')

    if [ -z "$ISSUE_NUMBER" ]; then
        log_error "Could not extract issue number from output for $feature"
        log_warning "Output was: $ISSUE_OUTPUT"
        FAILED+=("$feature")
        notify "$feature failed - could not parse issue number"
        continue
    fi

    log "Created issue #$ISSUE_NUMBER"

    # Step 3: Run ADW workflow
    log "Running ADW workflow for issue #$ISSUE_NUMBER..."
    echo "--- ADW Start: $(date) ---"

    if uv run adws/adw_sdlc_zte_iso.py "$ISSUE_NUMBER" "${feature}"; then
        echo "--- ADW End: $(date) ---"
        log "ADW workflow completed for $feature"
        SUCCESSFUL+=("$feature:#$ISSUE_NUMBER")
    else
        echo "--- ADW End (with errors): $(date) ---"
        log_error "ADW workflow failed for $feature"
        FAILED+=("$feature:#$ISSUE_NUMBER")
        notify "$feature failed - ADW workflow error"
        continue
    fi

    # Step 4: Send success notification
    notify "$feature completed successfully"
    log "Notification sent for $feature"
    echo ""
done

# Summary
echo ""
echo "=============================================="
log "Batch ADW Workflow Complete"
echo "=============================================="
echo ""
echo -e "${GREEN}Successful (${#SUCCESSFUL[@]}):${NC}"
for item in "${SUCCESSFUL[@]}"; do
    echo "  - $item"
done
echo ""
echo -e "${RED}Failed (${#FAILED[@]}):${NC}"
for item in "${FAILED[@]}"; do
    echo "  - $item"
done
echo ""

# Exit with error if any failures
if [ ${#FAILED[@]} -gt 0 ]; then
    exit 1
fi
