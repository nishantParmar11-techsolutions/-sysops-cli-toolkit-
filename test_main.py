# ==============================================================================
# SysOps CLI Toolkit - Elite Enterprise Unit Test Suite
# ==============================================================================

from unittest.mock import patch, MagicMock
import requests
from typer.testing import CliRunner
from main import app

runner = CliRunner()


def test_system_info_command() -> None:
    """Verify that system-info prints environment details successfully."""
    result = runner.invoke(app, ["system-info"])
    assert result.exit_code == 0
    assert "SysOps Toolkit Environment Overview" in result.output
    assert "Typer" in result.output


def test_system_info_json_command() -> None:
    """Verify that system-info outputs valid JSON when requested."""
    result = runner.invoke(app, ["system-info", "--json"])
    assert result.exit_code == 0
    assert "cli_engine" in result.output
    assert "Typer (v0.12.3)" in result.output


@patch("main.requests.get")
def test_health_check_success(mock_get: MagicMock) -> None:
    """Verify health-check succeeds when target returns status 200."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"status": "healthy"}'
    mock_response.json.return_value = {"status": "healthy"}
    mock_get.return_value = mock_response

    result = runner.invoke(app, ["health-check", "--url", "http://test-server/health"])
    assert result.exit_code == 0
    assert "SUCCESS: Service is Healthy!" in result.output


@patch("main.requests.get")
def test_health_check_success_json(mock_get: MagicMock) -> None:
    """Verify health-check outputs JSON format correctly on success."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"status": "healthy"}'
    mock_response.json.return_value = {"status": "healthy"}
    mock_get.return_value = mock_response

    result = runner.invoke(app, ["health-check", "--url", "http://test-server/health", "--json"])
    assert result.exit_code == 0
    assert '"is_healthy": true' in result.output


@patch("main.requests.get")
def test_health_check_warning_status(mock_get: MagicMock) -> None:
    """Verify health-check warns and exits with 1 when target returns 500 error."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    result = runner.invoke(app, ["health-check", "--url", "http://test-server/health"])
    assert result.exit_code == 1
    assert "WARNING: Received unhealthy status code 500" in result.output


@patch("main.requests.get")
def test_health_check_connection_error(mock_get: MagicMock) -> None:
    """Verify health-check handles connection exceptions gracefully with exit code 1."""
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

    result = runner.invoke(app, ["health-check", "--url", "http://unreachable-server/health"])
    assert result.exit_code == 1
    assert "ERROR: Connection failed to target" in result.output


@patch("main.requests.get")
def test_health_check_connection_error_json(mock_get: MagicMock) -> None:
    """Verify health-check outputs JSON error structure on connection failure."""
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

    result = runner.invoke(app, ["health-check", "--url", "http://unreachable-server/health", "--json"])
    assert result.exit_code == 1
    assert '"is_healthy": false' in result.output
    assert '"error":' in result.output
