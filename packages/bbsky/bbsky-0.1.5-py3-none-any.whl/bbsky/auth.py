import base64
import enum
import hashlib
import os
from urllib.parse import urlencode

import httpx

from bbsky.config import SkyConfig
from bbsky.constants import TOKEN_URL
from bbsky.data_cls import URL
from bbsky.logging_utils import logger


class Scope(enum.Enum):
    """
    Scope for Blackbaud API authentication

    See this URL for more information:
    https://developer.blackbaud.com/skyapi/docs/applications/scopes

    """

    # Add other scopes as needed
    offline_access = "offline_access"


def generate_code_verifier(length: int = 64) -> str:
    return base64.urlsafe_b64encode(os.urandom(length)).decode("utf-8").replace("=", "")


def generate_code_challenge(verifier: str) -> str:
    sha256 = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(sha256).decode("utf-8").replace("=", "")


def get_random_state() -> str:
    return base64.urlsafe_b64encode(os.urandom(32)).decode().replace("=", "")


def get_state_from_oauth_url(url: URL) -> str | None:
    return url.query.get("state")


def build_authorization_url(
    client_id: str, code_challenge: str, code_challenge_method: str, redirect_uri: URL, scope: str, state: str
):
    # Build up auth params
    # See docs:
    # https://developer.blackbaud.com/skyapi/docs/authorization/auth-code-flow/confidential-application/tutorial
    # TODO: Add in PKCE stuff
    auth_params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",  # should always be 'code'
        "scope": scope,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": code_challenge_method,
    }
    auth_request_url = f"https://oauth2.sky.blackbaud.com/authorization?{urlencode(auth_params)}"
    return auth_request_url


def handle_exchange(config: SkyConfig, auth_code: str, state_echoed: str, code_verifier: str) -> httpx.Response:
    # Step 3: Exchange the authorization code for an access token
    client_id = config.client_id
    token_params: dict[str, str] = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": str(config.redirect_uri),
        "client_id": client_id,
        "client_secret": config.client_secret,
        "state": state_echoed,
        "code_verifier": code_verifier,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64.b64encode(client_id.encode()).decode()}",
    }
    response = httpx.post(str(TOKEN_URL), data=token_params, headers=headers)
    return response


def handle_refresh(config: SkyConfig, token_data: dict[str, str]) -> httpx.Response:
    logger.debug("Refreshing token")
    # https://developer.blackbaud.com/skyapi/docs/authorization/auth-code-flow/confidential-application/tutorial
    client_id_b64 = base64.b64encode(config.client_id.encode()).decode()
    client_secret_b64 = base64.b64encode(config.client_secret.encode()).decode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {client_id_b64}:{client_secret_b64}",
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": token_data["refresh_token"],
        "client_id": config.client_id,
        "client_secret": config.client_secret,
    }
    response = httpx.post(str(TOKEN_URL), data=data, headers=headers)
    response.raise_for_status()
    return response
