from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.constituent_profile_picture_view import ConstituentProfilePictureView
from ...types import Response


def _get_kwargs(
    constituent_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/constituents/{constituent_id}/profilepicture",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ConstituentProfilePictureView]:
    if response.status_code == 200:
        response_200 = ConstituentProfilePictureView.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ConstituentProfilePictureView]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    constituent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ConstituentProfilePictureView]:
    """View a constituent profile picture.

     Defines the fields for the individual personal inoperationation tile.

    Args:
        constituent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConstituentProfilePictureView]
    """

    kwargs = _get_kwargs(
        constituent_id=constituent_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    constituent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ConstituentProfilePictureView]:
    """View a constituent profile picture.

     Defines the fields for the individual personal inoperationation tile.

    Args:
        constituent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConstituentProfilePictureView
    """

    return sync_detailed(
        constituent_id=constituent_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    constituent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ConstituentProfilePictureView]:
    """View a constituent profile picture.

     Defines the fields for the individual personal inoperationation tile.

    Args:
        constituent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConstituentProfilePictureView]
    """

    kwargs = _get_kwargs(
        constituent_id=constituent_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    constituent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ConstituentProfilePictureView]:
    """View a constituent profile picture.

     Defines the fields for the individual personal inoperationation tile.

    Args:
        constituent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConstituentProfilePictureView
    """

    return (
        await asyncio_detailed(
            constituent_id=constituent_id,
            client=client,
        )
    ).parsed
