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
    Фиксация исторических данных происходит только по четным часам.
    """
    current_datetime = datetime.now()
    check_even = current_datetime.hour == 0 or current_datetime.hour % 2 == 0
    air_temperature = new_sensors_data.get('air_temperature')
    air_humidity = new_sensors_data.get('air_humidity')
    soil_humidity = new_sensors_data.get('soil_humidity')

    if not all([air_temperature, air_humidity, soil_humidity]):
        raise FieldError

    if check_even:
        last_growbox_datetime = GrowBoxDateTime.objects.order_by("-id").first()
        check_hour = last_growbox_datetime.hours != current_datetime.hour
        check_hour_and_day = not check_hour and current_datetime.day != last_growbox_datetime.day

        if not last_growbox_datetime or check_hour or check_hour_and_day:
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
