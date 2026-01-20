"""CLI interface for TAC Bootstrap."""
import typer

app = typer.Typer(
    name="tac-bootstrap",
    help="Bootstrap Agentic Layer for Claude Code with TAC patterns",
    add_completion=False,
)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Bootstrap Agentic Layer for Claude Code with TAC patterns."""
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())

@app.command()
def version():
    """Show version."""
    from tac_bootstrap import __version__
    print(f"tac-bootstrap v{__version__}")

if __name__ == "__main__":
    app()
