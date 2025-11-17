"""
Geometry Factory - Using factory_boy

Factory para criação de geometrias PostGIS para testes.
"""

import factory  # type: ignore
from factory import Faker, LazyAttribute  # type: ignore
import math


class PointFactory(factory.Factory):  # type: ignore
    """Factory para criar geometrias POINT usando factory_boy."""

    class Meta:
        model = dict

    # Coordenadas (defaults para Jaú, SP)
    latitude = -22.25
    longitude = -48.5
    srid = 4326

    @LazyAttribute  # type: ignore
    def wkt(self) -> str:
        """Gera WKT do POINT."""
        return f"POINT({self.longitude} {self.latitude})"

    @LazyAttribute  # type: ignore
    def ewkt(self) -> str:
        """Gera EWKT (Extended WKT) com SRID."""
        return f"SRID={self.srid};POINT({self.longitude} {self.latitude})"


class RandomPointFactory(PointFactory):  # type: ignore
    """Factory para criar POINTs com coordenadas aleatórias."""

    latitude = Faker("latitude")
    longitude = Faker("longitude")


# =============================================================================
# HELPER FUNCTIONS (compatibilidade com código antigo)
# =============================================================================


def create_point(latitude: float = -22.25, longitude: float = -48.5) -> str:
    """
    Cria WKT de POINT (compatibilidade).

    Args:
        latitude: Latitude em graus decimais
        longitude: Longitude em graus decimais

    Returns:
        String WKT do POINT
    """
    return f"POINT({longitude} {latitude})"


def create_point_ewkt(
    latitude: float = -22.25, longitude: float = -48.5, srid: int = 4326
) -> str:
    """
    Cria EWKT (Extended WKT) de POINT com SRID.

    Args:
        latitude: Latitude em graus decimais
        longitude: Longitude em graus decimais
        srid: Sistema de referência espacial (default: 4326 - WGS84)

    Returns:
        String EWKT do POINT
    """
    return f"SRID={srid};POINT({longitude} {latitude})"


def create_polygon_brazil() -> str:
    """
    Cria WKT de POLYGON representando área no Brasil.

    Returns:
        String WKT do POLYGON
    """
    return (
        "POLYGON(("
        "-48.6 -22.3, "
        "-48.4 -22.3, "
        "-48.4 -22.2, "
        "-48.6 -22.2, "
        "-48.6 -22.3"
        "))"
    )


def create_circle_wkt(
    center_lat: float, center_lon: float, radius_meters: float
) -> str:
    """
    Cria aproximação de círculo usando POLYGON (32 pontos).

    Args:
        center_lat: Latitude do centro
        center_lon: Longitude do centro
        radius_meters: Raio em metros

    Returns:
        String WKT do POLYGON circular
    """
    # Aproximação: 1 grau ≈ 111km
    radius_degrees = radius_meters / 111000

    points = []
    for i in range(33):  # 32 pontos + fechar o polígono
        angle = (i * 360 / 32) * math.pi / 180
        lat = center_lat + (radius_degrees * math.sin(angle))
        lon = center_lon + (radius_degrees * math.cos(angle))
        points.append(f"{lon} {lat}")

    return f"POLYGON(({', '.join(points)}))"


# Alias GeometryFactory para compatibilidade
class GeometryFactory:
    """Classe legacy para compatibilidade."""

    create_point = staticmethod(create_point)
    create_point_ewkt = staticmethod(create_point_ewkt)
    create_polygon_brazil = staticmethod(create_polygon_brazil)
    create_circle_wkt = staticmethod(create_circle_wkt)
