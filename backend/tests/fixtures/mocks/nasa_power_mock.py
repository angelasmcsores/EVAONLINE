"""
NASA Power API Mock

Mock responses para NASA Power API.
"""

from unittest.mock import Mock


class NASAPowerMock:
    """Mock para NASA Power API."""

    @staticmethod
    def mock_successful_response():
        """Cria mock de resposta bem-sucedida."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "header": {"title": "NASA/POWER", "api_version": "v2.5.4"},
            "parameters": {
                "T2M_MAX": {"20250701": 32.5},
                "T2M_MIN": {"20250701": 18.2},
            },
            "geometry": {"type": "Point", "coordinates": [-48.5, -22.25]},
        }
        return mock_response

    @staticmethod
    def mock_error_response(status_code: int = 500):
        """
        Cria mock de resposta com erro.

        Args:
            status_code: Código de status HTTP
        """
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = {"error": "Internal Server Error"}
        return mock_response

    @staticmethod
    def mock_timeout_error():
        """Cria mock de timeout."""
        import httpx

        raise httpx.TimeoutException("Request timeout")
