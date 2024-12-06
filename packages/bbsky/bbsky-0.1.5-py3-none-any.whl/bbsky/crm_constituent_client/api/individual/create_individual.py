from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.new_individual import NewIndividual
from ...models.post_response import PostResponse
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    *,
    body: NewIndividual,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/individuals",
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
    body: NewIndividual,
) -> Response[Union[Any, PostResponse, ProblemDetails]]:
    """Create an individual.

     This operation is used to add an individual constituent, spouse(optional), and business(optional).

    Args:
        body (NewIndividual): CreateIndividual Example: {'last_name': '', 'first_name': '',
            'middle_name': '', 'title': '', 'suffix': '', 'nickname': '', 'maiden_name': '',
            'birth_date': '', 'gender': 'Unknown', 'marital_status': '', 'address_type': '',
            'address_country': '', 'address_block': '', 'address_city': '', 'address_state': '',
            'address_post_code': '', 'address_do_not_mail': False, 'address_do_not_mail_reason': '',
            'phone_type': '', 'phone_number': '', 'email_address_type': '', 'email_address': '',
            'skip_adding_security_groups': False, 'existing_spouse': False, 'spouse_id': '',
            'spouse_last_name': '', 'spouse_first_name': '', 'spouse_middle_name': '', 'spouse_title':
            '', 'spouse_suffix': '', 'spouse_nick_name': '', 'spouse_maiden_name': '',
            'spouse_birth_date': '', 'spouse_gender': 'Unknown', 'spouse_relationship_type_code': '',
            'spouse_reciprocal_type_code': '', 'spouse_start_date': '', 'copy_primary_information':
            False, 'primary_soft_credit_relationship_exists': False,
            'primary_soft_credit_match_factor': 0, 'reciprocal_soft_credit_relationship_exists':
            False, 'reciprocal_soft_credit_match_factor': 0, 'existing_organization': False,
            'organization_id': '', 'organization_name': '', 'organization_address_type': '',
            'organization_country': '', 'organization_address_block': '', 'organization_city': '',
            'organization_state': '', 'organization_post_code': '', 'organization_do_not_mail': False,
            'organization_do_not_mail_reason': '', 'organization_phone_type': '',
            'organization_number': '', 'organization_relationship_type_code': '',
            'organization_reciprocal_type_code': '', 'organization_start_date': '',
            'organization_end_date': '', 'contact': False, 'contact_type': '', 'primary_contact':
            False, 'position': '', 'matching_gift_relationship': False, 'reciprocal_recognition_type':
            '', 'primary_recognition_type': '', 'address_omit_from_validation': False, 'address_dpc':
            '', 'address_cart': '', 'address_lot': '', 'address_county': '',
            'address_congressional_district': '', 'address_last_validation_attempt_date': '',
            'address_validation_message': '', 'address_certification_data': 0,
            'organization_omit_from_validation': False, 'organization_dpc': '', 'organization_cart':
            '', 'organization_lot': '', 'organization_county': '',
            'organization_congressional_district': '', 'organization_last_validation_attempt_date':
            '', 'organization_validation_message': '', 'organization_certification_data': 0,
            'validation_countries': [{'country_id': '', 'browsable': False}], 'zip_lookup_countries':
            [{'country_id': '', 'country_name': ''}], 'spouse_relationship': False,
            'house_hold_copy_primary_contact_info': False, 'job_category': '', 'career_level': '',
            'address_info_source': '', 'organization_info_source': '', 'title_2': '', 'suffix_2': '',
            'spouse_title_2': '', 'spouse_suffix_2': '', 'skip_adding_sites': False,
            'constituent_type': 0, 'organization_primary_soft_credit_relationship_exists': False,
            'organization_primary_soft_credit_match_factor': 0,
            'organization_reciprocal_soft_credit_relationship_exists': False,
            'organization_reciprocal_soft_credit_match_factor': 0,
            'organization_primary_recognition_type': '', 'organization_reciprocal_recognition_type':
            '', 'gender_code': '', 'spouse_gender_code': ''}.

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
    body: NewIndividual,
) -> Optional[Union[Any, PostResponse, ProblemDetails]]:
    """Create an individual.

     This operation is used to add an individual constituent, spouse(optional), and business(optional).

    Args:
        body (NewIndividual): CreateIndividual Example: {'last_name': '', 'first_name': '',
            'middle_name': '', 'title': '', 'suffix': '', 'nickname': '', 'maiden_name': '',
            'birth_date': '', 'gender': 'Unknown', 'marital_status': '', 'address_type': '',
            'address_country': '', 'address_block': '', 'address_city': '', 'address_state': '',
            'address_post_code': '', 'address_do_not_mail': False, 'address_do_not_mail_reason': '',
            'phone_type': '', 'phone_number': '', 'email_address_type': '', 'email_address': '',
            'skip_adding_security_groups': False, 'existing_spouse': False, 'spouse_id': '',
            'spouse_last_name': '', 'spouse_first_name': '', 'spouse_middle_name': '', 'spouse_title':
            '', 'spouse_suffix': '', 'spouse_nick_name': '', 'spouse_maiden_name': '',
            'spouse_birth_date': '', 'spouse_gender': 'Unknown', 'spouse_relationship_type_code': '',
            'spouse_reciprocal_type_code': '', 'spouse_start_date': '', 'copy_primary_information':
            False, 'primary_soft_credit_relationship_exists': False,
            'primary_soft_credit_match_factor': 0, 'reciprocal_soft_credit_relationship_exists':
            False, 'reciprocal_soft_credit_match_factor': 0, 'existing_organization': False,
            'organization_id': '', 'organization_name': '', 'organization_address_type': '',
            'organization_country': '', 'organization_address_block': '', 'organization_city': '',
            'organization_state': '', 'organization_post_code': '', 'organization_do_not_mail': False,
            'organization_do_not_mail_reason': '', 'organization_phone_type': '',
            'organization_number': '', 'organization_relationship_type_code': '',
            'organization_reciprocal_type_code': '', 'organization_start_date': '',
            'organization_end_date': '', 'contact': False, 'contact_type': '', 'primary_contact':
            False, 'position': '', 'matching_gift_relationship': False, 'reciprocal_recognition_type':
            '', 'primary_recognition_type': '', 'address_omit_from_validation': False, 'address_dpc':
            '', 'address_cart': '', 'address_lot': '', 'address_county': '',
            'address_congressional_district': '', 'address_last_validation_attempt_date': '',
            'address_validation_message': '', 'address_certification_data': 0,
            'organization_omit_from_validation': False, 'organization_dpc': '', 'organization_cart':
            '', 'organization_lot': '', 'organization_county': '',
            'organization_congressional_district': '', 'organization_last_validation_attempt_date':
            '', 'organization_validation_message': '', 'organization_certification_data': 0,
            'validation_countries': [{'country_id': '', 'browsable': False}], 'zip_lookup_countries':
            [{'country_id': '', 'country_name': ''}], 'spouse_relationship': False,
            'house_hold_copy_primary_contact_info': False, 'job_category': '', 'career_level': '',
            'address_info_source': '', 'organization_info_source': '', 'title_2': '', 'suffix_2': '',
            'spouse_title_2': '', 'spouse_suffix_2': '', 'skip_adding_sites': False,
            'constituent_type': 0, 'organization_primary_soft_credit_relationship_exists': False,
            'organization_primary_soft_credit_match_factor': 0,
            'organization_reciprocal_soft_credit_relationship_exists': False,
            'organization_reciprocal_soft_credit_match_factor': 0,
            'organization_primary_recognition_type': '', 'organization_reciprocal_recognition_type':
            '', 'gender_code': '', 'spouse_gender_code': ''}.

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
    body: NewIndividual,
) -> Response[Union[Any, PostResponse, ProblemDetails]]:
    """Create an individual.

     This operation is used to add an individual constituent, spouse(optional), and business(optional).

    Args:
        body (NewIndividual): CreateIndividual Example: {'last_name': '', 'first_name': '',
            'middle_name': '', 'title': '', 'suffix': '', 'nickname': '', 'maiden_name': '',
            'birth_date': '', 'gender': 'Unknown', 'marital_status': '', 'address_type': '',
            'address_country': '', 'address_block': '', 'address_city': '', 'address_state': '',
            'address_post_code': '', 'address_do_not_mail': False, 'address_do_not_mail_reason': '',
            'phone_type': '', 'phone_number': '', 'email_address_type': '', 'email_address': '',
            'skip_adding_security_groups': False, 'existing_spouse': False, 'spouse_id': '',
            'spouse_last_name': '', 'spouse_first_name': '', 'spouse_middle_name': '', 'spouse_title':
            '', 'spouse_suffix': '', 'spouse_nick_name': '', 'spouse_maiden_name': '',
            'spouse_birth_date': '', 'spouse_gender': 'Unknown', 'spouse_relationship_type_code': '',
            'spouse_reciprocal_type_code': '', 'spouse_start_date': '', 'copy_primary_information':
            False, 'primary_soft_credit_relationship_exists': False,
            'primary_soft_credit_match_factor': 0, 'reciprocal_soft_credit_relationship_exists':
            False, 'reciprocal_soft_credit_match_factor': 0, 'existing_organization': False,
            'organization_id': '', 'organization_name': '', 'organization_address_type': '',
            'organization_country': '', 'organization_address_block': '', 'organization_city': '',
            'organization_state': '', 'organization_post_code': '', 'organization_do_not_mail': False,
            'organization_do_not_mail_reason': '', 'organization_phone_type': '',
            'organization_number': '', 'organization_relationship_type_code': '',
            'organization_reciprocal_type_code': '', 'organization_start_date': '',
            'organization_end_date': '', 'contact': False, 'contact_type': '', 'primary_contact':
            False, 'position': '', 'matching_gift_relationship': False, 'reciprocal_recognition_type':
            '', 'primary_recognition_type': '', 'address_omit_from_validation': False, 'address_dpc':
            '', 'address_cart': '', 'address_lot': '', 'address_county': '',
            'address_congressional_district': '', 'address_last_validation_attempt_date': '',
            'address_validation_message': '', 'address_certification_data': 0,
            'organization_omit_from_validation': False, 'organization_dpc': '', 'organization_cart':
            '', 'organization_lot': '', 'organization_county': '',
            'organization_congressional_district': '', 'organization_last_validation_attempt_date':
            '', 'organization_validation_message': '', 'organization_certification_data': 0,
            'validation_countries': [{'country_id': '', 'browsable': False}], 'zip_lookup_countries':
            [{'country_id': '', 'country_name': ''}], 'spouse_relationship': False,
            'house_hold_copy_primary_contact_info': False, 'job_category': '', 'career_level': '',
            'address_info_source': '', 'organization_info_source': '', 'title_2': '', 'suffix_2': '',
            'spouse_title_2': '', 'spouse_suffix_2': '', 'skip_adding_sites': False,
            'constituent_type': 0, 'organization_primary_soft_credit_relationship_exists': False,
            'organization_primary_soft_credit_match_factor': 0,
            'organization_reciprocal_soft_credit_relationship_exists': False,
            'organization_reciprocal_soft_credit_match_factor': 0,
            'organization_primary_recognition_type': '', 'organization_reciprocal_recognition_type':
            '', 'gender_code': '', 'spouse_gender_code': ''}.

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
    body: NewIndividual,
) -> Optional[Union[Any, PostResponse, ProblemDetails]]:
    """Create an individual.

     This operation is used to add an individual constituent, spouse(optional), and business(optional).

    Args:
        body (NewIndividual): CreateIndividual Example: {'last_name': '', 'first_name': '',
            'middle_name': '', 'title': '', 'suffix': '', 'nickname': '', 'maiden_name': '',
            'birth_date': '', 'gender': 'Unknown', 'marital_status': '', 'address_type': '',
            'address_country': '', 'address_block': '', 'address_city': '', 'address_state': '',
            'address_post_code': '', 'address_do_not_mail': False, 'address_do_not_mail_reason': '',
            'phone_type': '', 'phone_number': '', 'email_address_type': '', 'email_address': '',
            'skip_adding_security_groups': False, 'existing_spouse': False, 'spouse_id': '',
            'spouse_last_name': '', 'spouse_first_name': '', 'spouse_middle_name': '', 'spouse_title':
            '', 'spouse_suffix': '', 'spouse_nick_name': '', 'spouse_maiden_name': '',
            'spouse_birth_date': '', 'spouse_gender': 'Unknown', 'spouse_relationship_type_code': '',
            'spouse_reciprocal_type_code': '', 'spouse_start_date': '', 'copy_primary_information':
            False, 'primary_soft_credit_relationship_exists': False,
            'primary_soft_credit_match_factor': 0, 'reciprocal_soft_credit_relationship_exists':
            False, 'reciprocal_soft_credit_match_factor': 0, 'existing_organization': False,
            'organization_id': '', 'organization_name': '', 'organization_address_type': '',
            'organization_country': '', 'organization_address_block': '', 'organization_city': '',
            'organization_state': '', 'organization_post_code': '', 'organization_do_not_mail': False,
            'organization_do_not_mail_reason': '', 'organization_phone_type': '',
            'organization_number': '', 'organization_relationship_type_code': '',
            'organization_reciprocal_type_code': '', 'organization_start_date': '',
            'organization_end_date': '', 'contact': False, 'contact_type': '', 'primary_contact':
            False, 'position': '', 'matching_gift_relationship': False, 'reciprocal_recognition_type':
            '', 'primary_recognition_type': '', 'address_omit_from_validation': False, 'address_dpc':
            '', 'address_cart': '', 'address_lot': '', 'address_county': '',
            'address_congressional_district': '', 'address_last_validation_attempt_date': '',
            'address_validation_message': '', 'address_certification_data': 0,
            'organization_omit_from_validation': False, 'organization_dpc': '', 'organization_cart':
            '', 'organization_lot': '', 'organization_county': '',
            'organization_congressional_district': '', 'organization_last_validation_attempt_date':
            '', 'organization_validation_message': '', 'organization_certification_data': 0,
            'validation_countries': [{'country_id': '', 'browsable': False}], 'zip_lookup_countries':
            [{'country_id': '', 'country_name': ''}], 'spouse_relationship': False,
            'house_hold_copy_primary_contact_info': False, 'job_category': '', 'career_level': '',
            'address_info_source': '', 'organization_info_source': '', 'title_2': '', 'suffix_2': '',
            'spouse_title_2': '', 'spouse_suffix_2': '', 'skip_adding_sites': False,
            'constituent_type': 0, 'organization_primary_soft_credit_relationship_exists': False,
            'organization_primary_soft_credit_match_factor': 0,
            'organization_reciprocal_soft_credit_relationship_exists': False,
            'organization_reciprocal_soft_credit_match_factor': 0,
            'organization_primary_recognition_type': '', 'organization_reciprocal_recognition_type':
            '', 'gender_code': '', 'spouse_gender_code': ''}.

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
