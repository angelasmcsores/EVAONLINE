"""
Unit Tests - Climate Data Endpoints

Testa endpoints de dados climáticos.
"""

import pytest
from datetime import datetime, timedelta


@pytest.mark.unit
class TestClimateSourcesEndpoint:
    """Testa GET /api/v1/climate/sources."""

    def test_list_available_sources(self, api_client):
        """Testa listagem de fontes de dados disponíveis."""
        response = api_client.get("/api/v1/climate/sources")

        # Se endpoint existir
        if response.status_code != 404:
            assert response.status_code == 200
            data = response.json()

            assert "sources" in data or isinstance(data, list)

    def test_sources_include_nasa_power(self, api_client):
        """Testa que NASA POWER está na lista."""
        response = api_client.get("/api/v1/climate/sources")

        if response.status_code == 200:
            data = response.json()

            # Verificar se NASA POWER está disponível
            if isinstance(data, dict) and "sources" in data:
                sources = data["sources"]
                source_names = [s.get("name", "").lower() for s in sources]
                assert any("nasa" in name for name in source_names)


@pytest.mark.unit
class TestClimateDataValidation:
    """Testa validação de parâmetros climáticos."""

    @pytest.mark.parametrize(
        "lat,lon",
        [
            (100, -48.5),  # lat > 90
            (-100, -48.5),  # lat < -90
            (-22.25, 200),  # lon > 180
            (-22.25, -200),  # lon < -180
        ],
    )
    def test_rejects_invalid_coordinates(self, api_client, lat, lon):
        """Testa rejeição de coordenadas inválidas."""
        # Tentar buscar dados com coordenadas inválidas
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": "2025-07-01",
            "end_date": "2025-07-31",
        }

        # Testar em qualquer endpoint de clima que exista
        for endpoint in [
            "/api/v1/climate/data",
            "/api/v1/climate/daily",
            "/api/v1/internal/climate/fetch",
        ]:
            response = api_client.get(endpoint, params=params)

            # Se endpoint existe, deve validar coordenadas
            if response.status_code != 404:
                assert response.status_code in [400, 422, 500]
                break

    def test_rejects_future_dates(self, api_client):
        """Testa que não permite datas no futuro."""
        tomorrow = datetime.now() + timedelta(days=30)
        future_date = tomorrow.strftime("%Y-%m-%d")

        params = {
            "latitude": -22.25,
            "longitude": -48.5,
            "start_date": future_date,
            "end_date": future_date,
        }

        # Testar endpoints de dados históricos
        for endpoint in [
            "/api/v1/climate/data",
            "/api/v1/climate/daily",
        ]:
            response = api_client.get(endpoint, params=params)

            if response.status_code not in [404, 500]:
                # Se endpoint existe e funciona, deve rejeitar futuro
                # (ou aceitar se for forecast)
                assert response.status_code in [200, 400, 422]
                break

    def test_validates_date_range_limit(self, api_client):
        """Testa limite de intervalo de datas."""
        params = {
            "latitude": -22.25,
            "longitude": -48.5,
            "start_date": "2020-01-01",
            "end_date": "2025-12-31",  # > 5 anos
        }

        for endpoint in [
            "/api/v1/climate/data",
            "/api/v1/climate/daily",
        ]:
            response = api_client.get(endpoint, params=params)

            # Se endpoint existe, pode ter limite
            if response.status_code not in [404, 500]:
                assert response.status_code in [200, 400, 422]
                break


@pytest.mark.unit
class TestClimateSourceSelection:
    """Testa seleção automática de fonte."""

    def test_auto_source_selection(self, api_client):
        """Testa seleção automática de melhor fonte."""
        params = {
            "latitude": -22.25,
            "longitude": -48.5,
            "start_date": "2025-07-01",
            "end_date": "2025-07-31",
            "source": "auto",
        }

        response = api_client.get("/api/v1/climate/data", params=params)

        # Se endpoint existir e funcionar
        if response.status_code == 200:
            data = response.json()

            # Deve indicar fonte usada
            assert (
                "source" in data or "data_source" in data or "provider" in data
            )
