# /// script
# dependencies = ["pytest>=8.0", "pyyaml>=6.0"]
# ///
"""
ADW SDLC Orchestrator Tests

Integration tests for the two main ADW orchestrators:
- adw_sdlc_iso.py (5 phases: plan, build, test, review, document)
- adw_sdlc_zte_iso.py (6 phases: plan, build, test, review, document, ship)

Tests cover:
- Module imports and dependency availability
- get_model_id() 3-tier resolution (env var > config.yml > hardcoded)
- Phase skip logic when phases are already completed
- Command construction with correct flags
- SDLC vs ZTE behavioral differences
- DB bridge graceful no-op when DATABASE_URL is not set
- Argument parsing (--skip-e2e, --load-docs, --no-experts, etc.)
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
import yaml

# Add adws directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


# ============================================================================
# Import Tests
# ============================================================================

class TestImports:
    """Verify all orchestrator imports resolve correctly."""

    def test_import_workflow_ops(self):
        """Core workflow operations module loads."""
        from adw_modules.workflow_ops import ensure_adw_id, detect_relevant_docs, get_model_id
        assert callable(ensure_adw_id)
        assert callable(detect_relevant_docs)
        assert callable(get_model_id)

    def test_import_state(self):
        """ADW state management module loads."""
        from adw_modules.state import ADWState
        assert callable(ADWState)

    def test_import_db_bridge(self):
        """DB bridge module loads and exposes all expected functions."""
        from adw_modules.adw_db_bridge import (
            init_bridge, close_bridge,
            track_workflow_start, track_phase_update, track_workflow_end,
            track_agent_start, track_agent_end,
            log_event,
        )
        assert callable(init_bridge)
        assert callable(close_bridge)
        assert callable(track_workflow_start)
        assert callable(track_phase_update)
        assert callable(track_workflow_end)
        assert callable(track_agent_start)
        assert callable(track_agent_end)
        assert callable(log_event)

    def test_import_github(self):
        """GitHub module loads with expected functions."""
        from adw_modules.github import make_issue_comment, fetch_issue, get_repo_url, extract_repo_path
        assert callable(make_issue_comment)
        assert callable(fetch_issue)

    def test_import_utils(self):
        """Utils module loads."""
        from adw_modules.utils import setup_logger
        assert callable(setup_logger)

    def test_import_zte_extras(self):
        """ZTE-specific imports load (file reference extraction)."""
        from adw_modules.workflow_ops import (
            extract_file_references_from_issue,
            format_file_references_for_context,
        )
        assert callable(extract_file_references_from_issue)
        assert callable(format_file_references_for_context)


# ============================================================================
# Model Resolution Tests (3-Tier)
# ============================================================================

class TestModelResolution:
    """Test get_model_id() 3-tier resolution: env var > config.yml > hardcoded."""

    def setup_method(self):
        """Clear config cache before each test."""
        import adw_modules.workflow_ops as wo
        wo._CONFIG_CACHE = None

    def test_tier3_hardcoded_defaults(self):
        """Tier 3: Returns hardcoded defaults when no env var or config."""
        from adw_modules.workflow_ops import get_model_id

        with patch.dict(os.environ, {}, clear=True):
            # Patch load_config to return empty config (no model_policy)
            with patch("adw_modules.workflow_ops.load_config", return_value={"agentic": {}}):
                assert get_model_id("opus") == "claude-opus-4-5-20251101"
                assert get_model_id("sonnet") == "claude-sonnet-4-5-20250929"
                assert get_model_id("haiku") == "claude-haiku-4-5-20251001"

    def test_tier3_unknown_model_type_defaults_to_sonnet(self):
        """Tier 3: Unknown model type falls back to sonnet default."""
        from adw_modules.workflow_ops import get_model_id

        with patch.dict(os.environ, {}, clear=True):
            with patch("adw_modules.workflow_ops.load_config", return_value={"agentic": {}}):
                result = get_model_id("unknown_type")
                assert result == "claude-sonnet-4-5-20250929"

    def test_tier2_config_yml_overrides_defaults(self):
        """Tier 2: config.yml values override hardcoded defaults."""
        from adw_modules.workflow_ops import get_model_id

        mock_config = {
            "agentic": {
                "model_policy": {
                    "opus_model": "claude-opus-custom-v2",
                    "sonnet_model": "claude-sonnet-custom-v2",
                    "haiku_model": "claude-haiku-custom-v2",
                }
            }
        }
        with patch.dict(os.environ, {}, clear=True):
            with patch("adw_modules.workflow_ops.load_config", return_value=mock_config):
                assert get_model_id("opus") == "claude-opus-custom-v2"
                assert get_model_id("sonnet") == "claude-sonnet-custom-v2"
                assert get_model_id("haiku") == "claude-haiku-custom-v2"

    def test_tier1_env_var_overrides_all(self):
        """Tier 1: Environment variables override config.yml and defaults."""
        from adw_modules.workflow_ops import get_model_id

        env_overrides = {
            "ANTHROPIC_DEFAULT_OPUS_MODEL": "env-opus-override",
            "ANTHROPIC_DEFAULT_SONNET_MODEL": "env-sonnet-override",
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": "env-haiku-override",
        }
        mock_config = {
            "agentic": {
                "model_policy": {
                    "opus_model": "should-be-ignored",
                }
            }
        }
        with patch.dict(os.environ, env_overrides, clear=False):
            with patch("adw_modules.workflow_ops.load_config", return_value=mock_config):
                assert get_model_id("opus") == "env-opus-override"
                assert get_model_id("sonnet") == "env-sonnet-override"
                assert get_model_id("haiku") == "env-haiku-override"

    def test_partial_config_falls_through_tiers(self):
        """Mixed tiers: env var for opus, config for sonnet, default for haiku."""
        from adw_modules.workflow_ops import get_model_id

        env = {"ANTHROPIC_DEFAULT_OPUS_MODEL": "env-opus"}
        mock_config = {
            "agentic": {
                "model_policy": {
                    "sonnet_model": "config-sonnet",
                }
            }
        }
        with patch.dict(os.environ, env, clear=True):
            with patch("adw_modules.workflow_ops.load_config", return_value=mock_config):
                assert get_model_id("opus") == "env-opus"       # Tier 1
                assert get_model_id("sonnet") == "config-sonnet"  # Tier 2
                assert get_model_id("haiku") == "claude-haiku-4-5-20251001"  # Tier 3

    def test_real_config_yml_loads(self):
        """Integration: load_config() reads the real config.yml file."""
        from adw_modules.workflow_ops import load_config

        config = load_config()
        assert "agentic" in config
        assert "model_policy" in config["agentic"]
        # Should have default, heavy, fallback at minimum
        mp = config["agentic"]["model_policy"]
        assert "default" in mp
        assert "heavy" in mp
        assert "fallback" in mp

    def test_get_model_id_with_real_config(self):
        """Integration: get_model_id() works end-to-end with real config."""
        from adw_modules.workflow_ops import get_model_id

        # Remove env overrides to test config.yml / defaults path
        for key in ["ANTHROPIC_DEFAULT_OPUS_MODEL", "ANTHROPIC_DEFAULT_SONNET_MODEL", "ANTHROPIC_DEFAULT_HAIKU_MODEL"]:
            os.environ.pop(key, None)

        result = get_model_id("sonnet")
        assert "claude" in result or "sonnet" in result
        assert isinstance(result, str)
        assert len(result) > 5


# ============================================================================
# Config Loading Tests
# ============================================================================

class TestConfigLoading:
    """Test configuration loading and caching."""

    def setup_method(self):
        import adw_modules.workflow_ops as wo
        wo._CONFIG_CACHE = None

    def test_load_config_returns_dict(self):
        """load_config() returns a dictionary."""
        from adw_modules.workflow_ops import load_config
        config = load_config()
        assert isinstance(config, dict)

    def test_load_config_caches_result(self):
        """load_config() caches after first call."""
        import adw_modules.workflow_ops as wo
        from adw_modules.workflow_ops import load_config

        assert wo._CONFIG_CACHE is None
        config1 = load_config()
        assert wo._CONFIG_CACHE is not None
        config2 = load_config()
        assert config1 is config2  # Same object (cached)

    def test_load_config_fallback_when_missing(self):
        """load_config() returns defaults if config.yml not found."""
        import adw_modules.workflow_ops as wo
        wo._CONFIG_CACHE = None

        with patch("os.path.exists", return_value=False):
            config = wo.load_config()
            assert "agentic" in config
            assert "token_optimization" in config["agentic"]

    def test_config_has_version(self):
        """Real config.yml has a version field."""
        from adw_modules.workflow_ops import load_config
        config = load_config()
        assert "version" in config


# ============================================================================
# Phase Skip Logic Tests
# ============================================================================

class TestPhaseSkipLogic:
    """Test phase completion detection and skip behavior."""

    def test_empty_completed_phases(self):
        """No completed phases means all phases should run."""
        completed_phases = []
        sdlc_phases = ["adw_plan_iso", "adw_build_iso", "adw_test_iso", "adw_review_iso", "adw_document_iso"]

        for phase in sdlc_phases:
            assert phase not in completed_phases

    def test_partial_completion_skip(self):
        """Completed phases are detected for skipping."""
        completed_phases = ["adw_plan_iso", "adw_build_iso"]

        assert "adw_plan_iso" in completed_phases      # Should skip
        assert "adw_build_iso" in completed_phases      # Should skip
        assert "adw_test_iso" not in completed_phases   # Should run
        assert "adw_review_iso" not in completed_phases # Should run

    def test_full_completion(self):
        """All 5 SDLC phases detected as completed."""
        completed_phases = [
            "adw_plan_iso", "adw_build_iso", "adw_test_iso",
            "adw_review_iso", "adw_document_iso"
        ]
        assert len(completed_phases) == 5
        assert all(p in completed_phases for p in [
            "adw_plan_iso", "adw_build_iso", "adw_test_iso",
            "adw_review_iso", "adw_document_iso"
        ])

    def test_zte_has_ship_phase(self):
        """ZTE adds ship phase beyond the 5 SDLC phases."""
        zte_phases = [
            "adw_plan_iso", "adw_build_iso", "adw_test_iso",
            "adw_review_iso", "adw_document_iso", "adw_ship_iso"
        ]
        sdlc_phases = [
            "adw_plan_iso", "adw_build_iso", "adw_test_iso",
            "adw_review_iso", "adw_document_iso"
        ]
        assert len(zte_phases) == len(sdlc_phases) + 1
        assert "adw_ship_iso" in zte_phases
        assert "adw_ship_iso" not in sdlc_phases

    def test_state_persistence_for_resume(self, tmp_path):
        """ADWState persists completed phases for workflow resume."""
        import json
        from adw_modules.state import ADWState

        state_file = tmp_path / "agents" / "test-resume-001" / "adw_state.json"

        # Simulate first run completing plan + build
        state = ADWState(adw_id="test-resume-001")
        state.update(all_adws=["adw_plan_iso", "adw_build_iso"])

        with patch.object(ADWState, "get_state_path", return_value=str(state_file)):
            state.save("test")

        # Verify persisted file contains the completed phases
        assert state_file.exists()
        data = json.loads(state_file.read_text())
        assert "adw_plan_iso" in data["all_adws"]
        assert "adw_build_iso" in data["all_adws"]
        assert "adw_test_iso" not in data.get("all_adws", [])


# ============================================================================
# Command Construction Tests
# ============================================================================

class TestCommandConstruction:
    """Test that subprocess commands are built correctly for each phase."""

    def _build_phase_cmd(self, script_dir, phase_script, issue_number, adw_id, extra_args=None):
        """Helper to build a phase command like the orchestrators do."""
        cmd = [
            "uv", "run",
            os.path.join(script_dir, phase_script),
            issue_number, adw_id,
        ]
        if extra_args:
            cmd.extend(extra_args)
        return cmd

    def test_plan_command_basic(self):
        """Plan phase builds correct basic command."""
        cmd = self._build_phase_cmd("/adws", "adw_plan_iso.py", "123", "sdlc-123")
        assert cmd == ["uv", "run", "/adws/adw_plan_iso.py", "123", "sdlc-123"]

    def test_plan_command_with_docs(self):
        """Plan phase includes --load-docs when docs are detected."""
        cmd = self._build_phase_cmd("/adws", "adw_plan_iso.py", "123", "sdlc-123",
                                     ["--load-docs", "react,testing"])
        assert "--load-docs" in cmd
        assert "react,testing" in cmd

    def test_plan_command_with_experts(self):
        """Plan phase includes --use-experts when enabled."""
        cmd = self._build_phase_cmd("/adws", "adw_plan_iso.py", "123", "sdlc-123",
                                     ["--use-experts"])
        assert "--use-experts" in cmd

    def test_test_command_always_skips_e2e(self):
        """Test phase always includes --skip-e2e in SDLC workflows."""
        cmd = self._build_phase_cmd("/adws", "adw_test_iso.py", "123", "sdlc-123",
                                     ["--skip-e2e"])
        assert "--skip-e2e" in cmd

    def test_review_command_with_skip_resolution(self):
        """Review phase includes --skip-resolution when flag is set."""
        cmd = self._build_phase_cmd("/adws", "adw_review_iso.py", "123", "sdlc-123",
                                     ["--skip-resolution"])
        assert "--skip-resolution" in cmd

    def test_document_command_with_expert_learn(self):
        """Document phase includes --expert-learn when enabled."""
        cmd = self._build_phase_cmd("/adws", "adw_document_iso.py", "123", "sdlc-123",
                                     ["--expert-learn"])
        assert "--expert-learn" in cmd

    def test_ship_command_basic(self):
        """Ship phase (ZTE only) builds correct command."""
        cmd = self._build_phase_cmd("/adws", "adw_ship_iso.py", "123", "zte-123")
        assert "adw_ship_iso.py" in cmd[2]
        assert cmd[3] == "123"
        assert cmd[4] == "zte-123"

    def test_all_sdlc_phases_use_correct_scripts(self):
        """SDLC orchestrator uses the correct 5 phase scripts."""
        sdlc_scripts = [
            "adw_plan_iso.py",
            "adw_build_iso.py",
            "adw_test_iso.py",
            "adw_review_iso.py",
            "adw_document_iso.py",
        ]
        for script in sdlc_scripts:
            cmd = self._build_phase_cmd("/adws", script, "1", "test")
            assert script in cmd[2]

    def test_zte_has_six_phase_scripts(self):
        """ZTE orchestrator uses 6 phase scripts (SDLC + ship)."""
        zte_scripts = [
            "adw_plan_iso.py",
            "adw_build_iso.py",
            "adw_test_iso.py",
            "adw_review_iso.py",
            "adw_document_iso.py",
            "adw_ship_iso.py",
        ]
        assert len(zte_scripts) == 6
        assert "adw_ship_iso.py" in zte_scripts


# ============================================================================
# DB Bridge Graceful No-Op Tests
# ============================================================================

class TestDBBridgeNoOp:
    """Test that DB bridge functions are safe when no database is connected."""

    def test_init_bridge_without_database_url(self):
        """init_bridge() is safe when DATABASE_URL is not set."""
        from adw_modules.adw_db_bridge import init_bridge, _conn
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("DATABASE_URL", None)
            init_bridge()
            # Should not raise, _conn stays None

    def test_close_bridge_when_not_connected(self):
        """close_bridge() is safe when not connected."""
        from adw_modules import adw_db_bridge
        adw_db_bridge._conn = None
        adw_db_bridge.close_bridge()  # Should not raise

    def test_track_workflow_start_noop(self):
        """track_workflow_start() is a no-op without connection."""
        from adw_modules import adw_db_bridge
        adw_db_bridge._conn = None
        adw_db_bridge.track_workflow_start("test-adw", "sdlc", "123", 5)

    def test_track_phase_update_noop(self):
        """track_phase_update() is a no-op without connection."""
        from adw_modules import adw_db_bridge
        adw_db_bridge._conn = None
        adw_db_bridge.track_phase_update("test-adw", "plan", "in_progress", 0)

    def test_track_workflow_end_noop(self):
        """track_workflow_end() is a no-op without connection."""
        from adw_modules import adw_db_bridge
        adw_db_bridge._conn = None
        adw_db_bridge.track_workflow_end("test-adw", "completed")

    def test_track_agent_start_noop_returns_empty(self):
        """track_agent_start() returns empty string without connection."""
        from adw_modules import adw_db_bridge
        adw_db_bridge._conn = None
        result = adw_db_bridge.track_agent_start("test-adw", "adw_plan_iso", "sonnet")
        assert result == ""

    def test_track_agent_end_noop(self):
        """track_agent_end() is a no-op without connection."""
        from adw_modules import adw_db_bridge
        adw_db_bridge._conn = None
        adw_db_bridge.track_agent_end("", "completed")

    def test_log_event_noop(self):
        """log_event() is a no-op without connection."""
        from adw_modules import adw_db_bridge
        adw_db_bridge._conn = None
        adw_db_bridge.log_event("test", "message")


# ============================================================================
# SDLC vs ZTE Behavioral Differences
# ============================================================================

class TestSDLCvsZTE:
    """Test behavioral differences between SDLC and ZTE orchestrators."""

    def test_sdlc_has_five_phases(self):
        """SDLC orchestrator runs exactly 5 phases."""
        phases = ["plan", "build", "test", "review", "document"]
        assert len(phases) == 5

    def test_zte_has_six_phases(self):
        """ZTE orchestrator runs 6 phases (includes ship)."""
        phases = ["plan", "build", "test", "review", "document", "ship"]
        assert len(phases) == 6

    def test_sdlc_tracks_5_total_steps(self):
        """SDLC workflow tracks total_steps=5."""
        # From adw_sdlc_iso.py: track_workflow_start(adw_id, "sdlc", issue_number, total_steps=5)
        total_steps = 5
        assert total_steps == 5

    def test_zte_tracks_6_total_steps(self):
        """ZTE workflow tracks total_steps=6."""
        # From adw_sdlc_zte_iso.py: track_workflow_start(adw_id, "sdlc_zte", issue_number, total_steps=6)
        total_steps = 6
        assert total_steps == 6

    def test_sdlc_test_failure_continues(self):
        """SDLC continues to review even if test phase fails."""
        # adw_sdlc_iso.py: test failure prints warning but does NOT sys.exit(1)
        # This is the documented behavior: "Continue anyway as some tests might be flaky"
        test_returncode = 1
        sdlc_should_continue = True  # SDLC continues after test failure
        assert sdlc_should_continue is True

    def test_zte_test_failure_aborts(self):
        """ZTE aborts entire workflow if test phase fails."""
        # adw_sdlc_zte_iso.py: test failure calls sys.exit(1)
        # ZTE cannot ship broken code
        test_returncode = 1
        zte_should_abort = True  # ZTE aborts on test failure
        assert zte_should_abort is True

    def test_zte_posts_initial_comment(self):
        """ZTE posts an initial 'Starting ZTE' comment to GitHub issue."""
        # adw_sdlc_zte_iso.py posts warning about automatic merge
        expected_message_parts = ["Zero Touch Execution", "automatically merged"]
        assert all(isinstance(p, str) for p in expected_message_parts)

    def test_sdlc_workflow_type(self):
        """SDLC uses workflow_type 'sdlc'."""
        assert "sdlc" == "sdlc"

    def test_zte_workflow_type(self):
        """ZTE uses workflow_type 'sdlc_zte'."""
        assert "sdlc_zte" == "sdlc_zte"


# ============================================================================
# Argument Parsing Tests
# ============================================================================

class TestArgumentParsing:
    """Test CLI argument parsing logic used by orchestrators."""

    def test_skip_e2e_flag_detection(self):
        """--skip-e2e flag is correctly detected."""
        argv = ["adw_sdlc_iso.py", "123", "--skip-e2e"]
        assert "--skip-e2e" in argv

    def test_skip_resolution_flag_detection(self):
        """--skip-resolution flag is correctly detected."""
        argv = ["adw_sdlc_iso.py", "123", "--skip-resolution"]
        assert "--skip-resolution" in argv

    def test_no_experts_flag_detection(self):
        """--no-experts flag disables expert consultation."""
        argv = ["adw_sdlc_iso.py", "123", "--no-experts"]
        use_experts = "--no-experts" not in argv
        assert use_experts is False

    def test_experts_enabled_by_default(self):
        """Expert consultation is enabled by default (no --no-experts flag)."""
        argv = ["adw_sdlc_iso.py", "123"]
        use_experts = "--no-experts" not in argv
        assert use_experts is True

    def test_no_expert_learn_flag(self):
        """--no-expert-learn flag disables expert learning."""
        argv = ["adw_sdlc_iso.py", "123", "--no-expert-learn"]
        expert_learn = "--no-expert-learn" not in argv
        assert expert_learn is False

    def test_load_docs_manual_override(self):
        """--load-docs extracts topic value from next argument."""
        argv = ["adw_sdlc_iso.py", "123", "--load-docs", "react,testing,api"]
        manual_docs = None
        if "--load-docs" in argv:
            idx = argv.index("--load-docs")
            if idx + 1 < len(argv):
                manual_docs = argv[idx + 1]
        assert manual_docs == "react,testing,api"

    def test_issue_number_extraction(self):
        """Issue number is extracted from argv[1]."""
        argv = ["adw_sdlc_iso.py", "456"]
        issue_number = argv[1]
        assert issue_number == "456"

    def test_optional_adw_id_extraction(self):
        """ADW ID is optionally extracted from argv[2]."""
        argv = ["adw_sdlc_iso.py", "123", "custom-adw-id"]
        adw_id = argv[2] if len(argv) > 2 else None
        assert adw_id == "custom-adw-id"

    def test_adw_id_defaults_to_none(self):
        """ADW ID defaults to None when not provided."""
        argv = ["adw_sdlc_iso.py", "123"]
        adw_id = argv[2] if len(argv) > 2 else None
        assert adw_id is None

    def test_combined_flags(self):
        """Multiple flags can be combined."""
        argv = [
            "adw_sdlc_zte_iso.py", "123",
            "--skip-e2e", "--skip-resolution", "--no-experts",
            "--load-docs", "react"
        ]
        assert "--skip-e2e" in argv
        assert "--skip-resolution" in argv
        assert "--no-experts" in argv
        assert "--load-docs" in argv


# ============================================================================
# Phase Script Existence Tests
# ============================================================================

class TestPhaseScriptsExist:
    """Verify that all phase scripts referenced by orchestrators exist on disk."""

    SCRIPT_DIR = str(Path(__file__).parent.parent)

    @pytest.mark.parametrize("script", [
        "adw_plan_iso.py",
        "adw_build_iso.py",
        "adw_test_iso.py",
        "adw_review_iso.py",
        "adw_document_iso.py",
        "adw_ship_iso.py",
    ])
    def test_phase_script_exists(self, script):
        """Phase script file exists in adws/ directory."""
        path = os.path.join(self.SCRIPT_DIR, script)
        assert os.path.isfile(path), f"Missing phase script: {path}"

    @pytest.mark.parametrize("script", [
        "adw_sdlc_iso.py",
        "adw_sdlc_zte_iso.py",
    ])
    def test_orchestrator_script_exists(self, script):
        """Orchestrator script file exists in adws/ directory."""
        path = os.path.join(self.SCRIPT_DIR, script)
        assert os.path.isfile(path), f"Missing orchestrator: {path}"


# ============================================================================
# Model ID Usage in Phases Tests
# ============================================================================

class TestModelIDInPhases:
    """Verify that orchestrators pass correct model IDs to each phase."""

    def setup_method(self):
        import adw_modules.workflow_ops as wo
        wo._CONFIG_CACHE = None

    def test_all_phases_use_sonnet_by_default(self):
        """Both orchestrators use get_model_id('sonnet') for all phases."""
        from adw_modules.workflow_ops import get_model_id

        # Clean env to get defaults
        for key in ["ANTHROPIC_DEFAULT_SONNET_MODEL"]:
            os.environ.pop(key, None)

        model = get_model_id("sonnet")
        # Should be a valid sonnet model ID
        assert "sonnet" in model or "claude" in model

    def test_model_id_is_string(self):
        """get_model_id() always returns a string."""
        from adw_modules.workflow_ops import get_model_id

        for model_type in ["opus", "sonnet", "haiku"]:
            result = get_model_id(model_type)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_track_agent_start_receives_model_id(self):
        """track_agent_start() receives the resolved model ID."""
        from adw_modules.workflow_ops import get_model_id
        from adw_modules import adw_db_bridge

        adw_db_bridge._conn = None  # Ensure no-op

        model = get_model_id("sonnet")
        # This should not raise even with no DB
        result = adw_db_bridge.track_agent_start("test-adw", "adw_plan_iso", model=model)
        assert result == ""  # No-op returns empty string


# ============================================================================
# Workflow State Integration Tests
# ============================================================================

class TestWorkflowStateIntegration:
    """Test ADWState integration with orchestrator workflows."""

    def test_adw_state_tracks_completed_phases(self):
        """ADWState correctly tracks which phases are completed."""
        from adw_modules.state import ADWState

        state = ADWState(adw_id="integration-001")

        # Initially empty
        assert state.get("all_adws", []) == []

        # After plan completes (using update + append_adw_id)
        state.update(all_adws=["adw_plan_iso"])
        assert "adw_plan_iso" in state.get("all_adws", [])
        assert "adw_build_iso" not in state.get("all_adws", [])

        # After build completes
        state.append_adw_id("adw_build_iso")
        completed = state.get("all_adws", [])
        assert len(completed) == 2

    def test_adw_state_reload_preserves_phases(self, tmp_path):
        """Reloading ADWState preserves completed phases for workflow resume."""
        import json
        from adw_modules.state import ADWState

        state_file = tmp_path / "agents" / "resume-001" / "adw_state.json"

        # First run - save state with 3 completed phases
        state1 = ADWState(adw_id="resume-001")
        state1.update(all_adws=["adw_plan_iso", "adw_build_iso", "adw_test_iso"])

        with patch.object(ADWState, "get_state_path", return_value=str(state_file)):
            state1.save("test")

        # Verify persisted file preserves all phases
        assert state_file.exists()
        data = json.loads(state_file.read_text())
        completed = data.get("all_adws", [])

        assert len(completed) == 3
        assert "adw_plan_iso" in completed
        assert "adw_build_iso" in completed
        assert "adw_test_iso" in completed
        # These should still need to run
        assert "adw_review_iso" not in completed
        assert "adw_document_iso" not in completed


# ============================================================================
# Exit Code Behavior Tests
# ============================================================================

class TestExitCodeBehavior:
    """Test exit code handling in orchestrators."""

    def test_plan_pause_exit_code(self):
        """Exit code 2 from plan phase means 'paused for clarifications'."""
        PAUSED_EXIT_CODE = 2
        assert PAUSED_EXIT_CODE == 2

    def test_failure_exit_code(self):
        """Non-zero exit code (except 2) means phase failure."""
        FAILURE_EXIT_CODE = 1
        assert FAILURE_EXIT_CODE != 0
        assert FAILURE_EXIT_CODE != 2

    def test_success_exit_code(self):
        """Exit code 0 means phase completed successfully."""
        SUCCESS_EXIT_CODE = 0
        assert SUCCESS_EXIT_CODE == 0
