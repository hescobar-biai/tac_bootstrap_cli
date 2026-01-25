"""
ADW Triggers Package - Automation entry points for AI Developer Workflows.

This package contains trigger scripts that monitor GitHub and automatically
invoke ADW workflows based on events or schedules.

Available Triggers:
    trigger_cron.py
        Polling-based monitor that checks GitHub issues at regular intervals.
        Detects workflow commands (adw_plan_iso, adw_sdlc_iso, etc.) in issue
        bodies or comments and triggers the corresponding workflow.
        Usage: uv run adw_triggers/trigger_cron.py [--interval N] [--once]

    trigger_issue_chain.py
        Sequential issue processor that handles issues in a specific order.
        Only processes issue N+1 after issue N is closed, enabling dependent
        workflows and ordered batch processing.
        Usage: uv run adw_triggers/trigger_issue_chain.py --issues 1,2,3 [--once]

    trigger_webhook.py
        Real-time webhook server that receives GitHub events instantly.
        Faster response than polling but requires public endpoint and
        webhook configuration in GitHub repository settings.
        Usage: uv run adw_triggers/trigger_webhook.py [--port N]

Common Features:
    - All triggers support workflow detection via keywords (adw_plan_iso, etc.)
    - All triggers post status comments to GitHub issues
    - All triggers create isolated worktrees for parallel execution
    - Graceful shutdown on SIGINT/SIGTERM signals

Environment Variables:
    GITHUB_TOKEN or gh auth: GitHub authentication
    ANTHROPIC_API_KEY: Claude API access
    GITHUB_WEBHOOK_SECRET: (webhook only) Signature validation

See Also:
    - adws/README.md for complete documentation
    - config.yml for interval and workflow configuration
"""
