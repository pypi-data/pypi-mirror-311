from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.constituent_fundraiser_list_collection import ConstituentFundraiserListCollection
from ...models.problem_details import ProblemDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    org_positions_selection_id: Union[Unset, str] = UNSET,
    include_stewardship: Union[Unset, bool] = UNSET,
    show_inactive: Union[Unset, bool] = UNSET,
    only_owned_interactions: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
    session_key: Union[Unset, str] = UNSET,
    infinity_session: Union[Unset, str] = UNSET,
    more_rows_range_key: Union[Unset, str] = UNSET,
    start_row_index: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["org_positions_selection_id"] = org_positions_selection_id

    params["include_stewardship"] = include_stewardship

    params["show_inactive"] = show_inactive

    params["only_owned_interactions"] = only_owned_interactions

    params["limit"] = limit

    params["session_key"] = session_key

    params["infinity_session"] = infinity_session

    params["more_rows_range_key"] = more_rows_range_key

    params["start_row_index"] = start_row_index

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/fundraisers/List",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ConstituentFundraiserListCollection, ProblemDetails]]:
    if response.status_code == 200:
        response_200 = ConstituentFundraiserListCollection.from_dict(response.json())

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
) -> Response[Union[Any, ConstituentFundraiserListCollection, ProblemDetails]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    org_positions_selection_id: Union[Unset, str] = UNSET,
    include_stewardship: Union[Unset, bool] = UNSET,
    show_inactive: Union[Unset, bool] = UNSET,
    only_owned_interactions: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
    session_key: Union[Unset, str] = UNSET,
    infinity_session: Union[Unset, str] = UNSET,
    more_rows_range_key: Union[Unset, str] = UNSET,
    start_row_index: Union[Unset, int] = UNSET,
) -> Response[Union[Any, ConstituentFundraiserListCollection, ProblemDetails]]:
    """List constituent fundraisers.

     Returns a list of all fundraisers

    Args:
        org_positions_selection_id (Union[Unset, str]):
        include_stewardship (Union[Unset, bool]):
        show_inactive (Union[Unset, bool]):
        only_owned_interactions (Union[Unset, bool]):
        limit (Union[Unset, int]):
        session_key (Union[Unset, str]):
        infinity_session (Union[Unset, str]):
        more_rows_range_key (Union[Unset, str]):
        start_row_index (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ConstituentFundraiserListCollection, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        org_positions_selection_id=org_positions_selection_id,
        include_stewardship=include_stewardship,
        show_inactive=show_inactive,
        only_owned_interactions=only_owned_interactions,
        limit=limit,
        session_key=session_key,
        infinity_session=infinity_session,
        more_rows_range_key=more_rows_range_key,
        start_row_index=start_row_index,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    org_positions_selection_id: Union[Unset, str] = UNSET,
    include_stewardship: Union[Unset, bool] = UNSET,
    show_inactive: Union[Unset, bool] = UNSET,
    only_owned_interactions: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
    session_key: Union[Unset, str] = UNSET,
    infinity_session: Union[Unset, str] = UNSET,
    more_rows_range_key: Union[Unset, str] = UNSET,
    start_row_index: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, ConstituentFundraiserListCollection, ProblemDetails]]:
    """List constituent fundraisers.

     Returns a list of all fundraisers

    Args:
        org_positions_selection_id (Union[Unset, str]):
        include_stewardship (Union[Unset, bool]):
        show_inactive (Union[Unset, bool]):
        only_owned_interactions (Union[Unset, bool]):
        limit (Union[Unset, int]):
        session_key (Union[Unset, str]):
        infinity_session (Union[Unset, str]):
        more_rows_range_key (Union[Unset, str]):
        start_row_index (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ConstituentFundraiserListCollection, ProblemDetails]
    """

    return sync_detailed(
        client=client,
        org_positions_selection_id=org_positions_selection_id,
        include_stewardship=include_stewardship,
        show_inactive=show_inactive,
        only_owned_interactions=only_owned_interactions,
        limit=limit,
        session_key=session_key,
        infinity_session=infinity_session,
        more_rows_range_key=more_rows_range_key,
        start_row_index=start_row_index,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    org_positions_selection_id: Union[Unset, str] = UNSET,
    include_stewardship: Union[Unset, bool] = UNSET,
    show_inactive: Union[Unset, bool] = UNSET,
    only_owned_interactions: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
    session_key: Union[Unset, str] = UNSET,
    infinity_session: Union[Unset, str] = UNSET,
    more_rows_range_key: Union[Unset, str] = UNSET,
    start_row_index: Union[Unset, int] = UNSET,
) -> Response[Union[Any, ConstituentFundraiserListCollection, ProblemDetails]]:
    """List constituent fundraisers.

     Returns a list of all fundraisers

    Args:
        org_positions_selection_id (Union[Unset, str]):
        include_stewardship (Union[Unset, bool]):
        show_inactive (Union[Unset, bool]):
        only_owned_interactions (Union[Unset, bool]):
        limit (Union[Unset, int]):
        session_key (Union[Unset, str]):
        infinity_session (Union[Unset, str]):
        more_rows_range_key (Union[Unset, str]):
        start_row_index (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ConstituentFundraiserListCollection, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        org_positions_selection_id=org_positions_selection_id,
        include_stewardship=include_stewardship,
        show_inactive=show_inactive,
        only_owned_interactions=only_owned_interactions,
        limit=limit,
        session_key=session_key,
        infinity_session=infinity_session,
        more_rows_range_key=more_rows_range_key,
        start_row_index=start_row_index,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    org_positions_selection_id: Union[Unset, str] = UNSET,
    include_stewardship: Union[Unset, bool] = UNSET,
    show_inactive: Union[Unset, bool] = UNSET,
    only_owned_interactions: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
    session_key: Union[Unset, str] = UNSET,
    infinity_session: Union[Unset, str] = UNSET,
    more_rows_range_key: Union[Unset, str] = UNSET,
    start_row_index: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, ConstituentFundraiserListCollection, ProblemDetails]]:
    """List constituent fundraisers.

     Returns a list of all fundraisers

    Args:
        org_positions_selection_id (Union[Unset, str]):
        include_stewardship (Union[Unset, bool]):
        show_inactive (Union[Unset, bool]):
        only_owned_interactions (Union[Unset, bool]):
        limit (Union[Unset, int]):
        session_key (Union[Unset, str]):
        infinity_session (Union[Unset, str]):
        more_rows_range_key (Union[Unset, str]):
        start_row_index (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ConstituentFundraiserListCollection, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            client=client,
            org_positions_selection_id=org_positions_selection_id,
            include_stewardship=include_stewardship,
            show_inactive=show_inactive,
            only_owned_interactions=only_owned_interactions,
            limit=limit,
            session_key=session_key,
            infinity_session=infinity_session,
            more_rows_range_key=more_rows_range_key,
            start_row_index=start_row_index,
        )
    ).parsed
