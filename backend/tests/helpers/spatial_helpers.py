"""
Spatial Helpers

Helpers para operações geoespaciais em testes.
"""

import math
from sqlalchemy import text
from sqlalchemy.orm import Session


class SpatialHelpers:
    """Helpers para testes com PostGIS."""

    @staticmethod
    def create_point(
        session: Session,
        table: str,
        latitude: float,
        longitude: float,
        srid: int = 4326,
    ) -> int:
        """
        Insere POINT em tabela PostGIS.

        Args:
            session: Sessão SQLAlchemy
            table: Nome da tabela
            latitude: Latitude em graus decimais
            longitude: Longitude em graus decimais
            srid: Sistema de referência espacial

        Returns:
            ID do registro inserido
        """
        result = session.execute(
            text(
                f"""
                INSERT INTO {table} (geometry)
                VALUES (ST_SetSRID(ST_MakePoint(:lon, :lat), :srid))
                RETURNING id
            """
            ),
            {"lon": longitude, "lat": latitude, "srid": srid},
        )
        session.commit()
        return result.scalar()

    @staticmethod
    def calculate_distance_meters(
        lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """
        Calcula distância aproximada entre dois pontos (Haversine).

        Args:
            lat1: Latitude do ponto 1
            lon1: Longitude do ponto 1
            lat2: Latitude do ponto 2
            lon2: Longitude do ponto 2

        Returns:
            Distância em metros
        """
        R = 6371000  # Raio da Terra em metros

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1_rad)
            * math.cos(lat2_rad)
            * math.sin(delta_lon / 2) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    @staticmethod
    def find_points_within_radius(
        session: Session,
        table: str,
        center_lat: float,
        center_lon: float,
        radius_meters: float,
    ) -> list:
        """
        Busca pontos dentro de raio usando ST_DWithin.

        Args:
            session: Sessão SQLAlchemy
            table: Nome da tabela
            center_lat: Latitude do centro
            center_lon: Longitude do centro
            radius_meters: Raio em metros

        Returns:
            Lista de registros dentro do raio
        """
        result = session.execute(
            text(
                f"""
                SELECT id, ST_AsText(geometry) as geom
                FROM {table}
                WHERE ST_DWithin(
                    geometry::geography,
                    ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
                    :radius
                )
            """
            ),
            {"lat": center_lat, "lon": center_lon, "radius": radius_meters},
        )
        return result.fetchall()

    @staticmethod
    def assert_geometry_valid(session: Session, table: str, row_id: int):
        """
        Assert que geometria é válida.

        Args:
            session: Sessão SQLAlchemy
            table: Nome da tabela
            row_id: ID do registro
        """
        result = session.execute(
            text(
                f"""
                SELECT ST_IsValid(geometry)
                FROM {table}
                WHERE id = :row_id
            """
            ),
            {"row_id": row_id},
        )
        is_valid = result.scalar()
        assert is_valid, f"Geometria inválida no registro {row_id}"

    @staticmethod
    def assert_srid_correct(
        session: Session, table: str, row_id: int, expected_srid: int = 4326
    ):
        """
        Assert que SRID está correto.

        Args:
            session: Sessão SQLAlchemy
            table: Nome da tabela
            row_id: ID do registro
            expected_srid: SRID esperado (default: 4326 - WGS84)
        """
        result = session.execute(
            text(
                f"""
                SELECT ST_SRID(geometry)
                FROM {table}
                WHERE id = :row_id
            """
            ),
            {"row_id": row_id},
        )
        actual_srid = result.scalar()
        assert (
            actual_srid == expected_srid
        ), f"SRID incorreto: esperado {expected_srid}, obtido {actual_srid}"
