from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_organization import EditOrganization
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    constituent_id: str,
    *,
    body: EditOrganization,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/organizations/{constituent_id}",
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
    constituent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditOrganization,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit an organization.

     Organization constituent edit operation for gift data entry

    Args:
        constituent_id (str):
        body (EditOrganization): EditOrganization Example: {'organization_name': 'ABC Learning
            Center', 'industry': 'Education', 'num_employees': 20, 'num_subsidiaries': 2,
            'parent_corp_id': '', 'picture': '', 'picture_thumbnail': '', 'picture_changed': False,
            'web_address': '', 'is_primary': False, 'primary_address_id':
            '4811c284-31b1-4ba1-a94b-424687975bda', 'address_type': 'Business', 'address_country':
            'United States', 'address_block': '29 Hitch Avenue', 'address_city': 'Morgan',
            'address_state': 'UT', 'address_postcode': '84050', 'address_do_not_mail': False,
            'address_do_not_mail_reason': '', 'primary_phone_id':
            '88f5c331-b465-413c-b955-976ec018beb5', 'phone_type': 'Business', 'phone_number':
            '801-557-2819', 'primary_email_address_id': '', 'email_address_type': '', 'email_address':
            ''}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        constituent_id=constituent_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    constituent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditOrganization,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit an organization.

     Organization constituent edit operation for gift data entry

    Args:
        constituent_id (str):
        body (EditOrganization): EditOrganization Example: {'organization_name': 'ABC Learning
            Center', 'industry': 'Education', 'num_employees': 20, 'num_subsidiaries': 2,
            'parent_corp_id': '', 'picture': '', 'picture_thumbnail': '', 'picture_changed': False,
            'web_address': '', 'is_primary': False, 'primary_address_id':
            '4811c284-31b1-4ba1-a94b-424687975bda', 'address_type': 'Business', 'address_country':
            'United States', 'address_block': '29 Hitch Avenue', 'address_city': 'Morgan',
            'address_state': 'UT', 'address_postcode': '84050', 'address_do_not_mail': False,
            'address_do_not_mail_reason': '', 'primary_phone_id':
            '88f5c331-b465-413c-b955-976ec018beb5', 'phone_type': 'Business', 'phone_number':
            '801-557-2819', 'primary_email_address_id': '', 'email_address_type': '', 'email_address':
            ''}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return sync_detailed(
        constituent_id=constituent_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    constituent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditOrganization,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit an organization.

     Organization constituent edit operation for gift data entry

    Args:
        constituent_id (str):
        body (EditOrganization): EditOrganization Example: {'organization_name': 'ABC Learning
            Center', 'industry': 'Education', 'num_employees': 20, 'num_subsidiaries': 2,
            'parent_corp_id': '', 'picture': '', 'picture_thumbnail': '', 'picture_changed': False,
            'web_address': '', 'is_primary': False, 'primary_address_id':
            '4811c284-31b1-4ba1-a94b-424687975bda', 'address_type': 'Business', 'address_country':
            'United States', 'address_block': '29 Hitch Avenue', 'address_city': 'Morgan',
            'address_state': 'UT', 'address_postcode': '84050', 'address_do_not_mail': False,
            'address_do_not_mail_reason': '', 'primary_phone_id':
            '88f5c331-b465-413c-b955-976ec018beb5', 'phone_type': 'Business', 'phone_number':
            '801-557-2819', 'primary_email_address_id': '', 'email_address_type': '', 'email_address':
            ''}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        constituent_id=constituent_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    constituent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditOrganization,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit an organization.

     Organization constituent edit operation for gift data entry

    Args:
        constituent_id (str):
        body (EditOrganization): EditOrganization Example: {'organization_name': 'ABC Learning
            Center', 'industry': 'Education', 'num_employees': 20, 'num_subsidiaries': 2,
            'parent_corp_id': '', 'picture': '', 'picture_thumbnail': '', 'picture_changed': False,
            'web_address': '', 'is_primary': False, 'primary_address_id':
            '4811c284-31b1-4ba1-a94b-424687975bda', 'address_type': 'Business', 'address_country':
            'United States', 'address_block': '29 Hitch Avenue', 'address_city': 'Morgan',
            'address_state': 'UT', 'address_postcode': '84050', 'address_do_not_mail': False,
            'address_do_not_mail_reason': '', 'primary_phone_id':
            '88f5c331-b465-413c-b955-976ec018beb5', 'phone_type': 'Business', 'phone_number':
            '801-557-2819', 'primary_email_address_id': '', 'email_address_type': '', 'email_address':
            ''}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            constituent_id=constituent_id,
            client=client,
            body=body,
        )
    ).parsed
