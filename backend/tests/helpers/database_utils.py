"""
Database Utils Helper

Helpers para operações de banco de dados em testes.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session


class DatabaseUtils:
    """Helpers para operações de banco em testes."""

    @staticmethod
    def create_postgis_extension(session: Session):
        """
        Cria extensão PostGIS (se não existir).

        Args:
            session: Sessão SQLAlchemy
        """
        session.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        session.commit()

    @staticmethod
    def truncate_table(session: Session, table_name: str):
        """
        Trunca tabela (remove todos os registros).

        Args:
            session: Sessão SQLAlchemy
            table_name: Nome da tabela
        """
        session.execute(text(f"TRUNCATE TABLE {table_name} CASCADE"))
        session.commit()

    @staticmethod
    def count_rows(session: Session, table_name: str) -> int:
        """
        Conta número de registros em tabela.

        Args:
            session: Sessão SQLAlchemy
            table_name: Nome da tabela

        Returns:
            Número de registros
        """
        result = session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        return result.scalar()

    @staticmethod
    def table_exists(session: Session, table_name: str) -> bool:
        """
        Verifica se tabela existe.

        Args:
            session: Sessão SQLAlchemy
            table_name: Nome da tabela

        Returns:
            True se tabela existe
        """
        result = session.execute(
            text(
                """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = :table_name
                )
            """
            ),
            {"table_name": table_name},
        )
        return result.scalar()

    @staticmethod
    def index_exists(session: Session, index_name: str) -> bool:
        """
        Verifica se índice existe.

        Args:
            session: Sessão SQLAlchemy
            index_name: Nome do índice

        Returns:
            True se índice existe
        """
        result = session.execute(
            text(
                """
                SELECT EXISTS (
                    SELECT FROM pg_indexes
                    WHERE indexname = :index_name
                )
            """
            ),
            {"index_name": index_name},
        )
        return result.scalar()
