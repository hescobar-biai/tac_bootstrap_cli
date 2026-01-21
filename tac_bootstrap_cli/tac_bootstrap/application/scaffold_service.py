"""Scaffold Service for building and applying generation plans.

This service is responsible for:
1. Building a ScaffoldPlan from TACConfig
2. Applying the plan to create directories and files
3. Handling idempotency and existing files
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from tac_bootstrap.domain.models import TACConfig
from tac_bootstrap.domain.plan import (
    FileAction,
    ScaffoldPlan,
)
from tac_bootstrap.infrastructure.template_repo import TemplateRepository


@dataclass
class ApplyResult:
    """Result of applying a scaffold plan."""

    success: bool = True
    directories_created: int = 0
    files_created: int = 0
    files_skipped: int = 0
    files_overwritten: int = 0
    error: Optional[str] = None
    errors: List[str] = field(default_factory=list)


class ScaffoldService:
    """Service for building and applying scaffold plans.

    Example:
        service = ScaffoldService()
        plan = service.build_plan(config)
        result = service.apply_plan(plan, output_dir, config)
    """

    def __init__(self, template_repo: Optional[TemplateRepository] = None):
        """Initialize scaffold service.

        Args:
            template_repo: Template repository (created if not provided)
        """
        self.template_repo = template_repo or TemplateRepository()

    def build_plan(
        self,
        config: TACConfig,
        existing_repo: bool = False,
    ) -> ScaffoldPlan:
        """Build a scaffold plan from configuration.

        Args:
            config: TAC configuration
            existing_repo: Whether scaffolding into existing repo

        Returns:
            ScaffoldPlan with all operations to perform
        """
        plan = ScaffoldPlan()

        # Add directory structure
        self._add_directories(plan, config)

        # Add Claude configuration files
        self._add_claude_files(plan, config, existing_repo)

        # Add ADW files
        self._add_adw_files(plan, config, existing_repo)

        # Add script files
        self._add_script_files(plan, config, existing_repo)

        # Add config files
        self._add_config_files(plan, config, existing_repo)

        # Add structure READMEs
        self._add_structure_files(plan, config, existing_repo)

        return plan

    def _add_directories(self, plan: ScaffoldPlan, config: TACConfig) -> None:
        """Add directory operations to plan."""
        directories = [
            (".claude", "Claude Code configuration"),
            (".claude/commands", "Slash commands"),
            (".claude/hooks", "Execution hooks"),
            (".claude/hooks/utils", "Hook utilities"),
            (config.paths.adws_dir, "AI Developer Workflows"),
            (f"{config.paths.adws_dir}/adw_modules", "ADW shared modules"),
            (f"{config.paths.adws_dir}/adw_triggers", "ADW triggers"),
            (config.paths.specs_dir, "Specifications"),
            (config.paths.logs_dir, "Execution logs"),
            (config.paths.scripts_dir, "Utility scripts"),
            (config.paths.prompts_dir, "Prompt templates"),
            (f"{config.paths.prompts_dir}/templates", "Document templates"),
            ("agents", "ADW agent state"),
            (config.paths.worktrees_dir, "Git worktrees"),
            ("app_docs", "Application documentation"),
            ("ai_docs", "AI-generated documentation"),
        ]

        for path, reason in directories:
            plan.add_directory(path, reason)

    def _add_claude_files(self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool) -> None:
        """Add .claude/ configuration files."""
        action = FileAction.CREATE if not existing_repo else FileAction.SKIP

        # Settings
        plan.add_file(
            ".claude/settings.json",
            action=action,
            template="claude/settings.json.j2",
            reason="Claude Code settings and permissions",
        )

        # Commands - all slash commands
        commands = [
            "prime",
            "start",
            "build",
            "test",
            "lint",
            "feature",
            "bug",
            "chore",
            "patch",
            "implement",
            "commit",
            "pull_request",
            "review",
            "document",
            "health_check",
            "prepare_app",
            "install",
            "track_agentic_kpis",
        ]

        for cmd in commands:
            plan.add_file(
                f".claude/commands/{cmd}.md",
                action=action,
                template=f"claude/commands/{cmd}.md.j2",
                reason=f"/{cmd} slash command",
            )

        # Hooks
        hooks = [
            ("pre_tool_use.py", "Pre-execution validation"),
            ("post_tool_use.py", "Post-execution logging"),
            ("stop.py", "Session cleanup"),
        ]

        for hook, reason in hooks:
            plan.add_file(
                f".claude/hooks/{hook}",
                action=action,
                template=f"claude/hooks/{hook}.j2",
                reason=reason,
                executable=True,
            )

        # Hook utils
        plan.add_file(
            ".claude/hooks/utils/__init__.py",
            action=action,
            template="claude/hooks/utils/__init__.py.j2",
            reason="Hook utilities package",
        )
        plan.add_file(
            ".claude/hooks/utils/constants.py",
            action=action,
            template="claude/hooks/utils/constants.py.j2",
            reason="Shared constants for hooks",
        )

    def _add_adw_files(self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool) -> None:
        """Add adws/ workflow files."""
        action = FileAction.CREATE if not existing_repo else FileAction.SKIP
        adws_dir = config.paths.adws_dir

        # README
        plan.add_file(
            f"{adws_dir}/README.md",
            action=action,
            template="adws/README.md.j2",
            reason="ADW documentation",
        )

        # Modules - all ADW infrastructure modules
        modules = [
            ("__init__.py", "Package init"),
            ("agent.py", "Claude Code wrapper"),
            ("state.py", "State persistence"),
            ("git_ops.py", "Git operations"),
            ("workflow_ops.py", "Workflow orchestration"),
            ("data_types.py", "Data models and types"),
            ("github.py", "GitHub API operations"),
            ("utils.py", "Utility functions"),
            ("worktree_ops.py", "Git worktree management"),
            ("r2_uploader.py", "Cloudflare R2 uploader"),
        ]

        for module, reason in modules:
            plan.add_file(
                f"{adws_dir}/adw_modules/{module}",
                action=action,
                template=f"adws/adw_modules/{module}.j2",
                reason=reason,
            )

        # Workflows - all isolated ADW workflows
        workflows = [
            # Core orchestration
            ("adw_sdlc_iso.py", "SDLC workflow (isolated)"),
            ("adw_sdlc_zte_iso.py", "Zero Touch Execution workflow"),
            ("adw_patch_iso.py", "Patch workflow (isolated)"),
            # Individual phases
            ("adw_plan_iso.py", "Planning phase (isolated)"),
            ("adw_build_iso.py", "Build phase (isolated)"),
            ("adw_test_iso.py", "Test phase (isolated)"),
            ("adw_review_iso.py", "Review phase (isolated)"),
            ("adw_document_iso.py", "Documentation phase (isolated)"),
            ("adw_ship_iso.py", "Ship/merge phase (isolated)"),
            # Compositional workflows
            ("adw_plan_build_iso.py", "Plan + Build workflow"),
            ("adw_plan_build_test_iso.py", "Plan + Build + Test workflow"),
            ("adw_plan_build_test_review_iso.py", "Plan + Build + Test + Review workflow"),
            ("adw_plan_build_review_iso.py", "Plan + Build + Review workflow"),
            ("adw_plan_build_document_iso.py", "Plan + Build + Document workflow"),
        ]

        for workflow, reason in workflows:
            plan.add_file(
                f"{adws_dir}/{workflow}",
                action=action,
                template=f"adws/{workflow}.j2",
                reason=reason,
                executable=True,
            )

        # Triggers
        plan.add_file(
            f"{adws_dir}/adw_triggers/__init__.py",
            action=action,
            template="adws/adw_triggers/__init__.py.j2",
            reason="Triggers package",
        )
        plan.add_file(
            f"{adws_dir}/adw_triggers/trigger_cron.py",
            action=action,
            template="adws/adw_triggers/trigger_cron.py.j2",
            reason="Cron-based task polling",
            executable=True,
        )

    def _add_script_files(self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool) -> None:
        """Add scripts/ utility files."""
        action = FileAction.CREATE if not existing_repo else FileAction.SKIP
        scripts_dir = config.paths.scripts_dir

        scripts = [
            ("start.sh", "Application starter"),
            ("test.sh", "Test runner"),
            ("lint.sh", "Linter runner"),
            ("build.sh", "Build script"),
        ]

        for script, reason in scripts:
            plan.add_file(
                f"{scripts_dir}/{script}",
                action=action,
                template=f"scripts/{script}.j2",
                reason=reason,
                executable=True,
            )

    def _add_config_files(self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool) -> None:
        """Add configuration files."""
        action = FileAction.CREATE if not existing_repo else FileAction.SKIP

        # config.yml - always create/overwrite to capture user settings
        plan.add_file(
            "config.yml",
            action=FileAction.OVERWRITE if existing_repo else FileAction.CREATE,
            template="config/config.yml.j2",
            reason="TAC Bootstrap configuration",
        )

        # .mcp.json
        plan.add_file(
            ".mcp.json",
            action=action,
            template="config/.mcp.json.j2",
            reason="MCP server configuration",
        )

        # playwright-mcp-config.json
        plan.add_file(
            "playwright-mcp-config.json",
            action=action,
            template="config/playwright-mcp-config.json.j2",
            reason="Playwright MCP browser configuration",
        )

        # .gitignore - append if exists
        plan.add_file(
            ".gitignore",
            action=FileAction.PATCH if existing_repo else FileAction.CREATE,
            template="config/.gitignore.j2",
            reason="Git ignore patterns",
        )

    def _add_structure_files(
        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool
    ) -> None:
        """Add README files for directory structure."""
        action = FileAction.CREATE if not existing_repo else FileAction.SKIP

        structure_readmes = [
            (f"{config.paths.specs_dir}/README.md", "structure/specs/README.md.j2"),
            ("app_docs/README.md", "structure/app_docs/README.md.j2"),
            ("ai_docs/README.md", "structure/ai_docs/README.md.j2"),
        ]

        for path, template in structure_readmes:
            plan.add_file(
                path,
                action=action,
                template=template,
                reason="Directory documentation",
            )

        # Add AI reference documentation
        ai_docs_files = [
            ("ai_docs/anthropic_quick_start.md", "structure/ai_docs/anthropic_quick_start.md.j2", "Anthropic API quickstart"),
            ("ai_docs/claude_code_cli_reference.md", "structure/ai_docs/claude_code_cli_reference.md.j2", "Claude Code CLI reference"),
            ("ai_docs/claude_code_sdk.md", "structure/ai_docs/claude_code_sdk.md.j2", "Claude Code SDK documentation"),
            ("ai_docs/claude-code-hooks.md", "structure/ai_docs/claude-code-hooks.md.j2", "Claude Code hooks reference"),
            ("ai_docs/e2b.md", "structure/ai_docs/e2b.md.j2", "E2B sandbox documentation"),
            ("ai_docs/mcp-python-sdk.md", "structure/ai_docs/mcp-python-sdk.md.j2", "MCP Python SDK documentation"),
            ("ai_docs/openai_quick_start.md", "structure/ai_docs/openai_quick_start.md.j2", "OpenAI API quickstart"),
            ("ai_docs/uv-scripts.md", "structure/ai_docs/uv-scripts.md.j2", "UV scripts guide"),
        ]

        for path, template, reason in ai_docs_files:
            plan.add_file(
                path,
                action=action,
                template=template,
                reason=reason,
            )

        # Add app_docs files
        app_docs_files = [
            ("app_docs/agentic_kpis.md", "structure/app_docs/agentic_kpis.md.j2", "ADW performance metrics"),
        ]

        for path, template, reason in app_docs_files:
            plan.add_file(
                path,
                action=action,
                template=template,
                reason=reason,
            )

    def apply_plan(
        self,
        plan: ScaffoldPlan,
        output_dir: Path,
        config: TACConfig,
        force: bool = False,
    ) -> ApplyResult:
        """Apply a scaffold plan to create files and directories.

        Args:
            plan: The scaffold plan to apply
            output_dir: Target directory
            config: Configuration for template rendering
            force: Overwrite existing files

        Returns:
            ApplyResult with statistics and any errors
        """
        from tac_bootstrap.infrastructure.fs import FileSystem

        result = ApplyResult()
        fs = FileSystem()

        # Create directories first
        for dir_op in plan.directories:
            dir_path = output_dir / dir_op.path
            try:
                fs.ensure_directory(dir_path)
                result.directories_created += 1
            except Exception as e:
                result.errors.append(f"Failed to create {dir_op.path}: {e}")

        # Process files
        for file_op in plan.files:
            file_path = output_dir / file_op.path

            try:
                # Determine action based on existence and force flag
                if file_path.exists() and file_op.action == FileAction.CREATE:
                    if not force:
                        result.files_skipped += 1
                        continue
                    # Force mode - treat as overwrite
                    actual_action = FileAction.OVERWRITE
                else:
                    actual_action = file_op.action

                if actual_action == FileAction.SKIP:
                    result.files_skipped += 1
                    continue

                # Render content
                if file_op.template:
                    content = self.template_repo.render(file_op.template, config)
                elif file_op.content:
                    content = file_op.content
                else:
                    content = ""

                # Apply based on action
                if actual_action == FileAction.PATCH:
                    fs.append_file(file_path, content)
                else:
                    fs.write_file(file_path, content)

                # Make executable if needed
                if file_op.executable:
                    fs.make_executable(file_path)

                if actual_action == FileAction.OVERWRITE and file_path.exists():
                    result.files_overwritten += 1
                else:
                    result.files_created += 1

            except Exception as e:
                result.errors.append(f"Failed to create {file_op.path}: {e}")

        # Set success based on errors
        if result.errors:
            result.success = False
            result.error = f"{len(result.errors)} error(s) occurred"

        return result
