import json
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from bbsky.cli import app
from bbsky.token import BBSKY_TOKEN_FILE

runner = CliRunner()


@pytest.fixture
def mock_token_file():
    """Fixture to simulate the presence of a token file."""
    with patch("pathlib.Path.exists", return_value=True):
        yield


@pytest.fixture
def mock_no_token_file():
    """Fixture to simulate the absence of a token file."""
    with patch("pathlib.Path.exists", return_value=False):
        yield


@pytest.fixture
def mock_oauth2token():
    """Fixture to mock the OAuth2Token class."""
    with patch("bbsky.token.OAuth2Token") as mock_token:
        yield mock_token


@pytest.fixture
def mock_skyconfig():
    """Fixture to mock the SkyConfig class."""
    with patch("bbsky.config.SkyConfig") as mock_config:
        yield mock_config


def test_show_token_str_format(mock_token_file, mock_oauth2token):
    """Test the `show` command with string format output."""
    mock_token = MagicMock(email="test@example.com", __str__=lambda self: "TokenString")
    mock_oauth2token.load.return_value = mock_token

    result = runner.invoke(app, ["token", "show", "--fmt", "str"])

    assert result.exit_code == 0
    assert "Token for test@example.com: TokenString" in result.output
    mock_oauth2token.load.assert_called_once_with(BBSKY_TOKEN_FILE)


def test_show_token_json_format(mock_token_file, mock_oauth2token):
    """Test the `show` command with JSON format output."""
    mock_token = MagicMock(email="test@example.com", to_dict=lambda: {"key": "value"})
    mock_oauth2token.load.return_value = mock_token

    result = runner.invoke(app, ["token", "show", "--fmt", "json"])

    assert result.exit_code == 0
    assert json.dumps({"key": "value"}, indent=4) in result.output
    mock_oauth2token.load.assert_called_once_with(BBSKY_TOKEN_FILE)


def test_show_no_token(mock_no_token_file):
    """Test the `show` command when no token file exists."""
    result = runner.invoke(app, ["token", "show"])

    assert result.exit_code == 0
    assert "No token found." in result.output


def test_purge_token_confirm(mock_token_file, mock_oauth2token):
    """Test the `purge` command with user confirmation."""
    mock_token = MagicMock(__str__=lambda self: "TokenString")
    mock_oauth2token.load.return_value = mock_token

    with patch("typer.confirm", return_value=True) as mock_confirm:
        with patch("pathlib.Path.unlink") as mock_unlink:
            result = runner.invoke(app, ["token", "purge"])

            assert result.exit_code == 0
            assert "Token purged." in result.output
            mock_confirm.assert_called_once()
            mock_unlink.assert_called_once_with()


def test_purge_token_abort(mock_token_file, mock_oauth2token):
    """Test the `purge` command when user aborts confirmation."""
    mock_token = MagicMock(__str__=lambda self: "TokenString")
    mock_oauth2token.load.return_value = mock_token

    with patch("typer.confirm", return_value=False) as mock_confirm:
        result = runner.invoke(app, ["token", "purge"])

        assert result.exit_code == 0
        assert "Aborted. Token not purged." in result.output
        mock_confirm.assert_called_once()


def test_purge_no_token(mock_no_token_file):
    """Test the `purge` command when no token file exists."""
    result = runner.invoke(app, ["token", "purge"])

    assert result.exit_code == 0
    assert "No token found." in result.output


@pytest.mark.skip("TODO: Need to fix so that FileNotFoundError isn't thrown in CI pipeline")
def test_refresh_token(mock_token_file, mock_oauth2token, mock_skyconfig) -> None:
    """Test the `refresh` command."""
    mock_token = MagicMock(refresh=lambda config: MagicMock(__str__=lambda self: "NewTokenString"))
    mock_oauth2token.load.return_value = mock_token
    mock_config = MagicMock()
    mock_skyconfig.load.return_value = mock_config

    with patch("bbsky.token.OAuth2Token.to_cache"):
        with patch("pathlib.Path.exists", return_value=True):  # Simulate token file exists
            result = runner.invoke(app, ["token", "refresh"])

            # Assertions
            assert result.exit_code == 0, f"CLI failed with output: {result.output}"
            assert "Token refreshed: NewTokenString" in result.output
