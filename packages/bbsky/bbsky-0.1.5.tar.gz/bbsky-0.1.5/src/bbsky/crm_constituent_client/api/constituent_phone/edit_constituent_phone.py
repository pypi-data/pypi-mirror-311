from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_constituent_phone import EditConstituentPhone
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    phone_id: str,
    *,
    body: EditConstituentPhone,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/phones/{phone_id}",
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
    phone_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentPhone,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit a constituent phone.

     This operation is used to edit phone records.

    Args:
        phone_id (str):
        body (EditConstituentPhone): EditConstituentPhone Example: {'phone_type': 'Business',
            'number': '8439195648', 'primary': True, 'do_not_call': False, 'spouse_name': '',
            'spouse_has_matching_phone': False, 'update_matching_spouse_phone': False, 'household':
            False, 'household_member': False, 'update_matching_household_phone': False,
            'matching_household_members': [], 'start_time': {'hour': 3, 'minute': 30}, 'end_time':
            {'hour': 5, 'minute': 30}, 'info_source': '', 'info_source_comments': '', 'country': '',
            'seasonal_start_date': {'month': 3, 'day': 21}, 'seasonal_end_date': {'month': 3, 'day':
            21}, 'start_date': '', 'end_date': '', 'do_not_call_reason': '', 'confidential': False,
            'country_codes': [{'countryid': '', 'countrycode': ''}],
            'constituent_data_review_rollback_reason': '', 'forced_primary': False,
            'can_edit_primary': False, 'invalid_fields': '', 'origin_code': 'User'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        phone_id=phone_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    phone_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentPhone,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit a constituent phone.

     This operation is used to edit phone records.

    Args:
        phone_id (str):
        body (EditConstituentPhone): EditConstituentPhone Example: {'phone_type': 'Business',
            'number': '8439195648', 'primary': True, 'do_not_call': False, 'spouse_name': '',
            'spouse_has_matching_phone': False, 'update_matching_spouse_phone': False, 'household':
            False, 'household_member': False, 'update_matching_household_phone': False,
            'matching_household_members': [], 'start_time': {'hour': 3, 'minute': 30}, 'end_time':
            {'hour': 5, 'minute': 30}, 'info_source': '', 'info_source_comments': '', 'country': '',
            'seasonal_start_date': {'month': 3, 'day': 21}, 'seasonal_end_date': {'month': 3, 'day':
            21}, 'start_date': '', 'end_date': '', 'do_not_call_reason': '', 'confidential': False,
            'country_codes': [{'countryid': '', 'countrycode': ''}],
            'constituent_data_review_rollback_reason': '', 'forced_primary': False,
            'can_edit_primary': False, 'invalid_fields': '', 'origin_code': 'User'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return sync_detailed(
        phone_id=phone_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    phone_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentPhone,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit a constituent phone.

     This operation is used to edit phone records.

    Args:
        phone_id (str):
        body (EditConstituentPhone): EditConstituentPhone Example: {'phone_type': 'Business',
            'number': '8439195648', 'primary': True, 'do_not_call': False, 'spouse_name': '',
            'spouse_has_matching_phone': False, 'update_matching_spouse_phone': False, 'household':
            False, 'household_member': False, 'update_matching_household_phone': False,
            'matching_household_members': [], 'start_time': {'hour': 3, 'minute': 30}, 'end_time':
            {'hour': 5, 'minute': 30}, 'info_source': '', 'info_source_comments': '', 'country': '',
            'seasonal_start_date': {'month': 3, 'day': 21}, 'seasonal_end_date': {'month': 3, 'day':
            21}, 'start_date': '', 'end_date': '', 'do_not_call_reason': '', 'confidential': False,
            'country_codes': [{'countryid': '', 'countrycode': ''}],
            'constituent_data_review_rollback_reason': '', 'forced_primary': False,
            'can_edit_primary': False, 'invalid_fields': '', 'origin_code': 'User'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        phone_id=phone_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    phone_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentPhone,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit a constituent phone.

     This operation is used to edit phone records.

    Args:
        phone_id (str):
        body (EditConstituentPhone): EditConstituentPhone Example: {'phone_type': 'Business',
            'number': '8439195648', 'primary': True, 'do_not_call': False, 'spouse_name': '',
            'spouse_has_matching_phone': False, 'update_matching_spouse_phone': False, 'household':
            False, 'household_member': False, 'update_matching_household_phone': False,
            'matching_household_members': [], 'start_time': {'hour': 3, 'minute': 30}, 'end_time':
            {'hour': 5, 'minute': 30}, 'info_source': '', 'info_source_comments': '', 'country': '',
            'seasonal_start_date': {'month': 3, 'day': 21}, 'seasonal_end_date': {'month': 3, 'day':
            21}, 'start_date': '', 'end_date': '', 'do_not_call_reason': '', 'confidential': False,
            'country_codes': [{'countryid': '', 'countrycode': ''}],
            'constituent_data_review_rollback_reason': '', 'forced_primary': False,
            'can_edit_primary': False, 'invalid_fields': '', 'origin_code': 'User'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            phone_id=phone_id,
            client=client,
            body=body,
        )
    ).parsed
