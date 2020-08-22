# Этот модуль предназначен для работы с данными получаемыми от сенсоров
from datetime import datetime

from django.core.exceptions import FieldError
from django.core.cache import cache

from hvoya_app.models import GrowBoxDateTime, GrowBoxHistoricalData
from .lighting_utils import get_lighting_data


def update_sensors_data(new_sensors_data: dict) -> None:
    """
    Фиксирует исторические данные для графиков.
    Кеширует свежие показания сенсоров как значения атрибутов класса GrowBox.
    """
    trigger_hours_values = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
    current_datetime = datetime.now()

    air_temperature = new_sensors_data.get('air_temperature')
    air_humidity = new_sensors_data.get('air_humidity')
    soil_humidity = new_sensors_data.get('soil_humidity')

    if not all([air_temperature, air_humidity, soil_humidity]):
        raise FieldError

    if current_datetime.hour in trigger_hours_values:
        last_growbox_datetime = GrowBoxDateTime.objects.order_by("-id").first()

        if not last_growbox_datetime or last_growbox_datetime.hours != current_datetime.hour:
            new_growbox_datetime = GrowBoxDateTime(
                year=current_datetime.year,
                month=current_datetime.month,
                day=current_datetime.day,
                hours=current_datetime.hour
            )
            new_growbox_datetime.save()
            GrowBoxHistoricalData(
                air_temperature=air_temperature,
                air_humidity=air_humidity,
                soil_humidity=soil_humidity,
                datetime=new_growbox_datetime
            ).save()

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
