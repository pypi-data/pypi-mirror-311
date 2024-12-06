from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from bbsky.apis import api_name_to_url, load_detailed_functions
from bbsky.data_cls import URL

mock_base_url = URL("http://mockapi.example.com")
runner = CliRunner()


@pytest.fixture
def mock_imported_modules():
    """Fixture for mocking dynamically imported modules."""
    with patch("bbsky.apis.importlib.import_module") as mock_import:
        mock_module = MagicMock()
        mock_module.asyncio_detailed = MagicMock()
        mock_module.sync_detailed = MagicMock()
        mock_import.return_value = mock_module
        yield mock_import, mock_module


def test_api_name_to_url_valid_name():
    url = api_name_to_url("crm_constituent", base_url=mock_base_url)
    assert url.path == "/crm-conmg"


def test_api_name_to_url_invalid_name():
    with pytest.raises(ValueError, match="Invalid API name: invalid_name"):
        api_name_to_url("invalid_name", base_url=mock_base_url)


def test_load_detailed_functions(mock_imported_modules):
    mock_import, mock_module = mock_imported_modules
    with patch("bbsky.apis.Path.rglob") as mock_rglob:
        mock_rglob.return_value = [MagicMock()]

        sync_funcs, async_funcs = load_detailed_functions()
        assert mock_import.called
        assert mock_module.sync_detailed in sync_funcs.values()
        assert mock_module.asyncio_detailed in async_funcs.values()


def test_show_api_functions():
    """Ensure `show_api_functions` runs without errors."""
    # You could capture the output if needed.
    from bbsky.apis import show_api_functions

    show_api_functions()
