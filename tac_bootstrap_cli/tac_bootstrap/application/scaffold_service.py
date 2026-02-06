"""
IDK: scaffold-service, plan-builder, code-generation, template-rendering,
     file-operations, expert-registration
Responsibility: Builds scaffold plans from TACConfig and applies them to filesystem,
                including TAC-13 expert agent templates
Invariants: Plans are idempotent, templates must exist, output directory must be writable,
            expert templates follow 3-component pattern
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from tac_bootstrap.application.exceptions import ScaffoldValidationError
from tac_bootstrap.application.validation_service import ValidationService
from tac_bootstrap.domain.models import Architecture, Framework, TACConfig
from tac_bootstrap.domain.plan import (
    FileAction,
    ScaffoldPlan,
)
from tac_bootstrap.infrastructure.template_repo import TemplateRepository


@dataclass
class ApplyResult:
    """
    IDK: operation-result, statistics-tracking, error-reporting
    Responsibility: Tracks scaffold application statistics and errors
    Invariants: Success is false when errors exist, counters are always non-negative
    """

    success: bool = True
    directories_created: int = 0
    files_created: int = 0
    files_skipped: int = 0
    files_overwritten: int = 0
    error: Optional[str] = None
    errors: List[str] = field(default_factory=list)


class ScaffoldService:
    """
    IDK: plan-execution, template-application, directory-creation, validation-gate
    Responsibility: Orchestrates scaffold plan building and application with pre-validation
    Invariants: Validates before applying, tracks operation statistics, handles errors gracefully
    """

    def __init__(
        self,
        template_repo: Optional[TemplateRepository] = None,
        validation_service: Optional[ValidationService] = None,
    ):
        """Initialize scaffold service.

        Args:
            template_repo: Template repository (created if not provided)
            validation_service: Validation service (created if not provided)
        """
        self.template_repo = template_repo or TemplateRepository()
        self.validation_service = validation_service or ValidationService(self.template_repo)

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

        # Add shared infrastructure for DDD-style architectures with FastAPI
        ddd_architectures = [Architecture.DDD, Architecture.CLEAN, Architecture.HEXAGONAL]
        if config.project.architecture in ddd_architectures:
            if config.project.framework == Framework.FASTAPI:
                self._add_shared_infrastructure(plan, config)

        # Add Claude configuration files
        self._add_claude_files(plan, config, existing_repo)

        # Add ADW files
        self._add_adw_files(plan, config, existing_repo)

        # Add consolidated workflow files (TAC-14 Task 10)
        self._add_adw_workflow_files(plan, config, existing_repo)

        # Add schema files
        self._add_schema_files(plan, config, existing_repo)

        # Add script files
        self._add_script_files(plan, config, existing_repo)

        # Add config files
        self._add_config_files(plan, config, existing_repo)

        # Add structure READMEs
        self._add_structure_files(plan, config, existing_repo)

        # Add fractal documentation scripts
        self._add_fractal_docs_scripts(plan, config)

        # Add orchestrator components only if enabled (TAC-14 Task 16)
        if config.orchestrator.enabled:
            # Add orchestrator web backend
            self._add_orchestrator_backend(plan, config, existing_repo)

            # Add orchestrator frontend (Vue 3 + TypeScript)
            self._add_orchestrator_frontend(plan, config, existing_repo)

            # Add test suites (TAC-14 Task 15)
            self._add_test_files(plan, config, existing_repo)

            # Add orchestrator utility scripts (TAC-14 Task 19)
            self._add_orchestrator_scripts(plan, config)

            # Add orchestrator Makefile (TAC-14)
            plan.add_file(
                "Makefile",
                action=FileAction.CREATE,
                template="Makefile.j2",
                reason="Orchestrator build and run commands",
            )

        return plan

    def _add_directories(self, plan: ScaffoldPlan, config: TACConfig) -> None:
        """Add directory operations to plan."""
        directories = [
            (".claude", "Claude Code configuration"),
            (".claude/commands", "Slash commands"),
            (".claude/commands/e2e", "E2E test command examples"),
            (".claude/commands/experts", "TAC-13 expert command groups"),
            (".claude/commands/experts/cc_hook_expert", "Hook expert: Claude Code hooks"),
            (".claude/commands/experts/cli", "CLI expert: TAC Bootstrap CLI"),
            (".claude/commands/experts/adw", "ADW expert: AI Developer Workflows"),
            (".claude/commands/experts/commands", "Commands expert: .claude/commands structure"),
            (".claude/agents", "Agent definitions"),
            (".claude/output-styles", "Output style presets"),
            (".claude/status_lines", "Claude Code status line definitions"),
            (".claude/skills", "Agent skills directory"),
            (".claude/skills/meta-skill", "Meta-skill for creating new skills"),
            (".claude/skills/meta-skill/docs", "Meta-skill documentation resources"),
            (".claude/skills/start-orchestrator", "Start orchestrator skill"),
            (".claude/hooks", "Execution hooks"),
            (".claude/hooks/utils", "Hook utilities"),
            (".claude/hooks/utils/llm", "LLM provider utilities"),
            (".claude/hooks/utils/tts", "Text-to-speech utilities"),
            (".claude/data", "Session and data storage"),
            (".claude/data/sessions", "Claude Code session data"),
            (".claude/data/claude-model-cache", "Model info cache storage"),
            (config.paths.adws_dir, "AI Developer Workflows"),
            (f"{config.paths.adws_dir}/adw_modules", "ADW shared modules"),
            (f"{config.paths.adws_dir}/adw_triggers", "ADW triggers"),
            (config.paths.specs_dir, "Specifications"),
            (config.paths.logs_dir, "Execution logs"),
            (config.paths.scripts_dir, "Utility scripts"),
            (config.paths.prompts_dir, "Prompt templates"),
            (f"{config.paths.prompts_dir}/templates", "Document templates"),
            ("agents", "ADW agent state"),
            ("agents/hook_logs", "Hook execution logs"),
            ("agents/context_bundles", "Agent context bundles"),
            ("agents/security_logs", "Security hook execution logs"),
            ("agents/scout_files", "Scout command state and cache"),
            (config.paths.worktrees_dir, "Git worktrees"),
            ("app_docs", "Application documentation"),
            ("ai_docs", "AI-generated documentation"),
        ]

        for path, reason in directories:
            plan.add_directory(path, reason)

        # Add .gitkeep files to preserve empty agent directories
        plan.add_file(
            "agents/hook_logs/.gitkeep",
            action=FileAction.CREATE,
            content="",
            reason="Keep empty directory in Git",
        )
        plan.add_file(
            "agents/context_bundles/.gitkeep",
            action=FileAction.CREATE,
            content="",
            reason="Keep empty directory in Git",
        )
        plan.add_file(
            "agents/security_logs/.gitkeep",
            action=FileAction.CREATE,
            content="",
            reason="Keep empty directory in Git",
        )
        plan.add_file(
            "agents/scout_files/.gitkeep",
            action=FileAction.CREATE,
            content="",
            reason="Keep empty directory in Git",
        )
        plan.add_file(
            ".claude/data/sessions/.gitkeep",
            action=FileAction.CREATE,
            content="",
            reason="Keep empty directory in Git",
        )
        plan.add_file(
            ".claude/data/claude-model-cache/.gitkeep",
            action=FileAction.CREATE,
            content="",
            reason="Keep empty directory in Git",
        )

    def _add_shared_infrastructure(self, plan: ScaffoldPlan, config: TACConfig) -> None:
        """Add shared infrastructure base classes for DDD/Clean/Hexagonal architectures."""
        action = FileAction.CREATE  # CREATE only creates if file doesn't exist

        # Add directory structure
        directories = [
            ("src/shared", "Shared infrastructure"),
            ("src/shared/domain", "Domain base classes"),
            ("src/shared/application", "Application base classes"),
            ("src/shared/infrastructure", "Infrastructure base classes"),
            ("src/shared/api", "Shared API utilities"),
        ]

        for path, reason in directories:
            plan.add_directory(path, reason)

        # Add __init__.py files
        init_files = [
            "src/shared/__init__.py",
            "src/shared/domain/__init__.py",
            "src/shared/application/__init__.py",
            "src/shared/infrastructure/__init__.py",
            "src/shared/api/__init__.py",
        ]

        for init_file in init_files:
            plan.add_file(
                init_file,
                action=action,
                content="",
                reason="Python package marker",
            )

        # Add domain base classes
        plan.add_file(
            "src/shared/domain/base_entity.py",
            action=action,
            template="shared/base_entity.py.j2",
            reason="Base entity for domain models",
        )
        plan.add_file(
            "src/shared/domain/base_schema.py",
            action=action,
            template="shared/base_schema.py.j2",
            reason="Base schema for API models",
        )

        # Add application base class
        plan.add_file(
            "src/shared/application/base_service.py",
            action=action,
            template="shared/base_service.py.j2",
            reason="Base service for business logic",
        )

        # Add infrastructure base classes
        plan.add_file(
            "src/shared/infrastructure/base_repository.py",
            action=action,
            template="shared/base_repository.py.j2",
            reason="Base repository (synchronous)",
        )
        plan.add_file(
            "src/shared/infrastructure/base_repository_async.py",
            action=action,
            template="shared/base_repository_async.py.j2",
            reason="Base repository (asynchronous)",
        )
        plan.add_file(
            "src/shared/infrastructure/database.py",
            action=action,
            template="shared/database.py.j2",
            reason="Database configuration and session",
        )
        plan.add_file(
            "src/shared/infrastructure/exceptions.py",
            action=action,
            template="shared/exceptions.py.j2",
            reason="Standard exception hierarchy",
        )
        plan.add_file(
            "src/shared/infrastructure/responses.py",
            action=action,
            template="shared/responses.py.j2",
            reason="Standard API response models",
        )
        plan.add_file(
            "src/shared/infrastructure/dependencies.py",
            action=action,
            template="shared/dependencies.py.j2",
            reason="FastAPI dependency injection",
        )

        # Add API utilities
        plan.add_file(
            "src/shared/api/health.py",
            action=action,
            template="shared/health.py.j2",
            reason="Health check endpoint",
        )

    def _add_claude_files(self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool) -> None:
        """Add .claude/ configuration files.

        Includes TAC-13 expert agent templates following the dual-strategy pattern:
        1. CLI Templates (Jinja2): In tac_bootstrap/templates/
        2. Repo Implementations: Generated in .claude/commands/
        3. Expertise Files: Working memory maintained by self-improve workflow
        """
        action = FileAction.CREATE  # CREATE only creates if file doesn't exist

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
            "build_in_parallel",
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
            # ADW workflow commands
            "classify_adw",
            "classify_issue",
            "cleanup_worktrees",
            "generate_branch_name",
            "install_worktree",
            # Test resolution commands
            "resolve_failed_test",
            "resolve_failed_e2e_test",
            "test_e2e",
            # Utility commands
            "tools",
            "all_tools",
            "in_loop_review",
            "github_check",
            "conditional_docs",
            "find_and_summarize",
            "scout",
            "question",
            # TAC-9/10: Context and agent delegation commands
            "background",
            "load_ai_docs",
            "load_bundle",
            "prime_cc",
            "prime_3",
            "quick-plan",
            "parallel_subagents",
            "t_metaprompt_workflow",
            "meta-prompt",
            "meta-agent",
            "expert-orchestrate",
            "expert-parallel",
            "build_w_report",
            # TAC-12: Enhanced planning commands
            "plan_w_docs",
            "plan_w_scouters",
            "plan",
            "scout_plan_build",
            # TAC-14: Orchestrator commands
            "orch_plan_w_scouts_build_review",
            "orch_scout_and_build",
            "orch_one_shot_agent",
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
            ("pre_tool_use.py", "Pre-tool observability logging"),
            ("post_tool_use.py", "Post-execution logging"),
            ("stop.py", "Session cleanup"),
            ("notification.py", "Notification logging"),
            ("pre_compact.py", "Pre-compact logging"),
            ("subagent_stop.py", "Subagent stop handler"),
            ("user_prompt_submit.py", "User prompt validation and logging"),
            ("dangerous_command_blocker.py", "Security validation hook"),
            ("context_bundle_builder.py", "Context bundle building for session recovery"),
            ("universal_hook_logger.py", "Universal event logging for all hooks"),
            ("send_event.py", "Event observability hook"),
            ("session_start.py", "Session initialization context capture"),
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
        plan.add_file(
            ".claude/hooks/utils/summarizer.py",
            action=action,
            template="claude/hooks/utils/summarizer.py.j2",
            reason="Event summarizer utility",
        )
        plan.add_file(
            ".claude/hooks/utils/model_extractor.py",
            action=action,
            template="claude/hooks/utils/model_extractor.py.j2",
            reason="Model extractor with caching",
        )

        # LLM provider utilities
        llm_utils = [
            ("__init__.py", "LLM utilities package"),
            ("anth.py", "Anthropic API wrapper"),
            ("oai.py", "OpenAI API wrapper"),
            ("ollama.py", "Ollama local LLM wrapper"),
        ]
        for util, reason in llm_utils:
            plan.add_file(
                f".claude/hooks/utils/llm/{util}",
                action=action,
                template=f"claude/hooks/utils/llm/{util}.j2",
                reason=reason,
            )

        # TTS utilities
        tts_utils = [
            ("__init__.py", "TTS utilities package"),
            ("elevenlabs_tts.py", "ElevenLabs TTS wrapper"),
            ("openai_tts.py", "OpenAI TTS wrapper"),
            ("pyttsx3_tts.py", "pyttsx3 local TTS wrapper"),
        ]
        for util, reason in tts_utils:
            plan.add_file(
                f".claude/hooks/utils/tts/{util}",
                action=action,
                template=f"claude/hooks/utils/tts/{util}.j2",
                reason=reason,
            )

        # Agent definitions
        agents = [
            ("docs-scraper.md", "Documentation scraping agent"),
            ("meta-agent.md", "Agent generation from specifications"),
            ("research-docs-fetcher.md", "Research and documentation fetcher agent"),
            ("build-agent.md", "Parallel build file implementation agent"),
            ("planner.md", "Implementation planning specialist agent"),
            ("playwright-validator.md", "Playwright E2E validation agent"),
            ("scout-report-suggest.md", "Codebase scouting and analysis agent"),
            ("scout-report-suggest-fast.md", "Fast codebase scouting agent (haiku)"),
        ]
        for agent, reason in agents:
            plan.add_file(
                f".claude/agents/{agent}",
                action=action,
                template=f"claude/agents/{agent}.j2",
                reason=reason,
            )

        # Output style presets
        output_styles = [
            ("concise-done.md", "Concise output with done confirmation"),
            ("concise-ultra.md", "Ultra-concise minimal output"),
            ("concise-tts.md", "TTS-optimized concise output"),
            ("verbose-bullet-points.md", "Verbose bullet-point format"),
            ("verbose-yaml-structured.md", "Verbose YAML-structured output"),
        ]
        for style, reason in output_styles:
            plan.add_file(
                f".claude/output-styles/{style}",
                action=action,
                template=f"claude/output-styles/{style}.j2",
                reason=reason,
            )

        # Status line
        plan.add_file(
            ".claude/status_lines/status_line_main.py",
            action=action,
            template="claude/status_lines/status_line_main.py.j2",
            reason="Status line script for agent/model/branch display",
            executable=True,
        )

        # ============================================================================
        # TAC-14: SKILLS SYSTEM
        # ============================================================================
        # Skills are self-contained, discoverable automation units with progressive
        # disclosure (metadata → instructions → resources). The meta-skill enables
        # agents to create new skills following best practices.
        # ============================================================================

        # Skills - Meta-skill for creating new skills
        plan.add_file(
            ".claude/skills/meta-skill/SKILL.md",
            action=action,
            template="claude/skills/meta-skill/SKILL.md.j2",
            reason="Meta-skill for creating agent skills",
        )

        # Skills documentation (static resources)
        skills_docs = [
            ("claude_code_agent_skills.md", "Complete skills guide"),
            ("claude_code_agent_skills_overview.md", "Skills architecture"),
            ("blog_equipping_agents_with_skills.md", "Skills design principles"),
        ]
        for doc, reason in skills_docs:
            plan.add_file(
                f".claude/skills/meta-skill/docs/{doc}",
                action=action,
                template=f"claude/skills/meta-skill/docs/{doc}.j2",
                reason=reason,
            )

        # Skills - Start orchestrator (TAC-14)
        plan.add_file(
            ".claude/skills/start-orchestrator/SKILL.md",
            action=action,
            template="claude/skills/start-orchestrator/SKILL.md.j2",
            reason="Skill for launching orchestrator services",
        )

        # ============================================================================
        # TAC-13: AGENT EXPERT COMMANDS
        # ============================================================================
        # Expert agents are self-learning command templates that maintain expertise files.
        # Each expert has 3 components:
        #   1. question.md    - Read-only Q&A using expertise file + codebase validation
        #   2. self-improve.md - 7-phase self-improvement workflow
        #   3. expertise.yaml  - Mental model (working memory, not source of truth)
        #
        # Pattern: experts/<domain>/{question,self-improve,expertise}.*
        # Domains: cli, adw, commands, cc_hook_expert
        # ============================================================================

        # --- Hook Expert (pre-existing): Claude Code hooks implementation ---
        expert_commands = [
            ("experts/cc_hook_expert/cc_hook_expert_plan.md", "Hook expert planning command"),
            ("experts/cc_hook_expert/cc_hook_expert_build.md", "Hook expert build command"),
            ("experts/cc_hook_expert/cc_hook_expert_improve.md", "Hook expert improvement command"),
        ]

        # --- CLI Expert (Tasks 4-6): TAC Bootstrap CLI architecture ---
        expert_commands.extend([
            ("experts/cli/question.md", "CLI expert question prompt for read-only queries"),
            ("experts/cli/self-improve.md", "CLI expert 7-phase self-improve workflow"),
        ])

        # --- ADW Expert (Tasks 7-9): AI Developer Workflows ---
        expert_commands.extend([
            ("experts/adw/question.md", "ADW expert question prompt for workflow queries"),
            ("experts/adw/self-improve.md", "ADW expert 7-phase self-improve workflow"),
        ])

        # --- Commands Expert (Tasks 10-12): .claude/commands/* structure ---
        expert_commands.extend([
            (
                "experts/commands/question.md",
                "Commands expert question prompt for command structure queries",
            ),
            ("experts/commands/self-improve.md", "Commands expert 7-phase self-improve workflow"),
        ])

        # Register all expert command .md files
        for cmd, reason in expert_commands:
            plan.add_file(
                f".claude/commands/{cmd}",
                action=action,
                template=f"claude/commands/{cmd}.j2",
                reason=reason,
            )

        # Register expert expertise seed files (don't overwrite if exists)
        expertise_files = [
            ("cli", "CLI expert expertise seed file"),
            ("adw", "ADW expert expertise seed file"),
            ("commands", "Commands expert expertise seed file"),
        ]
        for domain, reason in expertise_files:
            plan.add_file(
                f".claude/commands/experts/{domain}/expertise.yaml",
                action=FileAction.CREATE,  # Don't overwrite if exists
                template=f"claude/commands/experts/{domain}/expertise.yaml.j2",
                reason=reason,
            )

        # E2E test command examples
        e2e_commands = [
            ("e2e/README.md", "E2E test examples documentation"),
            ("e2e/test_basic_query.md", "E2E test: basic query execution"),
            ("e2e/test_complex_query.md", "E2E test: complex query filtering"),
            ("e2e/test_disable_input_debounce.md", "E2E test: input disabling and debouncing"),
            ("e2e/test_export_functionality.md", "E2E test: export functionality"),
            ("e2e/test_sql_injection.md", "E2E test: SQL injection protection"),
            ("e2e/test_random_query_generator.md", "E2E test: random query generator"),
        ]
        for cmd, reason in e2e_commands:
            plan.add_file(
                f".claude/commands/{cmd}",
                action=action,
                template=f"claude/commands/{cmd}.j2",
                reason=reason,
            )

        # Settings local override
        plan.add_file(
            ".claude/settings.local.json",
            action=action,
            template="claude/settings.local.json.j2",
            reason="Local settings override for output style",
        )

    def _add_adw_files(self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool) -> None:
        """Add adws/ workflow files."""
        action = FileAction.CREATE  # CREATE only creates if file doesn't exist
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
            ("adw_agent_sdk.py", "Agent SDK type-safe layer"),
            ("agent.py", "Claude Code wrapper"),
            ("state.py", "State persistence"),
            ("git_ops.py", "Git operations"),
            ("workflow_ops.py", "Workflow orchestration"),
            ("data_types.py", "Data models and types"),
            ("github.py", "GitHub API operations"),
            ("utils.py", "Utility functions"),
            ("worktree_ops.py", "Git worktree management"),
            ("r2_uploader.py", "Cloudflare R2 uploader"),
            ("tool_sequencer.py", "Tool sequence orchestration"),
            ("orch_database_models.py", "SQLite database models for orchestrator (TAC-14)"),
            ("adw_database.py", "SQLite database operations with aiosqlite (TAC-14)"),
            ("adw_logging.py", "Structured database logging for workflows (TAC-14)"),
            ("adw_websockets.py", "WebSocket server for real-time event broadcasting (TAC-14)"),
            ("adw_db_bridge.py", "Sync SQLite bridge for workflow tracking (TAC-14)"),
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
        plan.add_file(
            f"{adws_dir}/adw_triggers/trigger_webhook.py",
            action=action,
            template="adws/adw_triggers/trigger_webhook.py.j2",
            reason="Webhook-based task trigger",
            executable=True,
        )
        plan.add_file(
            f"{adws_dir}/adw_triggers/trigger_issue_chain.py",
            action=action,
            template="adws/adw_triggers/trigger_issue_chain.py.j2",
            reason="Chain processing for GitHub issues",
            executable=True,
        )
        plan.add_file(
            f"{adws_dir}/adw_triggers/trigger_issue_parallel.py",
            action=action,
            template="adws/adw_triggers/trigger_issue_parallel.py.j2",
            reason="Parallel processing for GitHub issues",
            executable=True,
        )
        plan.add_file(
            f"{adws_dir}/adw_triggers/trigger_plan_parallel.py",
            action=action,
            template="adws/adw_triggers/trigger_plan_parallel.py.j2",
            reason="Parallel execution of tasks from plan files",
            executable=True,
        )

    def _add_adw_workflow_files(
        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool
    ) -> None:
        """Add consolidated workflow templates to plan (TAC-14 Task 10).

        Adds three database-backed orchestration workflows:
        - adw_plan_build.py: Basic Plan → Build orchestration
        - adw_plan_build_review.py: Plan → Build → Review with validation
        - adw_plan_build_review_fix.py: Plan → Build → Review → Fix with self-healing
        """
        action = FileAction.CREATE  # CREATE only creates if file doesn't exist
        adws_dir = config.paths.adws_dir

        workflows = [
            ("adw_plan_build.py", "Plan + Build workflow with database logging"),
            (
                "adw_plan_build_review.py",
                "Plan + Build + Review workflow with database logging",
            ),
            (
                "adw_plan_build_review_fix.py",
                "Plan + Build + Review + Fix workflow with database logging",
            ),
        ]

        for workflow, reason in workflows:
            plan.add_file(
                f"{adws_dir}/adw_workflows/{workflow}",
                action=action,
                template=f"adws/adw_workflows/{workflow}.j2",
                reason=reason,
                executable=True,
            )

    def _add_schema_files(self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool) -> None:
        """Add adws/schema/ database schema files.

        Creates SQLite schema for orchestrator database (TAC-14 Task 6):
        - schema_orchestrator.sql: Complete schema with 5 tables, triggers, indexes
        - README.md: Zero-config documentation, data types, migrations guide
        - migrations/.gitkeep: Preserve migrations directory in git
        """
        action = FileAction.CREATE  # CREATE only creates if file doesn't exist
        adws_dir = config.paths.adws_dir

        # Schema SQL file
        plan.add_file(
            f"{adws_dir}/schema/schema_orchestrator.sql",
            action=action,
            template="adws/schema/schema_orchestrator.sql.j2",
            reason="SQLite orchestrator database schema",
        )

        # Schema README
        plan.add_file(
            f"{adws_dir}/schema/README.md",
            action=action,
            template="adws/schema/README.md.j2",
            reason="Database schema documentation",
        )

        # Migrations directory .gitkeep
        plan.add_file(
            f"{adws_dir}/schema/migrations/.gitkeep",
            action=action,
            template="adws/schema/migrations/.gitkeep",
            reason="Preserve migrations directory in git",
        )

    def _add_script_files(self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool) -> None:
        """Add scripts/ utility files."""
        action = FileAction.CREATE  # CREATE only creates if file doesn't exist
        scripts_dir = config.paths.scripts_dir

        scripts = [
            ("start.sh", "Application starter"),
            ("test.sh", "Test runner"),
            ("lint.sh", "Linter runner"),
            ("build.sh", "Build script"),
            ("setup_worktree.sh", "Worktree environment setup for ADW workflows"),
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
        action = FileAction.CREATE  # CREATE only creates if file doesn't exist

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
        action = FileAction.CREATE  # CREATE only creates if file doesn't exist

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
            (
                "ai_docs/anthropic_quick_start.md",
                "structure/ai_docs/anthropic_quick_start.md.j2",
                "Anthropic API quickstart",
            ),
            (
                "ai_docs/claude_code_cli_reference.md",
                "structure/ai_docs/claude_code_cli_reference.md.j2",
                "Claude Code CLI reference",
            ),
            (
                "ai_docs/claude_code_sdk.md",
                "structure/ai_docs/claude_code_sdk.md.j2",
                "Claude Code SDK documentation",
            ),
            (
                "ai_docs/claude-code-hooks.md",
                "structure/ai_docs/claude-code-hooks.md.j2",
                "Claude Code hooks reference",
            ),
            (
                "ai_docs/e2b.md",
                "structure/ai_docs/e2b.md.j2",
                "E2B sandbox documentation",
            ),
            (
                "ai_docs/mcp-python-sdk.md",
                "structure/ai_docs/mcp-python-sdk.md.j2",
                "MCP Python SDK documentation",
            ),
            (
                "ai_docs/openai_quick_start.md",
                "structure/ai_docs/openai_quick_start.md.j2",
                "OpenAI API quickstart",
            ),
            (
                "ai_docs/uv-scripts.md",
                "structure/ai_docs/uv-scripts.md.j2",
                "UV scripts guide",
            ),
            (
                "ai_docs/ddd.md",
                "structure/ai_docs/ddd.md.j2",
                "Domain-Driven Design reference",
            ),
            (
                "ai_docs/design_patterns.md",
                "structure/ai_docs/design_patterns.md.j2",
                "Design patterns reference",
            ),
            (
                "ai_docs/solid.md",
                "structure/ai_docs/solid.md.j2",
                "SOLID principles reference",
            ),
            (
                "ai_docs/ddd_lite.md",
                "structure/ai_docs/ddd_lite.md.j2",
                "DDD Lite vertical slice architecture reference",
            ),
            (
                "ai_docs/fractal_docs.md",
                "structure/ai_docs/fractal_docs.md.j2",
                "Fractal documentation system reference",
            ),
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
            (
                "app_docs/agentic_kpis.md",
                "structure/app_docs/agentic_kpis.md.j2",
                "ADW performance metrics",
            ),
        ]

        for path, template, reason in app_docs_files:
            plan.add_file(
                path,
                action=action,
                template=template,
                reason=reason,
            )

    def _add_fractal_docs_scripts(self, plan: ScaffoldPlan, config: TACConfig) -> None:
        """Add fractal documentation generation scripts."""
        action = FileAction.CREATE  # CREATE only creates if file doesn't exist

        # Scripts
        plan.add_file(
            f"{config.paths.scripts_dir}/gen_docstring_jsdocs.py",
            action=action,
            template="scripts/gen_docstring_jsdocs.py.j2",
            reason="Docstring/JSDoc generator",
            executable=True,
        )
        plan.add_file(
            f"{config.paths.scripts_dir}/gen_docs_fractal.py",
            action=action,
            template="scripts/gen_docs_fractal.py.j2",
            reason="Fractal documentation generator",
            executable=True,
        )
        plan.add_file(
            f"{config.paths.scripts_dir}/run_generators.sh",
            action=action,
            template="scripts/run_generators.sh.j2",
            reason="Run all documentation generators",
            executable=True,
        )

        # Canonical IDK vocabulary
        plan.add_file(
            "canonical_idk.yml",
            action=action,
            template="config/canonical_idk.yml.j2",
            reason="Canonical IDK vocabulary for fractal docs",
        )

        # Slash command
        plan.add_file(
            ".claude/commands/generate_fractal_docs.md",
            action=action,
            template="claude/commands/generate_fractal_docs.md.j2",
            reason="/generate_fractal_docs slash command",
        )

        # Docs directory
        plan.add_directory("docs", "Fractal documentation output")

    def _add_orchestrator_backend(
        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool
    ) -> None:
        """Add apps/orchestrator_3_stream/backend/ FastAPI backend files (TAC-14 Task 12).

        Adds FastAPI backend with SQLite persistence:
        - main.py: FastAPI app with DatabaseManager lifespan
        - routers/: CQRS endpoints for agents, runtime, WebSocket
        - dependencies.py: Dependency injection
        - .env.sample: Environment variables template
        """
        action = FileAction.CREATE  # CREATE only creates if file doesn't exist

        # Add directory structure
        plan.add_directory("apps/orchestrator_3_stream/backend", "Orchestrator web backend")
        plan.add_directory("apps/orchestrator_3_stream/backend/routers", "FastAPI routers")

        # Add main files
        plan.add_file(
            "apps/orchestrator_3_stream/backend/__init__.py",
            action=action,
            template="apps/orchestrator_3_stream/backend/__init__.py.j2",
            reason="Orchestrator package init",
        )
        plan.add_file(
            "apps/orchestrator_3_stream/backend/main.py",
            action=action,
            template="apps/orchestrator_3_stream/backend/main.py.j2",
            reason="FastAPI app with lifespan manager",
        )
        plan.add_file(
            "apps/orchestrator_3_stream/backend/dependencies.py",
            action=action,
            template="apps/orchestrator_3_stream/backend/dependencies.py.j2",
            reason="FastAPI dependency injection",
        )
        plan.add_file(
            "apps/orchestrator_3_stream/backend/.env.sample",
            action=action,
            template="apps/orchestrator_3_stream/backend/.env.sample",
            reason="Environment variables template",
        )

        # Add routers
        plan.add_file(
            "apps/orchestrator_3_stream/backend/routers/__init__.py",
            action=action,
            template="apps/orchestrator_3_stream/backend/routers/__init__.py.j2",
            reason="Routers package init",
        )
        plan.add_file(
            "apps/orchestrator_3_stream/backend/routers/agents.py",
            action=action,
            template="apps/orchestrator_3_stream/backend/routers/agents.py.j2",
            reason="CQRS endpoints for orchestrator agents",
        )
        plan.add_file(
            "apps/orchestrator_3_stream/backend/routers/runtime.py",
            action=action,
            template="apps/orchestrator_3_stream/backend/routers/runtime.py.j2",
            reason="Endpoints for runtime agents and logs",
        )
        plan.add_file(
            "apps/orchestrator_3_stream/backend/routers/websocket.py",
            action=action,
            template="apps/orchestrator_3_stream/backend/routers/websocket.py.j2",
            reason="WebSocket for real-time updates",
        )
        plan.add_file(
            "apps/orchestrator_3_stream/backend/routers/compat.py",
            action=action,
            template="apps/orchestrator_3_stream/backend/routers/compat.py.j2",
            reason="TAC-14 compatible endpoints for tac-14 frontend",
        )
        plan.add_file(
            "apps/orchestrator_3_stream/backend/config.py",
            action=action,
            template="apps/orchestrator_3_stream/backend/config.py.j2",
            reason="Orchestrator configuration management",
        )
        plan.add_file(
            "apps/orchestrator_3_stream/backend/logger.py",
            action=action,
            template="apps/orchestrator_3_stream/backend/logger.py.j2",
            reason="Orchestrator structured logger",
        )

    def _add_orchestrator_frontend(
        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool
    ) -> None:
        """Add orchestrator frontend Vue 3 + TypeScript files (TAC-14 Task 13).

        Adds Vue 3 SPA with Pinia state management and WebSocket integration:
        - package.json: Vue 3, Pinia, Axios dependencies
        - vite.config.ts.j2: Build configuration with template variables
        - src/main.ts: Vue app initialization
        - src/App.vue: Root component with 3-column layout
        - src/stores/: Pinia orchestrator store
        - src/services/: Chat, Agent, ADW, Event, Autocomplete services
        - src/components/: Vue SFC components (AdwSwimlanes, EventStream, etc.)
        - src/composables/: Vue composition functions (agent pulse, filters, etc.)
        - .env.j2: Templated environment variables
        """
        action = FileAction.CREATE  # CREATE only creates if file doesn't exist

        # Add directory structure
        plan.add_directory("apps", "Application projects")
        plan.add_directory("apps/orchestrator_3_stream", "Orchestrator application")
        plan.add_directory("apps/orchestrator_3_stream/frontend", "Orchestrator web frontend")

        # Add frontend config files from template
        plan.add_file(
            "apps/orchestrator_3_stream/frontend/package.json",
            action=action,
            template="apps/orchestrator_3_stream/frontend/package.json",
            reason="Frontend dependencies",
        )
        plan.add_file(
            "apps/orchestrator_3_stream/frontend/.env",
            action=action,
            template="apps/orchestrator_3_stream/frontend/.env.j2",
            reason="Templated environment variables",
        )
        plan.add_file(
            "apps/orchestrator_3_stream/frontend/vite.config.ts",
            action=action,
            template="apps/orchestrator_3_stream/frontend/vite.config.ts.j2",
            reason="Templated Vite configuration",
        )
        plan.add_file(
            "apps/orchestrator_3_stream/frontend/index.html",
            action=action,
            template="apps/orchestrator_3_stream/frontend/index.html",
            reason="HTML entry point",
        )
        plan.add_file(
            "apps/orchestrator_3_stream/frontend/tsconfig.json",
            action=action,
            template="apps/orchestrator_3_stream/frontend/tsconfig.json",
            reason="TypeScript configuration",
        )
        plan.add_file(
            "apps/orchestrator_3_stream/frontend/tsconfig.node.json",
            action=action,
            template="apps/orchestrator_3_stream/frontend/tsconfig.node.json",
            reason="TypeScript node configuration for Vite",
        )

        # Root-level static files (no Jinja2 rendering needed)
        frontend_root_files = [
            ("env.d.ts", "TypeScript environment declarations for Vue/Vite", False),
            ("start.sh", "Frontend start script", True),
            ("public/favicon.svg", "Application favicon", False),
        ]
        for path, reason, executable in frontend_root_files:
            frontend_path = f"apps/orchestrator_3_stream/frontend/{path}"
            template_path = self.template_repo.templates_dir / frontend_path
            try:
                content = template_path.read_text(encoding="utf-8")
                plan.add_file(
                    frontend_path,
                    action=action,
                    content=content,
                    reason=reason,
                    executable=executable,
                )
            except Exception:
                continue

        # Source files - read as static content to avoid Jinja2/Vue syntax conflicts
        frontend_files = [
            # Core
            ("src/main.ts", "Vue app entry point"),
            ("src/App.vue", "Root component with 3-column layout"),
            ("src/vite-env.d.ts", "Vite environment type declarations"),
            ("src/types.d.ts", "TypeScript type definitions"),
            # Config
            ("src/config/constants.ts", "Application constants"),
            # Styles
            ("src/styles/global.css", "Dark theme CSS with cyan/teal accents"),
            # Store
            ("src/stores/orchestratorStore.ts", "Pinia orchestrator state management"),
            # Services
            ("src/services/api.ts", "Axios API client"),
            ("src/services/chatService.ts", "Chat and WebSocket service"),
            ("src/services/agentService.ts", "Agent management service"),
            ("src/services/adwService.ts", "ADW workflow service"),
            ("src/services/eventService.ts", "Event stream service"),
            ("src/services/autocompleteService.ts", "Autocomplete service"),
            ("src/services/fileService.ts", "File operations service"),
            # Composables
            ("src/composables/useAgentPulse.ts", "Agent pulse animation composable"),
            ("src/composables/useAgentColors.ts", "Agent color assignment composable"),
            ("src/composables/useEventStreamFilter.ts", "Event stream filter composable"),
            ("src/composables/useHeaderBar.ts", "Header bar state composable"),
            ("src/composables/useKeyboardShortcuts.ts", "Keyboard shortcuts composable"),
            ("src/composables/useAutocomplete.ts", "Autocomplete composable"),
            # Utils
            ("src/utils/markdown.ts", "Markdown rendering utility"),
            ("src/utils/agentColors.ts", "Agent color utility"),
            # Components
            ("src/components/AdwSwimlanes.vue", "ADW swimlane board"),
            ("src/components/AgentList.vue", "Agent list sidebar"),
            ("src/components/AppHeader.vue", "Application header bar"),
            ("src/components/EventStream.vue", "Event log stream"),
            ("src/components/FilterControls.vue", "Filter UI controls"),
            ("src/components/GlobalCommandInput.vue", "Command palette overlay"),
            ("src/components/OrchestratorChat.vue", "Chat interface"),
            # Chat sub-components
            ("src/components/chat/ThinkingBubble.vue", "Thinking block bubble"),
            ("src/components/chat/ToolUseBubble.vue", "Tool use block bubble"),
            # Event row sub-components
            ("src/components/event-rows/AgentLogRow.vue", "Agent log event row"),
            ("src/components/event-rows/AgentToolUseBlockRow.vue", "Agent tool use row"),
            ("src/components/event-rows/FileChangesDisplay.vue", "File changes display"),
            ("src/components/event-rows/OrchestratorChatRow.vue", "Orchestrator chat row"),
            ("src/components/event-rows/SystemLogRow.vue", "System log event row"),
            ("src/components/event-rows/ToolUseBlockRow.vue", "Tool use block row"),
        ]

        for path, reason in frontend_files:
            # Read Vue/TypeScript files as static content (don't template them)
            # to avoid Jinja2 conflicts with Vue syntax ({{ }}, @, :class, etc.)
            frontend_path = f"apps/orchestrator_3_stream/frontend/{path}"
            template_path = self.template_repo.templates_dir / frontend_path
            try:
                content = template_path.read_text(encoding='utf-8')
                plan.add_file(
                    frontend_path,
                    action=action,
                    content=content,
                    reason=reason,
                )
            except Exception:
                # If file doesn't exist or can't be read, skip it
                continue

    def _add_test_files(
        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool
    ) -> None:
        """Add test suites for ADW modules and orchestrator frontend (TAC-14 Task 15).

        Adds:
        - adws/adw_tests/: Pytest fixtures and tests for database, workflows, agent SDK, websockets
        - apps/orchestrator_3_stream/playwright-tests/: Playwright E2E tests for frontend
        - apps/orchestrator_3_stream/playwright.config.ts: Playwright configuration
        """
        action = FileAction.CREATE  # CREATE only creates if file doesn't exist
        adws_dir = config.paths.adws_dir

        # Add test directory structure
        plan.add_directory(f"{adws_dir}/adw_tests", "ADW pytest test suite")
        plan.add_directory(
            "apps/orchestrator_3_stream/playwright-tests", "Playwright E2E tests"
        )

        # Pytest test files
        pytest_files = [
            ("conftest.py", "Pytest fixtures and configuration"),
            ("pytest.ini", "Pytest settings"),
            ("test_database.py", "Database module tests"),
            ("test_workflows.py", "Workflow operations tests"),
            ("test_agent_sdk.py", "Agent SDK abstraction tests"),
            ("test_websockets.py", "WebSocket server tests"),
        ]

        for file, reason in pytest_files:
            plan.add_file(
                f"{adws_dir}/adw_tests/{file}",
                action=action,
                template=f"adws/adw_tests/{file}.j2",
                reason=reason,
            )

        # Playwright configuration
        plan.add_file(
            "apps/orchestrator_3_stream/playwright.config.ts",
            action=action,
            template="apps/orchestrator_3_stream/playwright.config.ts.j2",
            reason="Playwright E2E test configuration",
        )

        # Playwright E2E test files
        playwright_tests = [
            ("app-loads.spec.ts", "Application loading tests"),
            ("command-palette.spec.ts", "Command palette tests"),
            ("websocket-status.spec.ts", "WebSocket status tests"),
            ("swimlane-board.spec.ts", "Swimlane board tests"),
            ("keyboard-navigation.spec.ts", "Keyboard navigation tests"),
            ("visual-styling.spec.ts", "Visual styling tests"),
        ]

        for file, reason in playwright_tests:
            # Read static TypeScript files (no Jinja templating needed)
            test_path = f"apps/orchestrator_3_stream/playwright-tests/{file}"
            template_path = self.template_repo.templates_dir / test_path
            try:
                content = template_path.read_text(encoding='utf-8')
                plan.add_file(
                    test_path,
                    action=action,
                    content=content,
                    reason=reason,
                )
            except Exception:
                # If file doesn't exist, skip it
                continue

    def _add_orchestrator_scripts(self, plan: ScaffoldPlan, config: TACConfig) -> None:
        """Add orchestrator utility scripts (TAC-14 Task 19)."""
        scripts_dir = config.paths.scripts_dir
        plan.add_file(
            f"{scripts_dir}/setup_database.sh",
            action=FileAction.CREATE,
            template="scripts/setup_database.sh.j2",
            reason="SQLite database initialization script",
            executable=True,
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
        from datetime import datetime, timezone

        from rich.console import Console

        from tac_bootstrap.infrastructure.fs import FileSystem

        # Pre-scaffold validation gate
        console = Console()
        validation = self.validation_service.validate_pre_scaffold(config, output_dir)

        if not validation.valid:
            raise ScaffoldValidationError(validation)

        # Show warnings but continue
        if validation.warnings():
            for warning in validation.warnings():
                console.print(f"[yellow]Warning: {warning.message}[/yellow]")

        # Register bootstrap metadata before rendering templates
        # This enables audit trail for when/how the project was generated
        try:
            from tac_bootstrap import __version__
        except ImportError:
            __version__ = "unknown"

        from tac_bootstrap.domain.models import BootstrapMetadata

        # Handle metadata for initial generation vs upgrade
        if config.metadata is not None:
            # This is an upgrade - preserve original generated_at and update last_upgrade
            original_generated_at = config.metadata.generated_at
            config.metadata = BootstrapMetadata(
                generated_at=original_generated_at,
                generated_by=f"tac-bootstrap v{__version__}",
                schema_version=2,
                last_upgrade=datetime.now(timezone.utc).isoformat(),
            )
        else:
            # This is initial generation
            config.metadata = BootstrapMetadata(
                generated_at=datetime.now(timezone.utc).isoformat(),
                generated_by=f"tac-bootstrap v{__version__}",
                schema_version=2,
                last_upgrade=None,  # Not set on initial generation, only on upgrade
            )

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
