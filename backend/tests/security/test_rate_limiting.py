"""
Security Tests - Rate Limiting

Tests: Proteção contra abuse
"""

import pytest


@pytest.mark.integration
@pytest.mark.requires_redis
class TestRateLimitingSecurity:
    """Testa rate limiting."""

    def test_rate_limit_enforcement(self, api_client):
        """Testa enforcement de rate limit."""
        # TODO: Fazer 100 requests e verificar 429 Too Many Requests
        assert True
