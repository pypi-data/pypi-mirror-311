from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.new_constituent_address import NewConstituentAddress
from ...models.post_response import PostResponse
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    *,
    body: NewConstituentAddress,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/addresses",
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
    body: NewConstituentAddress,
) -> Response[Union[Any, PostResponse, ProblemDetails]]:
    """Create a constituent address.

     This operation is used to add an address.

    Args:
        body (NewConstituentAddress): CreateConstituentAddress Example: {'constituent_id':
            '4B358EDA-9374-4DED-BE55-7C404BB5E4AB', 'address_type': '', 'address_block': '', 'city':
            '', 'state': '', 'postcode': '', 'country': '', 'do_not_mail': False, 'cart': '', 'lot':
            '', 'dpc': '', 'start_date': {'year': 2014, 'month': 4, 'day': 13}, 'end_date': {'year':
            2024, 'month': 4, 'day': 13}, 'primary': False, 'historical_start_date':
            '2014-11-04T10:04:00.0000000+00:00', 'recent_move': False, 'old_address': '',
            'spouse_name': '', 'update_matching_spouse_addresses': False, 'omit_from_validation':
            False, 'county': '', 'congressional_district': '', 'state_house_district': '',
            'state_senate_district': '', 'local_precinct': '', 'info_source': '', 'region': '',
            'last_validation_attempt_date': '2019-11-04T10:04:00.0000000+00:00', 'validation_message':
            '', 'certification_data': 0, 'zip_lookup_countries': [{'country_id': '4B358EDA-9374-4DED-
            BE55-7C404BB5E3AB', 'country_name': 'us'}], 'household': False, 'household_member': False,
            'update_matching_household_addresses': False, 'validation_countries': [{'country_id': '',
            'browsable': False}], 'do_not_mail_reason': '', 'info_source_comments': '',
            'confidential': False, 'constituent_data_review_rollback_reason': '', 'forced_primary':
            False, 'can_edit_primary': False, 'invalid_fields': '', 'origin': 'User'}.

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
    body: NewConstituentAddress,
) -> Optional[Union[Any, PostResponse, ProblemDetails]]:
    """Create a constituent address.

     This operation is used to add an address.

    Args:
        body (NewConstituentAddress): CreateConstituentAddress Example: {'constituent_id':
            '4B358EDA-9374-4DED-BE55-7C404BB5E4AB', 'address_type': '', 'address_block': '', 'city':
            '', 'state': '', 'postcode': '', 'country': '', 'do_not_mail': False, 'cart': '', 'lot':
            '', 'dpc': '', 'start_date': {'year': 2014, 'month': 4, 'day': 13}, 'end_date': {'year':
            2024, 'month': 4, 'day': 13}, 'primary': False, 'historical_start_date':
            '2014-11-04T10:04:00.0000000+00:00', 'recent_move': False, 'old_address': '',
            'spouse_name': '', 'update_matching_spouse_addresses': False, 'omit_from_validation':
            False, 'county': '', 'congressional_district': '', 'state_house_district': '',
            'state_senate_district': '', 'local_precinct': '', 'info_source': '', 'region': '',
            'last_validation_attempt_date': '2019-11-04T10:04:00.0000000+00:00', 'validation_message':
            '', 'certification_data': 0, 'zip_lookup_countries': [{'country_id': '4B358EDA-9374-4DED-
            BE55-7C404BB5E3AB', 'country_name': 'us'}], 'household': False, 'household_member': False,
            'update_matching_household_addresses': False, 'validation_countries': [{'country_id': '',
            'browsable': False}], 'do_not_mail_reason': '', 'info_source_comments': '',
            'confidential': False, 'constituent_data_review_rollback_reason': '', 'forced_primary':
            False, 'can_edit_primary': False, 'invalid_fields': '', 'origin': 'User'}.

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
    body: NewConstituentAddress,
) -> Response[Union[Any, PostResponse, ProblemDetails]]:
    """Create a constituent address.

     This operation is used to add an address.

    Args:
        body (NewConstituentAddress): CreateConstituentAddress Example: {'constituent_id':
            '4B358EDA-9374-4DED-BE55-7C404BB5E4AB', 'address_type': '', 'address_block': '', 'city':
            '', 'state': '', 'postcode': '', 'country': '', 'do_not_mail': False, 'cart': '', 'lot':
            '', 'dpc': '', 'start_date': {'year': 2014, 'month': 4, 'day': 13}, 'end_date': {'year':
            2024, 'month': 4, 'day': 13}, 'primary': False, 'historical_start_date':
            '2014-11-04T10:04:00.0000000+00:00', 'recent_move': False, 'old_address': '',
            'spouse_name': '', 'update_matching_spouse_addresses': False, 'omit_from_validation':
            False, 'county': '', 'congressional_district': '', 'state_house_district': '',
            'state_senate_district': '', 'local_precinct': '', 'info_source': '', 'region': '',
            'last_validation_attempt_date': '2019-11-04T10:04:00.0000000+00:00', 'validation_message':
            '', 'certification_data': 0, 'zip_lookup_countries': [{'country_id': '4B358EDA-9374-4DED-
            BE55-7C404BB5E3AB', 'country_name': 'us'}], 'household': False, 'household_member': False,
            'update_matching_household_addresses': False, 'validation_countries': [{'country_id': '',
            'browsable': False}], 'do_not_mail_reason': '', 'info_source_comments': '',
            'confidential': False, 'constituent_data_review_rollback_reason': '', 'forced_primary':
            False, 'can_edit_primary': False, 'invalid_fields': '', 'origin': 'User'}.

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
    body: NewConstituentAddress,
) -> Optional[Union[Any, PostResponse, ProblemDetails]]:
    """Create a constituent address.

     This operation is used to add an address.

    Args:
        body (NewConstituentAddress): CreateConstituentAddress Example: {'constituent_id':
            '4B358EDA-9374-4DED-BE55-7C404BB5E4AB', 'address_type': '', 'address_block': '', 'city':
            '', 'state': '', 'postcode': '', 'country': '', 'do_not_mail': False, 'cart': '', 'lot':
            '', 'dpc': '', 'start_date': {'year': 2014, 'month': 4, 'day': 13}, 'end_date': {'year':
            2024, 'month': 4, 'day': 13}, 'primary': False, 'historical_start_date':
            '2014-11-04T10:04:00.0000000+00:00', 'recent_move': False, 'old_address': '',
            'spouse_name': '', 'update_matching_spouse_addresses': False, 'omit_from_validation':
            False, 'county': '', 'congressional_district': '', 'state_house_district': '',
            'state_senate_district': '', 'local_precinct': '', 'info_source': '', 'region': '',
            'last_validation_attempt_date': '2019-11-04T10:04:00.0000000+00:00', 'validation_message':
            '', 'certification_data': 0, 'zip_lookup_countries': [{'country_id': '4B358EDA-9374-4DED-
            BE55-7C404BB5E3AB', 'country_name': 'us'}], 'household': False, 'household_member': False,
            'update_matching_household_addresses': False, 'validation_countries': [{'country_id': '',
            'browsable': False}], 'do_not_mail_reason': '', 'info_source_comments': '',
            'confidential': False, 'constituent_data_review_rollback_reason': '', 'forced_primary':
            False, 'can_edit_primary': False, 'invalid_fields': '', 'origin': 'User'}.

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
