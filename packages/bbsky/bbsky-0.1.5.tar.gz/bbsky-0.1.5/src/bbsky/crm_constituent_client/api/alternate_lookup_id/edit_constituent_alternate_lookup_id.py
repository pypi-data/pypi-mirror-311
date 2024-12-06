from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_constituent_alternate_lookup_id import EditConstituentAlternateLookupId
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    alternate_lookup_id_id: str,
    *,
    body: EditConstituentAlternateLookupId,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/alternatelookupids/{alternate_lookup_id_id}",
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
    alternate_lookup_id_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentAlternateLookupId,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit a constituent alternate lookup id.

     This operation is used to edit a constituent's alternate lookup id.

    Args:
        alternate_lookup_id_id (str):
        body (EditConstituentAlternateLookupId): EditConstituentAlternateLookupId Example:
            {'alternate_lookup_id_type': '', 'alternate_lookup_id': ''}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        alternate_lookup_id_id=alternate_lookup_id_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    alternate_lookup_id_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentAlternateLookupId,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit a constituent alternate lookup id.

     This operation is used to edit a constituent's alternate lookup id.

    Args:
        alternate_lookup_id_id (str):
        body (EditConstituentAlternateLookupId): EditConstituentAlternateLookupId Example:
            {'alternate_lookup_id_type': '', 'alternate_lookup_id': ''}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return sync_detailed(
        alternate_lookup_id_id=alternate_lookup_id_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    alternate_lookup_id_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentAlternateLookupId,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit a constituent alternate lookup id.

     This operation is used to edit a constituent's alternate lookup id.

    Args:
        alternate_lookup_id_id (str):
        body (EditConstituentAlternateLookupId): EditConstituentAlternateLookupId Example:
            {'alternate_lookup_id_type': '', 'alternate_lookup_id': ''}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        alternate_lookup_id_id=alternate_lookup_id_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    alternate_lookup_id_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentAlternateLookupId,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit a constituent alternate lookup id.

     This operation is used to edit a constituent's alternate lookup id.

    Args:
        alternate_lookup_id_id (str):
        body (EditConstituentAlternateLookupId): EditConstituentAlternateLookupId Example:
            {'alternate_lookup_id_type': '', 'alternate_lookup_id': ''}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            alternate_lookup_id_id=alternate_lookup_id_id,
            client=client,
            body=body,
        )
    ).parsed
