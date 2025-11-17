"""
Security Tests - Input Validation

Tests: Validação de inputs maliciosos
"""

import pytest


@pytest.mark.integration
class TestInputValidation:
    """Testa validação de inputs."""

    def test_sql_injection_prevention(self, api_client):
        """Testa prevenção de SQL injection."""
        # TODO: Testar inputs maliciosos
        # Ex: lat="1'; DROP TABLE climate_data;--"
        assert True

    def test_xss_prevention(self, api_client):
        """Testa prevenção de XSS."""
        # TODO: Testar inputs com scripts
        assert True

    def test_coordinate_validation(self, api_client):
        """Testa validação de coordenadas maliciosas."""
        response = api_client.get(
            "/api/climate/data",
            params={"lat": 999, "lon": -999},  # Coordenadas inválidas
        )
        assert response.status_code == 422  # Validation error
