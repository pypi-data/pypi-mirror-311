from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_constituent_note import EditConstituentNote
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    constituent_note_id: str,
    *,
    body: EditConstituentNote,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/constituentnotes/{constituent_note_id}",
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
    constituent_note_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentNote,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit a constituent note.

     This operation is for editing a given constituent's note.

    Args:
        constituent_note_id (str):
        body (EditConstituentNote): EditConstituentNote Example: {'context_type': 0, 'title':
            'Merge note', 'date_entered': '2022-08-24T01:02:47.0000000+00:00', 'author_id':
            'E6B5E48F-9AC5-40AB-B091-DFB168CB19BE', 'note_type': 'Merge', 'text_note': 'Constituent
            merged 10/12/20', 'html_note': '<!DOCTYPE html><html><head></head><body><p>Constituent
            merged 10/12/20</p></body></html>'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        constituent_note_id=constituent_note_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    constituent_note_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentNote,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit a constituent note.

     This operation is for editing a given constituent's note.

    Args:
        constituent_note_id (str):
        body (EditConstituentNote): EditConstituentNote Example: {'context_type': 0, 'title':
            'Merge note', 'date_entered': '2022-08-24T01:02:47.0000000+00:00', 'author_id':
            'E6B5E48F-9AC5-40AB-B091-DFB168CB19BE', 'note_type': 'Merge', 'text_note': 'Constituent
            merged 10/12/20', 'html_note': '<!DOCTYPE html><html><head></head><body><p>Constituent
            merged 10/12/20</p></body></html>'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return sync_detailed(
        constituent_note_id=constituent_note_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    constituent_note_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentNote,
) -> Response[Union[Any, ProblemDetails]]:
    """Edit a constituent note.

     This operation is for editing a given constituent's note.

    Args:
        constituent_note_id (str):
        body (EditConstituentNote): EditConstituentNote Example: {'context_type': 0, 'title':
            'Merge note', 'date_entered': '2022-08-24T01:02:47.0000000+00:00', 'author_id':
            'E6B5E48F-9AC5-40AB-B091-DFB168CB19BE', 'note_type': 'Merge', 'text_note': 'Constituent
            merged 10/12/20', 'html_note': '<!DOCTYPE html><html><head></head><body><p>Constituent
            merged 10/12/20</p></body></html>'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        constituent_note_id=constituent_note_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    constituent_note_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EditConstituentNote,
) -> Optional[Union[Any, ProblemDetails]]:
    """Edit a constituent note.

     This operation is for editing a given constituent's note.

    Args:
        constituent_note_id (str):
        body (EditConstituentNote): EditConstituentNote Example: {'context_type': 0, 'title':
            'Merge note', 'date_entered': '2022-08-24T01:02:47.0000000+00:00', 'author_id':
            'E6B5E48F-9AC5-40AB-B091-DFB168CB19BE', 'note_type': 'Merge', 'text_note': 'Constituent
            merged 10/12/20', 'html_note': '<!DOCTYPE html><html><head></head><body><p>Constituent
            merged 10/12/20</p></body></html>'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            constituent_note_id=constituent_note_id,
            client=client,
            body=body,
        )
    ).parsed
