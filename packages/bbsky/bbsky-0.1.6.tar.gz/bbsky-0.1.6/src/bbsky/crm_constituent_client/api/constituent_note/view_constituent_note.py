from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.constituent_note_view import ConstituentNoteView
from ...types import Response


def _get_kwargs(
    constituent_note_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/constituentnotes/{constituent_note_id}/view",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ConstituentNoteView]:
    if response.status_code == 200:
        response_200 = ConstituentNoteView.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ConstituentNoteView]:
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
) -> Response[ConstituentNoteView]:
    """View a constituent note.

     This operation displays a constituent note.

    Args:
        constituent_note_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConstituentNoteView]
    """

    kwargs = _get_kwargs(
        constituent_note_id=constituent_note_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    constituent_note_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ConstituentNoteView]:
    """View a constituent note.

     This operation displays a constituent note.

    Args:
        constituent_note_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConstituentNoteView
    """

    return sync_detailed(
        constituent_note_id=constituent_note_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    constituent_note_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ConstituentNoteView]:
    """View a constituent note.

     This operation displays a constituent note.

    Args:
        constituent_note_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConstituentNoteView]
    """

    kwargs = _get_kwargs(
        constituent_note_id=constituent_note_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    constituent_note_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ConstituentNoteView]:
    """View a constituent note.

     This operation displays a constituent note.

    Args:
        constituent_note_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConstituentNoteView
    """

    return (
        await asyncio_detailed(
            constituent_note_id=constituent_note_id,
            client=client,
        )
    ).parsed
