from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from bbsky.cli import app, get_command_app, init_logging

runner = CliRunner()


@pytest.fixture
def mock_import_module():
    """Mock importlib.import_module to simulate loading dynamic modules."""
    with patch("bbsky.cli.importlib.import_module") as mock_import:
        yield mock_import


@pytest.fixture
def mock_setup_logger():
    """Mock setup_logger to ensure logging is initialized without real setup."""
    with patch("bbsky.cli.setup_logger") as mock_logger:
        yield mock_logger


def test_get_command_app_with_app(mock_import_module):
    """Test get_command_app loads a module with an `app` attribute."""
    mock_app = MagicMock()
    mock_import_module.return_value = MagicMock(app=mock_app)

    command_app = get_command_app("mock_command")
    assert command_app == mock_app
    mock_import_module.assert_called_once_with("bbsky.mock_command")


def test_get_command_app_not_found(mock_import_module):
    """Test get_command_app returns None if module is not found."""
    mock_import_module.side_effect = ImportError("Module not found")

    command_app = get_command_app("non_existent_command")
    assert command_app is None


def test_init_logging(mock_setup_logger):
    """Test that init_logging initializes logging."""
    init_logging()
    mock_setup_logger.assert_called_once_with(name="bbsky.cli")


def test_cli_no_arguments():
    """Test running the CLI with no arguments shows the help message."""
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "Command line interface for bbsky." in result.output


def test_cli_invalid_command():
    """Test running the CLI with an invalid command."""
    result = runner.invoke(app, ["invalid_command"])
    assert result.exit_code == 2
    assert "No such command 'invalid_command'." in result.output


@pytest.mark.parametrize("command_name", ["server", "config", "token", "paths", "apis"])
def test_cli_valid_commands(command_name, mock_import_module):
    """Test running valid commands dynamically."""
    # Simulate that each command has an app attribute
    mock_app = MagicMock()
    mock_import_module.return_value = MagicMock(app=mock_app)
    result = runner.invoke(app, [command_name, "--help"])

    assert "Usage: " in result.output
    assert result.exit_code == 0
