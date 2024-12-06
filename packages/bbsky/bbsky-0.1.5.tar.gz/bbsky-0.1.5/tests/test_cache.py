import tempfile
from pathlib import Path

import hishel
import httpx
import pytest
from hishel._utils import httpcore

from bbsky.cache import generate_key, normalized_url, setup_controller, setup_storage, setup_transport


# Fixtures
@pytest.fixture
def temp_cache_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_httpcore_url():
    return httpcore.URL(
        scheme=b"https",
        host=b"api.example.com",
        port=None,
        target=b"/path/to/resource",
    )


@pytest.fixture
def sample_request(sample_httpcore_url):
    return httpcore.Request(
        method=b"GET",
        url=sample_httpcore_url,
        headers=[(b"host", b"api.example.com")],
    )


def test_setup_storage_default_params(temp_cache_dir):
    storage = setup_storage(base_path=temp_cache_dir)
    assert storage._base_path == temp_cache_dir
    assert storage._ttl == 3600
    assert storage._check_ttl_every == 60


def test_setup_storage_custom_params(temp_cache_dir):
    storage = setup_storage(base_path=temp_cache_dir, ttl=7200, check_ttl_every=120)
    assert storage._base_path == temp_cache_dir
    assert storage._ttl == 7200
    assert storage._check_ttl_every == 120


def test_normalized_url_string():
    url = "https://api.example.com/path"
    assert normalized_url(url) == url


def test_normalized_url_bytes():
    url = b"https://api.example.com/path"
    assert normalized_url(url) == "https://api.example.com/path"


def test_normalized_url_httpcore(sample_httpcore_url):
    expected = "https://api.example.com/path/to/resource"
    assert normalized_url(sample_httpcore_url) == expected


def test_normalized_url_with_port():
    url = httpcore.URL(
        scheme=b"https",
        host=b"api.example.com",
        port=8443,
        target=b"/path",
    )
    assert normalized_url(url) == "https://api.example.com:8443/path"


def test_generate_key_basic(sample_request):
    key = generate_key(sample_request)
    assert isinstance(key, str)
    assert len(key) == 64  # blake3 hexdigest length


def test_generate_key_with_body(sample_request):
    body = b'{"key": "value"}'
    key1 = generate_key(sample_request)
    key2 = generate_key(sample_request, body)
    assert key1 != key2  # Different bodies should produce different keys


def test_generate_key_identical_requests(sample_request):
    key1 = generate_key(sample_request)
    key2 = generate_key(sample_request)
    assert key1 == key2  # Same request should produce same key


def test_setup_controller_default_params():
    controller = setup_controller()
    assert controller._cacheable_methods == ["GET", "POST"]
    assert controller._cacheable_status_codes == [200]
    assert controller._cache_private is True
    assert controller._always_revalidate is True
    assert controller._force_cache is True


def test_setup_controller_custom_params():
    controller = setup_controller(
        cacheable_methods=["GET", "HEAD"],
        cacheable_status_codes=[200, 203, 304],
    )
    assert controller._cacheable_methods == ["GET", "HEAD"]
    assert controller._cacheable_status_codes == [200, 203, 304]


def test_setup_transport():
    transport = setup_transport()
    assert isinstance(transport, hishel.CacheTransport)
    assert isinstance(transport._transport, httpx.HTTPTransport)
    assert isinstance(transport._controller, hishel.Controller)
    assert isinstance(transport._storage, hishel.FileStorage)


def test_full_cache_flow(temp_cache_dir):
    # Setup components
    storage = setup_storage(base_path=temp_cache_dir)
    controller = setup_controller()
    transport = hishel.CacheTransport(
        transport=httpx.HTTPTransport(),
        controller=controller,
        storage=storage,
    )

    # Verify the complete setup works together
    assert transport._storage._base_path == temp_cache_dir
    assert transport._controller._cacheable_methods == ["GET", "POST"]
    assert callable(transport._controller._key_generator)
