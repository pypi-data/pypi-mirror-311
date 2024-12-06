import json
import os
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional

import typer
from attrs import define, evolve

from .data_cls import URL, structure, unstructure
from .paths import BBSKY_CONFIG_DIR, BBSKY_CONFIG_FILE


class SkyConfigError(Exception):
    pass


class SkyConfigEnvVars(Enum):
    CLIENT_ID = "BLACKBAUD_CLIENT_ID"
    CLIENT_SECRET = "BLACKBAUD_CLIENT_SECRET"
    REDIRECT_URI = "BLACKBAUD_REDIRECT_URI"
    SUBSCRIPTION_KEY = "BLACKBAUD_SUBSCRIPTION_KEY"

    @staticmethod
    def are_all_env_vars_set() -> bool:
        return all([os.getenv(var.value) for var in SkyConfigEnvVars])


def ensure_config_dir(func: Callable[..., Any]) -> Callable[..., Any]:
    """Ensure the config directory exists, and create it if it doesn't."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        BBSKY_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        return func(*args, **kwargs)

    return wrapper


@define(frozen=True, slots=True)
class SkyConfig:
    """
    Blackbaud app authentication credentials

    See this URL for helpful troubleshooting tips:
    https://developer.blackbaud.com/skyapi/docs/authorization/common-auth-issues

    client_id: str - Your Blackbaud client ID (should be same as app ID)
    client_secret: str - Your Blackbaud client secret (should be same as app secret)
    redirect_uri: URL - The URL you've pre-configured for the application
    subscription_key: str - Your Blackbaud subscription key
    """

    client_id: str
    client_secret: str
    redirect_uri: URL
    subscription_key: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SkyConfig":
        return structure(data, cls)

    @classmethod
    def from_env(cls) -> "SkyConfig":
        return cls.from_dict(
            {
                "client_id": os.environ[SkyConfigEnvVars.CLIENT_ID.value],
                "client_secret": os.environ[SkyConfigEnvVars.CLIENT_SECRET.value],
                "redirect_uri": os.environ[SkyConfigEnvVars.REDIRECT_URI.value],
                "subscription_key": os.environ[SkyConfigEnvVars.SUBSCRIPTION_KEY.value],
            }
        )

    @classmethod
    def from_json_file(cls, path: Path) -> "SkyConfig":
        return cls.from_dict(json.loads(Path(path).read_text()))

    @classmethod
    def from_stored_config(cls) -> "SkyConfig":
        return cls.from_json_file(BBSKY_CONFIG_FILE)

    def to_dict(self) -> dict[str, Any]:
        return unstructure(self)

    def to_json_file(self, path: Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=4))

    @classmethod
    def load(cls, input_file: Optional[Path] = None):
        f"""
        Loading Priority:

        1. Provided JSON file path
        2. Environment variables
        3. JSON file (default: {BBSKY_CONFIG_FILE})

        """
        if input_file:
            return cls.from_json_file(input_file)
        elif SkyConfigEnvVars.are_all_env_vars_set():
            return cls.from_env()
        elif BBSKY_CONFIG_FILE.exists():
            return cls.from_stored_config()
        else:
            raise SkyConfigError("No config found. Please provide a file path or set environment variables.")


cli = typer.Typer(help="Create and manage Blackbaud Sky API config.")


@cli.command()
def create(
    client_id: str = typer.Option(..., prompt=True, help="Client ID"),
    client_secret: str = typer.Option(..., prompt=True, help="Client Secret"),
    redirect_uri: str = typer.Option(..., prompt=True, help="Redirect URI"),
    subscription_key: str = typer.Option(..., prompt=True, help="Subscription Key"),
    output_path: Path = typer.Option(BBSKY_CONFIG_FILE, help="Output path for config file"),
) -> None:
    """Create a new Blackbaud Sky API config."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Check if the file already exists, and prompt the user to overwrite it
    if output_path.exists():
        if not typer.confirm(f"Config file already exists at {output_path}. Overwrite?"):
            typer.echo("Aborted.")
            return

    config = SkyConfig(client_id, client_secret, URL(redirect_uri), subscription_key)
    config.to_json_file(output_path)
    typer.echo(f"Config saved to {output_path}")


@cli.command()
def show(
    input_path: Path = typer.Option(BBSKY_CONFIG_FILE, "-i", "--input-path", help="Input config file path"),
    fmt: str = typer.Option("json", "-f", "--fmt", help="Output format", show_choices=True),
) -> None:
    """Show the current Blackbaud Sky API config."""
    if not input_path.exists():
        typer.echo(f"Config not found at {input_path}.")
        return
    config = SkyConfig.from_json_file(input_path)
    _show(config, fmt)


def _show(config: SkyConfig, fmt: str) -> None:
    """Show the current Blackbaud Sky API config.

    Format options:
    - json: JSON format
    - env: Environment variables

    """
    if fmt == "json":
        typer.echo(json.dumps(config.to_dict(), indent=4))
    elif fmt == "env":
        typer.echo(f"export {SkyConfigEnvVars.CLIENT_ID.value}={config.client_id}")
        typer.echo(f"export {SkyConfigEnvVars.CLIENT_SECRET.value}={config.client_secret}")
        typer.echo(f"export {SkyConfigEnvVars.REDIRECT_URI.value}={config.redirect_uri}")
        typer.echo(f"export {SkyConfigEnvVars.SUBSCRIPTION_KEY.value}={config.subscription_key}")


@cli.command()
def update(
    input_path: Path = typer.Option(BBSKY_CONFIG_FILE, "-i", "--input-path", help="Input config file path"),
    client_id: str = typer.Option("", prompt="Client ID (leave blank to keep current value)"),
    client_secret: str = typer.Option("", prompt="Client Secret (leave blank to keep current value)"),
    redirect_uri: str = typer.Option("", prompt="Redirect URI (leave blank to keep current value)"),
    subscription_key: str = typer.Option("", prompt="Subscription Key (leave blank to keep current value)"),
) -> None:
    """Update the current Blackbaud Sky API config."""
    # Keep the existing update logic, but replace click.echo with typer.echo
    # and click.confirm with typer.confirm
    if not any([client_id, client_secret, redirect_uri, subscription_key]):
        typer.echo("No new values provided. Exiting.")
        return

    # Load the original config
    input_path = Path(input_path)
    input_path.parent.mkdir(parents=True, exist_ok=True)
    config_orig = SkyConfig.from_json_file(input_path)

    # Show the original config
    typer.echo("\nCurrent SkyConfig:")
    _show(config_orig, "json")

    # Update with new values
    config_updated = evolve(
        config_orig,
        **{
            "client_id": client_id if client_id else config_orig.client_id,
            "client_secret": client_secret if client_secret else config_orig.client_secret,
            "redirect_uri": URL(redirect_uri) if redirect_uri else config_orig.redirect_uri,
            "subscription_key": subscription_key if subscription_key else config_orig.subscription_key,
        },
    )

    # Show the updated config
    typer.echo("\nUpdated SkyConfig:")
    _show(config_updated, "json")

    # Confirm user wants to save the updated config
    if typer.confirm("Save the updated config?"):
        config_updated.to_json_file(input_path)
        typer.echo(f"Config updated and saved to {input_path}")
    else:
        typer.echo("Config not saved.")


@cli.command()
def purge(
    input_path: Path = typer.Option(BBSKY_CONFIG_FILE, "-i", "--input-path", help="Input config file path"),
) -> None:
    """Delete the current Blackbaud Sky API config."""
    if not input_path.exists():  # Check if the file exists first
        typer.echo(f"Config not found at {input_path}. Nothing to delete.")
        return

    if typer.confirm(f"Are you sure you want to delete the current config '{input_path}'?"):
        input_path.unlink()
        typer.echo(f"Config deleted at {input_path}")
    else:
        typer.echo("Aborted.")
