from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.constituent_address_view import ConstituentAddressView
from ...types import Response


def _get_kwargs(
    address_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/addresses/{address_id}/view",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ConstituentAddressView]:
    if response.status_code == 200:
        response_200 = ConstituentAddressView.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ConstituentAddressView]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ConstituentAddressView]:
    """View a constituent address.

     This operation is used for viewing basic address inoperationation.

    Args:
        address_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConstituentAddressView]
    """

    kwargs = _get_kwargs(
        address_id=address_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ConstituentAddressView]:
    """View a constituent address.

     This operation is used for viewing basic address inoperationation.

    Args:
        address_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConstituentAddressView
    """

    return sync_detailed(
        address_id=address_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ConstituentAddressView]:
    """View a constituent address.

     This operation is used for viewing basic address inoperationation.

    Args:
        address_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConstituentAddressView]
    """

    kwargs = _get_kwargs(
        address_id=address_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ConstituentAddressView]:
    """View a constituent address.

     This operation is used for viewing basic address inoperationation.

    Args:
        address_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConstituentAddressView
    """

    return (
        await asyncio_detailed(
            address_id=address_id,
            client=client,
        )
    ).parsed
