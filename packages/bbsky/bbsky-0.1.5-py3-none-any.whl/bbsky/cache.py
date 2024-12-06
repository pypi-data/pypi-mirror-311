import logging
from pathlib import Path
from typing import Sequence, Union

import hishel
import httpx
from blake3 import blake3
from hishel._utils import httpcore  # type: ignore

from bbsky.paths import BBSKY_CACHE_DIR

logging.getLogger("hishel.controller").setLevel(logging.DEBUG)


def setup_storage(base_path: Path = BBSKY_CACHE_DIR, ttl: int = 3600, check_ttl_every: int = 60) -> hishel.FileStorage:
    return hishel.FileStorage(base_path=base_path, ttl=ttl, check_ttl_every=check_ttl_every)


def normalized_url(url: Union[httpcore.URL, str, bytes]) -> str:
    if isinstance(url, str):
        return url

    if isinstance(url, bytes):
        return url.decode("ascii")

    port = f":{url.port}" if url.port is not None else ""
    return f'{url.scheme.decode("ascii")}://{url.host.decode("ascii")}{port}{url.target.decode("ascii")}'


def get_header(key: bytes, headers: Sequence[tuple[bytes, bytes]]) -> bytes:
    for header, value in headers:
        if header == key:
            return value
    return b""


def generate_key(request: httpcore.Request, body: bytes = b"") -> str:
    encoded_url = normalized_url(request.url).encode("ascii")

    user_token = get_header(b"Authorization", request.headers)
    team_slug = get_header(b"X-Team-Slug", request.headers)
    subscription_key = get_header(b"Bb-Api-Subscription-Key", request.headers)
    key_parts = [request.method, encoded_url, body, user_token, subscription_key, team_slug]

    key = blake3()
    for part in key_parts:
        key.update(part)
    return key.hexdigest()


def setup_controller(
    cacheable_methods: Sequence[str] = ("GET", "POST"),
    cacheable_status_codes: Sequence[int] = (200,),
) -> hishel.Controller:
    return hishel.Controller(
        cacheable_methods=list(cacheable_methods),
        cacheable_status_codes=list(cacheable_status_codes),
        key_generator=generate_key,  # type: ignore
        cache_private=True,
        always_revalidate=True,
        force_cache=True,
    )


def setup_transport() -> hishel.CacheTransport:
    return hishel.CacheTransport(
        transport=httpx.HTTPTransport(), controller=setup_controller(), storage=setup_storage()
    )
