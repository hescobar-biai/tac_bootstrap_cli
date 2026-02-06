# /// script
# dependencies = ["pytest>=8.0", "pytest-asyncio>=0.23", "pydantic>=2.0"]
# ///
"""
Agent SDK Tests

Tests for adw_modules/adw_agent_sdk.py - typed abstractions for Claude Agent SDK.
Covers models, enums, hooks, and query configuration.
"""

import sys
from pathlib import Path

import pytest

# Add adws directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


# ============================================================================
# Enum Tests
# ============================================================================

class TestEnums:
    """Test SDK enum definitions."""

    def test_model_name_values(self):
        """Test ModelName enum values."""
        from adw_modules.adw_agent_sdk import ModelName

        assert ModelName.OPUS.value == "claude-opus-4-5-20251101"
        assert ModelName.SONNET.value == "claude-sonnet-4-5-20250929"
        assert ModelName.HAIKU.value == "claude-haiku-4-5-20251001"

    def test_hook_event_names(self):
        """Test HookEventName enum values."""
        from adw_modules.adw_agent_sdk import HookEventName

        assert HookEventName.PRE_TOOL_USE.value == "PreToolUse"
        assert HookEventName.POST_TOOL_USE.value == "PostToolUse"
        assert HookEventName.STOP.value == "Stop"

    def test_permission_decision(self):
        """Test PermissionDecision enum values."""
        from adw_modules.adw_agent_sdk import PermissionDecision

        assert PermissionDecision.ALLOW.value == "allow"
        assert PermissionDecision.DENY.value == "deny"
        assert PermissionDecision.ASK.value == "ask"

    def test_built_in_tools(self):
        """Test BuiltInTool enum values."""
        from adw_modules.adw_agent_sdk import BuiltInTool

        assert BuiltInTool.BASH.value == "Bash"
        assert BuiltInTool.READ.value == "Read"
        assert BuiltInTool.WRITE.value == "Write"
        assert BuiltInTool.GLOB.value == "Glob"
        assert BuiltInTool.GREP.value == "Grep"


# ============================================================================
# Token Usage Tests
# ============================================================================

class TestTokenUsage:
    """Test token usage tracking."""

    def test_token_usage_creation(self, sample_token_usage):
        """Test TokenUsage model creation."""
        assert sample_token_usage.input_tokens == 1000
        assert sample_token_usage.output_tokens == 500
        assert sample_token_usage.cache_read_input_tokens == 200

    def test_token_usage_cost_calculation(self, sample_token_usage):
        """Test cost calculation from token counts."""
        cost = sample_token_usage.calculate_cost()

        # Verify cost is calculated
        assert cost > 0
        # Input: 1000 * 0.00003 = 0.03
        # Output: 500 * 0.00015 = 0.075
        # Cache: 200 * 0.0000075 = 0.0015
        expected = 0.03 + 0.075 + 0.0015
        assert abs(cost - expected) < 0.0001

    def test_usage_accumulator(self):
        """Test UsageAccumulator deduplication."""
        from adw_modules.adw_agent_sdk import UsageAccumulator, TokenUsage

        accumulator = UsageAccumulator()

        usage1 = TokenUsage(input_tokens=100, output_tokens=50)
        usage2 = TokenUsage(input_tokens=200, output_tokens=100)

        # Process first message
        processed = accumulator.process("msg-001", usage1)
        assert processed is True
        assert accumulator.total_input_tokens == 100

        # Process same message again (should be deduplicated)
        processed = accumulator.process("msg-001", usage1)
        assert processed is False
        assert accumulator.total_input_tokens == 100  # Unchanged

        # Process new message
        processed = accumulator.process("msg-002", usage2)
        assert processed is True
        assert accumulator.total_input_tokens == 300


# ============================================================================
# Query Options Tests
# ============================================================================

class TestQueryOptions:
    """Test query configuration options."""

    def test_query_options_defaults(self):
        """Test QueryOptions default values."""
        from adw_modules.adw_agent_sdk import QueryOptions, ModelName

        options = QueryOptions()

        assert options.model == ModelName.SONNET.value
        assert options.allowed_tools == []
        assert options.bypass_permissions is True

    def test_query_options_with_model(self, mock_query_options):
        """Test QueryOptions with custom model."""
        from adw_modules.adw_agent_sdk import ModelName

        assert mock_query_options.model == ModelName.SONNET.value
        assert "Read" in mock_query_options.allowed_tools
        assert mock_query_options.max_turns == 10

    def test_query_options_with_cwd(self):
        """Test QueryOptions with working directory."""
        from adw_modules.adw_agent_sdk import QueryOptions

        options = QueryOptions(cwd="/path/to/project")

        assert options.cwd == "/path/to/project"

    def test_query_options_model_validation(self):
        """Test model validation in QueryOptions."""
        from adw_modules.adw_agent_sdk import QueryOptions, ModelName

        # Using enum
        options1 = QueryOptions(model=ModelName.OPUS)
        assert options1.model == ModelName.OPUS.value

        # Using string
        options2 = QueryOptions(model="claude-sonnet-4-5-20250929")
        assert options2.model == "claude-sonnet-4-5-20250929"


# ============================================================================
# Tool Permissions Tests
# ============================================================================

class TestToolPermissions:
    """Test tool permission configuration."""

    def test_tool_permissions_creation(self):
        """Test ToolPermissions model creation."""
        from adw_modules.adw_agent_sdk import ToolPermissions

        permissions = ToolPermissions(
            allow=["Read", "Glob", "Grep"],
            ask=["Bash(git push:*)"],
            deny=["Write(./.env)"]
        )

        assert "Read" in permissions.allow
        assert "Bash(git push:*)" in permissions.ask
        assert "Write(./.env)" in permissions.deny

    def test_tool_permissions_defaults(self):
        """Test ToolPermissions default values."""
        from adw_modules.adw_agent_sdk import ToolPermissions

        permissions = ToolPermissions()

        assert permissions.allow == []
        assert permissions.ask == []
        assert permissions.deny == []


# ============================================================================
# Hook Types Tests
# ============================================================================

class TestHookTypes:
    """Test hook configuration types."""

    def test_hook_response_allow(self):
        """Test HookResponse.allow() factory."""
        from adw_modules.adw_agent_sdk import HookResponse

        response = HookResponse.allow()

        assert response.continue_execution is True
        assert response.stop_reason is None

    def test_hook_response_deny(self):
        """Test HookResponse.deny() factory."""
        from adw_modules.adw_agent_sdk import HookResponse, PermissionDecision

        response = HookResponse.deny(
            reason="Sensitive file access blocked",
            system_message="Cannot access .env files"
        )

        assert response.system_message == "Cannot access .env files"
        assert response.hook_specific_output is not None
        assert response.hook_specific_output.permission_decision == PermissionDecision.DENY

    def test_hook_response_stop(self):
        """Test HookResponse.stop() factory."""
        from adw_modules.adw_agent_sdk import HookResponse

        response = HookResponse.stop(reason="Max iterations reached")

        assert response.continue_execution is False
        assert response.stop_reason == "Max iterations reached"

    def test_hooks_config_from_callbacks(self):
        """Test HooksConfig.from_callbacks() factory."""
        from adw_modules.adw_agent_sdk import (
            HooksConfig, HookEventName, HookResponse, HookInput, HookContext
        )

        async def my_hook(input_data: HookInput, tool_use_id: str, ctx: HookContext) -> HookResponse:
            return HookResponse.allow()

        config = HooksConfig.from_callbacks({
            HookEventName.PRE_TOOL_USE: [my_hook],
            "PostToolUse": [my_hook],
        })

        assert len(config.pre_tool_use) == 1
        assert len(config.post_tool_use) == 1


# ============================================================================
# Message Types Tests
# ============================================================================

class TestMessageTypes:
    """Test message type definitions."""

    def test_assistant_message(self):
        """Test AssistantMessage model."""
        from adw_modules.adw_agent_sdk import AssistantMessage

        msg = AssistantMessage(
            id="msg-001",
            message="I found the following files...",
            tool_use={"id": "tool-001", "name": "Glob", "input": {"pattern": "*.py"}}
        )

        assert msg.id == "msg-001"
        assert msg.message is not None
        assert msg.tool_use["name"] == "Glob"

    def test_result_message_success(self):
        """Test ResultMessage with success."""
        from adw_modules.adw_agent_sdk import ResultMessage, ResultSubtype

        msg = ResultMessage(
            subtype=ResultSubtype.SUCCESS,
            result="Analysis completed successfully",
            session_id="session-123"
        )

        assert msg.subtype == ResultSubtype.SUCCESS
        assert msg.result is not None
        assert msg.error is None

    def test_result_message_error(self):
        """Test ResultMessage with error."""
        from adw_modules.adw_agent_sdk import ResultMessage, ResultSubtype

        msg = ResultMessage(
            subtype=ResultSubtype.ERROR,
            error="Tool execution failed",
            session_id="session-456"
        )

        assert msg.subtype == ResultSubtype.ERROR
        assert msg.error is not None


# ============================================================================
# System Prompt Config Tests
# ============================================================================

class TestSystemPromptConfig:
    """Test system prompt configuration."""

    def test_system_prompt_default_mode(self):
        """Test DEFAULT system prompt mode."""
        from adw_modules.adw_agent_sdk import SystemPromptConfig, SystemPromptMode

        config = SystemPromptConfig(mode=SystemPromptMode.DEFAULT)
        sdk_config = config.to_sdk_config()

        assert sdk_config["type"] == "preset"
        assert sdk_config["preset"] == "claude_code"

    def test_system_prompt_append_mode(self):
        """Test APPEND system prompt mode."""
        from adw_modules.adw_agent_sdk import SystemPromptConfig, SystemPromptMode

        config = SystemPromptConfig(
            mode=SystemPromptMode.APPEND,
            system_prompt="Always respond in JSON format."
        )
        sdk_config = config.to_sdk_config()

        assert sdk_config["type"] == "preset"
        assert sdk_config["preset"] == "claude_code"
        assert sdk_config["append"] == "Always respond in JSON format."

    def test_system_prompt_overwrite_mode(self):
        """Test OVERWRITE system prompt mode."""
        from adw_modules.adw_agent_sdk import SystemPromptConfig, SystemPromptMode

        config = SystemPromptConfig(
            mode=SystemPromptMode.OVERWRITE,
            system_prompt="You are a pirate."
        )
        sdk_config = config.to_sdk_config()

        assert sdk_config == "You are a pirate."


# ============================================================================
# AdhocPrompt Tests
# ============================================================================

class TestAdhocPrompt:
    """Test adhoc prompt configuration."""

    def test_adhoc_prompt_minimal(self):
        """Test AdhocPrompt with minimal config."""
        from adw_modules.adw_agent_sdk import AdhocPrompt, ModelName

        prompt = AdhocPrompt(prompt="What is 2+2?")

        assert prompt.prompt == "What is 2+2?"
        assert prompt.model == ModelName.SONNET.value
        assert prompt.system_prompt is None

    def test_adhoc_prompt_with_model(self):
        """Test AdhocPrompt with custom model."""
        from adw_modules.adw_agent_sdk import AdhocPrompt, ModelName

        prompt = AdhocPrompt(
            prompt="Analyze this code",
            model=ModelName.OPUS
        )

        assert prompt.model == ModelName.OPUS.value

    def test_adhoc_prompt_with_system_prompt(self):
        """Test AdhocPrompt with system prompt override."""
        from adw_modules.adw_agent_sdk import AdhocPrompt

        prompt = AdhocPrompt(
            prompt="Say hello",
            system_prompt="You are a pirate."
        )

        assert prompt.system_prompt == "You are a pirate."
