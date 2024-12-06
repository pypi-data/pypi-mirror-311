import json
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from bbsky.config import BBSKY_CONFIG_FILE, SkyConfig, SkyConfigEnvVars, cli
from bbsky.data_cls import URL

runner: CliRunner = CliRunner()


@pytest.fixture
def mock_config_file() -> Generator[None, None, None]:
    """Fixture to simulate the existence of a configuration file."""
    with patch("pathlib.Path.exists", return_value=True):
        yield


@pytest.fixture
def mock_no_config_file() -> Generator[None, None, None]:
    """Fixture to simulate the absence of a configuration file."""
    with patch("pathlib.Path.exists", return_value=False):
        yield


@pytest.fixture
def mock_skyconfig() -> Generator[MagicMock, None, None]:
    """Fixture to mock the SkyConfig class."""
    with patch("bbsky.config.SkyConfig") as mock_config:
        yield mock_config


def test_create_config() -> None:
    """Test the `create` command."""
    config_data: dict[str, str] = {
        "client_id": "test_client_id",
        "client_secret": "test_client_secret",
        "redirect_uri": "http://localhost/callback",
        "subscription_key": "test_subscription_key",
    }

    with patch("pathlib.Path.exists", return_value=True):  # Simulate file exists
        with patch("typer.confirm", return_value=True):  # Simulate user confirms overwrite
            with patch("pathlib.Path.write_text") as mock_write:
                result = runner.invoke(
                    cli,
                    [
                        "create",
                        "--client-id",
                        config_data["client_id"],
                        "--client-secret",
                        config_data["client_secret"],
                        "--redirect-uri",
                        config_data["redirect_uri"],
                        "--subscription-key",
                        config_data["subscription_key"],
                        "--output-path",
                        str(BBSKY_CONFIG_FILE),
                    ],
                )

                assert result.exit_code == 0
                assert f"Config saved to {BBSKY_CONFIG_FILE}" in result.output
                mock_write.assert_called_once()


def test_show_config_json(mock_config_file: None, mock_skyconfig: MagicMock) -> None:
    """Test the `show` command with JSON output."""
    mock_config: MagicMock = MagicMock(to_dict=lambda: {"key": "value"})
    mock_skyconfig.from_json_file.return_value = mock_config

    result = runner.invoke(cli, ["show", "--fmt", "json"])
    assert result.exit_code == 0
    assert json.dumps({"key": "value"}, indent=4) in result.output
    mock_skyconfig.from_json_file.assert_called_once_with(BBSKY_CONFIG_FILE)


def test_show_config_env(mock_config_file: None, mock_skyconfig: MagicMock) -> None:
    """Test the `show` command with environment variable output."""
    mock_config: MagicMock = MagicMock(
        client_id="client_id",
        client_secret="client_secret",
        redirect_uri="http://localhost",
        subscription_key="subscription_key",
    )
    mock_skyconfig.from_json_file.return_value = mock_config

    result = runner.invoke(cli, ["show", "--fmt", "env"])
    assert result.exit_code == 0
    assert f"export {SkyConfigEnvVars.CLIENT_ID.value}=client_id" in result.output
    assert f"export {SkyConfigEnvVars.CLIENT_SECRET.value}=client_secret" in result.output
    assert f"export {SkyConfigEnvVars.REDIRECT_URI.value}=http://localhost" in result.output
    assert f"export {SkyConfigEnvVars.SUBSCRIPTION_KEY.value}=subscription_key" in result.output


def test_show_no_config(mock_no_config_file: None) -> None:
    """Test the `show` command when no config file exists."""
    result = runner.invoke(cli, ["show"])
    assert result.exit_code == 0
    assert f"Config not found at {BBSKY_CONFIG_FILE}" in result.output


def test_update_config(mock_config_file: None) -> None:
    """Test the `update` command."""
    # Create an actual SkyConfig instance to work with `evolve`
    original_config = SkyConfig(
        client_id="old_client_id",
        client_secret="old_client_secret",
        redirect_uri=URL("http://old_redirect"),
        subscription_key="old_subscription_key",
    )

    with patch("bbsky.config.SkyConfig.from_json_file", return_value=original_config):
        with patch("typer.confirm", return_value=True):  # Mock user confirmation
            with patch("pathlib.Path.write_text") as mock_write:
                result = runner.invoke(
                    cli,
                    [
                        "update",
                        "--client-id",
                        "new_client_id",
                        "--client-secret",
                        "new_client_secret",
                        "--redirect-uri",
                        "http://new_redirect",
                        "--subscription-key",
                        "new_subscription_key",
                    ],
                )

                # Assertions
                assert result.exit_code == 0, f"CLI failed with output: {result.output}"
                assert "Updated SkyConfig:" in result.output
                assert "new_client_id" in result.output

                # Ensure the updated config is written to the file
                mock_write.assert_called_once()
                saved_data = json.loads(mock_write.call_args[0][0])  # Extract the JSON payload
                assert saved_data["client_id"] == "new_client_id"
                assert saved_data["client_secret"] == "new_client_secret"
                assert saved_data["redirect_uri"] == "http://new_redirect"
                assert saved_data["subscription_key"] == "new_subscription_key"


def test_update_no_changes(mock_config_file: None) -> None:
    """Test the `update` command when no values are provided."""
    result = runner.invoke(cli, ["update"])
    assert result.exit_code == 0
    assert "No new values provided. Exiting." in result.output


def test_purge_config_confirm(mock_config_file: None) -> None:
    """Test the `purge` command with user confirmation."""
    with patch("pathlib.Path.unlink") as mock_unlink:
        with patch("typer.confirm", return_value=True):
            result = runner.invoke(cli, ["purge"])

            assert result.exit_code == 0
            assert f"Config deleted at {BBSKY_CONFIG_FILE}" in result.output
            mock_unlink.assert_called_once_with()


def test_purge_config_abort(mock_config_file: None) -> None:
    """Test the `purge` command when user aborts confirmation."""
    with patch("typer.confirm", return_value=False):
        result = runner.invoke(cli, ["purge"])

        assert result.exit_code == 0
        assert "Aborted." in result.output


def test_purge_no_config(mock_no_config_file: None) -> None:
    """Test the `purge` command when no config file exists."""
    result = runner.invoke(cli, ["purge"])

    assert result.exit_code == 0
    assert f"Config not found at {BBSKY_CONFIG_FILE}" in result.output
