import json
import logging
from pathlib import Path
from typing import Any

import typer
from attrs import asdict, define

from bbsky.auth import handle_refresh
from bbsky.config import SkyConfig
from bbsky.paths import BBSKY_TOKEN_FILE

logger = logging.getLogger(__name__)


@define(slots=True, frozen=True)
class OAuth2Token:
    """User Access Credentials for Blackbaud Sky API"""

    access_token: str
    refresh_token: str
    expires_in: int
    refresh_token_expires_in: int
    token_type: str
    environment_id: str
    environment_name: str
    legal_entity_id: str
    legal_entity_name: str
    user_id: str
    email: str
    family_name: str
    given_name: str
    mode: str

    def __str__(self):
        token_trunc = self.access_token[:4] + "..." + self.access_token[-4:]
        return (
            f"Access Token: {token_trunc} (expires in {self.expires_in} seconds) | Refresh Token: {self.refresh_token}"
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OAuth2Token":
        return cls(**data)

    @classmethod
    def load(cls, input_file: Path) -> "OAuth2Token":
        """Load the token from a file."""
        return cls(**json.loads(input_file.read_text()))

    @classmethod
    def from_cache(cls) -> "OAuth2Token":
        """Load the token from the default cache file."""
        return cls.load(BBSKY_TOKEN_FILE)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def save(self, output_file: Path) -> None:
        """Save the token to a file."""
        output_file.write_text(json.dumps(self.to_dict(), indent=4))

    def to_cache(self) -> None:
        """Save the token to the default cache file."""
        self.save(BBSKY_TOKEN_FILE)

    def refresh(self, config: SkyConfig) -> "OAuth2Token":
        token_data = self.to_dict()
        response = handle_refresh(config, token_data)
        new_token = OAuth2Token(**response.json())
        return new_token


cli = typer.Typer(help="Manage Blackbaud Sky API tokens.")


@cli.command()
def show(
    token_file: Path = typer.Option(BBSKY_TOKEN_FILE, "-t", "--token-file", help="Input token file path"),
    fmt: str = typer.Option("str", "-f", "--fmt", help="Output format (str, json)"),
) -> None:
    """Show the current token."""

    # Check if the token file exists
    if not token_file.exists():
        typer.echo("No token found.")
        return

    token = OAuth2Token.load(token_file)
    typer.echo(f"Token file: {token_file}")
    if fmt == "str":
        typer.echo(f"Token for {token.email}: {str(token)}")
    elif fmt == "json":
        typer.echo(json.dumps(token.to_dict(), indent=4))


@cli.command()
def purge(
    token_file: Path = typer.Option(BBSKY_TOKEN_FILE, "-t", "--token-file", help="Input token file path"),
) -> None:
    """Purge the current token."""

    # Check if the token file exists
    if not token_file.exists():
        typer.echo("No token found.")
        return

    # Confirm with the user
    token = OAuth2Token.load(token_file)
    typer.echo(f"Current token: {str(token)}")

    if typer.confirm("Are you sure you want to purge the current token?"):
        token_file.unlink()
        typer.echo("Token purged.")
    else:
        typer.echo("Aborted. Token not purged.")


@cli.command()
def refresh(
    token_file: Path = typer.Option(BBSKY_TOKEN_FILE, "-t", "--token-file", help="Input token file path"),
) -> None:
    """Refresh the current token."""
    token = OAuth2Token.load(token_file)
    config = SkyConfig.load()

    new_token = token.refresh(config)
    new_token.to_cache()

    typer.echo(f"Token refreshed: {str(new_token)}")
