from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_constituent_email_address import EditConstituentEmailAddress
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    email_address_id: str,
    *,
    body: EditConstituentEmailAddress,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/emailaddresses/{email_address_id}",
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
    email_address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentEmailAddress,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit a constituent email address.

     This operation is used to edit email addresses.

    Args:
        email_address_id (str):
        body (EditConstituentEmailAddress): EditConstituentEmailAddress Example:
            {'email_address_type': 'Email', 'email_address': 'jules@att.com', 'primary': False,
            'do_not_email': False, 'spouse_name': '', 'spouse_has_matching_email_address': False,
            'update_matching_spouse_email_address': False, 'household': False, 'household_member':
            False, 'update_matching_household_email_address': False, 'matching_household_members':
            [{'constituent_id': '', 'name': '', 'relationship_to_primary': ''}], 'info_source': '',
            'info_source_comments': '', 'constituent_data_review_rollback_reason': '',
            'forced_primary': False, 'can_edit_primary': False, 'invalid_fields': '', 'origin':
            'User', 'start_date': '2016-02-18T12:00:00.0000000+00:00', 'end_date':
            '2017-06-12T12:00:00.0000000+00:00', 'invalid_email': False, 'email_bounced_date':
            '2018-01-03T12:00:00.0000000+00:00'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        email_address_id=email_address_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    email_address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentEmailAddress,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit a constituent email address.

     This operation is used to edit email addresses.

    Args:
        email_address_id (str):
        body (EditConstituentEmailAddress): EditConstituentEmailAddress Example:
            {'email_address_type': 'Email', 'email_address': 'jules@att.com', 'primary': False,
            'do_not_email': False, 'spouse_name': '', 'spouse_has_matching_email_address': False,
            'update_matching_spouse_email_address': False, 'household': False, 'household_member':
            False, 'update_matching_household_email_address': False, 'matching_household_members':
            [{'constituent_id': '', 'name': '', 'relationship_to_primary': ''}], 'info_source': '',
            'info_source_comments': '', 'constituent_data_review_rollback_reason': '',
            'forced_primary': False, 'can_edit_primary': False, 'invalid_fields': '', 'origin':
            'User', 'start_date': '2016-02-18T12:00:00.0000000+00:00', 'end_date':
            '2017-06-12T12:00:00.0000000+00:00', 'invalid_email': False, 'email_bounced_date':
            '2018-01-03T12:00:00.0000000+00:00'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return sync_detailed(
        email_address_id=email_address_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    email_address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentEmailAddress,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit a constituent email address.

     This operation is used to edit email addresses.

    Args:
        email_address_id (str):
        body (EditConstituentEmailAddress): EditConstituentEmailAddress Example:
            {'email_address_type': 'Email', 'email_address': 'jules@att.com', 'primary': False,
            'do_not_email': False, 'spouse_name': '', 'spouse_has_matching_email_address': False,
            'update_matching_spouse_email_address': False, 'household': False, 'household_member':
            False, 'update_matching_household_email_address': False, 'matching_household_members':
            [{'constituent_id': '', 'name': '', 'relationship_to_primary': ''}], 'info_source': '',
            'info_source_comments': '', 'constituent_data_review_rollback_reason': '',
            'forced_primary': False, 'can_edit_primary': False, 'invalid_fields': '', 'origin':
            'User', 'start_date': '2016-02-18T12:00:00.0000000+00:00', 'end_date':
            '2017-06-12T12:00:00.0000000+00:00', 'invalid_email': False, 'email_bounced_date':
            '2018-01-03T12:00:00.0000000+00:00'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        email_address_id=email_address_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    email_address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentEmailAddress,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit a constituent email address.

     This operation is used to edit email addresses.

    Args:
        email_address_id (str):
        body (EditConstituentEmailAddress): EditConstituentEmailAddress Example:
            {'email_address_type': 'Email', 'email_address': 'jules@att.com', 'primary': False,
            'do_not_email': False, 'spouse_name': '', 'spouse_has_matching_email_address': False,
            'update_matching_spouse_email_address': False, 'household': False, 'household_member':
            False, 'update_matching_household_email_address': False, 'matching_household_members':
            [{'constituent_id': '', 'name': '', 'relationship_to_primary': ''}], 'info_source': '',
            'info_source_comments': '', 'constituent_data_review_rollback_reason': '',
            'forced_primary': False, 'can_edit_primary': False, 'invalid_fields': '', 'origin':
            'User', 'start_date': '2016-02-18T12:00:00.0000000+00:00', 'end_date':
            '2017-06-12T12:00:00.0000000+00:00', 'invalid_email': False, 'email_bounced_date':
            '2018-01-03T12:00:00.0000000+00:00'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            email_address_id=email_address_id,
            client=client,
            body=body,
        )
    ).parsed
