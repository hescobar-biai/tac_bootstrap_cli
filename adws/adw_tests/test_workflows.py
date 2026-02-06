# /// script
# dependencies = ["pytest>=8.0", "pytest-asyncio>=0.23", "pyyaml>=6.0"]
# ///
"""
Workflow Operations Tests

Tests for ADW workflow operations including:
- ADW state management
- Git operations helpers
- Worktree operations
- Workflow lifecycle management
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add adws directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


# ============================================================================
# ADW State Tests
# ============================================================================

class TestADWState:
    """Test ADW state management."""

    def test_state_initialization(self, temp_state_dir):
        """Test state initialization with new ADW ID."""
        from adw_modules.state import ADWState

        state = ADWState(adw_id="test-adw-001", state_dir=temp_state_dir)

        assert state.adw_id == "test-adw-001"
        assert state.get("issue_number") is None

    def test_state_set_and_get(self, temp_state_dir):
        """Test setting and getting state values."""
        from adw_modules.state import ADWState

        state = ADWState(adw_id="test-adw-002", state_dir=temp_state_dir)

        state.set("issue_number", "123")
        state.set("branch_name", "feature/test")
        state.set("model_set", "heavy")

        assert state.get("issue_number") == "123"
        assert state.get("branch_name") == "feature/test"
        assert state.get("model_set") == "heavy"

    def test_state_persistence(self, temp_state_dir):
        """Test that state persists across instances."""
        from adw_modules.state import ADWState

        # Create and populate state
        state1 = ADWState(adw_id="test-adw-003", state_dir=temp_state_dir)
        state1.set("issue_number", "456")
        state1.set("worktree_path", "/tmp/test-worktree")

        # Create new instance with same ID
        state2 = ADWState(adw_id="test-adw-003", state_dir=temp_state_dir)

        assert state2.get("issue_number") == "456"
        assert state2.get("worktree_path") == "/tmp/test-worktree"

    def test_state_all_adws_tracking(self, temp_state_dir):
        """Test tracking of completed ADW phases."""
        from adw_modules.state import ADWState

        state = ADWState(adw_id="test-adw-004", state_dir=temp_state_dir)

        # Initially empty
        all_adws = state.get("all_adws", [])
        assert all_adws == []

        # Add completed phases
        state.set("all_adws", ["plan", "build"])

        all_adws = state.get("all_adws", [])
        assert "plan" in all_adws
        assert "build" in all_adws

    def test_state_with_complex_values(self, temp_state_dir):
        """Test state with complex nested values."""
        from adw_modules.state import ADWState

        state = ADWState(adw_id="test-adw-005", state_dir=temp_state_dir)

        complex_value = {
            "files": ["src/main.py", "tests/test_main.py"],
            "config": {"debug": True, "verbose": False},
            "metrics": {"lines_added": 100, "lines_removed": 50}
        }

        state.set("build_result", complex_value)

        retrieved = state.get("build_result")
        assert retrieved["files"] == ["src/main.py", "tests/test_main.py"]
        assert retrieved["config"]["debug"] is True


# ============================================================================
# Data Types Tests
# ============================================================================

class TestDataTypes:
    """Test ADW data type definitions."""

    def test_agent_template_request(self):
        """Test AgentTemplateRequest model."""
        from adw_modules.data_types import AgentTemplateRequest

        request = AgentTemplateRequest(
            agent_name="scout-agent",
            slash_command="/scout",
            args=["find auth logic"],
            adw_id="test-adw",
            model="sonnet",
            working_dir="/tmp/project"
        )

        assert request.agent_name == "scout-agent"
        assert request.slash_command == "/scout"
        assert request.args == ["find auth logic"]
        assert request.model == "sonnet"

    def test_agent_prompt_response(self):
        """Test AgentPromptResponse model."""
        from adw_modules.data_types import AgentPromptResponse

        response = AgentPromptResponse(
            agent_name="build-agent",
            success=True,
            result="Build completed successfully",
            error=None,
            session_id="session-123",
            adw_id="test-adw"
        )

        assert response.success is True
        assert response.result == "Build completed successfully"
        assert response.error is None

    def test_agent_prompt_response_failure(self):
        """Test AgentPromptResponse with failure."""
        from adw_modules.data_types import AgentPromptResponse

        response = AgentPromptResponse(
            agent_name="test-agent",
            success=False,
            result=None,
            error="Tool execution failed: permission denied",
            session_id="session-456",
            adw_id="test-adw"
        )

        assert response.success is False
        assert response.error is not None
        assert "permission denied" in response.error


# ============================================================================
# Utils Tests
# ============================================================================

class TestUtils:
    """Test utility functions."""

    def test_generate_adw_id(self):
        """Test ADW ID generation."""
        from adw_modules.utils import generate_adw_id

        adw_id = generate_adw_id("feature", "123", "test-branch")

        assert "feature" in adw_id
        assert "123" in adw_id

    def test_parse_issue_number(self):
        """Test issue number parsing from various formats."""
        from adw_modules.utils import parse_issue_number

        # Direct number
        assert parse_issue_number("123") == "123"

        # URL format
        assert parse_issue_number("https://github.com/org/repo/issues/456") == "456"

        # With hash
        assert parse_issue_number("#789") == "789"

    def test_sanitize_branch_name(self):
        """Test branch name sanitization."""
        from adw_modules.utils import sanitize_branch_name

        # Basic sanitization
        assert sanitize_branch_name("feature/test branch") == "feature/test-branch"

        # Special characters
        assert sanitize_branch_name("fix: bug #123") == "fix-bug-123"


# ============================================================================
# Workflow Lifecycle Tests
# ============================================================================

class TestWorkflowLifecycle:
    """Test workflow phase management."""

    def test_phase_skip_detection(self, temp_state_dir):
        """Test detection of completed phases for resume."""
        from adw_modules.state import ADWState

        state = ADWState(adw_id="test-workflow-001", state_dir=temp_state_dir)

        # Simulate completed phases
        state.set("all_adws", ["plan", "build", "test"])

        # Check phase completion
        all_adws = state.get("all_adws", [])

        assert "plan" in all_adws  # Should skip
        assert "build" in all_adws  # Should skip
        assert "test" in all_adws  # Should skip
        assert "review" not in all_adws  # Should execute
        assert "document" not in all_adws  # Should execute

    def test_phase_result_storage(self, temp_state_dir):
        """Test storing and retrieving phase results."""
        from adw_modules.state import ADWState

        state = ADWState(adw_id="test-workflow-002", state_dir=temp_state_dir)

        # Store plan phase result
        plan_result = {
            "status": "completed",
            "files_identified": ["src/auth.py", "src/models.py"],
            "strategy": "incremental"
        }
        state.set("plan_result", plan_result)

        # Store build phase result
        build_result = {
            "status": "completed",
            "files_modified": ["src/auth.py"],
            "lines_added": 50
        }
        state.set("build_result", build_result)

        # Verify retrieval
        assert state.get("plan_result")["status"] == "completed"
        assert state.get("build_result")["lines_added"] == 50


# ============================================================================
# Model Selection Tests
# ============================================================================

class TestModelSelection:
    """Test model selection logic."""

    def test_model_set_base(self, temp_state_dir):
        """Test base model set selection."""
        from adw_modules.state import ADWState

        state = ADWState(adw_id="test-model-001", state_dir=temp_state_dir)
        state.set("model_set", "base")

        assert state.get("model_set") == "base"

    def test_model_set_heavy(self, temp_state_dir):
        """Test heavy model set selection."""
        from adw_modules.state import ADWState

        state = ADWState(adw_id="test-model-002", state_dir=temp_state_dir)
        state.set("model_set", "heavy")

        assert state.get("model_set") == "heavy"

    def test_model_fallback_chain(self):
        """Test model fallback chain constants."""
        from adw_modules.agent import MODEL_FALLBACK_CHAIN

        assert "opus" in MODEL_FALLBACK_CHAIN
        assert "sonnet" in MODEL_FALLBACK_CHAIN
        assert "haiku" in MODEL_FALLBACK_CHAIN

        # Verify fallback chain
        assert MODEL_FALLBACK_CHAIN["opus"] == "sonnet"
        assert MODEL_FALLBACK_CHAIN["sonnet"] == "haiku"
        # haiku should loop to haiku (for time-based retry)
        assert MODEL_FALLBACK_CHAIN["haiku"] == "haiku"
