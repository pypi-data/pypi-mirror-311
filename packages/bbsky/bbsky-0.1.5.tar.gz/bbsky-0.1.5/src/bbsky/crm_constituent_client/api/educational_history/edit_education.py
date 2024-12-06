from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_education import EditEducation
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    educational_history_id: str,
    *,
    body: EditEducation,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/educationalhistories/{educational_history_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ProblemDetails]]:
    if response.status_code == 200:
        response_200 = cast(Any, None)
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
) -> Response[Union[Any, ProblemDetails]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    educational_history_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditEducation,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit an education.

     Edits educational history.

    Args:
        educational_history_id (str):
        body (EditEducation): EditEducation Example: {'primary_record': False,
            'educational_institution_id': '6d31a4d0-57fb-454e-9ce9-f09049327153',
            'academic_catalog_program': '', 'educational_program': 'FullCourse',
            'constituency_status': 'Unknown', 'date_graduated': {'year': 2015, 'month': 6, 'day': 17},
            'date_left': {'year': 2017, 'month': 4, 'day': 19}, 'academic_catalog_degree': '',
            'educational_degree': 'MBA', 'educational_award': '', 'start_date': {'year': 2014,
            'month': 4, 'day': 13}, 'class_year': 0, 'preferred_class_year': 0, 'educational_source':
            '', 'educational_source_date': {'year': 0, 'month': 0, 'day': 0}, 'comment': '',
            'affiliated': False, 'educational_history_level': '', 'educational_history_reason': '',
            'use_academic_catalog': False, 'educational_history_status':
            '00000000-0000-0000-0000-000000000004'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        educational_history_id=educational_history_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    educational_history_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditEducation,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit an education.

     Edits educational history.

    Args:
        educational_history_id (str):
        body (EditEducation): EditEducation Example: {'primary_record': False,
            'educational_institution_id': '6d31a4d0-57fb-454e-9ce9-f09049327153',
            'academic_catalog_program': '', 'educational_program': 'FullCourse',
            'constituency_status': 'Unknown', 'date_graduated': {'year': 2015, 'month': 6, 'day': 17},
            'date_left': {'year': 2017, 'month': 4, 'day': 19}, 'academic_catalog_degree': '',
            'educational_degree': 'MBA', 'educational_award': '', 'start_date': {'year': 2014,
            'month': 4, 'day': 13}, 'class_year': 0, 'preferred_class_year': 0, 'educational_source':
            '', 'educational_source_date': {'year': 0, 'month': 0, 'day': 0}, 'comment': '',
            'affiliated': False, 'educational_history_level': '', 'educational_history_reason': '',
            'use_academic_catalog': False, 'educational_history_status':
            '00000000-0000-0000-0000-000000000004'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return sync_detailed(
        educational_history_id=educational_history_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    educational_history_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditEducation,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit an education.

     Edits educational history.

    Args:
        educational_history_id (str):
        body (EditEducation): EditEducation Example: {'primary_record': False,
            'educational_institution_id': '6d31a4d0-57fb-454e-9ce9-f09049327153',
            'academic_catalog_program': '', 'educational_program': 'FullCourse',
            'constituency_status': 'Unknown', 'date_graduated': {'year': 2015, 'month': 6, 'day': 17},
            'date_left': {'year': 2017, 'month': 4, 'day': 19}, 'academic_catalog_degree': '',
            'educational_degree': 'MBA', 'educational_award': '', 'start_date': {'year': 2014,
            'month': 4, 'day': 13}, 'class_year': 0, 'preferred_class_year': 0, 'educational_source':
            '', 'educational_source_date': {'year': 0, 'month': 0, 'day': 0}, 'comment': '',
            'affiliated': False, 'educational_history_level': '', 'educational_history_reason': '',
            'use_academic_catalog': False, 'educational_history_status':
            '00000000-0000-0000-0000-000000000004'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        educational_history_id=educational_history_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    educational_history_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditEducation,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit an education.

     Edits educational history.

    Args:
        educational_history_id (str):
        body (EditEducation): EditEducation Example: {'primary_record': False,
            'educational_institution_id': '6d31a4d0-57fb-454e-9ce9-f09049327153',
            'academic_catalog_program': '', 'educational_program': 'FullCourse',
            'constituency_status': 'Unknown', 'date_graduated': {'year': 2015, 'month': 6, 'day': 17},
            'date_left': {'year': 2017, 'month': 4, 'day': 19}, 'academic_catalog_degree': '',
            'educational_degree': 'MBA', 'educational_award': '', 'start_date': {'year': 2014,
            'month': 4, 'day': 13}, 'class_year': 0, 'preferred_class_year': 0, 'educational_source':
            '', 'educational_source_date': {'year': 0, 'month': 0, 'day': 0}, 'comment': '',
            'affiliated': False, 'educational_history_level': '', 'educational_history_reason': '',
            'use_academic_catalog': False, 'educational_history_status':
            '00000000-0000-0000-0000-000000000004'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            educational_history_id=educational_history_id,
            client=client,
            body=body,
        )
    ).parsed
