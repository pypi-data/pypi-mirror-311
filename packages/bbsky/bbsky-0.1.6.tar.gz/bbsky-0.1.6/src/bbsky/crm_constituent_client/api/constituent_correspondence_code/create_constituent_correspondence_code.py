from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.new_constituent_correspondence_code import NewConstituentCorrespondenceCode
from ...models.post_response import PostResponse
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    *,
    body: NewConstituentCorrespondenceCode,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/constituentcorrespondencecodes",
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
    body: NewConstituentCorrespondenceCode,
) -> Response[Union[Any, PostResponse, ProblemDetails]]:
    """Create a constituent correspondence code.

     This operation is used to add correspondence record for a constituent.

    Args:
        body (NewConstituentCorrespondenceCode): CreateConstituentCorrespondenceCode Example:
            {'constituent_id': 'FE204CAB-0E67-4F28-990C-3E1B3B5C40A5', 'correspondence_code':
            'Newsletter', 'date_sent': '2018-05-22T12:00:00.0000000+00:00', 'comments': 'Newsletter
            discussing the volunteer drive.'}.

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
    body: NewConstituentCorrespondenceCode,
) -> Optional[Union[Any, PostResponse, ProblemDetails]]:
    """Create a constituent correspondence code.

     This operation is used to add correspondence record for a constituent.

    Args:
        body (NewConstituentCorrespondenceCode): CreateConstituentCorrespondenceCode Example:
            {'constituent_id': 'FE204CAB-0E67-4F28-990C-3E1B3B5C40A5', 'correspondence_code':
            'Newsletter', 'date_sent': '2018-05-22T12:00:00.0000000+00:00', 'comments': 'Newsletter
            discussing the volunteer drive.'}.

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
    body: NewConstituentCorrespondenceCode,
) -> Response[Union[Any, PostResponse, ProblemDetails]]:
    """Create a constituent correspondence code.

     This operation is used to add correspondence record for a constituent.

    Args:
        body (NewConstituentCorrespondenceCode): CreateConstituentCorrespondenceCode Example:
            {'constituent_id': 'FE204CAB-0E67-4F28-990C-3E1B3B5C40A5', 'correspondence_code':
            'Newsletter', 'date_sent': '2018-05-22T12:00:00.0000000+00:00', 'comments': 'Newsletter
            discussing the volunteer drive.'}.

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
    body: NewConstituentCorrespondenceCode,
) -> Optional[Union[Any, PostResponse, ProblemDetails]]:
    """Create a constituent correspondence code.

     This operation is used to add correspondence record for a constituent.

    Args:
        body (NewConstituentCorrespondenceCode): CreateConstituentCorrespondenceCode Example:
            {'constituent_id': 'FE204CAB-0E67-4F28-990C-3E1B3B5C40A5', 'correspondence_code':
            'Newsletter', 'date_sent': '2018-05-22T12:00:00.0000000+00:00', 'comments': 'Newsletter
            discussing the volunteer drive.'}.

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
