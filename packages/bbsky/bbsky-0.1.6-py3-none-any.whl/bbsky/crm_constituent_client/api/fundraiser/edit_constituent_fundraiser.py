from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_constituent_fundraiser import EditConstituentFundraiser
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    fundraiser_date_range_id: str,
    *,
    body: EditConstituentFundraiser,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/fundraisers/{fundraiser_date_range_id}",
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
    fundraiser_date_range_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentFundraiser,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit a constituent fundraiser.

     This operation is used to edit a fundraiser constituency of a constituent.

    Args:
        fundraiser_date_range_id (str):
        body (EditConstituentFundraiser): EditConstituentFundraiser Example: {'date_from':
            '2021-11-28T12:00:00.0000000+00:00', 'date_to': '2022-12-28T12:00:00.0000000+00:00'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        fundraiser_date_range_id=fundraiser_date_range_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    fundraiser_date_range_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentFundraiser,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit a constituent fundraiser.

     This operation is used to edit a fundraiser constituency of a constituent.

    Args:
        fundraiser_date_range_id (str):
        body (EditConstituentFundraiser): EditConstituentFundraiser Example: {'date_from':
            '2021-11-28T12:00:00.0000000+00:00', 'date_to': '2022-12-28T12:00:00.0000000+00:00'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return sync_detailed(
        fundraiser_date_range_id=fundraiser_date_range_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    fundraiser_date_range_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentFundraiser,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit a constituent fundraiser.

     This operation is used to edit a fundraiser constituency of a constituent.

    Args:
        fundraiser_date_range_id (str):
        body (EditConstituentFundraiser): EditConstituentFundraiser Example: {'date_from':
            '2021-11-28T12:00:00.0000000+00:00', 'date_to': '2022-12-28T12:00:00.0000000+00:00'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        fundraiser_date_range_id=fundraiser_date_range_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    fundraiser_date_range_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentFundraiser,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit a constituent fundraiser.

     This operation is used to edit a fundraiser constituency of a constituent.

    Args:
        fundraiser_date_range_id (str):
        body (EditConstituentFundraiser): EditConstituentFundraiser Example: {'date_from':
            '2021-11-28T12:00:00.0000000+00:00', 'date_to': '2022-12-28T12:00:00.0000000+00:00'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            fundraiser_date_range_id=fundraiser_date_range_id,
            client=client,
            body=body,
        )
    ).parsed
