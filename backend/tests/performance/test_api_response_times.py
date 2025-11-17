"""
Performance Tests - API Response Times

Tests: Benchmark de tempo de resposta de endpoints
"""

import pytest


@pytest.mark.performance
@pytest.mark.requires_docker
class TestAPIResponseTimes:
    """Testa performance de endpoints."""

    def test_climate_endpoint_response_time(self, api_client):
        """Testa tempo de resposta de /api/climate."""
        # TODO: Benchmark de endpoint
        # Target: < 500ms (p95)
        assert True
