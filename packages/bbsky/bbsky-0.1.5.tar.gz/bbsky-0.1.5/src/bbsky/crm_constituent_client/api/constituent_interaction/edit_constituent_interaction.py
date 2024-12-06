from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_constituent_interaction import EditConstituentInteraction
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    constituent_interaction_id: str,
    *,
    body: EditConstituentInteraction,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/interactions/{constituent_interaction_id}",
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
    constituent_interaction_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentInteraction,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit a constituent interaction.

     Edit operation for a non-move interaction.

    Args:
        constituent_interaction_id (str):
        body (EditConstituentInteraction): EditConstituentInteraction Example:
            {'interaction_type': 'Phone call', 'objective': 'Introductory call', 'fundraiser_id':
            '0DE9D2A3-82EE-4979-AA40-AF9C9DF2C0A2', 'expected_date':
            '2015-02-17T12:00:00.0000000+00:00', 'actual_date': '2015-02-17T12:00:00.0000000+00:00',
            'status': 'Completed', 'comment': '', 'step': False, 'event_id': '', 'participants':
            [{'id': 'd4873d67-c341-442c-bdc4-2cdb47bff7e2', 'constituent_id':
            '83ED6E63-4687-447A-B94F-35611ADF47B3'}], 'constituent_id': '', 'constituent_name': '',
            'interaction_category': '', 'interaction_subcategory': '', 'sites': [{'id':
            'a62483d4-cb71-46ae-9f06-da0644d0629f', 'site_id': 'D0AD4D30-800D-4F81-A5BA-
            DDA2A60C85A9'}], 'expected_start_time': {'hour': 1, 'minute': 26}, 'expected_end_time':
            {'hour': 3, 'minute': 33}, 'all_day_event': False, 'time_zone_entry': '',
            'actual_start_time': {'hour': 2, 'minute': 19}, 'actual_end_time': {'hour': 6, 'minute':
            40}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        constituent_interaction_id=constituent_interaction_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    constituent_interaction_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentInteraction,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit a constituent interaction.

     Edit operation for a non-move interaction.

    Args:
        constituent_interaction_id (str):
        body (EditConstituentInteraction): EditConstituentInteraction Example:
            {'interaction_type': 'Phone call', 'objective': 'Introductory call', 'fundraiser_id':
            '0DE9D2A3-82EE-4979-AA40-AF9C9DF2C0A2', 'expected_date':
            '2015-02-17T12:00:00.0000000+00:00', 'actual_date': '2015-02-17T12:00:00.0000000+00:00',
            'status': 'Completed', 'comment': '', 'step': False, 'event_id': '', 'participants':
            [{'id': 'd4873d67-c341-442c-bdc4-2cdb47bff7e2', 'constituent_id':
            '83ED6E63-4687-447A-B94F-35611ADF47B3'}], 'constituent_id': '', 'constituent_name': '',
            'interaction_category': '', 'interaction_subcategory': '', 'sites': [{'id':
            'a62483d4-cb71-46ae-9f06-da0644d0629f', 'site_id': 'D0AD4D30-800D-4F81-A5BA-
            DDA2A60C85A9'}], 'expected_start_time': {'hour': 1, 'minute': 26}, 'expected_end_time':
            {'hour': 3, 'minute': 33}, 'all_day_event': False, 'time_zone_entry': '',
            'actual_start_time': {'hour': 2, 'minute': 19}, 'actual_end_time': {'hour': 6, 'minute':
            40}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return sync_detailed(
        constituent_interaction_id=constituent_interaction_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    constituent_interaction_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentInteraction,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit a constituent interaction.

     Edit operation for a non-move interaction.

    Args:
        constituent_interaction_id (str):
        body (EditConstituentInteraction): EditConstituentInteraction Example:
            {'interaction_type': 'Phone call', 'objective': 'Introductory call', 'fundraiser_id':
            '0DE9D2A3-82EE-4979-AA40-AF9C9DF2C0A2', 'expected_date':
            '2015-02-17T12:00:00.0000000+00:00', 'actual_date': '2015-02-17T12:00:00.0000000+00:00',
            'status': 'Completed', 'comment': '', 'step': False, 'event_id': '', 'participants':
            [{'id': 'd4873d67-c341-442c-bdc4-2cdb47bff7e2', 'constituent_id':
            '83ED6E63-4687-447A-B94F-35611ADF47B3'}], 'constituent_id': '', 'constituent_name': '',
            'interaction_category': '', 'interaction_subcategory': '', 'sites': [{'id':
            'a62483d4-cb71-46ae-9f06-da0644d0629f', 'site_id': 'D0AD4D30-800D-4F81-A5BA-
            DDA2A60C85A9'}], 'expected_start_time': {'hour': 1, 'minute': 26}, 'expected_end_time':
            {'hour': 3, 'minute': 33}, 'all_day_event': False, 'time_zone_entry': '',
            'actual_start_time': {'hour': 2, 'minute': 19}, 'actual_end_time': {'hour': 6, 'minute':
            40}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        constituent_interaction_id=constituent_interaction_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    constituent_interaction_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentInteraction,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit a constituent interaction.

     Edit operation for a non-move interaction.

    Args:
        constituent_interaction_id (str):
        body (EditConstituentInteraction): EditConstituentInteraction Example:
            {'interaction_type': 'Phone call', 'objective': 'Introductory call', 'fundraiser_id':
            '0DE9D2A3-82EE-4979-AA40-AF9C9DF2C0A2', 'expected_date':
            '2015-02-17T12:00:00.0000000+00:00', 'actual_date': '2015-02-17T12:00:00.0000000+00:00',
            'status': 'Completed', 'comment': '', 'step': False, 'event_id': '', 'participants':
            [{'id': 'd4873d67-c341-442c-bdc4-2cdb47bff7e2', 'constituent_id':
            '83ED6E63-4687-447A-B94F-35611ADF47B3'}], 'constituent_id': '', 'constituent_name': '',
            'interaction_category': '', 'interaction_subcategory': '', 'sites': [{'id':
            'a62483d4-cb71-46ae-9f06-da0644d0629f', 'site_id': 'D0AD4D30-800D-4F81-A5BA-
            DDA2A60C85A9'}], 'expected_start_time': {'hour': 1, 'minute': 26}, 'expected_end_time':
            {'hour': 3, 'minute': 33}, 'all_day_event': False, 'time_zone_entry': '',
            'actual_start_time': {'hour': 2, 'minute': 19}, 'actual_end_time': {'hour': 6, 'minute':
            40}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            constituent_interaction_id=constituent_interaction_id,
            client=client,
            body=body,
        )
    ).parsed
