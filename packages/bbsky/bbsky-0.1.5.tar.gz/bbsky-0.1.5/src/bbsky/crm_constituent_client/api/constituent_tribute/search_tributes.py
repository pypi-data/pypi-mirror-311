from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_details import ProblemDetails
from ...models.search_tributes_date_filter import SearchTributesDateFilter
from ...models.tribute_search_collection import TributeSearchCollection
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    tribute_text: Union[Unset, str] = UNSET,
    tributee_key_name: Union[Unset, str] = UNSET,
    tributee_first_name: Union[Unset, str] = UNSET,
    tributee_lookup_id: Union[Unset, str] = UNSET,
    tribute_type: Union[Unset, str] = UNSET,
    acknowledgee_key_name: Union[Unset, str] = UNSET,
    acknowledgee_first_name: Union[Unset, str] = UNSET,
    date_filter: Union[Unset, SearchTributesDateFilter] = UNSET,
    designation: Union[Unset, str] = UNSET,
    site_id: Union[Unset, str] = UNSET,
    include_inactive: Union[Unset, bool] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["tribute_text"] = tribute_text

    params["tributee_key_name"] = tributee_key_name

    params["tributee_first_name"] = tributee_first_name

    params["tributee_lookup_id"] = tributee_lookup_id

    params["tribute_type"] = tribute_type

    params["acknowledgee_key_name"] = acknowledgee_key_name

    params["acknowledgee_first_name"] = acknowledgee_first_name

    json_date_filter: Union[Unset, str] = UNSET
    if not isinstance(date_filter, Unset):
        json_date_filter = date_filter.value

    params["date_filter"] = json_date_filter

    params["designation"] = designation

    params["site_id"] = site_id

    params["include_inactive"] = include_inactive

    params["exact_match_only"] = exact_match_only

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/tributes/search",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ProblemDetails, TributeSearchCollection]]:
    if response.status_code == 200:
        response_200 = TributeSearchCollection.from_dict(response.json())

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
) -> Response[Union[Any, ProblemDetails, TributeSearchCollection]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    tribute_text: Union[Unset, str] = UNSET,
    tributee_key_name: Union[Unset, str] = UNSET,
    tributee_first_name: Union[Unset, str] = UNSET,
    tributee_lookup_id: Union[Unset, str] = UNSET,
    tribute_type: Union[Unset, str] = UNSET,
    acknowledgee_key_name: Union[Unset, str] = UNSET,
    acknowledgee_first_name: Union[Unset, str] = UNSET,
    date_filter: Union[Unset, SearchTributesDateFilter] = UNSET,
    designation: Union[Unset, str] = UNSET,
    site_id: Union[Unset, str] = UNSET,
    include_inactive: Union[Unset, bool] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Union[Any, ProblemDetails, TributeSearchCollection]]:
    """Search for tributes.

     Search for tributes.

    Args:
        tribute_text (Union[Unset, str]):
        tributee_key_name (Union[Unset, str]):
        tributee_first_name (Union[Unset, str]):
        tributee_lookup_id (Union[Unset, str]):
        tribute_type (Union[Unset, str]):
        acknowledgee_key_name (Union[Unset, str]):
        acknowledgee_first_name (Union[Unset, str]):
        date_filter (Union[Unset, SearchTributesDateFilter]):
        designation (Union[Unset, str]):
        site_id (Union[Unset, str]):
        include_inactive (Union[Unset, bool]):
        exact_match_only (Union[Unset, bool]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails, TributeSearchCollection]]
    """

    kwargs = _get_kwargs(
        tribute_text=tribute_text,
        tributee_key_name=tributee_key_name,
        tributee_first_name=tributee_first_name,
        tributee_lookup_id=tributee_lookup_id,
        tribute_type=tribute_type,
        acknowledgee_key_name=acknowledgee_key_name,
        acknowledgee_first_name=acknowledgee_first_name,
        date_filter=date_filter,
        designation=designation,
        site_id=site_id,
        include_inactive=include_inactive,
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
    tribute_text: Union[Unset, str] = UNSET,
    tributee_key_name: Union[Unset, str] = UNSET,
    tributee_first_name: Union[Unset, str] = UNSET,
    tributee_lookup_id: Union[Unset, str] = UNSET,
    tribute_type: Union[Unset, str] = UNSET,
    acknowledgee_key_name: Union[Unset, str] = UNSET,
    acknowledgee_first_name: Union[Unset, str] = UNSET,
    date_filter: Union[Unset, SearchTributesDateFilter] = UNSET,
    designation: Union[Unset, str] = UNSET,
    site_id: Union[Unset, str] = UNSET,
    include_inactive: Union[Unset, bool] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, ProblemDetails, TributeSearchCollection]]:
    """Search for tributes.

     Search for tributes.

    Args:
        tribute_text (Union[Unset, str]):
        tributee_key_name (Union[Unset, str]):
        tributee_first_name (Union[Unset, str]):
        tributee_lookup_id (Union[Unset, str]):
        tribute_type (Union[Unset, str]):
        acknowledgee_key_name (Union[Unset, str]):
        acknowledgee_first_name (Union[Unset, str]):
        date_filter (Union[Unset, SearchTributesDateFilter]):
        designation (Union[Unset, str]):
        site_id (Union[Unset, str]):
        include_inactive (Union[Unset, bool]):
        exact_match_only (Union[Unset, bool]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails, TributeSearchCollection]
    """

    return sync_detailed(
        client=client,
        tribute_text=tribute_text,
        tributee_key_name=tributee_key_name,
        tributee_first_name=tributee_first_name,
        tributee_lookup_id=tributee_lookup_id,
        tribute_type=tribute_type,
        acknowledgee_key_name=acknowledgee_key_name,
        acknowledgee_first_name=acknowledgee_first_name,
        date_filter=date_filter,
        designation=designation,
        site_id=site_id,
        include_inactive=include_inactive,
        exact_match_only=exact_match_only,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    tribute_text: Union[Unset, str] = UNSET,
    tributee_key_name: Union[Unset, str] = UNSET,
    tributee_first_name: Union[Unset, str] = UNSET,
    tributee_lookup_id: Union[Unset, str] = UNSET,
    tribute_type: Union[Unset, str] = UNSET,
    acknowledgee_key_name: Union[Unset, str] = UNSET,
    acknowledgee_first_name: Union[Unset, str] = UNSET,
    date_filter: Union[Unset, SearchTributesDateFilter] = UNSET,
    designation: Union[Unset, str] = UNSET,
    site_id: Union[Unset, str] = UNSET,
    include_inactive: Union[Unset, bool] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Union[Any, ProblemDetails, TributeSearchCollection]]:
    """Search for tributes.

     Search for tributes.

    Args:
        tribute_text (Union[Unset, str]):
        tributee_key_name (Union[Unset, str]):
        tributee_first_name (Union[Unset, str]):
        tributee_lookup_id (Union[Unset, str]):
        tribute_type (Union[Unset, str]):
        acknowledgee_key_name (Union[Unset, str]):
        acknowledgee_first_name (Union[Unset, str]):
        date_filter (Union[Unset, SearchTributesDateFilter]):
        designation (Union[Unset, str]):
        site_id (Union[Unset, str]):
        include_inactive (Union[Unset, bool]):
        exact_match_only (Union[Unset, bool]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails, TributeSearchCollection]]
    """

    kwargs = _get_kwargs(
        tribute_text=tribute_text,
        tributee_key_name=tributee_key_name,
        tributee_first_name=tributee_first_name,
        tributee_lookup_id=tributee_lookup_id,
        tribute_type=tribute_type,
        acknowledgee_key_name=acknowledgee_key_name,
        acknowledgee_first_name=acknowledgee_first_name,
        date_filter=date_filter,
        designation=designation,
        site_id=site_id,
        include_inactive=include_inactive,
        exact_match_only=exact_match_only,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    tribute_text: Union[Unset, str] = UNSET,
    tributee_key_name: Union[Unset, str] = UNSET,
    tributee_first_name: Union[Unset, str] = UNSET,
    tributee_lookup_id: Union[Unset, str] = UNSET,
    tribute_type: Union[Unset, str] = UNSET,
    acknowledgee_key_name: Union[Unset, str] = UNSET,
    acknowledgee_first_name: Union[Unset, str] = UNSET,
    date_filter: Union[Unset, SearchTributesDateFilter] = UNSET,
    designation: Union[Unset, str] = UNSET,
    site_id: Union[Unset, str] = UNSET,
    include_inactive: Union[Unset, bool] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, ProblemDetails, TributeSearchCollection]]:
    """Search for tributes.

     Search for tributes.

    Args:
        tribute_text (Union[Unset, str]):
        tributee_key_name (Union[Unset, str]):
        tributee_first_name (Union[Unset, str]):
        tributee_lookup_id (Union[Unset, str]):
        tribute_type (Union[Unset, str]):
        acknowledgee_key_name (Union[Unset, str]):
        acknowledgee_first_name (Union[Unset, str]):
        date_filter (Union[Unset, SearchTributesDateFilter]):
        designation (Union[Unset, str]):
        site_id (Union[Unset, str]):
        include_inactive (Union[Unset, bool]):
        exact_match_only (Union[Unset, bool]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails, TributeSearchCollection]
    """

    return (
        await asyncio_detailed(
            client=client,
            tribute_text=tribute_text,
            tributee_key_name=tributee_key_name,
            tributee_first_name=tributee_first_name,
            tributee_lookup_id=tributee_lookup_id,
            tribute_type=tribute_type,
            acknowledgee_key_name=acknowledgee_key_name,
            acknowledgee_first_name=acknowledgee_first_name,
            date_filter=date_filter,
            designation=designation,
            site_id=site_id,
            include_inactive=include_inactive,
            exact_match_only=exact_match_only,
            limit=limit,
        )
    ).parsed
