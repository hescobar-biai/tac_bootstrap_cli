"""
IDK: scaffold-service, plan-builder, code-generation, template-rendering,
     file-operations, expert-registration
Responsibility: Builds scaffold plans from TACConfig and applies them to filesystem,
                including TAC-13 expert agent templates
Invariants: Plans are idempotent, templates must exist, output directory must be writable,
            expert templates follow 3-component pattern
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional

from tac_bootstrap.application.exceptions import ScaffoldValidationError

if TYPE_CHECKING:
    from tac_bootstrap.infrastructure.telemetry import TelemetryService
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
        telemetry: Optional["TelemetryService"] = None,
    ):
        """Initialize scaffold service.

        Args:
            template_repo: Template repository (created if not provided)
            validation_service: Validation service (created if not provided)
            telemetry: Optional TelemetryService instance for usage tracking
        """
        self.template_repo = template_repo or TemplateRepository()
        self.validation_service = validation_service or ValidationService(self.template_repo)
        self.telemetry = telemetry

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
        import time

        start_time = time.time()
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
            # Add apps/ directories as bulk copy (orchestrator_3_stream + orchestrator_db)
            self._add_orchestrator_apps(plan, config, existing_repo)

            # Add ADW test suites (TAC-14 Task 15)
            self._add_test_files(plan, config, existing_repo)

            # Add orchestrator utility scripts (TAC-14 Task 19)
            self._add_orchestrator_scripts(plan, config, existing_repo)

            # Add orchestrator Makefile (TAC-14)
            plan.add_file(
                "Makefile",
                action=FileAction.OVERWRITE if existing_repo else FileAction.CREATE,
                template="Makefile.j2",
                reason="Orchestrator build and run commands",
            )

        # Track build_plan performance
        duration_ms = (time.time() - start_time) * 1000
        if self.telemetry:
            self.telemetry.track_performance("scaffold_plan_build", duration_ms)

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
            (".claude/commands/experts/database", "Database expert: schema and operations"),
            (".claude/commands/experts/websocket", "WebSocket expert: real-time communication"),
            (".claude/commands/experts/data-engineering", "Data engineering expert: dbt, BigQuery, ETL"),
            (".claude/commands/experts/ml-forecasting", "ML forecasting expert: demand forecasting, models"),
            (".claude/commands/experts/gcp-infra", "GCP infrastructure expert: Terraform, IAM, Cloud"),
            (".claude/commands/experts/react-frontend", "React frontend expert: components, dashboards"),
            (".claude/agents", "Agent definitions"),
            (".claude/output-styles", "Output style presets"),
            (".claude/status_lines", "Claude Code status line definitions"),
            (".claude/skills", "Agent skills directory"),
            (".claude/skills/meta-skill", "Meta-skill for creating new skills"),
            (".claude/skills/meta-skill/docs", "Meta-skill documentation resources"),
            (".claude/skills/start-orchestrator", "Start orchestrator skill"),
            # Documentation & planning skills (from celes-support)
            (".claude/skills/generate-prd", "PRD generation skill"),
            (".claude/skills/generate-prd/references", "PRD templates"),
            (".claude/skills/generate-adrs", "ADR generation skill"),
            (".claude/skills/generate-adrs/references", "ADR common decisions"),
            (".claude/skills/generate-tdd", "TDD generation skill"),
            (".claude/skills/generate-tdd/references", "TDD templates"),
            (".claude/skills/generate-roadmap", "Roadmap generation skill"),
            (".claude/skills/generate-roadmap/references", "Roadmap templates"),
            (".claude/skills/generate-tasks", "Task generation skill"),
            (".claude/skills/generate-tasks/references", "Task generation templates"),
            (".claude/skills/generating-fractal-docs", "Fractal documentation skill"),
            (".claude/skills/generating-fractal-docs/scripts", "Fractal docs scripts"),
            (".claude/skills/product-issues", "Product issue classification skill"),
            (".claude/skills/product-issues/reference", "Issue type templates"),
            # DDD pattern skills (from celes-support)
            (".claude/skills/create-crud-entity", "CRUD entity generation skill"),
            (".claude/skills/create-crud-entity/shared", "Shared base classes"),
            (".claude/skills/create-crud-entity/templates", "CRUD entity templates"),
            (".claude/skills/create-domain-service", "Domain service skill"),
            (".claude/skills/create-domain-service/templates", "Domain service templates"),
            (".claude/skills/create-value-object", "Value object skill"),
            (".claude/skills/create-value-object/templates", "Value object templates"),
            (".claude/skills/create-domain-event", "Domain event skill"),
            (".claude/skills/create-domain-event/templates", "Domain event templates"),
            (".claude/skills/create-provider-adapter", "Provider adapter skill"),
            (".claude/skills/create-provider-adapter/templates", "Provider adapter templates"),
            (".claude/skills/create-strategy-pattern", "Strategy pattern skill"),
            (".claude/skills/create-strategy-pattern/templates", "Strategy pattern templates"),
            (".claude/skills/create-caching-layer", "Caching layer skill"),
            (".claude/skills/create-caching-layer/templates", "Caching templates"),
            (".claude/skills/create-middleware-decorator", "Middleware decorator skill"),
            (".claude/skills/create-middleware-decorator/templates", "Middleware templates"),
            (".claude/skills/create-comparison-analyzer", "Comparison analyzer skill"),
            (".claude/skills/create-comparison-analyzer/templates", "Analyzer templates"),
            # Frontend scaffolding skills (from celes-support)
            (".claude/skills/scaffold-ui-component", "UI component scaffolding skill"),
            (".claude/skills/scaffold-chart-component", "Chart component scaffolding skill"),
            (".claude/skills/scaffold-chart-component/references", "Chart patterns"),
            (".claude/skills/scaffold-frontend-page", "Frontend page scaffolding skill"),
            (".claude/skills/scaffold-frontend-page/references", "Page patterns"),
            # Infrastructure scaffolding skills (from celes-support)
            (".claude/skills/scaffold-docker-stack", "Docker stack scaffolding skill"),
            (".claude/skills/scaffold-docker-stack/assets", "Docker template assets"),
            (".claude/skills/scaffold-backend-service", "Backend service scaffolding skill"),
            (".claude/skills/scaffold-backend-service/references", "Backend service patterns"),
            (".claude/skills/scaffold-project", "Project orchestrator skill"),
            (".claude/skills/scaffold-project/references", "Project phase map"),
            # Meta skills (from celes-support)
            (".claude/skills/skill-creator", "Skill creation guide"),
            (".claude/skills/skill-creator/references", "Skill creator references"),
            (".claude/skills/skill-creator/scripts", "Skill creator scripts"),
            # Celes stack skills (v1.1.0)
            (".claude/skills/bigquery-ops", "BigQuery operations skill"),
            (".claude/skills/bigquery-ops/examples", "BigQuery query examples"),
            (".claude/skills/dbt-workflow", "dbt workflow skill"),
            (".claude/skills/dbt-workflow/templates", "dbt model templates"),
            (".claude/skills/dbt-workflow/examples", "dbt model examples"),
            (".claude/skills/ml-forecast", "ML forecasting skill"),
            (".claude/skills/ml-forecast/templates", "ML pipeline templates"),
            (".claude/skills/ml-forecast/examples", "ML forecasting examples"),
            (".claude/skills/fastapi-ddd", "FastAPI DDD skill"),
            (".claude/skills/fastapi-ddd/templates", "DDD component templates"),
            (".claude/skills/react-frontend", "React frontend skill"),
            (".claude/skills/react-frontend/templates", "React component templates"),
            (".claude/skills/gcp-infra", "GCP infrastructure skill"),
            (".claude/skills/gcp-infra/templates", "Terraform module templates"),
            (".claude/skills/aws-ops", "AWS operations skill"),
            (".claude/skills/data-pipeline", "Data pipeline skill"),
            (".claude/skills/data-pipeline/templates", "Pipeline templates"),
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
            "create-gh-issue",
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
            # Additional utility commands
            "fix",
            "ping",
            "prime_nile",
            "prime_specific_docs",
            "question-w-mermaid-diagrams",
            "start_nile",
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
            # Celes stack agents (v1.1.0)
            ("data-engineer.md", "Data engineering agent (dbt, BigQuery, pipelines)"),
            ("ml-engineer.md", "ML engineering agent (demand forecasting, multi-framework)"),
            ("infra-ops.md", "Infrastructure operations agent (GCP/AWS, Terraform)"),
            ("frontend-engineer.md", "Frontend engineering agent (React 19, TanStack Query)"),
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
            ("bullet-points.md", "Bullet-point output format"),
            ("genui.md", "GenUI output format"),
            ("html-structured.md", "HTML-structured output format"),
            ("markdown-focused.md", "Markdown-focused output format"),
            ("observable-tools-diffs-tts.md", "Observable tools diffs with TTS"),
            ("observable-tools-diffs.md", "Observable tools diffs output"),
            ("table-based.md", "Table-based output format"),
            ("tts-summary-base.md", "TTS summary base format"),
            ("tts-summary.md", "TTS summary output format"),
            ("ultra-concise.md", "Ultra-concise output format"),
            ("yaml-structured.md", "YAML-structured output format"),
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
        # CELES STACK SKILLS (v1.1.0)
        # ============================================================================
        # Specialized skills for the Celes supply chain AI stack:
        # bigquery-ops, dbt-workflow, ml-forecast, fastapi-ddd,
        # react-frontend, gcp-infra, aws-ops, data-pipeline
        # ============================================================================

        # --- bigquery-ops: BigQuery datasets, tables, and queries ---
        _bq_files = [
            ("SKILL.md", "BigQuery operations skill"),
            ("reference.md", "BigQuery best practices reference"),
            ("examples/supply_chain_queries.sql", "Supply chain BigQuery query examples"),
        ]
        for fname, reason in _bq_files:
            plan.add_file(
                f".claude/skills/bigquery-ops/{fname}",
                action=action,
                template=f"claude/skills/bigquery-ops/{fname}.j2",
                reason=reason,
            )

        # --- dbt-workflow: dbt models, tests, dual-target BQ+PG ---
        _dbt_files = [
            ("SKILL.md", "dbt workflow skill"),
            ("reference.md", "dbt conventions and patterns reference"),
            ("templates/stg_template.sql", "dbt staging model template"),
            ("templates/fct_template.sql", "dbt fact model template"),
            ("templates/schema_template.yml", "dbt schema YAML template"),
            ("examples/stg_orders.sql", "dbt staging model example"),
            ("examples/fct_demand.sql", "dbt fact model example"),
            ("examples/dim_products.sql", "dbt dimension model example"),
            ("templates/agg_template.sql", "dbt aggregation model template"),
            ("examples/stg_products.sql", "dbt staging products example"),
            ("examples/dm_supply_chain.sql", "dbt supply chain data mart example"),
        ]
        for fname, reason in _dbt_files:
            plan.add_file(
                f".claude/skills/dbt-workflow/{fname}",
                action=action,
                template=f"claude/skills/dbt-workflow/{fname}.j2",
                reason=reason,
            )

        # --- ml-forecast: ML/forecasting multi-framework ---
        _ml_files = [
            ("SKILL.md", "ML forecasting skill"),
            ("reference.md", "ML forecasting patterns reference"),
            ("templates/train_pipeline.py", "ML training pipeline template"),
            ("templates/evaluate.py", "ML evaluation pipeline template"),
            ("examples/demand_forecast_lightgbm.py", "LightGBM forecasting example"),
            ("examples/demand_forecast_prophet.py", "Prophet forecasting example"),
        ]
        for fname, reason in _ml_files:
            plan.add_file(
                f".claude/skills/ml-forecast/{fname}",
                action=action,
                template=f"claude/skills/ml-forecast/{fname}.j2",
                reason=reason,
            )

        # --- fastapi-ddd: FastAPI + Domain-Driven Design ---
        _fastapi_files = [
            ("SKILL.md", "FastAPI DDD skill"),
            ("reference.md", "FastAPI DDD patterns reference"),
            ("templates/entity.py", "DDD entity template"),
            ("templates/repository.py", "DDD repository template"),
            ("templates/service.py", "DDD service template"),
            ("templates/routes.py", "FastAPI routes template"),
            ("templates/schemas.py", "Pydantic schemas template"),
        ]
        for fname, reason in _fastapi_files:
            plan.add_file(
                f".claude/skills/fastapi-ddd/{fname}",
                action=action,
                template=f"claude/skills/fastapi-ddd/{fname}.j2",
                reason=reason,
            )

        # --- react-frontend: React 19 + Celes stack ---
        _react_files = [
            ("SKILL.md", "React frontend skill (Celes stack)"),
            ("reference.md", "React frontend comprehensive reference"),
            ("templates/Component.tsx", "React component template (Celes theme)"),
            ("templates/useDataHook.ts", "Ky + TanStack Query data hook template"),
            ("templates/DashboardPage.tsx", "Dashboard page with DataTable.Root template"),
        ]
        for fname, reason in _react_files:
            plan.add_file(
                f".claude/skills/react-frontend/{fname}",
                action=action,
                template=f"claude/skills/react-frontend/{fname}.j2",
                reason=reason,
            )

        # --- gcp-infra: GCP infrastructure ---
        _gcp_files = [
            ("SKILL.md", "GCP infrastructure skill"),
            ("reference.md", "GCP infrastructure patterns reference"),
            ("templates/main.tf", "Terraform main configuration template"),
            ("templates/bigquery.tf", "Terraform BigQuery resources template"),
            ("templates/storage.tf", "Terraform Cloud Storage template"),
            ("templates/cloudrun.tf", "Terraform Cloud Run template"),
            ("templates/iam_member.tf", "Terraform IAM member module template"),
            ("templates/iam_service_account.tf", "Terraform service account module template"),
            ("templates/iam_role.tf", "Terraform custom IAM role module template"),
        ]
        for fname, reason in _gcp_files:
            plan.add_file(
                f".claude/skills/gcp-infra/{fname}",
                action=action,
                template=f"claude/skills/gcp-infra/{fname}.j2",
                reason=reason,
            )

        # --- aws-ops: AWS infrastructure ---
        _aws_files = [
            ("SKILL.md", "AWS operations skill"),
            ("reference.md", "AWS operations patterns reference"),
        ]
        for fname, reason in _aws_files:
            plan.add_file(
                f".claude/skills/aws-ops/{fname}",
                action=action,
                template=f"claude/skills/aws-ops/{fname}.j2",
                reason=reason,
            )

        # --- data-pipeline: ETL/ELT workflows ---
        _pipeline_files = [
            ("SKILL.md", "Data pipeline skill"),
            ("reference.md", "Data pipeline patterns reference"),
            ("templates/dag_template.py", "Airflow DAG template"),
            ("templates/loader.py", "BigQuery data loader template"),
        ]
        for fname, reason in _pipeline_files:
            plan.add_file(
                f".claude/skills/data-pipeline/{fname}",
                action=action,
                template=f"claude/skills/data-pipeline/{fname}.j2",
                reason=reason,
            )

        # ============================================================================
        # Skills imported from celes-support: documentation, DDD patterns,
        # frontend scaffolding, infrastructure, and meta skills
        # ============================================================================

        # --- generate-prd: Product Requirements Documents ---
        _prd_files = [
            ("SKILL.md", "PRD generation skill"),
            ("references/prd-template.md", "PRD template"),
        ]
        for fname, reason in _prd_files:
            plan.add_file(
                f".claude/skills/generate-prd/{fname}",
                action=action,
                template=f"claude/skills/generate-prd/{fname}.j2",
                reason=reason,
            )

        # --- generate-adrs: Architecture Decision Records ---
        _adrs_files = [
            ("SKILL.md", "ADR generation skill"),
            ("references/common-decisions.md", "ADR common decisions catalog"),
        ]
        for fname, reason in _adrs_files:
            plan.add_file(
                f".claude/skills/generate-adrs/{fname}",
                action=action,
                template=f"claude/skills/generate-adrs/{fname}.j2",
                reason=reason,
            )

        # --- generate-tdd: Technical Design Documents ---
        _tdd_files = [
            ("SKILL.md", "TDD generation skill"),
            ("references/tdd-template.md", "TDD template"),
        ]
        for fname, reason in _tdd_files:
            plan.add_file(
                f".claude/skills/generate-tdd/{fname}",
                action=action,
                template=f"claude/skills/generate-tdd/{fname}.j2",
                reason=reason,
            )

        # --- generate-roadmap: Implementation roadmaps ---
        _roadmap_files = [
            ("SKILL.md", "Roadmap generation skill"),
            ("references/roadmap-template.md", "Roadmap template"),
        ]
        for fname, reason in _roadmap_files:
            plan.add_file(
                f".claude/skills/generate-roadmap/{fname}",
                action=action,
                template=f"claude/skills/generate-roadmap/{fname}.j2",
                reason=reason,
            )

        # --- generate-tasks: Task generation from roadmap ---
        _tasks_files = [
            ("SKILL.md", "Task generation skill"),
            ("references/skill-mapping.md", "Skill-to-task mapping reference"),
            ("references/inline-skill-context-template.md", "Inline skill context template"),
            ("references/execution-template.md", "Execution plan template"),
        ]
        for fname, reason in _tasks_files:
            plan.add_file(
                f".claude/skills/generate-tasks/{fname}",
                action=action,
                template=f"claude/skills/generate-tasks/{fname}.j2",
                reason=reason,
            )

        # --- generating-fractal-docs: Fractal documentation generation ---
        _fractal_docs = [
            ("SKILL.md", "Fractal documentation skill"),
            ("FLAGS.md", "Fractal docs feature flags"),
            ("RUNBOOK.md", "Fractal docs runbook"),
        ]
        for fname, reason in _fractal_docs:
            plan.add_file(
                f".claude/skills/generating-fractal-docs/{fname}",
                action=action,
                template=f"claude/skills/generating-fractal-docs/{fname}.j2",
                reason=reason,
            )
        _fractal_scripts = [
            ("scripts/run_generators.sh", "Documentation generator runner script"),
            ("scripts/gen_docstring_jsdocs.py", "Docstring/JSDoc generator"),
            ("scripts/gen_docs_fractal.py", "Fractal documentation generator"),
        ]
        for fname, reason in _fractal_scripts:
            plan.add_file(
                f".claude/skills/generating-fractal-docs/{fname}",
                action=action,
                template=f"claude/skills/generating-fractal-docs/{fname}.j2",
                reason=reason,
                executable=True,
            )

        # --- product-issues: Issue classification and templates ---
        _issues_files = [
            ("SKILL.md", "Product issue classification skill"),
            ("reference/feature.md", "Feature issue template"),
            ("reference/bug.md", "Bug issue template"),
            ("reference/chore.md", "Chore issue template"),
            ("reference/refactor.md", "Refactor issue template"),
            ("reference/perf.md", "Performance issue template"),
        ]
        for fname, reason in _issues_files:
            plan.add_file(
                f".claude/skills/product-issues/{fname}",
                action=action,
                template=f"claude/skills/product-issues/{fname}.j2",
                reason=reason,
            )

        # --- create-crud-entity: CRUD entity generation (DDD vertical slice) ---
        _crud_files = [
            ("SKILL.md", "CRUD entity generation skill"),
            ("WORKFLOW.md", "CRUD entity workflow guide"),
            ("DOCUMENTATION_STANDARDS.md", "Documentation standards for entities"),
        ]
        _crud_shared = [
            "alembic.py.md", "base_entity.py.md", "base_repository.py.md",
            "base_repository_async.py.md", "base_schema.py.md", "base_service.py.md",
            "config.py.md", "database.py.md", "dependencies.py.md",
            "exceptions.py.md", "health.py.md", "responses.py.md",
        ]
        _crud_templates = [
            "domain_entity.py.md", "domain_events.py.md", "orm_model.py.md",
            "repository.py.md", "repository_authorized.py.md", "routes.py.md",
            "routes_authorized.py.md", "schemas.py.md", "service.py.md",
            "service_authorized.py.md", "tests.py.md", "value_objects.py.md",
        ]
        for fname, reason in _crud_files:
            plan.add_file(
                f".claude/skills/create-crud-entity/{fname}",
                action=action,
                template=f"claude/skills/create-crud-entity/{fname}.j2",
                reason=reason,
            )
        for fname in _crud_shared:
            plan.add_file(
                f".claude/skills/create-crud-entity/shared/{fname}",
                action=action,
                template=f"claude/skills/create-crud-entity/shared/{fname}.j2",
                reason=f"Shared base: {fname}",
            )
        for fname in _crud_templates:
            plan.add_file(
                f".claude/skills/create-crud-entity/templates/{fname}",
                action=action,
                template=f"claude/skills/create-crud-entity/templates/{fname}.j2",
                reason=f"CRUD template: {fname}",
            )

        # --- create-domain-service: Non-CRUD domain services ---
        _dsvc_files = [
            ("SKILL.md", "Domain service creation skill"),
            ("WORKFLOW.md", "Domain service workflow"),
            ("templates/domain_service.py.md", "Domain service template"),
            ("templates/domain_service_test.py.md", "Domain service test template"),
        ]
        for fname, reason in _dsvc_files:
            plan.add_file(
                f".claude/skills/create-domain-service/{fname}",
                action=action,
                template=f"claude/skills/create-domain-service/{fname}.j2",
                reason=reason,
            )

        # --- create-value-object: Frozen Pydantic value objects ---
        _vo_files = [
            ("SKILL.md", "Value object creation skill"),
            ("WORKFLOW.md", "Value object workflow"),
            ("templates/value_object.py.md", "Value object template"),
            ("templates/value_object_test.py.md", "Value object test template"),
        ]
        for fname, reason in _vo_files:
            plan.add_file(
                f".claude/skills/create-value-object/{fname}",
                action=action,
                template=f"claude/skills/create-value-object/{fname}.j2",
                reason=reason,
            )

        # --- create-domain-event: Domain events and handlers ---
        _event_files = [
            ("SKILL.md", "Domain event creation skill"),
            ("WORKFLOW.md", "Domain event workflow"),
            ("templates/domain_event.py.md", "Domain event template"),
            ("templates/event_handler.py.md", "Event handler template"),
            ("templates/event_test.py.md", "Event test template"),
        ]
        for fname, reason in _event_files:
            plan.add_file(
                f".claude/skills/create-domain-event/{fname}",
                action=action,
                template=f"claude/skills/create-domain-event/{fname}.j2",
                reason=reason,
            )

        # --- create-provider-adapter: LLM provider adapters ---
        _adapter_files = [
            ("SKILL.md", "Provider adapter creation skill"),
            ("WORKFLOW.md", "Provider adapter workflow"),
            ("templates/provider_adapter.py.md", "Provider adapter template"),
            ("templates/provider_config.py.md", "Provider config template"),
            ("templates/provider_error_mapping.py.md", "Provider error mapping template"),
            ("templates/provider_test.py.md", "Provider adapter test template"),
        ]
        for fname, reason in _adapter_files:
            plan.add_file(
                f".claude/skills/create-provider-adapter/{fname}",
                action=action,
                template=f"claude/skills/create-provider-adapter/{fname}.j2",
                reason=reason,
            )

        # --- create-strategy-pattern: Strategy pattern scaffolding ---
        _strategy_files = [
            ("SKILL.md", "Strategy pattern creation skill"),
            ("WORKFLOW.md", "Strategy pattern workflow"),
            ("templates/strategy_interface.py.md", "Strategy interface template"),
            ("templates/strategy_concrete.py.md", "Strategy concrete template"),
            ("templates/strategy_factory.py.md", "Strategy factory template"),
            ("templates/strategy_test.py.md", "Strategy test template"),
        ]
        for fname, reason in _strategy_files:
            plan.add_file(
                f".claude/skills/create-strategy-pattern/{fname}",
                action=action,
                template=f"claude/skills/create-strategy-pattern/{fname}.j2",
                reason=reason,
            )

        # --- create-caching-layer: LRU + Redis caching ---
        _cache_files = [
            ("SKILL.md", "Caching layer creation skill"),
            ("WORKFLOW.md", "Caching layer workflow"),
            ("templates/lru_cache.py.md", "LRU cache template"),
            ("templates/async_cache_wrapper.py.md", "Async cache wrapper template"),
            ("templates/redis_cache.py.md", "Redis cache template"),
            ("templates/cache_warmer.py.md", "Cache warmer template"),
            ("templates/cache_test.py.md", "Cache test template"),
        ]
        for fname, reason in _cache_files:
            plan.add_file(
                f".claude/skills/create-caching-layer/{fname}",
                action=action,
                template=f"claude/skills/create-caching-layer/{fname}.j2",
                reason=reason,
            )

        # --- create-middleware-decorator: Middleware and decorators ---
        _middleware_files = [
            ("SKILL.md", "Middleware decorator creation skill"),
            ("WORKFLOW.md", "Middleware decorator workflow"),
            ("templates/fastapi_middleware.py.md", "FastAPI middleware template"),
            ("templates/provider_decorator.py.md", "Provider decorator template"),
            ("templates/middleware_config.py.md", "Middleware config template"),
            ("templates/middleware_test.py.md", "Middleware test template"),
        ]
        for fname, reason in _middleware_files:
            plan.add_file(
                f".claude/skills/create-middleware-decorator/{fname}",
                action=action,
                template=f"claude/skills/create-middleware-decorator/{fname}.j2",
                reason=reason,
            )

        # --- create-comparison-analyzer: Evaluation analyzer service ---
        _analyzer_files = [
            ("SKILL.md", "Comparison analyzer creation skill"),
            ("WORKFLOW.md", "Comparison analyzer workflow"),
            ("templates/analysis_metrics_vo.py.md", "Analysis metrics value object template"),
            ("templates/analyzer_service.py.md", "Analyzer service template"),
            ("templates/analysis_endpoint.py.md", "Analysis endpoint template"),
            ("templates/analyzer_test.py.md", "Analyzer test template"),
        ]
        for fname, reason in _analyzer_files:
            plan.add_file(
                f".claude/skills/create-comparison-analyzer/{fname}",
                action=action,
                template=f"claude/skills/create-comparison-analyzer/{fname}.j2",
                reason=reason,
            )

        # --- scaffold-ui-component: React UI component scaffolding ---
        plan.add_file(
            ".claude/skills/scaffold-ui-component/SKILL.md",
            action=action,
            template="claude/skills/scaffold-ui-component/SKILL.md.j2",
            reason="UI component scaffolding skill",
        )

        # --- scaffold-chart-component: Chart component scaffolding ---
        _chart_files = [
            ("SKILL.md", "Chart component scaffolding skill"),
            ("references/chart-patterns.md", "Chart patterns reference"),
        ]
        for fname, reason in _chart_files:
            plan.add_file(
                f".claude/skills/scaffold-chart-component/{fname}",
                action=action,
                template=f"claude/skills/scaffold-chart-component/{fname}.j2",
                reason=reason,
            )

        # --- scaffold-frontend-page: Frontend page scaffolding ---
        _page_files = [
            ("SKILL.md", "Frontend page scaffolding skill"),
            ("references/page-pattern.md", "Page patterns reference"),
        ]
        for fname, reason in _page_files:
            plan.add_file(
                f".claude/skills/scaffold-frontend-page/{fname}",
                action=action,
                template=f"claude/skills/scaffold-frontend-page/{fname}.j2",
                reason=reason,
            )

        # --- scaffold-docker-stack: Docker Compose stack scaffolding ---
        _docker_files = [
            ("SKILL.md", "Docker stack scaffolding skill"),
            ("assets/docker-compose.template.yml", "Docker Compose template"),
            ("assets/backend.Dockerfile.template", "Backend Dockerfile template"),
            ("assets/frontend.Dockerfile.template", "Frontend Dockerfile template"),
            ("assets/env.example.template", "Environment variables example template"),
        ]
        for fname, reason in _docker_files:
            plan.add_file(
                f".claude/skills/scaffold-docker-stack/{fname}",
                action=action,
                template=f"claude/skills/scaffold-docker-stack/{fname}.j2",
                reason=reason,
            )

        # --- scaffold-backend-service: Backend service scaffolding ---
        _backend_files = [
            ("SKILL.md", "Backend service scaffolding skill"),
            ("references/patterns.md", "Backend service patterns reference"),
        ]
        for fname, reason in _backend_files:
            plan.add_file(
                f".claude/skills/scaffold-backend-service/{fname}",
                action=action,
                template=f"claude/skills/scaffold-backend-service/{fname}.j2",
                reason=reason,
            )

        # --- scaffold-project: Master project orchestrator ---
        _project_files = [
            ("SKILL.md", "Project orchestrator skill"),
            ("references/phase-map.md", "Project scaffolding phase map"),
        ]
        for fname, reason in _project_files:
            plan.add_file(
                f".claude/skills/scaffold-project/{fname}",
                action=action,
                template=f"claude/skills/scaffold-project/{fname}.j2",
                reason=reason,
            )

        # --- skill-creator: Skill creation guide and tools ---
        _creator_docs = [
            ("SKILL.md", "Skill creator guide"),
            ("LICENSE.txt", "Skill creator license"),
            ("references/workflows.md", "Skill creation workflows"),
            ("references/output-patterns.md", "Skill output patterns"),
        ]
        for fname, reason in _creator_docs:
            plan.add_file(
                f".claude/skills/skill-creator/{fname}",
                action=action,
                template=f"claude/skills/skill-creator/{fname}.j2",
                reason=reason,
            )
        _creator_scripts = [
            ("scripts/init_skill.py", "Skill initialization script"),
            ("scripts/package_skill.py", "Skill packaging script"),
            ("scripts/quick_validate.py", "Skill quick validation script"),
        ]
        for fname, reason in _creator_scripts:
            plan.add_file(
                f".claude/skills/skill-creator/{fname}",
                action=action,
                template=f"claude/skills/skill-creator/{fname}.j2",
                reason=reason,
                executable=True,
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

        # --- Database Expert: schema, models, and operations ---
        expert_commands.extend([
            ("experts/database/question.md", "Database expert question prompt"),
            ("experts/database/self-improve.md", "Database expert self-improve workflow"),
        ])

        # --- WebSocket Expert: real-time communication ---
        expert_commands.extend([
            ("experts/websocket/question.md", "WebSocket expert question prompt"),
            ("experts/websocket/self-improve.md", "WebSocket expert self-improve workflow"),
            ("experts/websocket/plan.md", "WebSocket expert planning command"),
            (
                "experts/websocket/plan_build_improve.md",
                "WebSocket expert plan-build-improve workflow",
            ),
        ])

        # --- ADW Expert extended commands ---
        expert_commands.extend([
            ("experts/adw/plan.md", "ADW expert planning command"),
            ("experts/adw/plan_build_improve.md", "ADW expert plan-build-improve workflow"),
        ])

        # --- Celes Stack Experts (v1.1.0) ---
        expert_commands.extend([
            ("experts/data-engineering/question.md", "Data engineering expert question prompt"),
            ("experts/data-engineering/self-improve.md", "Data engineering expert self-improve workflow"),
            ("experts/ml-forecasting/question.md", "ML forecasting expert question prompt"),
            ("experts/ml-forecasting/self-improve.md", "ML forecasting expert self-improve workflow"),
            ("experts/gcp-infra/question.md", "GCP infrastructure expert question prompt"),
            ("experts/gcp-infra/self-improve.md", "GCP infrastructure expert self-improve workflow"),
            ("experts/react-frontend/question.md", "React frontend expert question prompt"),
            ("experts/react-frontend/self-improve.md", "React frontend expert self-improve workflow"),
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
            ("database", "Database expert expertise seed file"),
            ("websocket", "WebSocket expert expertise seed file"),
            # Celes stack experts (v1.1.0)
            ("data-engineering", "Data engineering expert expertise seed file"),
            ("ml-forecasting", "ML forecasting expert expertise seed file"),
            ("gcp-infra", "GCP infrastructure expert expertise seed file"),
            ("react-frontend", "React frontend expert expertise seed file"),
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
            ("adw_summarizer.py", "Event summarization module (TAC-14)"),
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
            ("adw_database.py", "Database operations workflow"),
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
        plan.add_file(
            f"{adws_dir}/adw_triggers/adw_manual_trigger.py",
            action=action,
            template="adws/adw_triggers/adw_manual_trigger.py.j2",
            reason="Manual workflow trigger",
            executable=True,
        )
        plan.add_file(
            f"{adws_dir}/adw_triggers/adw_scripts.py",
            action=action,
            template="adws/adw_triggers/adw_scripts.py.j2",
            reason="ADW utility scripts trigger",
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

        # Schema migration file
        plan.add_file(
            f"{adws_dir}/schema/migrations/001_initial.sql",
            action=action,
            template="adws/schema/migrations/001_initial.sql.j2",
            reason="Initial database migration",
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
            ("purge_tree.sh", "Worktree cleanup and branch deletion for ADW workflows"),
            ("kill_trigger_webhook.sh", "Kill webhook trigger process"),
            ("aea_server_start.sh", "AEA server start script"),
            ("aea_server_reset.sh", "AEA server reset script"),
            ("clear_issue_comments.sh", "Clear GitHub issue comments"),
            ("copy_dot_env.sh", "Copy .env file to worktrees"),
            ("check_ports.sh", "Check port availability"),
            ("copy_claude.py", "Copy Claude configuration"),
            ("delete_pr.sh", "Delete pull request branch"),
            ("dev_build.sh", "Development build script"),
            ("dev_lint.sh", "Development lint script"),
            ("dev_start.sh", "Development start script"),
            ("dev_test.sh", "Development test script"),
            ("expose_webhook.sh", "Expose webhook endpoint"),
            ("reset_db.sh", "Reset database script"),
            ("stop_apps.sh", "Stop all application processes"),
            ("sync_model_config.py", "Sync model configuration across .claude/ commands and agents"),
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

    # Directories to exclude when walking apps/ templates
    _APPS_EXCLUDE_DIRS = {
        ".venv", "node_modules", "__pycache__", ".mypy_cache",
        ".pytest_cache", "logs", ".git",
    }

    def _add_orchestrator_apps(
        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool
    ) -> None:
        """Add apps/ directories as bulk copy from templates.

        Walks templates/apps/orchestrator_db/ and templates/apps/orchestrator_3_stream/
        recursively, reading all source files and adding them to the plan.
        Excludes build artifacts (.venv, node_modules, __pycache__, etc.).
        """
        import os

        action = FileAction.OVERWRITE if existing_repo else FileAction.CREATE
        templates_dir = self.template_repo.templates_dir

        # Both app directories to copy
        app_dirs = ["apps/orchestrator_db", "apps/orchestrator_3_stream"]

        for app_dir in app_dirs:
            source_dir = templates_dir / app_dir
            if not source_dir.exists():
                print(f"  [warn] App template directory not found: {source_dir}")
                continue

            # Walk the directory tree
            for root, dirs, files in os.walk(source_dir):
                # Prune excluded directories in-place
                dirs[:] = [d for d in dirs if d not in self._APPS_EXCLUDE_DIRS]

                rel_root = os.path.relpath(root, templates_dir)

                # Add directory to plan
                if rel_root != app_dir:
                    plan.add_directory(rel_root, f"Orchestrator: {os.path.basename(rel_root)}")

                for filename in sorted(files):
                    # Skip binary/generated files
                    if filename.endswith((".pyc", ".pyo")):
                        continue

                    rel_path = os.path.join(rel_root, filename)
                    full_path = os.path.join(root, filename)

                    try:
                        content = open(full_path, encoding="utf-8").read()
                        executable = filename.endswith(".sh")
                        plan.add_file(
                            rel_path,
                            action=action,
                            content=content,
                            reason=f"Orchestrator: {filename}",
                            executable=executable,
                        )
                    except (UnicodeDecodeError, FileNotFoundError):
                        # Skip binary files or missing files
                        continue

    def _add_test_files(
        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool
    ) -> None:
        """Add ADW test suites (TAC-14 Task 15).

        Adds:
        - adws/adw_tests/: Pytest fixtures and tests for database, workflows, agent SDK, websockets
        """
        action = FileAction.CREATE  # CREATE only creates if file doesn't exist
        adws_dir = config.paths.adws_dir

        # Add test directory structure
        plan.add_directory(f"{adws_dir}/adw_tests", "ADW pytest test suite")

        # Pytest test files
        pytest_files = [
            ("__init__.py", "Test package init"),
            ("conftest.py", "Pytest fixtures and configuration"),
            ("pytest.ini", "Pytest settings"),
            ("test_database.py", "Database module tests"),
            ("test_workflows.py", "Workflow operations tests"),
            ("test_agent_sdk.py", "Agent SDK abstraction tests"),
            ("test_websockets.py", "WebSocket server tests"),
            ("health_check.py", "Health check test"),
            ("sandbox_poc.py", "Sandbox proof of concept test"),
            ("test_agents.py", "Agent integration tests"),
            ("test_model_selection.py", "Model selection tests"),
            ("test_r2_uploader.py", "R2 uploader tests"),
            ("test_webhook_simplified.py", "Simplified webhook tests"),
            ("test_adw_sdlc_orchestrators.py", "SDLC/ZTE orchestrator integration tests"),
        ]

        for file, reason in pytest_files:
            plan.add_file(
                f"{adws_dir}/adw_tests/{file}",
                action=action,
                template=f"adws/adw_tests/{file}.j2",
                reason=reason,
            )

        # ADW test submodule
        plan.add_directory(f"{adws_dir}/adw_tests/adw_modules", "ADW test modules")
        plan.add_file(
            f"{adws_dir}/adw_tests/adw_modules/adw_agent_sdk.py",
            action=action,
            template="adws/adw_tests/adw_modules/adw_agent_sdk.py.j2",
            reason="Agent SDK test module",
        )

    def _add_orchestrator_scripts(
        self,
        plan: ScaffoldPlan,
        config: TACConfig,
        existing_repo: bool = False,
    ) -> None:
        """Add orchestrator utility scripts (TAC-14 Task 19)."""
        action = FileAction.OVERWRITE if existing_repo else FileAction.CREATE
        scripts_dir = config.paths.scripts_dir
        plan.add_file(
            f"{scripts_dir}/setup_database.sh",
            action=action,
            template="scripts/setup_database.sh.j2",
            reason="PostgreSQL database migration script",
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
        import time
        from datetime import datetime, timezone

        from rich.console import Console

        from tac_bootstrap.infrastructure.fs import FileSystem

        apply_start_time = time.time()

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

        # Track scaffold application via telemetry
        apply_duration_ms = (time.time() - apply_start_time) * 1000
        if self.telemetry:
            self.telemetry.track_event(
                "scaffold_applied",
                {
                    "success": result.success,
                    "files_created": result.files_created,
                    "directories_created": result.directories_created,
                    "files_skipped": result.files_skipped,
                    "files_overwritten": result.files_overwritten,
                    "duration_ms": round(apply_duration_ms, 2),
                },
            )
            if not result.success:
                self.telemetry.track_error(
                    RuntimeError("scaffold_apply_errors"),
                    {
                        "operation": "scaffold_apply",
                        "error_count": len(result.errors),
                    },
                )

        return result
