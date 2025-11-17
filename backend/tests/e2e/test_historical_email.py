"""
End-to-End Tests - Historical Email Flow

Tests: Fluxo completo de 90 dias (historical_email mode)
"""

import pytest


@pytest.mark.e2e
@pytest.mark.requires_docker
@pytest.mark.requires_postgres
@pytest.mark.requires_apis
@pytest.mark.slow
class TestHistoricalEmailFlow:
    """Testa fluxo completo historical_email (90 dias)."""

    def test_complete_90_day_flow(self):
        """Testa fluxo completo de 90 dias."""
        # TODO: Implementar teste E2E completo
        # 1. Request com coordenadas
        # 2. Chamada NASA Power
        # 3. Cálculo de ETO
        # 4. Armazenamento em PostgreSQL
        # 5. Geração de relatório
        assert True
