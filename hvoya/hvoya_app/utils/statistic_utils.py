# Этот модуль предназначен для работы со статистическими данными

from typing import Dict
from datetime import datetime, timedelta

from hvoya_app.models import GrowBoxHistoricalData, GrowBoxDateTime


def get_historical_data() -> Dict[str, list]:
    """
    Получает исторические данные за текуший и вчеращний день.
    Если не найдено данных за сегоднящний день, то они будут
    сгенерированы с нулевыми значениями вплоть до текущего часа
    фиксации реальных данных.
    """
    air_temperature, air_humidity, soil_humidity = [], [], []
    yesterday_air_temperature, yesterday_air_humidity, yesterday_soil_humidity = [], [], []

    historical_data = {
        'air_temperature': air_temperature,
        'air_humidity': air_humidity,
        'soil_humidity': soil_humidity,
        'yesterday_air_temperature': yesterday_air_temperature,
        'yesterday_air_humidity': yesterday_air_humidity,
        'yesterday_soil_humidity': yesterday_soil_humidity
    }
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    historical_data_queryset = GrowBoxHistoricalData.objects.select_related().filter(
        datetime__year__gte=yesterday.year,
        datetime__month__gte=yesterday.month,
        datetime__day__gte=yesterday.day
    ).order_by('id')

    for data in historical_data_queryset:

        if data.datetime.day == today.day:
            air_temperature.append(data.air_temperature)
            air_humidity.append(data.air_humidity)
            soil_humidity.append(data.soil_humidity)
        else:
            yesterday_air_temperature.append(data.air_temperature)
            yesterday_air_humidity.append(data.air_humidity)
            yesterday_soil_humidity.append(data.soil_humidity)

    if not all([air_temperature, air_humidity, soil_humidity]):
        fill_blank_data()

    return historical_data


def fill_blank_data() -> None:
    today = datetime.now()
    fake_datetime = today.replace(hour=0, minute=0, second=0, microsecond=0)

    while fake_datetime < today - timedelta(hours=1):
        new_growbox_datetime = GrowBoxDateTime(
            year=fake_datetime.year,
            month=fake_datetime.month,
            day=fake_datetime.day,
            hours=fake_datetime.hour
        )
        new_growbox_datetime.save()

        GrowBoxHistoricalData(
            air_temperature=0,
            air_humidity=0,
            soil_humidity=0,
            datetime=new_growbox_datetime
        ).save()
        fake_datetime += timedelta(hours=2)
