from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.constituent_address_search_collection import ConstituentAddressSearchCollection
from ...models.problem_details import ProblemDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    key_name: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    lookup_id: Union[Unset, str] = UNSET,
    address_block: Union[Unset, str] = UNSET,
    city: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
    post_code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    only_primary_address: Union[Unset, bool] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["key_name"] = key_name

    params["first_name"] = first_name

    params["lookup_id"] = lookup_id

    params["address_block"] = address_block

    params["city"] = city

    params["state"] = state

    params["post_code"] = post_code

    params["country"] = country

    params["only_primary_address"] = only_primary_address

    params["exact_match_only"] = exact_match_only

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/addresses/search",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ConstituentAddressSearchCollection, ProblemDetails]]:
    if response.status_code == 200:
        response_200 = ConstituentAddressSearchCollection.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ProblemDetails.from_dict(response.json())

        return response_400
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ConstituentAddressSearchCollection, ProblemDetails]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    key_name: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    lookup_id: Union[Unset, str] = UNSET,
    address_block: Union[Unset, str] = UNSET,
    city: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
    post_code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    only_primary_address: Union[Unset, bool] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Union[Any, ConstituentAddressSearchCollection, ProblemDetails]]:
    """Search for constituent addresses.

     This provides the ability to search for a constituent's addresses.

    Args:
        key_name (Union[Unset, str]):
        first_name (Union[Unset, str]):
        lookup_id (Union[Unset, str]):
        address_block (Union[Unset, str]):
        city (Union[Unset, str]):
        state (Union[Unset, str]):
        post_code (Union[Unset, str]):
        country (Union[Unset, str]):
        only_primary_address (Union[Unset, bool]):
        exact_match_only (Union[Unset, bool]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ConstituentAddressSearchCollection, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        key_name=key_name,
        first_name=first_name,
        lookup_id=lookup_id,
        address_block=address_block,
        city=city,
        state=state,
        post_code=post_code,
        country=country,
        only_primary_address=only_primary_address,
        exact_match_only=exact_match_only,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    key_name: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    lookup_id: Union[Unset, str] = UNSET,
    address_block: Union[Unset, str] = UNSET,
    city: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
    post_code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    only_primary_address: Union[Unset, bool] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, ConstituentAddressSearchCollection, ProblemDetails]]:
    """Search for constituent addresses.

     This provides the ability to search for a constituent's addresses.

    Args:
        key_name (Union[Unset, str]):
        first_name (Union[Unset, str]):
        lookup_id (Union[Unset, str]):
        address_block (Union[Unset, str]):
        city (Union[Unset, str]):
        state (Union[Unset, str]):
        post_code (Union[Unset, str]):
        country (Union[Unset, str]):
        only_primary_address (Union[Unset, bool]):
        exact_match_only (Union[Unset, bool]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ConstituentAddressSearchCollection, ProblemDetails]
    """

    return sync_detailed(
        client=client,
        key_name=key_name,
        first_name=first_name,
        lookup_id=lookup_id,
        address_block=address_block,
        city=city,
        state=state,
        post_code=post_code,
        country=country,
        only_primary_address=only_primary_address,
        exact_match_only=exact_match_only,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    key_name: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    lookup_id: Union[Unset, str] = UNSET,
    address_block: Union[Unset, str] = UNSET,
    city: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
    post_code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    only_primary_address: Union[Unset, bool] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Union[Any, ConstituentAddressSearchCollection, ProblemDetails]]:
    """Search for constituent addresses.

     This provides the ability to search for a constituent's addresses.

    Args:
        key_name (Union[Unset, str]):
        first_name (Union[Unset, str]):
        lookup_id (Union[Unset, str]):
        address_block (Union[Unset, str]):
        city (Union[Unset, str]):
        state (Union[Unset, str]):
        post_code (Union[Unset, str]):
        country (Union[Unset, str]):
        only_primary_address (Union[Unset, bool]):
        exact_match_only (Union[Unset, bool]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ConstituentAddressSearchCollection, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        key_name=key_name,
        first_name=first_name,
        lookup_id=lookup_id,
        address_block=address_block,
        city=city,
        state=state,
        post_code=post_code,
        country=country,
        only_primary_address=only_primary_address,
        exact_match_only=exact_match_only,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    key_name: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    lookup_id: Union[Unset, str] = UNSET,
    address_block: Union[Unset, str] = UNSET,
    city: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
    post_code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    only_primary_address: Union[Unset, bool] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, ConstituentAddressSearchCollection, ProblemDetails]]:
    """Search for constituent addresses.

     This provides the ability to search for a constituent's addresses.

    Args:
        key_name (Union[Unset, str]):
        first_name (Union[Unset, str]):
        lookup_id (Union[Unset, str]):
        address_block (Union[Unset, str]):
        city (Union[Unset, str]):
        state (Union[Unset, str]):
        post_code (Union[Unset, str]):
        country (Union[Unset, str]):
        only_primary_address (Union[Unset, bool]):
        exact_match_only (Union[Unset, bool]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ConstituentAddressSearchCollection, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            client=client,
            key_name=key_name,
            first_name=first_name,
            lookup_id=lookup_id,
            address_block=address_block,
            city=city,
            state=state,
            post_code=post_code,
            country=country,
            only_primary_address=only_primary_address,
            exact_match_only=exact_match_only,
            limit=limit,
        )
    ).parsed
