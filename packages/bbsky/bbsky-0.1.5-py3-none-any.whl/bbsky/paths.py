import os
from pathlib import Path

import typer


def getenv_path(key: str, default: Path) -> Path:
    value = os.getenv(key)
    return Path(value) if value else default


BBSKY_HOME_DIR = getenv_path("BBSKY_HOME_DIR", (Path.home() / ".bbsky").resolve())
BBSKY_CONFIG_DIR = getenv_path("BBSKY_CONFIG_DIR", BBSKY_HOME_DIR / "config")
BBSKY_CACHE_DIR = getenv_path("BBSKY_CACHE_DIR", BBSKY_HOME_DIR / "cache")
BBSKY_CONFIG_FILE = BBSKY_CONFIG_DIR / "config.json"
BBSKY_TOKEN_FILE = BBSKY_CACHE_DIR / "token.json"


cli = typer.Typer(help="Display the default paths used by bbsky.")


@cli.command()
def show() -> None:
    """Display the default paths used by bbsky."""
    typer.echo(f"BBSKY_HOME_DIR: {BBSKY_HOME_DIR}")
    typer.echo(f"BBSKY_CONFIG_DIR: {BBSKY_CONFIG_DIR}")
    typer.echo(f"BBSKY_CACHE_DIR: {BBSKY_CACHE_DIR}")
    typer.echo(f"BBSKY_CONFIG_FILE: {BBSKY_CONFIG_FILE}")
    typer.echo(f"BBSKY_TOKEN_FILE: {BBSKY_TOKEN_FILE}")
