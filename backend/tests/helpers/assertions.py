"""
Custom Assertions

Custom assertions para testes mais expressivos.
"""


class CustomAssertions:
    """Custom assertions para testes."""

    @staticmethod
    def assert_coordinates_valid(latitude: float, longitude: float):
        """
        Assert que coordenadas são válidas.

        Args:
            latitude: Latitude em graus decimais
            longitude: Longitude em graus decimais
        """
        assert (
            -90 <= latitude <= 90
        ), f"Latitude {latitude} fora do range [-90, 90]"
        assert (
            -180 <= longitude <= 180
        ), f"Longitude {longitude} fora do range [-180, 180]"

    @staticmethod
    def assert_temperature_valid(
        temperature: float, min_temp: float = -100, max_temp: float = 100
    ):
        """
        Assert que temperatura é válida.

        Args:
            temperature: Temperatura em °C
            min_temp: Temperatura mínima válida
            max_temp: Temperatura máxima válida
        """
        assert (
            min_temp <= temperature <= max_temp
        ), f"Temperatura {temperature} fora do range [{min_temp}, {max_temp}]"

    @staticmethod
    def assert_dict_contains_keys(data: dict, required_keys: list[str]):
        """
        Assert que dicionário contém chaves obrigatórias.

        Args:
            data: Dicionário para verificar
            required_keys: Lista de chaves obrigatórias
        """
        missing_keys = [key for key in required_keys if key not in data]
        assert not missing_keys, f"Chaves faltando: {missing_keys}"

    @staticmethod
    def assert_climate_data_valid(data: dict):
        """
        Assert que dados climáticos são válidos.

        Args:
            data: Dicionário com dados climáticos
        """
        required_keys = [
            "latitude",
            "longitude",
            "date",
            "temperature_max",
            "temperature_min",
        ]
        CustomAssertions.assert_dict_contains_keys(data, required_keys)

        CustomAssertions.assert_coordinates_valid(
            data["latitude"], data["longitude"]
        )

        CustomAssertions.assert_temperature_valid(data["temperature_max"])
        CustomAssertions.assert_temperature_valid(data["temperature_min"])

        # Tmax >= Tmin
        assert (
            data["temperature_max"] >= data["temperature_min"]
        ), "Tmax deve ser >= Tmin"

    @staticmethod
    def assert_eto_value_valid(eto: float):
        """
        Assert que valor de ETO é válido.

        Args:
            eto: Evapotranspiração (mm/dia)
        """
        assert 0 <= eto <= 20, f"ETO {eto} fora do range [0, 20] mm/dia"
