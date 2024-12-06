from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.new_tribute import NewTribute
from ...models.post_response import PostResponse
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    *,
    body: NewTribute,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/tribute",
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
    body: NewTribute,
) -> Response[Union[Any, PostResponse, ProblemDetails]]:
    """Create a tribute.

     This operation is used for adding a new tribute to a revenue record.

    Args:
        body (NewTribute): CreateTribute Example: {'revenue_id': '', 'tribute_id': '', 'amount':
            0, 'designation_id': '', 'splits': [{'id': '', 'designation_id': '', 'amount': 0,
            'base_currency_id': ''}], 'apply_default_designation': False, 'revenue_posted': False,
            'revenue_designation_id': '', 'allow_default': False, 'base_currency_id': '',
            'tribute_anonymous': False, 'friends_asking_friends': False}.

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
    body: NewTribute,
) -> Optional[Union[Any, PostResponse, ProblemDetails]]:
    """Create a tribute.

     This operation is used for adding a new tribute to a revenue record.

    Args:
        body (NewTribute): CreateTribute Example: {'revenue_id': '', 'tribute_id': '', 'amount':
            0, 'designation_id': '', 'splits': [{'id': '', 'designation_id': '', 'amount': 0,
            'base_currency_id': ''}], 'apply_default_designation': False, 'revenue_posted': False,
            'revenue_designation_id': '', 'allow_default': False, 'base_currency_id': '',
            'tribute_anonymous': False, 'friends_asking_friends': False}.

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
    body: NewTribute,
) -> Response[Union[Any, PostResponse, ProblemDetails]]:
    """Create a tribute.

     This operation is used for adding a new tribute to a revenue record.

    Args:
        body (NewTribute): CreateTribute Example: {'revenue_id': '', 'tribute_id': '', 'amount':
            0, 'designation_id': '', 'splits': [{'id': '', 'designation_id': '', 'amount': 0,
            'base_currency_id': ''}], 'apply_default_designation': False, 'revenue_posted': False,
            'revenue_designation_id': '', 'allow_default': False, 'base_currency_id': '',
            'tribute_anonymous': False, 'friends_asking_friends': False}.

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
    body: NewTribute,
) -> Optional[Union[Any, PostResponse, ProblemDetails]]:
    """Create a tribute.

     This operation is used for adding a new tribute to a revenue record.

    Args:
        body (NewTribute): CreateTribute Example: {'revenue_id': '', 'tribute_id': '', 'amount':
            0, 'designation_id': '', 'splits': [{'id': '', 'designation_id': '', 'amount': 0,
            'base_currency_id': ''}], 'apply_default_designation': False, 'revenue_posted': False,
            'revenue_designation_id': '', 'allow_default': False, 'base_currency_id': '',
            'tribute_anonymous': False, 'friends_asking_friends': False}.

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
