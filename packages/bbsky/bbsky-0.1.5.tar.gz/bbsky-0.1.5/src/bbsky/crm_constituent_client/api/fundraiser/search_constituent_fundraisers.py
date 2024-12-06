import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.constituent_fundraiser_search_collection import ConstituentFundraiserSearchCollection
from ...models.problem_details import ProblemDetails
from ...models.search_constituent_fundraisers_site_filter_mode import (
    SearchConstituentFundraisersSiteFilterMode,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    constituent_type: Union[Unset, int] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    key_name: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    lookup_id: Union[Unset, str] = UNSET,
    address_block: Union[Unset, str] = UNSET,
    city: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
    post_code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    include_inactive: Union[Unset, bool] = UNSET,
    include_deceased: Union[Unset, bool] = UNSET,
    only_primary_address: Union[Unset, bool] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    only_prospects: Union[Unset, bool] = UNSET,
    only_fundraisers: Union[Unset, bool] = UNSET,
    only_staff: Union[Unset, bool] = UNSET,
    only_volunteers: Union[Unset, bool] = UNSET,
    ssn: Union[Unset, str] = UNSET,
    check_nick_name: Union[Unset, bool] = UNSET,
    check_aliases: Union[Unset, bool] = UNSET,
    check_merged_constituents: Union[Unset, bool] = UNSET,
    minimum_date: Union[Unset, datetime.date] = UNSET,
    include_individuals: Union[Unset, bool] = UNSET,
    include_organizations: Union[Unset, bool] = UNSET,
    include_groups: Union[Unset, bool] = UNSET,
    check_alternate_lookup_ids: Union[Unset, bool] = UNSET,
    fuzzy_search_on_name: Union[Unset, bool] = UNSET,
    site_filter_mode: Union[Unset, SearchConstituentFundraisersSiteFilterMode] = UNSET,
    sites_selected: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["constituent_type"] = constituent_type

    params["full_name"] = full_name

    params["key_name"] = key_name

    params["first_name"] = first_name

    params["lookup_id"] = lookup_id

    params["address_block"] = address_block

    params["city"] = city

    params["state"] = state

    params["post_code"] = post_code

    params["country"] = country

    params["include_inactive"] = include_inactive

    params["include_deceased"] = include_deceased

    params["only_primary_address"] = only_primary_address

    params["exact_match_only"] = exact_match_only

    params["only_prospects"] = only_prospects

    params["only_fundraisers"] = only_fundraisers

    params["only_staff"] = only_staff

    params["only_volunteers"] = only_volunteers

    params["ssn"] = ssn

    params["check_nick_name"] = check_nick_name

    params["check_aliases"] = check_aliases

    params["check_merged_constituents"] = check_merged_constituents

    json_minimum_date: Union[Unset, str] = UNSET
    if not isinstance(minimum_date, Unset):
        json_minimum_date = minimum_date.isoformat()
    params["minimum_date"] = json_minimum_date

    params["include_individuals"] = include_individuals

    params["include_organizations"] = include_organizations

    params["include_groups"] = include_groups

    params["check_alternate_lookup_ids"] = check_alternate_lookup_ids

    params["fuzzy_search_on_name"] = fuzzy_search_on_name

    json_site_filter_mode: Union[Unset, str] = UNSET
    if not isinstance(site_filter_mode, Unset):
        json_site_filter_mode = site_filter_mode.value

    params["site_filter_mode"] = json_site_filter_mode

    params["sites_selected"] = sites_selected

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/constituents/fundraisersearch",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ConstituentFundraiserSearchCollection, ProblemDetails]]:
    if response.status_code == 200:
        response_200 = ConstituentFundraiserSearchCollection.from_dict(response.json())

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
) -> Response[Union[Any, ConstituentFundraiserSearchCollection, ProblemDetails]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    constituent_type: Union[Unset, int] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    key_name: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    lookup_id: Union[Unset, str] = UNSET,
    address_block: Union[Unset, str] = UNSET,
    city: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
    post_code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    include_inactive: Union[Unset, bool] = UNSET,
    include_deceased: Union[Unset, bool] = UNSET,
    only_primary_address: Union[Unset, bool] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    only_prospects: Union[Unset, bool] = UNSET,
    only_fundraisers: Union[Unset, bool] = UNSET,
    only_staff: Union[Unset, bool] = UNSET,
    only_volunteers: Union[Unset, bool] = UNSET,
    ssn: Union[Unset, str] = UNSET,
    check_nick_name: Union[Unset, bool] = UNSET,
    check_aliases: Union[Unset, bool] = UNSET,
    check_merged_constituents: Union[Unset, bool] = UNSET,
    minimum_date: Union[Unset, datetime.date] = UNSET,
    include_individuals: Union[Unset, bool] = UNSET,
    include_organizations: Union[Unset, bool] = UNSET,
    include_groups: Union[Unset, bool] = UNSET,
    check_alternate_lookup_ids: Union[Unset, bool] = UNSET,
    fuzzy_search_on_name: Union[Unset, bool] = UNSET,
    site_filter_mode: Union[Unset, SearchConstituentFundraisersSiteFilterMode] = UNSET,
    sites_selected: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Union[Any, ConstituentFundraiserSearchCollection, ProblemDetails]]:
    """Search for constituent fundraisers.

     Search for fundraisers.

    Args:
        constituent_type (Union[Unset, int]):
        full_name (Union[Unset, str]):
        key_name (Union[Unset, str]):
        first_name (Union[Unset, str]):
        lookup_id (Union[Unset, str]):
        address_block (Union[Unset, str]):
        city (Union[Unset, str]):
        state (Union[Unset, str]):
        post_code (Union[Unset, str]):
        country (Union[Unset, str]):
        include_inactive (Union[Unset, bool]):
        include_deceased (Union[Unset, bool]):
        only_primary_address (Union[Unset, bool]):
        exact_match_only (Union[Unset, bool]):
        only_prospects (Union[Unset, bool]):
        only_fundraisers (Union[Unset, bool]):
        only_staff (Union[Unset, bool]):
        only_volunteers (Union[Unset, bool]):
        ssn (Union[Unset, str]):
        check_nick_name (Union[Unset, bool]):
        check_aliases (Union[Unset, bool]):
        check_merged_constituents (Union[Unset, bool]):
        minimum_date (Union[Unset, datetime.date]):
        include_individuals (Union[Unset, bool]):
        include_organizations (Union[Unset, bool]):
        include_groups (Union[Unset, bool]):
        check_alternate_lookup_ids (Union[Unset, bool]):
        fuzzy_search_on_name (Union[Unset, bool]):
        site_filter_mode (Union[Unset, SearchConstituentFundraisersSiteFilterMode]):
        sites_selected (Union[Unset, str]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ConstituentFundraiserSearchCollection, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        constituent_type=constituent_type,
        full_name=full_name,
        key_name=key_name,
        first_name=first_name,
        lookup_id=lookup_id,
        address_block=address_block,
        city=city,
        state=state,
        post_code=post_code,
        country=country,
        include_inactive=include_inactive,
        include_deceased=include_deceased,
        only_primary_address=only_primary_address,
        exact_match_only=exact_match_only,
        only_prospects=only_prospects,
        only_fundraisers=only_fundraisers,
        only_staff=only_staff,
        only_volunteers=only_volunteers,
        ssn=ssn,
        check_nick_name=check_nick_name,
        check_aliases=check_aliases,
        check_merged_constituents=check_merged_constituents,
        minimum_date=minimum_date,
        include_individuals=include_individuals,
        include_organizations=include_organizations,
        include_groups=include_groups,
        check_alternate_lookup_ids=check_alternate_lookup_ids,
        fuzzy_search_on_name=fuzzy_search_on_name,
        site_filter_mode=site_filter_mode,
        sites_selected=sites_selected,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    constituent_type: Union[Unset, int] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    key_name: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    lookup_id: Union[Unset, str] = UNSET,
    address_block: Union[Unset, str] = UNSET,
    city: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
    post_code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    include_inactive: Union[Unset, bool] = UNSET,
    include_deceased: Union[Unset, bool] = UNSET,
    only_primary_address: Union[Unset, bool] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    only_prospects: Union[Unset, bool] = UNSET,
    only_fundraisers: Union[Unset, bool] = UNSET,
    only_staff: Union[Unset, bool] = UNSET,
    only_volunteers: Union[Unset, bool] = UNSET,
    ssn: Union[Unset, str] = UNSET,
    check_nick_name: Union[Unset, bool] = UNSET,
    check_aliases: Union[Unset, bool] = UNSET,
    check_merged_constituents: Union[Unset, bool] = UNSET,
    minimum_date: Union[Unset, datetime.date] = UNSET,
    include_individuals: Union[Unset, bool] = UNSET,
    include_organizations: Union[Unset, bool] = UNSET,
    include_groups: Union[Unset, bool] = UNSET,
    check_alternate_lookup_ids: Union[Unset, bool] = UNSET,
    fuzzy_search_on_name: Union[Unset, bool] = UNSET,
    site_filter_mode: Union[Unset, SearchConstituentFundraisersSiteFilterMode] = UNSET,
    sites_selected: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, ConstituentFundraiserSearchCollection, ProblemDetails]]:
    """Search for constituent fundraisers.

     Search for fundraisers.

    Args:
        constituent_type (Union[Unset, int]):
        full_name (Union[Unset, str]):
        key_name (Union[Unset, str]):
        first_name (Union[Unset, str]):
        lookup_id (Union[Unset, str]):
        address_block (Union[Unset, str]):
        city (Union[Unset, str]):
        state (Union[Unset, str]):
        post_code (Union[Unset, str]):
        country (Union[Unset, str]):
        include_inactive (Union[Unset, bool]):
        include_deceased (Union[Unset, bool]):
        only_primary_address (Union[Unset, bool]):
        exact_match_only (Union[Unset, bool]):
        only_prospects (Union[Unset, bool]):
        only_fundraisers (Union[Unset, bool]):
        only_staff (Union[Unset, bool]):
        only_volunteers (Union[Unset, bool]):
        ssn (Union[Unset, str]):
        check_nick_name (Union[Unset, bool]):
        check_aliases (Union[Unset, bool]):
        check_merged_constituents (Union[Unset, bool]):
        minimum_date (Union[Unset, datetime.date]):
        include_individuals (Union[Unset, bool]):
        include_organizations (Union[Unset, bool]):
        include_groups (Union[Unset, bool]):
        check_alternate_lookup_ids (Union[Unset, bool]):
        fuzzy_search_on_name (Union[Unset, bool]):
        site_filter_mode (Union[Unset, SearchConstituentFundraisersSiteFilterMode]):
        sites_selected (Union[Unset, str]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ConstituentFundraiserSearchCollection, ProblemDetails]
    """

    return sync_detailed(
        client=client,
        constituent_type=constituent_type,
        full_name=full_name,
        key_name=key_name,
        first_name=first_name,
        lookup_id=lookup_id,
        address_block=address_block,
        city=city,
        state=state,
        post_code=post_code,
        country=country,
        include_inactive=include_inactive,
        include_deceased=include_deceased,
        only_primary_address=only_primary_address,
        exact_match_only=exact_match_only,
        only_prospects=only_prospects,
        only_fundraisers=only_fundraisers,
        only_staff=only_staff,
        only_volunteers=only_volunteers,
        ssn=ssn,
        check_nick_name=check_nick_name,
        check_aliases=check_aliases,
        check_merged_constituents=check_merged_constituents,
        minimum_date=minimum_date,
        include_individuals=include_individuals,
        include_organizations=include_organizations,
        include_groups=include_groups,
        check_alternate_lookup_ids=check_alternate_lookup_ids,
        fuzzy_search_on_name=fuzzy_search_on_name,
        site_filter_mode=site_filter_mode,
        sites_selected=sites_selected,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    constituent_type: Union[Unset, int] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    key_name: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    lookup_id: Union[Unset, str] = UNSET,
    address_block: Union[Unset, str] = UNSET,
    city: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
    post_code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    include_inactive: Union[Unset, bool] = UNSET,
    include_deceased: Union[Unset, bool] = UNSET,
    only_primary_address: Union[Unset, bool] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    only_prospects: Union[Unset, bool] = UNSET,
    only_fundraisers: Union[Unset, bool] = UNSET,
    only_staff: Union[Unset, bool] = UNSET,
    only_volunteers: Union[Unset, bool] = UNSET,
    ssn: Union[Unset, str] = UNSET,
    check_nick_name: Union[Unset, bool] = UNSET,
    check_aliases: Union[Unset, bool] = UNSET,
    check_merged_constituents: Union[Unset, bool] = UNSET,
    minimum_date: Union[Unset, datetime.date] = UNSET,
    include_individuals: Union[Unset, bool] = UNSET,
    include_organizations: Union[Unset, bool] = UNSET,
    include_groups: Union[Unset, bool] = UNSET,
    check_alternate_lookup_ids: Union[Unset, bool] = UNSET,
    fuzzy_search_on_name: Union[Unset, bool] = UNSET,
    site_filter_mode: Union[Unset, SearchConstituentFundraisersSiteFilterMode] = UNSET,
    sites_selected: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Union[Any, ConstituentFundraiserSearchCollection, ProblemDetails]]:
    """Search for constituent fundraisers.

     Search for fundraisers.

    Args:
        constituent_type (Union[Unset, int]):
        full_name (Union[Unset, str]):
        key_name (Union[Unset, str]):
        first_name (Union[Unset, str]):
        lookup_id (Union[Unset, str]):
        address_block (Union[Unset, str]):
        city (Union[Unset, str]):
        state (Union[Unset, str]):
        post_code (Union[Unset, str]):
        country (Union[Unset, str]):
        include_inactive (Union[Unset, bool]):
        include_deceased (Union[Unset, bool]):
        only_primary_address (Union[Unset, bool]):
        exact_match_only (Union[Unset, bool]):
        only_prospects (Union[Unset, bool]):
        only_fundraisers (Union[Unset, bool]):
        only_staff (Union[Unset, bool]):
        only_volunteers (Union[Unset, bool]):
        ssn (Union[Unset, str]):
        check_nick_name (Union[Unset, bool]):
        check_aliases (Union[Unset, bool]):
        check_merged_constituents (Union[Unset, bool]):
        minimum_date (Union[Unset, datetime.date]):
        include_individuals (Union[Unset, bool]):
        include_organizations (Union[Unset, bool]):
        include_groups (Union[Unset, bool]):
        check_alternate_lookup_ids (Union[Unset, bool]):
        fuzzy_search_on_name (Union[Unset, bool]):
        site_filter_mode (Union[Unset, SearchConstituentFundraisersSiteFilterMode]):
        sites_selected (Union[Unset, str]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ConstituentFundraiserSearchCollection, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        constituent_type=constituent_type,
        full_name=full_name,
        key_name=key_name,
        first_name=first_name,
        lookup_id=lookup_id,
        address_block=address_block,
        city=city,
        state=state,
        post_code=post_code,
        country=country,
        include_inactive=include_inactive,
        include_deceased=include_deceased,
        only_primary_address=only_primary_address,
        exact_match_only=exact_match_only,
        only_prospects=only_prospects,
        only_fundraisers=only_fundraisers,
        only_staff=only_staff,
        only_volunteers=only_volunteers,
        ssn=ssn,
        check_nick_name=check_nick_name,
        check_aliases=check_aliases,
        check_merged_constituents=check_merged_constituents,
        minimum_date=minimum_date,
        include_individuals=include_individuals,
        include_organizations=include_organizations,
        include_groups=include_groups,
        check_alternate_lookup_ids=check_alternate_lookup_ids,
        fuzzy_search_on_name=fuzzy_search_on_name,
        site_filter_mode=site_filter_mode,
        sites_selected=sites_selected,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    constituent_type: Union[Unset, int] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    key_name: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    lookup_id: Union[Unset, str] = UNSET,
    address_block: Union[Unset, str] = UNSET,
    city: Union[Unset, str] = UNSET,
    state: Union[Unset, str] = UNSET,
    post_code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    include_inactive: Union[Unset, bool] = UNSET,
    include_deceased: Union[Unset, bool] = UNSET,
    only_primary_address: Union[Unset, bool] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    only_prospects: Union[Unset, bool] = UNSET,
    only_fundraisers: Union[Unset, bool] = UNSET,
    only_staff: Union[Unset, bool] = UNSET,
    only_volunteers: Union[Unset, bool] = UNSET,
    ssn: Union[Unset, str] = UNSET,
    check_nick_name: Union[Unset, bool] = UNSET,
    check_aliases: Union[Unset, bool] = UNSET,
    check_merged_constituents: Union[Unset, bool] = UNSET,
    minimum_date: Union[Unset, datetime.date] = UNSET,
    include_individuals: Union[Unset, bool] = UNSET,
    include_organizations: Union[Unset, bool] = UNSET,
    include_groups: Union[Unset, bool] = UNSET,
    check_alternate_lookup_ids: Union[Unset, bool] = UNSET,
    fuzzy_search_on_name: Union[Unset, bool] = UNSET,
    site_filter_mode: Union[Unset, SearchConstituentFundraisersSiteFilterMode] = UNSET,
    sites_selected: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, ConstituentFundraiserSearchCollection, ProblemDetails]]:
    """Search for constituent fundraisers.

     Search for fundraisers.

    Args:
        constituent_type (Union[Unset, int]):
        full_name (Union[Unset, str]):
        key_name (Union[Unset, str]):
        first_name (Union[Unset, str]):
        lookup_id (Union[Unset, str]):
        address_block (Union[Unset, str]):
        city (Union[Unset, str]):
        state (Union[Unset, str]):
        post_code (Union[Unset, str]):
        country (Union[Unset, str]):
        include_inactive (Union[Unset, bool]):
        include_deceased (Union[Unset, bool]):
        only_primary_address (Union[Unset, bool]):
        exact_match_only (Union[Unset, bool]):
        only_prospects (Union[Unset, bool]):
        only_fundraisers (Union[Unset, bool]):
        only_staff (Union[Unset, bool]):
        only_volunteers (Union[Unset, bool]):
        ssn (Union[Unset, str]):
        check_nick_name (Union[Unset, bool]):
        check_aliases (Union[Unset, bool]):
        check_merged_constituents (Union[Unset, bool]):
        minimum_date (Union[Unset, datetime.date]):
        include_individuals (Union[Unset, bool]):
        include_organizations (Union[Unset, bool]):
        include_groups (Union[Unset, bool]):
        check_alternate_lookup_ids (Union[Unset, bool]):
        fuzzy_search_on_name (Union[Unset, bool]):
        site_filter_mode (Union[Unset, SearchConstituentFundraisersSiteFilterMode]):
        sites_selected (Union[Unset, str]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ConstituentFundraiserSearchCollection, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            client=client,
            constituent_type=constituent_type,
            full_name=full_name,
            key_name=key_name,
            first_name=first_name,
            lookup_id=lookup_id,
            address_block=address_block,
            city=city,
            state=state,
            post_code=post_code,
            country=country,
            include_inactive=include_inactive,
            include_deceased=include_deceased,
            only_primary_address=only_primary_address,
            exact_match_only=exact_match_only,
            only_prospects=only_prospects,
            only_fundraisers=only_fundraisers,
            only_staff=only_staff,
            only_volunteers=only_volunteers,
            ssn=ssn,
            check_nick_name=check_nick_name,
            check_aliases=check_aliases,
            check_merged_constituents=check_merged_constituents,
            minimum_date=minimum_date,
            include_individuals=include_individuals,
            include_organizations=include_organizations,
            include_groups=include_groups,
            check_alternate_lookup_ids=check_alternate_lookup_ids,
            fuzzy_search_on_name=fuzzy_search_on_name,
            site_filter_mode=site_filter_mode,
            sites_selected=sites_selected,
            limit=limit,
        )
    ).parsed
