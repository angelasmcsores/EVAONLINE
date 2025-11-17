# backend/tests/fixtures/factories/climate_data_factory.py
"""
Climate Data Factory - Using factory_boy with Faker

Factory para criação de objetos ClimateData para testes.
Usa factory_boy para DRY factories e Faker para dados realistas.
"""
from factory import Factory, Faker, LazyAttribute  # type: ignore
from datetime import datetime, timedelta


class ClimateDataFactory(Factory):
    """
    Factory para criar dados climáticos de teste usando factory_boy.

    Uso básico:
        data = ClimateDataFactory()
        batch = ClimateDataFactory.build_batch(90)
        custom = ClimateDataFactory(latitude=-15.0, temperature_max=35.0)
    """

    class Meta:
        model = dict

    # Localização (defaults para Jaú, SP)
    latitude = -22.25
    longitude = -48.5
    elevation = 580

    # Data
    date = Faker("date_this_year")

    # Temperaturas (°C) - Faker gera valores realistas
    temperature_max = Faker(
        "pyfloat", min_value=20.0, max_value=40.0, right_digits=1
    )
    temperature_min = Faker(
        "pyfloat", min_value=10.0, max_value=25.0, right_digits=1
    )

    @LazyAttribute
    def temperature_avg(self):
        """Calcula temperatura média automaticamente."""
        return round((self.temperature_max + self.temperature_min) / 2, 1)

    # Umidade (%)
    humidity = Faker("pyfloat", min_value=40.0, max_value=90.0, right_digits=1)

    # Vento (m/s)
    wind_speed = Faker("pyfloat", min_value=0.5, max_value=8.0, right_digits=1)

    # Radiação solar (MJ/m²/dia)
    solar_radiation = Faker(
        "pyfloat", min_value=15.0, max_value=30.0, right_digits=1
    )

    # Precipitação (mm)
    precipitation = Faker(
        "pyfloat", min_value=0.0, max_value=50.0, right_digits=1
    )

    # Fonte de dados
    source = "NASA_POWER"


class SummerDayFactory(ClimateDataFactory):
    """Factory para dias de verão típicos."""

    temperature_max = 32.5
    temperature_min = 18.2
    humidity = 65.0
    wind_speed = 2.5
    solar_radiation = 20.5
    precipitation = 0.0

    @LazyAttribute
    def temperature_avg(self):
        return 25.4


class WinterDayFactory(ClimateDataFactory):
    """Factory para dias de inverno típicos."""

    temperature_max = 22.0
    temperature_min = 10.0
    humidity = 80.0
    wind_speed = 1.5
    solar_radiation = 15.0
    precipitation = 0.0

    @LazyAttribute
    def temperature_avg(self):
        return 16.0


class RainyDayFactory(ClimateDataFactory):
    """Factory para dias chuvosos."""

    temperature_max = 25.0
    temperature_min = 16.0
    humidity = 85.0
    wind_speed = 3.5
    solar_radiation = 12.0
    precipitation = Faker(
        "pyfloat", min_value=10.0, max_value=80.0, right_digits=1
    )

    @LazyAttribute
    def temperature_avg(self):
        return 20.5


# =============================================================================
# HELPER FUNCTIONS (compatibilidade com código antigo)
# =============================================================================


def create_sample_data(**kwargs):
    """
    Cria dados climáticos de exemplo (compatibilidade com código antigo).

    Args:
        **kwargs: Parâmetros para override

    Returns:
        dict: Dados climáticos
    """
    return ClimateDataFactory(**kwargs)


def create_90_day_series(start_date=None, **kwargs):
    """
    Cria série de 90 dias de dados climáticos.

    Args:
        start_date: Data inicial (default: 2025-07-01)
        **kwargs: Parâmetros adicionais

    Returns:
        list[dict]: Lista com 90 dicionários de dados climáticos
    """
    if start_date is None:
        start_date = datetime(2025, 7, 1).date()

    return [
        ClimateDataFactory(date=start_date + timedelta(days=i), **kwargs)
        for i in range(90)
    ]


def create_batch_with_sequence(size=10, start_date=None, **kwargs):
    """
    Cria batch com datas sequenciais.

    Args:
        size: Número de registros
        start_date: Data inicial
        **kwargs: Parâmetros adicionais

    Returns:
        list[dict]: Lista de dicionários
    """
    if start_date is None:
        start_date = datetime(2025, 7, 1).date()

    return [
        ClimateDataFactory(date=start_date + timedelta(days=i), **kwargs)
        for i in range(size)
    ]
