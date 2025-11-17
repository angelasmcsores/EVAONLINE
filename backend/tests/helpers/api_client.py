"""
API Client Helper

Helper para fazer chamadas HTTP em testes.
"""

from typing import Optional


class APIClientHelper:
    """Helper para testes de API."""

    def __init__(self, client):
        """
        Inicializa helper com cliente FastAPI TestClient.

        Args:
            client: TestClient ou AsyncClient
        """
        self.client = client

    def get_climate_data(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: Optional[str] = None,
    ):
        """
        Faz request para endpoint de dados climáticos.

        Args:
            latitude: Latitude em graus decimais
            longitude: Longitude em graus decimais
            start_date: Data inicial (YYYY-MM-DD)
            end_date: Data final (YYYY-MM-DD), opcional

        Returns:
            Response object
        """
        params = {
            "lat": latitude,
            "lon": longitude,
            "start_date": start_date,
        }
        if end_date:
            params["end_date"] = end_date

        return self.client.get("/api/climate/data", params=params)

    def calculate_eto(
        self, latitude: float, longitude: float, climate_data: list[dict]
    ):
        """
        Faz request para endpoint de cálculo de ETO.

        Args:
            latitude: Latitude em graus decimais
            longitude: Longitude em graus decimais
            climate_data: Lista de dados climáticos

        Returns:
            Response object
        """
        payload = {
            "latitude": latitude,
            "longitude": longitude,
            "climate_data": climate_data,
        }
        return self.client.post("/api/eto/calculate", json=payload)

    def assert_success(self, response, expected_status: int = 200):
        """
        Assert que response foi bem-sucedida.

        Args:
            response: Response object
            expected_status: Status code esperado
        """
        assert (
            response.status_code == expected_status
        ), f"Expected {expected_status}, got {response.status_code}: {response.text}"

    def assert_error(
        self,
        response,
        expected_status: int,
        expected_message: Optional[str] = None,
    ):
        """
        Assert que response retornou erro esperado.

        Args:
            response: Response object
            expected_status: Status code de erro esperado
            expected_message: Mensagem de erro esperada (opcional)
        """
        assert response.status_code == expected_status
        if expected_message:
            assert expected_message in response.text
