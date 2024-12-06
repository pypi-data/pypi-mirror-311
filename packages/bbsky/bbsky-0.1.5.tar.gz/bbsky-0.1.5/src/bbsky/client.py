import logging
import typing as t
from http import HTTPStatus
from typing import Any, Optional

import hishel
import httpx
from attr import define, field
from tenacity import retry, retry_if_result, stop_after_attempt, wait_exponential

from bbsky.apis import api_name_to_url, sync_functions
from bbsky.cache import setup_transport
from bbsky.config import SkyConfig
from bbsky.crm_constituent_client.client import AuthenticatedClient
from bbsky.data_cls import URL
from bbsky.token import OAuth2Token

logger = logging.getLogger(__name__)


@define
class SkyClient(AuthenticatedClient):
    """
    Builder for Blackbaud Sky API `httpx.Client`.

    Extends `AuthenticatedClient` to provide a flexible, builder-style interface for constructing
    an authenticated `httpx.Client` instance.
    """

    subscription_key = field(default=None, type=str)  # type: ignore

    def _add_header(self, key: str, value: str) -> None:
        """Add a header to the request."""
        self._headers[key] = value

    def _add_required_headers(self) -> None:
        """Add the required headers for Blackbaud Sky API authentication."""
        if not self.token:
            raise ValueError("User token is required to authenticate.")
        self._add_header("Authorization", f"Bearer {self.token}")
        self._add_header("Bb-Api-Subscription-Key", self.subscription_key)

    def get_httpx_client(self) -> hishel.CacheClient | httpx.Client:
        """
        Override of `AuthenticatedClient.get_httpx_client`.

        Constructs and returns an authenticated `httpx.Client`.
        """
        if not self.subscription_key:
            raise ValueError("Subscription key is required to authenticate.")
        if self._client is None:
            self._add_required_headers()
            self._client = hishel.CacheClient(
                base_url=str(self._base_url),
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                transport=setup_transport(),
            )
        return self._client


class BBSky:
    """
    Blackbaud Sky API client interface.

    Acts as a high-level interface to the Blackbaud Sky API,
    providing access to all available API functions.

    Since the API function implementations are generated using
    https://github.com/openapi-generators/openapi-python-client,
    a lot of these we haven't tried and/or do not have test cases for.
    YMMV when trying to use them.

    ---

    Example usage:

    sky = BBSky()
    results = sky.search_constituents(constituent_quick_find="Smith", limit=5)
    print(results)
    """

    def __init__(
        self,
        user_token: Optional[OAuth2Token] = None,
        config: Optional[SkyConfig] = None,
        api_name: str = "crm_constituent",
        base_url: Optional[URL] = None,
    ) -> None:
        """
        Initialize the SkyClient with optional overrides for configuration.
        """
        if api_name and base_url:
            raise ValueError("Cannot specify both `api_name` and `base_url`.")
        if not api_name and not base_url:
            raise ValueError("Must specify either `api_name` or `base_url`.")

        # Set the base URL
        # If base URL is explicitly provided, use it
        if base_url:
            self.base_url = base_url
        # Otherwise, convert the API name to a URL
        else:
            self.base_url = api_name_to_url(api_name)

        self.config = config or SkyConfig.from_stored_config()
        self.user_token = user_token or OAuth2Token.from_cache()
        self.client = SkyClient(
            base_url=str(self.base_url),
            token=self.user_token.access_token,
            subscription_key=self.config.subscription_key,  # type: ignore
        )

    def refresh_user_token(self, cache_token: bool = False) -> None:
        # Have to get a new instance since the token is frozen
        new_token = self.user_token.refresh(self.config)
        self.user_token = new_token
        # Update the client's token
        self.client.token = new_token.access_token

        if cache_token:
            new_token.to_cache()

    @retry(
        retry=retry_if_result(lambda response: response.status_code == HTTPStatus.UNAUTHORIZED),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    def request(self, api_name: str, **kwargs: Any) -> httpx.Response:
        """
        Make a request to the Blackbaud Sky API.

        Args:
            api_name: The name of the API to call.
            kwargs: Additional keyword arguments to pass to the API function.

        Returns:
            The response from the API.
        """
        response = sync_functions[api_name](client=self.client, **kwargs)

        # If 401 is returned, refresh the token and retry
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            logger.debug(f"Received {response.status_code} response from {api_name}. Refreshing token and retrying.")
            self.user_token.refresh(self.config)
            # Update the client's token
            self.client.token = self.user_token.access_token

        return response

    @retry(
        retry=retry_if_result(lambda response: response.status_code == HTTPStatus.UNAUTHORIZED),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    async def request_async(self, api_name: str, **kwargs: Any) -> httpx.Response:
        """
        Make an asynchronous request to the Blackbaud Sky API.

        Args:
            api_name: The name of the API to call.
            kwargs: Additional keyword arguments to pass to the API function.

        Returns:
            The response from the API.
        """
        raise NotImplementedError("Async functions are not yet implemented")

    def __getattr__(self, name: str) -> t.Callable[..., httpx.Response]:
        """
        Provide access to API functions as attributes.

        Args:
            name: The name of the attribute to access.

        Returns:
            The API function.
        """

        def _api_function(**kwargs: Any) -> httpx.Response:
            return self.request(name, **kwargs)

        return _api_function

    def __dir__(self) -> list[str]:
        """
        Provide a list of attributes available on the client.

        Returns:
            A list of attribute names.
        """
        return list(sync_functions.keys())
