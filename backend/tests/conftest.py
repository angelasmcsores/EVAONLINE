"""
Global Test Configuration - EVAonline

Este arquivo contém fixtures e configurações compartilhadas
por todos os tipos de testes.
"""

import os
import sys
from pathlib import Path
from typing import Generator

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

# Adicionar diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

# ============================================================================
# CONFIGURAÇÃO DE AMBIENTE
# ============================================================================


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Configura variáveis de ambiente para testes."""
    os.environ.update(
        {
            "ENVIRONMENT": "testing",
            "TESTING": "true",
            "POSTGRES_HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "POSTGRES_PORT": os.getenv("POSTGRES_PORT", "5432"),
            "POSTGRES_USER": os.getenv("POSTGRES_USER", "evaonline"),
            "POSTGRES_PASSWORD": os.getenv(
                "POSTGRES_PASSWORD", "test_password"
            ),
            "POSTGRES_DB": os.getenv("POSTGRES_DB", "evaonline_test"),
            "REDIS_HOST": os.getenv("REDIS_HOST", "localhost"),
            "REDIS_PORT": os.getenv("REDIS_PORT", "6379"),
            "REDIS_DB": "1",  # DB separado para testes
            "LOG_LEVEL": "WARNING",  # Reduzir logs em testes
        }
    )


# ============================================================================
# FIXTURES DE DATABASE (SYNC)
# ============================================================================


@pytest.fixture(scope="session")
def database_url() -> str:
    """URL de conexão ao banco de dados de teste."""
    return (
        f"postgresql://{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:"
        f"{os.getenv('POSTGRES_PORT')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )


@pytest.fixture(scope="session")
def engine(database_url: str):
    """Engine SQLAlchemy para testes (session-scoped)."""
    engine = create_engine(database_url, echo=False)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine) -> Generator[Session, None, None]:
    """
    Sessão de banco de dados com rollback automático.

    Cada teste roda em uma transação que é revertida ao final.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def clean_database(engine):
    """
    Limpa todas as tabelas antes de cada teste.

    Útil para testes de integração que precisam de um banco limpo.
    """
    with engine.connect() as conn:
        # Desabilitar constraints temporariamente
        conn.execute(text("SET session_replication_role = 'replica'"))

        # Listar todas as tabelas
        result = conn.execute(
            text(
                """
            SELECT tablename FROM pg_tables
            WHERE schemaname = 'public'
        """
            )
        )
        tables = [row[0] for row in result]

        # Truncar cada tabela
        for table in tables:
            if table != "alembic_version":
                conn.execute(text(f"TRUNCATE TABLE {table} CASCADE"))

        # Reabilitar constraints
        conn.execute(text("SET session_replication_role = 'origin'"))
        conn.commit()


# ============================================================================
# FIXTURES DE DATABASE (ASYNC)
# ============================================================================


@pytest.fixture(scope="session")
def async_database_url(database_url: str) -> str:
    """URL de conexão assíncrona ao banco de dados."""
    return database_url.replace("postgresql://", "postgresql+asyncpg://")


@pytest.fixture(scope="session")
async def async_engine(async_database_url: str):
    """Engine assíncrono SQLAlchemy para testes."""
    engine = create_async_engine(async_database_url, echo=False)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def async_db_session(async_engine):
    """Sessão assíncrona de banco de dados com rollback automático."""
    async with async_engine.connect() as connection:
        async with connection.begin():
            AsyncSessionLocal = sessionmaker(
                bind=connection,
                class_=AsyncSession,
                expire_on_commit=False,
            )
            session = AsyncSessionLocal()

            yield session

            # Cleanup é feito automaticamente pelo context manager


# ============================================================================
# FIXTURES DE REDIS
# ============================================================================


@pytest.fixture(scope="session")
def redis_url() -> str:
    """URL de conexão ao Redis de teste."""
    password = os.getenv("REDIS_PASSWORD", "")
    if password:
        return (
            f"redis://:{password}@"
            f"{os.getenv('REDIS_HOST')}:"
            f"{os.getenv('REDIS_PORT')}/"
            f"{os.getenv('REDIS_DB')}"
        )
    return (
        f"redis://{os.getenv('REDIS_HOST')}:"
        f"{os.getenv('REDIS_PORT')}/"
        f"{os.getenv('REDIS_DB')}"
    )


@pytest.fixture(scope="function")
def redis_client(redis_url: str):
    """Cliente Redis para testes com limpeza automática."""
    import redis

    client = redis.from_url(redis_url, decode_responses=True)

    # Limpar DB antes do teste
    client.flushdb()

    yield client

    # Limpar DB depois do teste
    client.flushdb()
    client.close()


# ============================================================================
# FIXTURES DE API CLIENT
# ============================================================================


@pytest.fixture(scope="function")
def api_client():
    """
    Cliente HTTP para testes de API.

    Usa TestClient do FastAPI.
    """
    from fastapi.testclient import TestClient

    from backend.main import app

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
async def async_api_client():
    """Cliente HTTP assíncrono para testes de API."""
    from httpx import ASGITransport, AsyncClient

    from backend.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        yield client


# ============================================================================
# FIXTURES DE DADOS DE TESTE
# ============================================================================


@pytest.fixture
def sample_coordinates():
    """Coordenadas de teste (Jaú, SP)."""
    return {"latitude": -22.25, "longitude": -48.5, "elevation": 580}


@pytest.fixture
def sample_date_range():
    """Período de teste (90 dias)."""
    from datetime import datetime

    return {
        "start_date": datetime(2025, 7, 1),
        "end_date": datetime(2025, 9, 28),
    }


@pytest.fixture
def sample_climate_data():
    """
    Dados climáticos de exemplo para testes.

    Retorna dict com dados completos para cálculo ETO.
    """
    from datetime import date

    return {
        "latitude": -22.25,
        "longitude": -48.5,
        "elevation": 580,
        "date": date(2025, 7, 1),
        "T2M_MAX": 32.5,
        "T2M_MIN": 18.2,
        "T2M_MEAN": 25.4,
        "RH2M": 65.0,
        "WS2M": 2.5,
        "PRECTOTCORR": 0.0,
        "ALLSKY_SFC_SW_DWN": 20.5,
    }


@pytest.fixture
def sample_eto_request():
    """Request payload de exemplo para endpoint ETO."""
    return {
        "lat": -22.25,
        "lng": -48.5,
        "start_date": "2025-07-01",
        "end_date": "2025-07-31",
        "elevation": 580,
    }


@pytest.fixture
def mock_nasa_power_response():
    """Mock de resposta da API NASA POWER."""
    return {
        "header": {
            "title": "NASA/POWER CERES/MERRA2 Native Resolution Daily Data",
            "api_version": "v2.5.4",
            "fill_value": -999.0,
        },
        "messages": [],
        "parameters": {
            "T2M_MAX": {
                "20250701": 32.5,
                "20250702": 31.8,
                "20250703": 33.2,
            },
            "T2M_MIN": {
                "20250701": 18.2,
                "20250702": 17.5,
                "20250703": 19.1,
            },
            "RH2M": {
                "20250701": 65.0,
                "20250702": 68.0,
                "20250703": 62.0,
            },
        },
        "geometry": {
            "type": "Point",
            "coordinates": [-48.5, -22.25],
        },
    }


# ============================================================================
# HOOKS DO PYTEST
# ============================================================================


def pytest_configure(config):
    """Configuração executada antes de rodar os testes."""
    # Adicionar marcadores customizados
    config.addinivalue_line(
        "markers",
        "unit: Marca testes unitários",
    )
    config.addinivalue_line(
        "markers",
        "integration: Marca testes de integração",
    )


def pytest_collection_modifyitems(config, items):
    """Modifica a coleção de testes antes da execução."""
    # Adicionar marcador 'unit' automaticamente para testes em unit/
    for item in items:
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
