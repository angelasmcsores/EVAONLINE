"""
OpenTopo API Mock

Mock responses para OpenTopo API.
"""

from unittest.mock import Mock


class OpenTopoMock:
    """Mock para OpenTopo API."""

    @staticmethod
    def mock_successful_response(elevation: float = 580.0):
        """
        Cria mock de resposta bem-sucedida.

        Args:
            elevation: Elevação em metros
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "OK",
            "results": [
                {
                    "elevation": elevation,
                    "location": {"lat": -22.25, "lng": -48.5},
                }
            ],
        }
        return mock_response
