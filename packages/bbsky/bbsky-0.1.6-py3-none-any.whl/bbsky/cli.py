import importlib
from typing import Optional

import typer
from typer import Typer

from bbsky.logging_utils import setup_logger


def get_command_app(command_name: str) -> Optional[Typer]:
    """Dynamically import and return a Typer app for a given command."""
    try:
        module = importlib.import_module(f"bbsky.{command_name}")
        if hasattr(module, "app"):
            return module.app
        elif hasattr(module, "cli"):
            return module.cli
        elif hasattr(module, "main"):
            # If only main exists, create a new Typer app and add the main function
            new_app = Typer()
            new_app.command()(module.main)
            return new_app
        raise ImportError(f"Module {command_name} does not have app, cli, or main function")
    except ImportError as e:
        typer.echo(f"Error loading command {command_name}: {str(e)}", err=True)
        return None


app = Typer(
    help="Command line interface for bbsky.",
    no_args_is_help=True,
)

# Define available commands
COMMANDS = [
    "server",
    "config",
    "token",
    "paths",
    "apis",
]

# Dynamically add all subcommands
for cmd in COMMANDS:
    cmd_app = get_command_app(cmd)
    if cmd_app:
        app.add_typer(cmd_app, name=cmd)


def init_logging():
    """Initialize logging configuration."""
    setup_logger(name=__name__)


def main():
    """Main entry point for the CLI."""
    init_logging()
    app()


if __name__ == "__main__":
    main()
