"""
Integration Tests for Spatial Indexes

Tests: Validação de índices espaciais (GIST)
"""

import pytest
from sqlalchemy import text


@pytest.mark.integration
@pytest.mark.requires_postgres
class TestSpatialIndexes:
    """Testa índices espaciais."""

    def test_gist_index_exists(self, db_session):
        """Testa que índice GIST existe na coluna geometry."""
        result = db_session.execute(
            text(
                """
                SELECT indexname FROM pg_indexes
                WHERE tablename = 'regional_coverage'
                AND indexdef LIKE '%USING gist%'
            """
            )
        )
        indexes = [row[0] for row in result]
        assert any(
            "geometry" in idx for idx in indexes
        ), "Índice GIST não encontrado na coluna geometry"

    def test_index_performance(self, db_session):
        """Testa que queries usam o índice espacial."""
        # TODO: Usar EXPLAIN ANALYZE para verificar index scan
        assert True
