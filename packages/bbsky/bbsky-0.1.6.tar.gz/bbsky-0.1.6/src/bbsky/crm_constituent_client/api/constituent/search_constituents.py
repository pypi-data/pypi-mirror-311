import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.constituent_search_collection import ConstituentSearchCollection
from ...models.problem_details import ProblemDetails
from ...models.search_constituents_site_filter_mode import SearchConstituentsSiteFilterMode
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    constituent_quick_find: Union[Unset, str] = UNSET,
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
    check_nickname: Union[Unset, bool] = UNSET,
    check_aliases: Union[Unset, bool] = UNSET,
    classof: Union[Unset, int] = UNSET,
    minimum_date: Union[Unset, datetime.date] = UNSET,
    exclude_households: Union[Unset, bool] = UNSET,
    email_address: Union[Unset, str] = UNSET,
    include_individuals: Union[Unset, bool] = UNSET,
    include_organizations: Union[Unset, bool] = UNSET,
    include_groups: Union[Unset, bool] = UNSET,
    check_alternate_lookup_ids: Union[Unset, bool] = UNSET,
    fuzzy_search_on_name: Union[Unset, bool] = UNSET,
    phone_number: Union[Unset, str] = UNSET,
    middle_name: Union[Unset, str] = UNSET,
    suffix: Union[Unset, str] = UNSET,
    constituency: Union[Unset, str] = UNSET,
    sourcecode: Union[Unset, str] = UNSET,
    site_filter_mode: Union[Unset, SearchConstituentsSiteFilterMode] = UNSET,
    sites_selected: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["constituent_quick_find"] = constituent_quick_find

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

    params["check_nickname"] = check_nickname

    params["check_aliases"] = check_aliases

    params["classof"] = classof

    json_minimum_date: Union[Unset, str] = UNSET
    if not isinstance(minimum_date, Unset):
        json_minimum_date = minimum_date.isoformat()
    params["minimum_date"] = json_minimum_date

    params["exclude_households"] = exclude_households

    params["email_address"] = email_address

    params["include_individuals"] = include_individuals

    params["include_organizations"] = include_organizations

    params["include_groups"] = include_groups

    params["check_alternate_lookup_ids"] = check_alternate_lookup_ids

    params["fuzzy_search_on_name"] = fuzzy_search_on_name

    params["phone_number"] = phone_number

    params["middle_name"] = middle_name

    params["suffix"] = suffix

    params["constituency"] = constituency

    params["sourcecode"] = sourcecode

    json_site_filter_mode: Union[Unset, str] = UNSET
    if not isinstance(site_filter_mode, Unset):
        json_site_filter_mode = site_filter_mode.value

    params["site_filter_mode"] = json_site_filter_mode

    params["sites_selected"] = sites_selected

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/constituents/search",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ConstituentSearchCollection, ProblemDetails]]:
    if response.status_code == 200:
        response_200 = ConstituentSearchCollection.from_dict(response.json())

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
) -> Response[Union[Any, ConstituentSearchCollection, ProblemDetails]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    constituent_quick_find: Union[Unset, str] = UNSET,
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
    check_nickname: Union[Unset, bool] = UNSET,
    check_aliases: Union[Unset, bool] = UNSET,
    classof: Union[Unset, int] = UNSET,
    minimum_date: Union[Unset, datetime.date] = UNSET,
    exclude_households: Union[Unset, bool] = UNSET,
    email_address: Union[Unset, str] = UNSET,
    include_individuals: Union[Unset, bool] = UNSET,
    include_organizations: Union[Unset, bool] = UNSET,
    include_groups: Union[Unset, bool] = UNSET,
    check_alternate_lookup_ids: Union[Unset, bool] = UNSET,
    fuzzy_search_on_name: Union[Unset, bool] = UNSET,
    phone_number: Union[Unset, str] = UNSET,
    middle_name: Union[Unset, str] = UNSET,
    suffix: Union[Unset, str] = UNSET,
    constituency: Union[Unset, str] = UNSET,
    sourcecode: Union[Unset, str] = UNSET,
    site_filter_mode: Union[Unset, SearchConstituentsSiteFilterMode] = UNSET,
    sites_selected: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Union[Any, ConstituentSearchCollection, ProblemDetails]]:
    """Search for constituents.

     This provides the ability to search for constituents.

    Args:
        constituent_quick_find (Union[Unset, str]):
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
        check_nickname (Union[Unset, bool]):
        check_aliases (Union[Unset, bool]):
        classof (Union[Unset, int]):
        minimum_date (Union[Unset, datetime.date]):
        exclude_households (Union[Unset, bool]):
        email_address (Union[Unset, str]):
        include_individuals (Union[Unset, bool]):
        include_organizations (Union[Unset, bool]):
        include_groups (Union[Unset, bool]):
        check_alternate_lookup_ids (Union[Unset, bool]):
        fuzzy_search_on_name (Union[Unset, bool]):
        phone_number (Union[Unset, str]):
        middle_name (Union[Unset, str]):
        suffix (Union[Unset, str]):
        constituency (Union[Unset, str]):
        sourcecode (Union[Unset, str]):
        site_filter_mode (Union[Unset, SearchConstituentsSiteFilterMode]):
        sites_selected (Union[Unset, str]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ConstituentSearchCollection, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        constituent_quick_find=constituent_quick_find,
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
        check_nickname=check_nickname,
        check_aliases=check_aliases,
        classof=classof,
        minimum_date=minimum_date,
        exclude_households=exclude_households,
        email_address=email_address,
        include_individuals=include_individuals,
        include_organizations=include_organizations,
        include_groups=include_groups,
        check_alternate_lookup_ids=check_alternate_lookup_ids,
        fuzzy_search_on_name=fuzzy_search_on_name,
        phone_number=phone_number,
        middle_name=middle_name,
        suffix=suffix,
        constituency=constituency,
        sourcecode=sourcecode,
        site_filter_mode=site_filter_mode,
        sites_selected=sites_selected,
        limit=limit,
    )

    response = client.get_httpx_client().request(**kwargs)
    # https://api.sky.blackbaud.com/crm-conmg/constituents/search
    # https://api.sky.blackbaud.com/constituents/search
    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    constituent_quick_find: Union[Unset, str] = UNSET,
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
    check_nickname: Union[Unset, bool] = UNSET,
    check_aliases: Union[Unset, bool] = UNSET,
    classof: Union[Unset, int] = UNSET,
    minimum_date: Union[Unset, datetime.date] = UNSET,
    exclude_households: Union[Unset, bool] = UNSET,
    email_address: Union[Unset, str] = UNSET,
    include_individuals: Union[Unset, bool] = UNSET,
    include_organizations: Union[Unset, bool] = UNSET,
    include_groups: Union[Unset, bool] = UNSET,
    check_alternate_lookup_ids: Union[Unset, bool] = UNSET,
    fuzzy_search_on_name: Union[Unset, bool] = UNSET,
    phone_number: Union[Unset, str] = UNSET,
    middle_name: Union[Unset, str] = UNSET,
    suffix: Union[Unset, str] = UNSET,
    constituency: Union[Unset, str] = UNSET,
    sourcecode: Union[Unset, str] = UNSET,
    site_filter_mode: Union[Unset, SearchConstituentsSiteFilterMode] = UNSET,
    sites_selected: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, ConstituentSearchCollection, ProblemDetails]]:
    """Search for constituents.

     This provides the ability to search for constituents.

    Args:
        constituent_quick_find (Union[Unset, str]):
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
        check_nickname (Union[Unset, bool]):
        check_aliases (Union[Unset, bool]):
        classof (Union[Unset, int]):
        minimum_date (Union[Unset, datetime.date]):
        exclude_households (Union[Unset, bool]):
        email_address (Union[Unset, str]):
        include_individuals (Union[Unset, bool]):
        include_organizations (Union[Unset, bool]):
        include_groups (Union[Unset, bool]):
        check_alternate_lookup_ids (Union[Unset, bool]):
        fuzzy_search_on_name (Union[Unset, bool]):
        phone_number (Union[Unset, str]):
        middle_name (Union[Unset, str]):
        suffix (Union[Unset, str]):
        constituency (Union[Unset, str]):
        sourcecode (Union[Unset, str]):
        site_filter_mode (Union[Unset, SearchConstituentsSiteFilterMode]):
        sites_selected (Union[Unset, str]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ConstituentSearchCollection, ProblemDetails]
    """

    return sync_detailed(
        client=client,
        constituent_quick_find=constituent_quick_find,
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
        check_nickname=check_nickname,
        check_aliases=check_aliases,
        classof=classof,
        minimum_date=minimum_date,
        exclude_households=exclude_households,
        email_address=email_address,
        include_individuals=include_individuals,
        include_organizations=include_organizations,
        include_groups=include_groups,
        check_alternate_lookup_ids=check_alternate_lookup_ids,
        fuzzy_search_on_name=fuzzy_search_on_name,
        phone_number=phone_number,
        middle_name=middle_name,
        suffix=suffix,
        constituency=constituency,
        sourcecode=sourcecode,
        site_filter_mode=site_filter_mode,
        sites_selected=sites_selected,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    constituent_quick_find: Union[Unset, str] = UNSET,
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
    check_nickname: Union[Unset, bool] = UNSET,
    check_aliases: Union[Unset, bool] = UNSET,
    classof: Union[Unset, int] = UNSET,
    minimum_date: Union[Unset, datetime.date] = UNSET,
    exclude_households: Union[Unset, bool] = UNSET,
    email_address: Union[Unset, str] = UNSET,
    include_individuals: Union[Unset, bool] = UNSET,
    include_organizations: Union[Unset, bool] = UNSET,
    include_groups: Union[Unset, bool] = UNSET,
    check_alternate_lookup_ids: Union[Unset, bool] = UNSET,
    fuzzy_search_on_name: Union[Unset, bool] = UNSET,
    phone_number: Union[Unset, str] = UNSET,
    middle_name: Union[Unset, str] = UNSET,
    suffix: Union[Unset, str] = UNSET,
    constituency: Union[Unset, str] = UNSET,
    sourcecode: Union[Unset, str] = UNSET,
    site_filter_mode: Union[Unset, SearchConstituentsSiteFilterMode] = UNSET,
    sites_selected: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Union[Any, ConstituentSearchCollection, ProblemDetails]]:
    """Search for constituents.

     This provides the ability to search for constituents.

    Args:
        constituent_quick_find (Union[Unset, str]):
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
        check_nickname (Union[Unset, bool]):
        check_aliases (Union[Unset, bool]):
        classof (Union[Unset, int]):
        minimum_date (Union[Unset, datetime.date]):
        exclude_households (Union[Unset, bool]):
        email_address (Union[Unset, str]):
        include_individuals (Union[Unset, bool]):
        include_organizations (Union[Unset, bool]):
        include_groups (Union[Unset, bool]):
        check_alternate_lookup_ids (Union[Unset, bool]):
        fuzzy_search_on_name (Union[Unset, bool]):
        phone_number (Union[Unset, str]):
        middle_name (Union[Unset, str]):
        suffix (Union[Unset, str]):
        constituency (Union[Unset, str]):
        sourcecode (Union[Unset, str]):
        site_filter_mode (Union[Unset, SearchConstituentsSiteFilterMode]):
        sites_selected (Union[Unset, str]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ConstituentSearchCollection, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        constituent_quick_find=constituent_quick_find,
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
        check_nickname=check_nickname,
        check_aliases=check_aliases,
        classof=classof,
        minimum_date=minimum_date,
        exclude_households=exclude_households,
        email_address=email_address,
        include_individuals=include_individuals,
        include_organizations=include_organizations,
        include_groups=include_groups,
        check_alternate_lookup_ids=check_alternate_lookup_ids,
        fuzzy_search_on_name=fuzzy_search_on_name,
        phone_number=phone_number,
        middle_name=middle_name,
        suffix=suffix,
        constituency=constituency,
        sourcecode=sourcecode,
        site_filter_mode=site_filter_mode,
        sites_selected=sites_selected,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    constituent_quick_find: Union[Unset, str] = UNSET,
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
    check_nickname: Union[Unset, bool] = UNSET,
    check_aliases: Union[Unset, bool] = UNSET,
    classof: Union[Unset, int] = UNSET,
    minimum_date: Union[Unset, datetime.date] = UNSET,
    exclude_households: Union[Unset, bool] = UNSET,
    email_address: Union[Unset, str] = UNSET,
    include_individuals: Union[Unset, bool] = UNSET,
    include_organizations: Union[Unset, bool] = UNSET,
    include_groups: Union[Unset, bool] = UNSET,
    check_alternate_lookup_ids: Union[Unset, bool] = UNSET,
    fuzzy_search_on_name: Union[Unset, bool] = UNSET,
    phone_number: Union[Unset, str] = UNSET,
    middle_name: Union[Unset, str] = UNSET,
    suffix: Union[Unset, str] = UNSET,
    constituency: Union[Unset, str] = UNSET,
    sourcecode: Union[Unset, str] = UNSET,
    site_filter_mode: Union[Unset, SearchConstituentsSiteFilterMode] = UNSET,
    sites_selected: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, ConstituentSearchCollection, ProblemDetails]]:
    """Search for constituents.

     This provides the ability to search for constituents.

    Args:
        constituent_quick_find (Union[Unset, str]):
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
        check_nickname (Union[Unset, bool]):
        check_aliases (Union[Unset, bool]):
        classof (Union[Unset, int]):
        minimum_date (Union[Unset, datetime.date]):
        exclude_households (Union[Unset, bool]):
        email_address (Union[Unset, str]):
        include_individuals (Union[Unset, bool]):
        include_organizations (Union[Unset, bool]):
        include_groups (Union[Unset, bool]):
        check_alternate_lookup_ids (Union[Unset, bool]):
        fuzzy_search_on_name (Union[Unset, bool]):
        phone_number (Union[Unset, str]):
        middle_name (Union[Unset, str]):
        suffix (Union[Unset, str]):
        constituency (Union[Unset, str]):
        sourcecode (Union[Unset, str]):
        site_filter_mode (Union[Unset, SearchConstituentsSiteFilterMode]):
        sites_selected (Union[Unset, str]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ConstituentSearchCollection, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            client=client,
            constituent_quick_find=constituent_quick_find,
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
            check_nickname=check_nickname,
            check_aliases=check_aliases,
            classof=classof,
            minimum_date=minimum_date,
            exclude_households=exclude_households,
            email_address=email_address,
            include_individuals=include_individuals,
            include_organizations=include_organizations,
            include_groups=include_groups,
            check_alternate_lookup_ids=check_alternate_lookup_ids,
            fuzzy_search_on_name=fuzzy_search_on_name,
            phone_number=phone_number,
            middle_name=middle_name,
            suffix=suffix,
            constituency=constituency,
            sourcecode=sourcecode,
            site_filter_mode=site_filter_mode,
            sites_selected=sites_selected,
            limit=limit,
        )
    ).parsed
