import logging
import signal
import sys
import threading
from pathlib import Path
from typing import Any

import typer
from bottle import (  # type: ignore
    LocalRequest,
    Response,
    redirect,  # type: ignore
    request,  # type: ignore
    route,  # type: ignore
    run,  # type: ignore
)  # type: ignore

from bbsky.auth import (
    Scope,
    build_authorization_url,
    generate_code_challenge,
    generate_code_verifier,
    get_random_state,
    handle_exchange,
)
from bbsky.config import SkyConfig
from bbsky.data_cls import URL
from bbsky.paths import BBSKY_CONFIG_FILE, BBSKY_TOKEN_FILE
from bbsky.token import OAuth2Token

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

request: LocalRequest

auth_code: str | None = None
oauth_token: OAuth2Token | None = None
config: SkyConfig | None = None

code_verifier = generate_code_verifier(length=64)
code_challenge = generate_code_challenge(code_verifier)
code_challenge_method = "S256"


def set_config_from_saved() -> None:
    if not BBSKY_CONFIG_FILE.exists():
        raise ValueError("No saved config found. Please set the config using the set_config function.")

    global config
    config = SkyConfig.from_stored_config()


def set_config_from_kwargs(
    *, client_id: str, client_secret: str, redirect_uri: str | URL, subscription_key: str
) -> None:
    global config
    redirect_uri = URL(redirect_uri) if isinstance(redirect_uri, str) else redirect_uri
    config = SkyConfig(
        client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, subscription_key=subscription_key
    )


def set_config(
    client_id: str | None = None,
    client_secret: str | None = None,
    redirect_uri: str | URL | None = None,
    subscription_key: str | None = None,
) -> None:
    if client_id and client_secret and redirect_uri and subscription_key:
        set_config_from_kwargs(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            subscription_key=subscription_key,
        )
    else:
        set_config_from_saved()


@route("/")
def home():
    """Home page with a button to login to Blackbaud."""
    return """
    <html>
    <body>
        <form action="/submit" method="post">
            <button type="submit">Login to Blackbaud</button>
        </form>
    </body>
    </html>
    """


@route("/submit", method="POST")
def submit():
    """Redirect to the Blackbaud OAuth2 login flow."""
    return redirect("/login")


@route("/login")
def login_to_blackbaud() -> Response:
    if not config:
        raise ValueError("No config found. Please set the config using the set_config function.")

    state = get_random_state()
    scope = " ".join([Scope.offline_access.value])
    auth_request_url = build_authorization_url(
        config.client_id, code_challenge, code_challenge_method, config.redirect_uri, scope, state
    )

    logger.debug(f"Blackbaud Auth Request URL: {auth_request_url}")
    resp = redirect(auth_request_url)
    return resp


@route("/callback")
def callback_from_blackbaud() -> Response:
    # Step 2: Get the authorization code from the request
    global auth_code
    auth_code = request.GET.get("code")  # type: ignore
    state_echoed = request.GET.get("state")  # type: ignore

    if not config:
        raise ValueError("No config found. Please set the config using the set_config function.")

    if not auth_code:
        raise ValueError("Authorization code not found in the request.")

    if not state_echoed:
        raise ValueError("State not found in the request.")

    response = handle_exchange(config, auth_code, state_echoed, code_verifier)  # type: ignore

    global oauth_token

    if response.status_code == 200:
        logger.info(f"Received access token from Blackbaud. Status code: {response.status_code}")
        oauth_token = OAuth2Token(**response.json())
        logger.debug(f"Access Token: f{str(oauth_token)}")
        return Response("OK", status=200)
    else:
        status_code = response.status_code
        logger.error(f"Error exchanging authorization code for access token. Status code: {status_code}")
        return Response("Error exchanging authorization code for access token", status=status_code)


@route("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "status_code": 200, "message": "Server is running"}


def run_server(host: str, port: int) -> None:
    run(host=host, port=port, quiet=True)


def start_server(host: str, port: int) -> threading.Thread:
    server_thread = threading.Thread(target=run_server, args=(host, port))
    server_thread.daemon = True
    server_thread.start()
    typer.echo(f"Server started on http://{host}:{port}")
    return server_thread


def stop_server(signum: int, frame: Any) -> None:
    typer.echo("\nServer stopped.")
    sys.exit(0)


cli = typer.Typer(help="Create and manage Blackbaud Sky API config.")


@cli.command()
def start(
    host: str = "localhost",
    port: int = 5000,
    token_file: Path = BBSKY_TOKEN_FILE,
    client_id: str = "",
    client_secret: str = "",
    redirect_uri: str = "",
    subscription_key: str = "",
) -> None:
    """
    Start the server to listen for OAuth callbacks.
    """

    # Validate the token file output path
    token_file = Path(token_file)
    if token_file.suffix != ".json":
        raise ValueError("Token file must be a .json file")

    # Set the config
    set_config(
        client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, subscription_key=subscription_key
    )

    signal.signal(signal.SIGINT, stop_server)

    start_server(host, port)

    typer.echo("Waiting for OAuth callback. Press CTRL+C to stop the server.")

    try:
        while True:
            if auth_code and oauth_token:
                typer.echo(f"Received authorization code: {auth_code}")

                # Ask if the user wants to save the token
                save_token = typer.confirm("Do you want to save the token?")
                if not save_token:
                    break

                # If it exists already, confirm overwrite
                if save_token and token_file.exists():
                    overwrite = typer.confirm(f"Token file already exists at {token_file}. Overwrite?")
                    if not overwrite:
                        save_token = False

                if save_token:
                    # Create output path if it doesn't exist
                    token_file.parent.mkdir(parents=True, exist_ok=True)

                    # Save the token
                    oauth_token.save(token_file)
                    typer.echo(f"Token saved to {token_file}")

                break

    except KeyboardInterrupt:
        pass

    sys.exit(0)
