from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.constituent_solicit_code_list_collection import ConstituentSolicitCodeListCollection
from ...models.list_constituent_solicit_codes_date_range import ListConstituentSolicitCodesDateRange
from ...models.list_constituent_solicit_codes_site_filter_mode import (
    ListConstituentSolicitCodesSiteFilterMode,
)
from ...models.problem_details import ProblemDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    constituent_id: str,
    *,
    site_id: Union[Unset, str] = UNSET,
    site_filter_mode: Union[Unset, ListConstituentSolicitCodesSiteFilterMode] = UNSET,
    sites_selected: Union[Unset, str] = UNSET,
    show_expired: Union[Unset, bool] = UNSET,
    date_range: Union[Unset, ListConstituentSolicitCodesDateRange] = UNSET,
    limit: Union[Unset, int] = UNSET,
    session_key: Union[Unset, str] = UNSET,
    infinity_session: Union[Unset, str] = UNSET,
    more_rows_range_key: Union[Unset, str] = UNSET,
    start_row_index: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["site_id"] = site_id

    json_site_filter_mode: Union[Unset, str] = UNSET
    if not isinstance(site_filter_mode, Unset):
        json_site_filter_mode = site_filter_mode.value

    params["site_filter_mode"] = json_site_filter_mode

    params["sites_selected"] = sites_selected

    params["show_expired"] = show_expired

    json_date_range: Union[Unset, str] = UNSET
    if not isinstance(date_range, Unset):
        json_date_range = date_range.value

    params["date_range"] = json_date_range

    params["limit"] = limit

    params["session_key"] = session_key

    params["infinity_session"] = infinity_session

    params["more_rows_range_key"] = more_rows_range_key

    params["start_row_index"] = start_row_index

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/constituents/{constituent_id}/solicitcodes",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ConstituentSolicitCodeListCollection, ProblemDetails]]:
    if response.status_code == 200:
        response_200 = ConstituentSolicitCodeListCollection.from_dict(response.json())

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
) -> Response[Union[Any, ConstituentSolicitCodeListCollection, ProblemDetails]]:
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
    site_id: Union[Unset, str] = UNSET,
    site_filter_mode: Union[Unset, ListConstituentSolicitCodesSiteFilterMode] = UNSET,
    sites_selected: Union[Unset, str] = UNSET,
    show_expired: Union[Unset, bool] = UNSET,
    date_range: Union[Unset, ListConstituentSolicitCodesDateRange] = UNSET,
    limit: Union[Unset, int] = UNSET,
    session_key: Union[Unset, str] = UNSET,
    infinity_session: Union[Unset, str] = UNSET,
    more_rows_range_key: Union[Unset, str] = UNSET,
    start_row_index: Union[Unset, int] = UNSET,
) -> Response[Union[Any, ConstituentSolicitCodeListCollection, ProblemDetails]]:
    """List constituent solicit codes.

     Constituent solicit code list

    Args:
        constituent_id (str):
        site_id (Union[Unset, str]):
        site_filter_mode (Union[Unset, ListConstituentSolicitCodesSiteFilterMode]):
        sites_selected (Union[Unset, str]):
        show_expired (Union[Unset, bool]):
        date_range (Union[Unset, ListConstituentSolicitCodesDateRange]):
        limit (Union[Unset, int]):
        session_key (Union[Unset, str]):
        infinity_session (Union[Unset, str]):
        more_rows_range_key (Union[Unset, str]):
        start_row_index (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ConstituentSolicitCodeListCollection, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        constituent_id=constituent_id,
        site_id=site_id,
        site_filter_mode=site_filter_mode,
        sites_selected=sites_selected,
        show_expired=show_expired,
        date_range=date_range,
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
    constituent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    site_id: Union[Unset, str] = UNSET,
    site_filter_mode: Union[Unset, ListConstituentSolicitCodesSiteFilterMode] = UNSET,
    sites_selected: Union[Unset, str] = UNSET,
    show_expired: Union[Unset, bool] = UNSET,
    date_range: Union[Unset, ListConstituentSolicitCodesDateRange] = UNSET,
    limit: Union[Unset, int] = UNSET,
    session_key: Union[Unset, str] = UNSET,
    infinity_session: Union[Unset, str] = UNSET,
    more_rows_range_key: Union[Unset, str] = UNSET,
    start_row_index: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, ConstituentSolicitCodeListCollection, ProblemDetails]]:
    """List constituent solicit codes.

     Constituent solicit code list

    Args:
        constituent_id (str):
        site_id (Union[Unset, str]):
        site_filter_mode (Union[Unset, ListConstituentSolicitCodesSiteFilterMode]):
        sites_selected (Union[Unset, str]):
        show_expired (Union[Unset, bool]):
        date_range (Union[Unset, ListConstituentSolicitCodesDateRange]):
        limit (Union[Unset, int]):
        session_key (Union[Unset, str]):
        infinity_session (Union[Unset, str]):
        more_rows_range_key (Union[Unset, str]):
        start_row_index (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ConstituentSolicitCodeListCollection, ProblemDetails]
    """

    return sync_detailed(
        constituent_id=constituent_id,
        client=client,
        site_id=site_id,
        site_filter_mode=site_filter_mode,
        sites_selected=sites_selected,
        show_expired=show_expired,
        date_range=date_range,
        limit=limit,
        session_key=session_key,
        infinity_session=infinity_session,
        more_rows_range_key=more_rows_range_key,
        start_row_index=start_row_index,
    ).parsed


async def asyncio_detailed(
    constituent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    site_id: Union[Unset, str] = UNSET,
    site_filter_mode: Union[Unset, ListConstituentSolicitCodesSiteFilterMode] = UNSET,
    sites_selected: Union[Unset, str] = UNSET,
    show_expired: Union[Unset, bool] = UNSET,
    date_range: Union[Unset, ListConstituentSolicitCodesDateRange] = UNSET,
    limit: Union[Unset, int] = UNSET,
    session_key: Union[Unset, str] = UNSET,
    infinity_session: Union[Unset, str] = UNSET,
    more_rows_range_key: Union[Unset, str] = UNSET,
    start_row_index: Union[Unset, int] = UNSET,
) -> Response[Union[Any, ConstituentSolicitCodeListCollection, ProblemDetails]]:
    """List constituent solicit codes.

     Constituent solicit code list

    Args:
        constituent_id (str):
        site_id (Union[Unset, str]):
        site_filter_mode (Union[Unset, ListConstituentSolicitCodesSiteFilterMode]):
        sites_selected (Union[Unset, str]):
        show_expired (Union[Unset, bool]):
        date_range (Union[Unset, ListConstituentSolicitCodesDateRange]):
        limit (Union[Unset, int]):
        session_key (Union[Unset, str]):
        infinity_session (Union[Unset, str]):
        more_rows_range_key (Union[Unset, str]):
        start_row_index (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ConstituentSolicitCodeListCollection, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        constituent_id=constituent_id,
        site_id=site_id,
        site_filter_mode=site_filter_mode,
        sites_selected=sites_selected,
        show_expired=show_expired,
        date_range=date_range,
        limit=limit,
        session_key=session_key,
        infinity_session=infinity_session,
        more_rows_range_key=more_rows_range_key,
        start_row_index=start_row_index,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    constituent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    site_id: Union[Unset, str] = UNSET,
    site_filter_mode: Union[Unset, ListConstituentSolicitCodesSiteFilterMode] = UNSET,
    sites_selected: Union[Unset, str] = UNSET,
    show_expired: Union[Unset, bool] = UNSET,
    date_range: Union[Unset, ListConstituentSolicitCodesDateRange] = UNSET,
    limit: Union[Unset, int] = UNSET,
    session_key: Union[Unset, str] = UNSET,
    infinity_session: Union[Unset, str] = UNSET,
    more_rows_range_key: Union[Unset, str] = UNSET,
    start_row_index: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, ConstituentSolicitCodeListCollection, ProblemDetails]]:
    """List constituent solicit codes.

     Constituent solicit code list

    Args:
        constituent_id (str):
        site_id (Union[Unset, str]):
        site_filter_mode (Union[Unset, ListConstituentSolicitCodesSiteFilterMode]):
        sites_selected (Union[Unset, str]):
        show_expired (Union[Unset, bool]):
        date_range (Union[Unset, ListConstituentSolicitCodesDateRange]):
        limit (Union[Unset, int]):
        session_key (Union[Unset, str]):
        infinity_session (Union[Unset, str]):
        more_rows_range_key (Union[Unset, str]):
        start_row_index (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ConstituentSolicitCodeListCollection, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            constituent_id=constituent_id,
            client=client,
            site_id=site_id,
            site_filter_mode=site_filter_mode,
            sites_selected=sites_selected,
            show_expired=show_expired,
            date_range=date_range,
            limit=limit,
            session_key=session_key,
            infinity_session=infinity_session,
            more_rows_range_key=more_rows_range_key,
            start_row_index=start_row_index,
        )
    ).parsed
