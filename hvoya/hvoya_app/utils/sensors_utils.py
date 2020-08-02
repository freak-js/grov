# Этот модуль предназначен для работы с данными получаемыми от сенсоров

from django.core.exceptions import FieldError
from django.core.cache import cache

from .lighting_utils import get_lighting_data


def update_sensors_data(new_sensors_data: dict) -> None:
    """
    Кеширует свежие показания сенсоров как значения атрибутов класса GrowBox.
    """
    air_temperature = new_sensors_data.get('air_temperature')
    air_humidity = new_sensors_data.get('air_humidity')
    soil_humidity = new_sensors_data.get('soil_humidity')

    if not all([air_temperature, air_humidity, soil_humidity]):
        raise FieldError

    cache.set('air_temperature', air_temperature)
    cache.set('air_humidity', air_humidity)
    cache.set('soil_humidity', soil_humidity)


def give_sensors_cashed_data() -> dict:
    """
    Отдает словарь с кешированными данными сенсоров.
    """
    air_temperature = cache.get('air_temperature')
    air_humidity = cache.get('air_humidity')
    soil_humidity = cache.get('soil_humidity')
    sensors_cashed_data = {
        'air_temperature': air_temperature,
        'air_humidity': air_humidity,
        'soil_humidity': soil_humidity,
        'lamp_time': get_lighting_data()['time_value']
    }
    return sensors_cashed_data
