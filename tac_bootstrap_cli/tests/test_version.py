"""Test basic package functionality."""

from tac_bootstrap import __version__


def test_version():
    """Test that version is defined."""
    assert __version__ == "0.9.8"


def test_version_format():
    """Test that version follows semantic versioning format."""
    parts = __version__.split(".")
    assert len(parts) == 3
    assert all(part.isdigit() for part in parts)
