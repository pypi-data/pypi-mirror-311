from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.new_education import NewEducation
from ...models.post_response import PostResponse
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    *,
    body: NewEducation,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/educationalhistories",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, PostResponse, ProblemDetails]]:
    if response.status_code == 200:
        response_200 = PostResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ProblemDetails.from_dict(response.json())

        return response_400
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == 404:
        response_404 = ProblemDetails.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, PostResponse, ProblemDetails]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: NewEducation,
) -> Response[Union[Any, PostResponse, ProblemDetails]]:
    """Create an education.

     Adds a new educational history record to an existing constituent.

    Args:
        body (NewEducation): CreateEducation Example: {'constituent_id': '', 'primary_record':
            False, 'educational_institution_id': '', 'academic_catalog_program': '',
            'educational_program': '', 'constituency_status': 'Unknown', 'date_graduated': '',
            'date_left': '', 'educational_history_level': '', 'educational_history_reason': '',
            'academic_catalog_degree': '', 'educational_degree': '', 'educational_award': '',
            'start_date': '', 'class_year': 0, 'preferred_class_year': 0, 'educational_source': '',
            'educational_source_date': '', 'comment': '', 'affiliate_dadditional_information': [{'id':
            '', 'academiccatalogcollege': '', 'academiccatalogdivision': '',
            'academiccatalogdepartment': '', 'academiccatalogsubdepartment': '',
            'academiccatalogdegreetype': ''}], 'unaffiliated_additional_information': [{'id': '',
            'educational_college': '', 'educational_division': '', 'educational_department': '',
            'educational_sub_department': '', 'educational_degree_type': ''}], 'affiliated': False,
            'use_academic_catalog': False, 'educational_history_status': ''}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PostResponse, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: NewEducation,
) -> Optional[Union[Any, PostResponse, ProblemDetails]]:
    """Create an education.

     Adds a new educational history record to an existing constituent.

    Args:
        body (NewEducation): CreateEducation Example: {'constituent_id': '', 'primary_record':
            False, 'educational_institution_id': '', 'academic_catalog_program': '',
            'educational_program': '', 'constituency_status': 'Unknown', 'date_graduated': '',
            'date_left': '', 'educational_history_level': '', 'educational_history_reason': '',
            'academic_catalog_degree': '', 'educational_degree': '', 'educational_award': '',
            'start_date': '', 'class_year': 0, 'preferred_class_year': 0, 'educational_source': '',
            'educational_source_date': '', 'comment': '', 'affiliate_dadditional_information': [{'id':
            '', 'academiccatalogcollege': '', 'academiccatalogdivision': '',
            'academiccatalogdepartment': '', 'academiccatalogsubdepartment': '',
            'academiccatalogdegreetype': ''}], 'unaffiliated_additional_information': [{'id': '',
            'educational_college': '', 'educational_division': '', 'educational_department': '',
            'educational_sub_department': '', 'educational_degree_type': ''}], 'affiliated': False,
            'use_academic_catalog': False, 'educational_history_status': ''}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PostResponse, ProblemDetails]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: NewEducation,
) -> Response[Union[Any, PostResponse, ProblemDetails]]:
    """Create an education.

     Adds a new educational history record to an existing constituent.

    Args:
        body (NewEducation): CreateEducation Example: {'constituent_id': '', 'primary_record':
            False, 'educational_institution_id': '', 'academic_catalog_program': '',
            'educational_program': '', 'constituency_status': 'Unknown', 'date_graduated': '',
            'date_left': '', 'educational_history_level': '', 'educational_history_reason': '',
            'academic_catalog_degree': '', 'educational_degree': '', 'educational_award': '',
            'start_date': '', 'class_year': 0, 'preferred_class_year': 0, 'educational_source': '',
            'educational_source_date': '', 'comment': '', 'affiliate_dadditional_information': [{'id':
            '', 'academiccatalogcollege': '', 'academiccatalogdivision': '',
            'academiccatalogdepartment': '', 'academiccatalogsubdepartment': '',
            'academiccatalogdegreetype': ''}], 'unaffiliated_additional_information': [{'id': '',
            'educational_college': '', 'educational_division': '', 'educational_department': '',
            'educational_sub_department': '', 'educational_degree_type': ''}], 'affiliated': False,
            'use_academic_catalog': False, 'educational_history_status': ''}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PostResponse, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: NewEducation,
) -> Optional[Union[Any, PostResponse, ProblemDetails]]:
    """Create an education.

     Adds a new educational history record to an existing constituent.

    Args:
        body (NewEducation): CreateEducation Example: {'constituent_id': '', 'primary_record':
            False, 'educational_institution_id': '', 'academic_catalog_program': '',
            'educational_program': '', 'constituency_status': 'Unknown', 'date_graduated': '',
            'date_left': '', 'educational_history_level': '', 'educational_history_reason': '',
            'academic_catalog_degree': '', 'educational_degree': '', 'educational_award': '',
            'start_date': '', 'class_year': 0, 'preferred_class_year': 0, 'educational_source': '',
            'educational_source_date': '', 'comment': '', 'affiliate_dadditional_information': [{'id':
            '', 'academiccatalogcollege': '', 'academiccatalogdivision': '',
            'academiccatalogdepartment': '', 'academiccatalogsubdepartment': '',
            'academiccatalogdegreetype': ''}], 'unaffiliated_additional_information': [{'id': '',
            'educational_college': '', 'educational_division': '', 'educational_department': '',
            'educational_sub_department': '', 'educational_degree_type': ''}], 'affiliated': False,
            'use_academic_catalog': False, 'educational_history_status': ''}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PostResponse, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
