"""
Station Factory - Using factory_boy

Factory para criação de estações meteorológicas para testes.
"""

import factory  # type: ignore
from factory import Faker, Sequence  # type: ignore


class MeteorologicalStationFactory(factory.Factory):  # type: ignore
    """Factory para criar estações meteorológicas usando factory_boy."""

    class Meta:
        model = dict

    # ID sequencial (TEST001, TEST002, ...)
    station_id = Sequence(lambda n: f"TEST{n:03d}")  # type: ignore

    # Nome gerado automaticamente
    name = Faker("city")

    # Coordenadas (defaults para Brasil)
    latitude = Faker("latitude")
    longitude = Faker("longitude")

    # Elevação realista (0-3000m)
    elevation = Faker("pyfloat", min_value=0, max_value=3000, right_digits=1)

    # País e estado
    country = "BR"
    state = "SP"


class BrazilStationFactory(MeteorologicalStationFactory):  # type: ignore
    """Factory para estações no Brasil com coordenadas válidas."""

    # Coordenadas dentro do Brasil (-33 to 5 lat, -73 to -34 lon)
    latitude = Faker("pyfloat", min_value=-33.0, max_value=5.0, right_digits=4)
    longitude = Faker(
        "pyfloat", min_value=-73.0, max_value=-34.0, right_digits=4
    )


# =============================================================================
# HELPER FUNCTIONS (compatibilidade com código antigo)
# =============================================================================


def create_station(
    station_id: str = "TEST001",
    name: str = "Estação Teste",
    latitude: float = -22.25,
    longitude: float = -48.5,
    elevation: float = 580.0,
    country: str = "BR",
    state: str = "SP",
) -> dict:
    """
    Cria dados de estação meteorológica (compatibilidade).

    Args:
        station_id: ID único da estação
        name: Nome da estação
        latitude: Latitude em graus decimais
        longitude: Longitude em graus decimais
        elevation: Elevação em metros
        country: Código do país (ISO 3166-1 alpha-2)
        state: Estado/província

    Returns:
        Dicionário com dados da estação
    """
    return {
        "station_id": station_id,
        "name": name,
        "latitude": latitude,
        "longitude": longitude,
        "elevation": elevation,
        "country": country,
        "state": state,
    }


def create_brazil_stations() -> list[dict]:
    """
    Cria lista de estações meteorológicas no Brasil.

    Returns:
        Lista com dados de várias estações
    """
    return [
        create_station(
            station_id="SP001",
            name="Jaú",
            latitude=-22.25,
            longitude=-48.5,
            elevation=580.0,
            state="SP",
        ),
        create_station(
            station_id="SP002",
            name="São Paulo",
            latitude=-23.55,
            longitude=-46.63,
            elevation=760.0,
            state="SP",
        ),
        create_station(
            station_id="RJ001",
            name="Rio de Janeiro",
            latitude=-22.91,
            longitude=-43.17,
            elevation=10.0,
            state="RJ",
        ),
    ]


# Alias StationFactory para compatibilidade
class StationFactory:
    """Classe legacy para compatibilidade."""

    create_station = staticmethod(create_station)
    create_brazil_stations = staticmethod(create_brazil_stations)
