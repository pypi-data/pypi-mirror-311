from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.education_search_collection import EducationSearchCollection
from ...models.problem_details import ProblemDetails
from ...models.search_educations_constituency_status import SearchEducationsConstituencyStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    full_name_educational_institution: Union[Unset, str] = UNSET,
    key_name: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    lookup_id: Union[Unset, str] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    check_nick_name: Union[Unset, bool] = UNSET,
    check_aliases: Union[Unset, bool] = UNSET,
    check_alternate_lookup_ids: Union[Unset, bool] = UNSET,
    educational_institution: Union[Unset, str] = UNSET,
    academic_catalog_program: Union[Unset, str] = UNSET,
    educational_program: Union[Unset, str] = UNSET,
    constituency_status: Union[Unset, SearchEducationsConstituencyStatus] = UNSET,
    educational_history_status: Union[Unset, str] = UNSET,
    academic_catalog_degree: Union[Unset, str] = UNSET,
    educational_degree: Union[Unset, str] = UNSET,
    class_of: Union[Unset, int] = UNSET,
    primary_only: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["full_name_educational_institution"] = full_name_educational_institution

    params["key_name"] = key_name

    params["first_name"] = first_name

    params["lookup_id"] = lookup_id

    params["exact_match_only"] = exact_match_only

    params["check_nick_name"] = check_nick_name

    params["check_aliases"] = check_aliases

    params["check_alternate_lookup_ids"] = check_alternate_lookup_ids

    params["educational_institution"] = educational_institution

    params["academic_catalog_program"] = academic_catalog_program

    params["educational_program"] = educational_program

    json_constituency_status: Union[Unset, str] = UNSET
    if not isinstance(constituency_status, Unset):
        json_constituency_status = constituency_status.value

    params["constituency_status"] = json_constituency_status

    params["educational_history_status"] = educational_history_status

    params["academic_catalog_degree"] = academic_catalog_degree

    params["educational_degree"] = educational_degree

    params["class_of"] = class_of

    params["primary_only"] = primary_only

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/educationalhistories/search",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, EducationSearchCollection, ProblemDetails]]:
    if response.status_code == 200:
        response_200 = EducationSearchCollection.from_dict(response.json())

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
) -> Response[Union[Any, EducationSearchCollection, ProblemDetails]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    full_name_educational_institution: Union[Unset, str] = UNSET,
    key_name: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    lookup_id: Union[Unset, str] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    check_nick_name: Union[Unset, bool] = UNSET,
    check_aliases: Union[Unset, bool] = UNSET,
    check_alternate_lookup_ids: Union[Unset, bool] = UNSET,
    educational_institution: Union[Unset, str] = UNSET,
    academic_catalog_program: Union[Unset, str] = UNSET,
    educational_program: Union[Unset, str] = UNSET,
    constituency_status: Union[Unset, SearchEducationsConstituencyStatus] = UNSET,
    educational_history_status: Union[Unset, str] = UNSET,
    academic_catalog_degree: Union[Unset, str] = UNSET,
    educational_degree: Union[Unset, str] = UNSET,
    class_of: Union[Unset, int] = UNSET,
    primary_only: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Union[Any, EducationSearchCollection, ProblemDetails]]:
    """Search for educations.

     This search list provides the ability to search for educational history records.

    Args:
        full_name_educational_institution (Union[Unset, str]):
        key_name (Union[Unset, str]):
        first_name (Union[Unset, str]):
        lookup_id (Union[Unset, str]):
        exact_match_only (Union[Unset, bool]):
        check_nick_name (Union[Unset, bool]):
        check_aliases (Union[Unset, bool]):
        check_alternate_lookup_ids (Union[Unset, bool]):
        educational_institution (Union[Unset, str]):
        academic_catalog_program (Union[Unset, str]):
        educational_program (Union[Unset, str]):
        constituency_status (Union[Unset, SearchEducationsConstituencyStatus]):
        educational_history_status (Union[Unset, str]):
        academic_catalog_degree (Union[Unset, str]):
        educational_degree (Union[Unset, str]):
        class_of (Union[Unset, int]):
        primary_only (Union[Unset, bool]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, EducationSearchCollection, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        full_name_educational_institution=full_name_educational_institution,
        key_name=key_name,
        first_name=first_name,
        lookup_id=lookup_id,
        exact_match_only=exact_match_only,
        check_nick_name=check_nick_name,
        check_aliases=check_aliases,
        check_alternate_lookup_ids=check_alternate_lookup_ids,
        educational_institution=educational_institution,
        academic_catalog_program=academic_catalog_program,
        educational_program=educational_program,
        constituency_status=constituency_status,
        educational_history_status=educational_history_status,
        academic_catalog_degree=academic_catalog_degree,
        educational_degree=educational_degree,
        class_of=class_of,
        primary_only=primary_only,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    full_name_educational_institution: Union[Unset, str] = UNSET,
    key_name: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    lookup_id: Union[Unset, str] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    check_nick_name: Union[Unset, bool] = UNSET,
    check_aliases: Union[Unset, bool] = UNSET,
    check_alternate_lookup_ids: Union[Unset, bool] = UNSET,
    educational_institution: Union[Unset, str] = UNSET,
    academic_catalog_program: Union[Unset, str] = UNSET,
    educational_program: Union[Unset, str] = UNSET,
    constituency_status: Union[Unset, SearchEducationsConstituencyStatus] = UNSET,
    educational_history_status: Union[Unset, str] = UNSET,
    academic_catalog_degree: Union[Unset, str] = UNSET,
    educational_degree: Union[Unset, str] = UNSET,
    class_of: Union[Unset, int] = UNSET,
    primary_only: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, EducationSearchCollection, ProblemDetails]]:
    """Search for educations.

     This search list provides the ability to search for educational history records.

    Args:
        full_name_educational_institution (Union[Unset, str]):
        key_name (Union[Unset, str]):
        first_name (Union[Unset, str]):
        lookup_id (Union[Unset, str]):
        exact_match_only (Union[Unset, bool]):
        check_nick_name (Union[Unset, bool]):
        check_aliases (Union[Unset, bool]):
        check_alternate_lookup_ids (Union[Unset, bool]):
        educational_institution (Union[Unset, str]):
        academic_catalog_program (Union[Unset, str]):
        educational_program (Union[Unset, str]):
        constituency_status (Union[Unset, SearchEducationsConstituencyStatus]):
        educational_history_status (Union[Unset, str]):
        academic_catalog_degree (Union[Unset, str]):
        educational_degree (Union[Unset, str]):
        class_of (Union[Unset, int]):
        primary_only (Union[Unset, bool]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, EducationSearchCollection, ProblemDetails]
    """

    return sync_detailed(
        client=client,
        full_name_educational_institution=full_name_educational_institution,
        key_name=key_name,
        first_name=first_name,
        lookup_id=lookup_id,
        exact_match_only=exact_match_only,
        check_nick_name=check_nick_name,
        check_aliases=check_aliases,
        check_alternate_lookup_ids=check_alternate_lookup_ids,
        educational_institution=educational_institution,
        academic_catalog_program=academic_catalog_program,
        educational_program=educational_program,
        constituency_status=constituency_status,
        educational_history_status=educational_history_status,
        academic_catalog_degree=academic_catalog_degree,
        educational_degree=educational_degree,
        class_of=class_of,
        primary_only=primary_only,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    full_name_educational_institution: Union[Unset, str] = UNSET,
    key_name: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    lookup_id: Union[Unset, str] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    check_nick_name: Union[Unset, bool] = UNSET,
    check_aliases: Union[Unset, bool] = UNSET,
    check_alternate_lookup_ids: Union[Unset, bool] = UNSET,
    educational_institution: Union[Unset, str] = UNSET,
    academic_catalog_program: Union[Unset, str] = UNSET,
    educational_program: Union[Unset, str] = UNSET,
    constituency_status: Union[Unset, SearchEducationsConstituencyStatus] = UNSET,
    educational_history_status: Union[Unset, str] = UNSET,
    academic_catalog_degree: Union[Unset, str] = UNSET,
    educational_degree: Union[Unset, str] = UNSET,
    class_of: Union[Unset, int] = UNSET,
    primary_only: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Union[Any, EducationSearchCollection, ProblemDetails]]:
    """Search for educations.

     This search list provides the ability to search for educational history records.

    Args:
        full_name_educational_institution (Union[Unset, str]):
        key_name (Union[Unset, str]):
        first_name (Union[Unset, str]):
        lookup_id (Union[Unset, str]):
        exact_match_only (Union[Unset, bool]):
        check_nick_name (Union[Unset, bool]):
        check_aliases (Union[Unset, bool]):
        check_alternate_lookup_ids (Union[Unset, bool]):
        educational_institution (Union[Unset, str]):
        academic_catalog_program (Union[Unset, str]):
        educational_program (Union[Unset, str]):
        constituency_status (Union[Unset, SearchEducationsConstituencyStatus]):
        educational_history_status (Union[Unset, str]):
        academic_catalog_degree (Union[Unset, str]):
        educational_degree (Union[Unset, str]):
        class_of (Union[Unset, int]):
        primary_only (Union[Unset, bool]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, EducationSearchCollection, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        full_name_educational_institution=full_name_educational_institution,
        key_name=key_name,
        first_name=first_name,
        lookup_id=lookup_id,
        exact_match_only=exact_match_only,
        check_nick_name=check_nick_name,
        check_aliases=check_aliases,
        check_alternate_lookup_ids=check_alternate_lookup_ids,
        educational_institution=educational_institution,
        academic_catalog_program=academic_catalog_program,
        educational_program=educational_program,
        constituency_status=constituency_status,
        educational_history_status=educational_history_status,
        academic_catalog_degree=academic_catalog_degree,
        educational_degree=educational_degree,
        class_of=class_of,
        primary_only=primary_only,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    full_name_educational_institution: Union[Unset, str] = UNSET,
    key_name: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    lookup_id: Union[Unset, str] = UNSET,
    exact_match_only: Union[Unset, bool] = UNSET,
    check_nick_name: Union[Unset, bool] = UNSET,
    check_aliases: Union[Unset, bool] = UNSET,
    check_alternate_lookup_ids: Union[Unset, bool] = UNSET,
    educational_institution: Union[Unset, str] = UNSET,
    academic_catalog_program: Union[Unset, str] = UNSET,
    educational_program: Union[Unset, str] = UNSET,
    constituency_status: Union[Unset, SearchEducationsConstituencyStatus] = UNSET,
    educational_history_status: Union[Unset, str] = UNSET,
    academic_catalog_degree: Union[Unset, str] = UNSET,
    educational_degree: Union[Unset, str] = UNSET,
    class_of: Union[Unset, int] = UNSET,
    primary_only: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, EducationSearchCollection, ProblemDetails]]:
    """Search for educations.

     This search list provides the ability to search for educational history records.

    Args:
        full_name_educational_institution (Union[Unset, str]):
        key_name (Union[Unset, str]):
        first_name (Union[Unset, str]):
        lookup_id (Union[Unset, str]):
        exact_match_only (Union[Unset, bool]):
        check_nick_name (Union[Unset, bool]):
        check_aliases (Union[Unset, bool]):
        check_alternate_lookup_ids (Union[Unset, bool]):
        educational_institution (Union[Unset, str]):
        academic_catalog_program (Union[Unset, str]):
        educational_program (Union[Unset, str]):
        constituency_status (Union[Unset, SearchEducationsConstituencyStatus]):
        educational_history_status (Union[Unset, str]):
        academic_catalog_degree (Union[Unset, str]):
        educational_degree (Union[Unset, str]):
        class_of (Union[Unset, int]):
        primary_only (Union[Unset, bool]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, EducationSearchCollection, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            client=client,
            full_name_educational_institution=full_name_educational_institution,
            key_name=key_name,
            first_name=first_name,
            lookup_id=lookup_id,
            exact_match_only=exact_match_only,
            check_nick_name=check_nick_name,
            check_aliases=check_aliases,
            check_alternate_lookup_ids=check_alternate_lookup_ids,
            educational_institution=educational_institution,
            academic_catalog_program=academic_catalog_program,
            educational_program=educational_program,
            constituency_status=constituency_status,
            educational_history_status=educational_history_status,
            academic_catalog_degree=academic_catalog_degree,
            educational_degree=educational_degree,
            class_of=class_of,
            primary_only=primary_only,
            limit=limit,
        )
    ).parsed
