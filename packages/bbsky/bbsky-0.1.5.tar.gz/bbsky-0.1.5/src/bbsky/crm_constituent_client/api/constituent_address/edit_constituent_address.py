from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_constituent_address import EditConstituentAddress
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    address_id: str,
    *,
    body: EditConstituentAddress,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/addresses/{address_id}",
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
    address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentAddress,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit a constituent address.

     This operation is used to edit an address.

    Args:
        address_id (str):
        body (EditConstituentAddress): EditConstituentAddress Example: {'address_type': '',
            'address_block': '', 'city': '', 'state_': '', 'postcode': '', 'country_': '', 'cart': '',
            'dpc': '', 'lot': '', 'start_date': {'year': 2014, 'month': 4, 'day': 13}, 'end_date':
            {'year': 2024, 'month': 4, 'day': 13}, 'primary': False, 'do_not_mail': False,
            'omit_from_validation': False, 'county': '', 'congressional_district': '',
            'state_house_district': '', 'state_senate_district': '', 'local_precinct': '',
            'info_source': '', 'region': '', 'last_validation_attempt_date':
            '2019-11-04T10:04:00.0000000+00:00', 'validation_message': '', 'certification_data': 0,
            'ncoa_last_submit_date': '2019-11-04T10:04:00.0000000+00:00', 'ncoa_return': '',
            'ncoa_footnote': '', 'ncoa_dpv_footnote': '', 'ncoa_move_date': {'year': 2024, 'month': 4,
            'day': 13}, 'ncoa_dma_suppression': False, 'ncoa_mail_grade': '', 'zip_lookup_countries':
            [{'country_id': '', 'country_name': ''}], 'validation_countries': [{'country_id': '',
            'browsable': False}], 'update_contacts': False, 'has_contacts': False,
            'do_not_mail_reason': '', 'household': False, 'household_member': False,
            'update_matching_household_addresses': False, 'matching_household_members':
            [{'constituent_id': '', 'name': '', 'relationship_to_primary': ''}],
            'historical_start_date': '2014-11-04T10:04:00.0000000+00:00', 'historical_end_date':
            '2024-11-04T10:04:00.0000000+00:00', 'date_added': '2014-11-04T11:04:00.0000000+00:00',
            'info_source_comments': '', 'confidential': False,
            'constituent_data_review_rollback_reason': '', 'forced_primary': False,
            'can_edit_primary': False, 'invalid_fields': '', 'origin': 'User'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        address_id=address_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentAddress,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit a constituent address.

     This operation is used to edit an address.

    Args:
        address_id (str):
        body (EditConstituentAddress): EditConstituentAddress Example: {'address_type': '',
            'address_block': '', 'city': '', 'state_': '', 'postcode': '', 'country_': '', 'cart': '',
            'dpc': '', 'lot': '', 'start_date': {'year': 2014, 'month': 4, 'day': 13}, 'end_date':
            {'year': 2024, 'month': 4, 'day': 13}, 'primary': False, 'do_not_mail': False,
            'omit_from_validation': False, 'county': '', 'congressional_district': '',
            'state_house_district': '', 'state_senate_district': '', 'local_precinct': '',
            'info_source': '', 'region': '', 'last_validation_attempt_date':
            '2019-11-04T10:04:00.0000000+00:00', 'validation_message': '', 'certification_data': 0,
            'ncoa_last_submit_date': '2019-11-04T10:04:00.0000000+00:00', 'ncoa_return': '',
            'ncoa_footnote': '', 'ncoa_dpv_footnote': '', 'ncoa_move_date': {'year': 2024, 'month': 4,
            'day': 13}, 'ncoa_dma_suppression': False, 'ncoa_mail_grade': '', 'zip_lookup_countries':
            [{'country_id': '', 'country_name': ''}], 'validation_countries': [{'country_id': '',
            'browsable': False}], 'update_contacts': False, 'has_contacts': False,
            'do_not_mail_reason': '', 'household': False, 'household_member': False,
            'update_matching_household_addresses': False, 'matching_household_members':
            [{'constituent_id': '', 'name': '', 'relationship_to_primary': ''}],
            'historical_start_date': '2014-11-04T10:04:00.0000000+00:00', 'historical_end_date':
            '2024-11-04T10:04:00.0000000+00:00', 'date_added': '2014-11-04T11:04:00.0000000+00:00',
            'info_source_comments': '', 'confidential': False,
            'constituent_data_review_rollback_reason': '', 'forced_primary': False,
            'can_edit_primary': False, 'invalid_fields': '', 'origin': 'User'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return sync_detailed(
        address_id=address_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentAddress,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit a constituent address.

     This operation is used to edit an address.

    Args:
        address_id (str):
        body (EditConstituentAddress): EditConstituentAddress Example: {'address_type': '',
            'address_block': '', 'city': '', 'state_': '', 'postcode': '', 'country_': '', 'cart': '',
            'dpc': '', 'lot': '', 'start_date': {'year': 2014, 'month': 4, 'day': 13}, 'end_date':
            {'year': 2024, 'month': 4, 'day': 13}, 'primary': False, 'do_not_mail': False,
            'omit_from_validation': False, 'county': '', 'congressional_district': '',
            'state_house_district': '', 'state_senate_district': '', 'local_precinct': '',
            'info_source': '', 'region': '', 'last_validation_attempt_date':
            '2019-11-04T10:04:00.0000000+00:00', 'validation_message': '', 'certification_data': 0,
            'ncoa_last_submit_date': '2019-11-04T10:04:00.0000000+00:00', 'ncoa_return': '',
            'ncoa_footnote': '', 'ncoa_dpv_footnote': '', 'ncoa_move_date': {'year': 2024, 'month': 4,
            'day': 13}, 'ncoa_dma_suppression': False, 'ncoa_mail_grade': '', 'zip_lookup_countries':
            [{'country_id': '', 'country_name': ''}], 'validation_countries': [{'country_id': '',
            'browsable': False}], 'update_contacts': False, 'has_contacts': False,
            'do_not_mail_reason': '', 'household': False, 'household_member': False,
            'update_matching_household_addresses': False, 'matching_household_members':
            [{'constituent_id': '', 'name': '', 'relationship_to_primary': ''}],
            'historical_start_date': '2014-11-04T10:04:00.0000000+00:00', 'historical_end_date':
            '2024-11-04T10:04:00.0000000+00:00', 'date_added': '2014-11-04T11:04:00.0000000+00:00',
            'info_source_comments': '', 'confidential': False,
            'constituent_data_review_rollback_reason': '', 'forced_primary': False,
            'can_edit_primary': False, 'invalid_fields': '', 'origin': 'User'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        address_id=address_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentAddress,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit a constituent address.

     This operation is used to edit an address.

    Args:
        address_id (str):
        body (EditConstituentAddress): EditConstituentAddress Example: {'address_type': '',
            'address_block': '', 'city': '', 'state_': '', 'postcode': '', 'country_': '', 'cart': '',
            'dpc': '', 'lot': '', 'start_date': {'year': 2014, 'month': 4, 'day': 13}, 'end_date':
            {'year': 2024, 'month': 4, 'day': 13}, 'primary': False, 'do_not_mail': False,
            'omit_from_validation': False, 'county': '', 'congressional_district': '',
            'state_house_district': '', 'state_senate_district': '', 'local_precinct': '',
            'info_source': '', 'region': '', 'last_validation_attempt_date':
            '2019-11-04T10:04:00.0000000+00:00', 'validation_message': '', 'certification_data': 0,
            'ncoa_last_submit_date': '2019-11-04T10:04:00.0000000+00:00', 'ncoa_return': '',
            'ncoa_footnote': '', 'ncoa_dpv_footnote': '', 'ncoa_move_date': {'year': 2024, 'month': 4,
            'day': 13}, 'ncoa_dma_suppression': False, 'ncoa_mail_grade': '', 'zip_lookup_countries':
            [{'country_id': '', 'country_name': ''}], 'validation_countries': [{'country_id': '',
            'browsable': False}], 'update_contacts': False, 'has_contacts': False,
            'do_not_mail_reason': '', 'household': False, 'household_member': False,
            'update_matching_household_addresses': False, 'matching_household_members':
            [{'constituent_id': '', 'name': '', 'relationship_to_primary': ''}],
            'historical_start_date': '2014-11-04T10:04:00.0000000+00:00', 'historical_end_date':
            '2024-11-04T10:04:00.0000000+00:00', 'date_added': '2014-11-04T11:04:00.0000000+00:00',
            'info_source_comments': '', 'confidential': False,
            'constituent_data_review_rollback_reason': '', 'forced_primary': False,
            'can_edit_primary': False, 'invalid_fields': '', 'origin': 'User'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            address_id=address_id,
            client=client,
            body=body,
        )
    ).parsed
