"""Test CLI interface."""
from typer.testing import CliRunner

from tac_bootstrap.interfaces.cli import app

runner = CliRunner()


def test_cli_app_exists():
    """Test that the CLI app is properly configured."""
    assert app is not None
    assert app.info.name == "tac-bootstrap"


def test_help_command():
    """Test the help command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Show version" in result.stdout
