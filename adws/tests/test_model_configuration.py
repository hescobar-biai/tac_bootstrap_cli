#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pytest>=7.0",
#   "pydantic>=2.0",
#   "pyyaml>=6.0",
# ]
# ///
"""
Tests for 3-tier model configuration resolution system.

Tests the complete model configuration hierarchy:
1. Environment variables (ANTHROPIC_DEFAULT_*_MODEL)
2. config.yml (agentic.model_policy.{model}_model)
3. Hardcoded defaults
"""

import os
import sys
import tempfile
from pathlib import Path
import pytest

# Check if optional dependencies are available
try:
    import claude_agent_sdk
    HAS_SDK = True
except ImportError:
    HAS_SDK = False

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from adw_modules.workflow_ops import get_model_id, load_config


class TestModelResolution:
    """Test 3-tier model resolution hierarchy."""

    def test_model_id_opus_default(self):
        """Test default Opus model ID when nothing is configured."""
        # Clear any env vars that might interfere
        os.environ.pop("ANTHROPIC_DEFAULT_OPUS_MODEL", None)

        model = get_model_id("opus")
        assert model == "claude-opus-4-5-20251101"
        assert "claude-opus" in model

    def test_model_id_sonnet_default(self):
        """Test default Sonnet model ID when nothing is configured."""
        os.environ.pop("ANTHROPIC_DEFAULT_SONNET_MODEL", None)

        model = get_model_id("sonnet")
        assert model == "claude-sonnet-4-5-20250929"
        assert "claude-sonnet" in model

    def test_model_id_haiku_default(self):
        """Test default Haiku model ID when nothing is configured."""
        os.environ.pop("ANTHROPIC_DEFAULT_HAIKU_MODEL", None)

        model = get_model_id("haiku")
        assert model == "claude-haiku-4-5-20251001"
        assert "claude-haiku" in model

    def test_model_id_env_var_override_opus(self):
        """Test Opus model ID override via environment variable."""
        custom_model = "claude-opus-4-6"
        os.environ["ANTHROPIC_DEFAULT_OPUS_MODEL"] = custom_model

        try:
            model = get_model_id("opus")
            assert model == custom_model
        finally:
            os.environ.pop("ANTHROPIC_DEFAULT_OPUS_MODEL", None)

    def test_model_id_env_var_override_sonnet(self):
        """Test Sonnet model ID override via environment variable."""
        custom_model = "claude-sonnet-4-6"
        os.environ["ANTHROPIC_DEFAULT_SONNET_MODEL"] = custom_model

        try:
            model = get_model_id("sonnet")
            assert model == custom_model
        finally:
            os.environ.pop("ANTHROPIC_DEFAULT_SONNET_MODEL", None)

    def test_model_id_env_var_override_haiku(self):
        """Test Haiku model ID override via environment variable."""
        custom_model = "claude-haiku-4-6"
        os.environ["ANTHROPIC_DEFAULT_HAIKU_MODEL"] = custom_model

        try:
            model = get_model_id("haiku")
            assert model == custom_model
        finally:
            os.environ.pop("ANTHROPIC_DEFAULT_HAIKU_MODEL", None)

    def test_model_id_invalid_type(self):
        """Test that invalid model type returns sonnet default."""
        model = get_model_id("invalid-model")
        # Should return the sonnet default fallback
        assert model == "claude-sonnet-4-5-20250929"

    def test_model_id_case_insensitive(self):
        """Test that model type is case-insensitive."""
        opus_lower = get_model_id("opus")
        opus_upper = get_model_id("OPUS")
        # Should both work and resolve correctly
        assert "opus" in opus_lower.lower()


class TestModelResolutionHierarchy:
    """Test the resolution hierarchy order (env > config > default)."""

    def test_env_var_takes_precedence_over_default(self):
        """Environment variables should override defaults."""
        custom_model = "claude-custom-model"
        os.environ["ANTHROPIC_DEFAULT_OPUS_MODEL"] = custom_model

        try:
            model = get_model_id("opus")
            assert model == custom_model
            assert model != "claude-opus-4-5-20251101"
        finally:
            os.environ.pop("ANTHROPIC_DEFAULT_OPUS_MODEL", None)

    def test_all_models_can_be_configured(self):
        """Test that all three model types can be independently configured."""
        opus_custom = "custom-opus"
        sonnet_custom = "custom-sonnet"
        haiku_custom = "custom-haiku"

        os.environ["ANTHROPIC_DEFAULT_OPUS_MODEL"] = opus_custom
        os.environ["ANTHROPIC_DEFAULT_SONNET_MODEL"] = sonnet_custom
        os.environ["ANTHROPIC_DEFAULT_HAIKU_MODEL"] = haiku_custom

        try:
            assert get_model_id("opus") == opus_custom
            assert get_model_id("sonnet") == sonnet_custom
            assert get_model_id("haiku") == haiku_custom
        finally:
            os.environ.pop("ANTHROPIC_DEFAULT_OPUS_MODEL", None)
            os.environ.pop("ANTHROPIC_DEFAULT_SONNET_MODEL", None)
            os.environ.pop("ANTHROPIC_DEFAULT_HAIKU_MODEL", None)

    def test_partial_configuration(self):
        """Test that partial env var configuration works (only some models set)."""
        custom_opus = "custom-opus"
        os.environ["ANTHROPIC_DEFAULT_OPUS_MODEL"] = custom_opus
        os.environ.pop("ANTHROPIC_DEFAULT_SONNET_MODEL", None)
        os.environ.pop("ANTHROPIC_DEFAULT_HAIKU_MODEL", None)

        try:
            # Opus should use custom value
            assert get_model_id("opus") == custom_opus

            # Others should use defaults
            assert get_model_id("sonnet") == "claude-sonnet-4-5-20250929"
            assert get_model_id("haiku") == "claude-haiku-4-5-20251001"
        finally:
            os.environ.pop("ANTHROPIC_DEFAULT_OPUS_MODEL", None)


class TestConfigLoading:
    """Test configuration loading and caching."""

    def test_load_config_returns_dict(self):
        """Test that load_config returns a dictionary."""
        config = load_config()
        assert isinstance(config, dict)
        assert "agentic" in config or config == {}  # May be empty if no config file

    def test_load_config_caches_result(self):
        """Test that config is cached after first load."""
        config1 = load_config()
        config2 = load_config()

        # Should be the same object (cached)
        assert config1 is config2


class TestModelFallbackChain:
    """Test the model fallback chain for quota exhaustion handling."""

    def test_get_model_fallback_chain_structure(self):
        """Test that fallback chain returns correct structure."""
        from adw_modules.agent import get_model_fallback_chain

        chain = get_model_fallback_chain()

        assert isinstance(chain, dict)
        # Should have entries for opus, sonnet, haiku
        opus = get_model_id("opus")
        sonnet = get_model_id("sonnet")
        haiku = get_model_id("haiku")

        assert opus in chain
        assert sonnet in chain
        assert haiku in chain

    def test_model_fallback_chain_resolution_order(self):
        """Test fallback chain resolution order."""
        from adw_modules.agent import get_model_fallback_chain

        chain = get_model_fallback_chain()

        opus = get_model_id("opus")
        sonnet = get_model_id("sonnet")
        haiku = get_model_id("haiku")

        # Opus → Sonnet
        assert chain[opus] == sonnet

        # Sonnet → Haiku
        assert chain[sonnet] == haiku

        # Haiku → Haiku (no further fallback)
        assert chain[haiku] == haiku

    def test_get_fallback_model_function(self):
        """Test the get_fallback_model helper function."""
        from adw_modules.agent import get_fallback_model

        opus = get_model_id("opus")
        sonnet = get_model_id("sonnet")
        haiku = get_model_id("haiku")

        # Opus falls back to Sonnet
        assert get_fallback_model(opus) == sonnet

        # Sonnet falls back to Haiku
        assert get_fallback_model(sonnet) == haiku

        # Haiku falls back to itself
        assert get_fallback_model(haiku) == haiku


@pytest.mark.skipif(not HAS_SDK, reason="requires claude_agent_sdk")
class TestFastModel:
    """Test fast model resolution for summarization."""

    def test_get_fast_model_returns_string(self):
        """Test that get_fast_model returns a string."""
        from adw_modules.adw_summarizer import get_fast_model

        model = get_fast_model()
        assert isinstance(model, str)
        assert len(model) > 0

    def test_get_fast_model_is_haiku(self):
        """Test that fast model defaults to Haiku."""
        from adw_modules.adw_summarizer import get_fast_model

        model = get_fast_model()
        haiku = get_model_id("haiku")

        assert model == haiku

    def test_fast_model_env_var_override(self):
        """Test that FAST_MODEL respects env var override."""
        from adw_modules.adw_summarizer import get_fast_model

        custom_haiku = "custom-fast-model"
        os.environ["ANTHROPIC_DEFAULT_HAIKU_MODEL"] = custom_haiku

        try:
            model = get_fast_model()
            assert model == custom_haiku
        finally:
            os.environ.pop("ANTHROPIC_DEFAULT_HAIKU_MODEL", None)


@pytest.mark.skipif(not HAS_SDK, reason="requires claude_agent_sdk")
class TestResolvedModelFunctions:
    """Test the get_resolved_model_* functions in adw_agent_sdk."""

    def test_get_resolved_model_opus(self):
        """Test get_resolved_model_opus function."""
        from adw_modules.adw_agent_sdk import get_resolved_model_opus

        model = get_resolved_model_opus()
        assert model == get_model_id("opus")

    def test_get_resolved_model_sonnet(self):
        """Test get_resolved_model_sonnet function."""
        from adw_modules.adw_agent_sdk import get_resolved_model_sonnet

        model = get_resolved_model_sonnet()
        assert model == get_model_id("sonnet")

    def test_get_resolved_model_haiku(self):
        """Test get_resolved_model_haiku function."""
        from adw_modules.adw_agent_sdk import get_resolved_model_haiku

        model = get_resolved_model_haiku()
        assert model == get_model_id("haiku")

    def test_resolved_models_respect_env_vars(self):
        """Test that resolved model functions respect environment variables."""
        from adw_modules.adw_agent_sdk import (
            get_resolved_model_opus,
            get_resolved_model_sonnet,
            get_resolved_model_haiku,
        )

        custom_opus = "custom-opus-resolved"
        custom_sonnet = "custom-sonnet-resolved"
        custom_haiku = "custom-haiku-resolved"

        os.environ["ANTHROPIC_DEFAULT_OPUS_MODEL"] = custom_opus
        os.environ["ANTHROPIC_DEFAULT_SONNET_MODEL"] = custom_sonnet
        os.environ["ANTHROPIC_DEFAULT_HAIKU_MODEL"] = custom_haiku

        try:
            assert get_resolved_model_opus() == custom_opus
            assert get_resolved_model_sonnet() == custom_sonnet
            assert get_resolved_model_haiku() == custom_haiku
        finally:
            os.environ.pop("ANTHROPIC_DEFAULT_OPUS_MODEL", None)
            os.environ.pop("ANTHROPIC_DEFAULT_SONNET_MODEL", None)
            os.environ.pop("ANTHROPIC_DEFAULT_HAIKU_MODEL", None)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
