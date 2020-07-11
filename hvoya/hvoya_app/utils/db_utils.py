# Этот модуль предназначен для утилит получения данных из БД и классов находящихся в моделях


from datetime import datetime, timedelta
from typing import Dict

from hvoya_app.models import GrowBoxHistoricalData, GrowBox


def get_historical_data() -> Dict[str, list]:
    """
    Получает исторические данные за текуший и вчеращний день.
    :return: словарь формата {'key': list}
    """
    historical_data: dict = {
        'air_temperature': [],
        'air_humidity': [],
        'soil_humidity': [],
        'yesterday_air_temperature': [],
        'yesterday_air_humidity': [],
        'yesterday_soil_humidity': []
    }
    today: datetime = datetime.now()
    yesterday: datetime = today - timedelta(days=1)
    historical_data_queryset = GrowBoxHistoricalData.objects.select_related().filter(
        datetime__year__gte=yesterday.year,
        datetime__month__gte=yesterday.month,
        datetime__day__gte=yesterday.day
    ).order_by('id')

    for data in historical_data_queryset:

        if data.datetime.day == today.day:
            historical_data['air_temperature'].append(data.air_temperature)
            historical_data['air_humidity'].append(data.air_humidity)
            historical_data['soil_humidity'].append(data.soil_humidity)
        else:
            historical_data['yesterday_air_temperature'].append(data.air_temperature)
            historical_data['yesterday_air_humidity'].append(data.air_humidity)
            historical_data['yesterday_soil_humidity'].append(data.soil_humidity)

    return historical_data


def get_current_data():
    """

    :return: словарь формата {'key': int}
    """
    current_data: dict = {
        'air_temperature': GrowBox.CURRENT_AIR_TEMPERATURE,
        'air_humidity': GrowBox.CURRENT_AIR_HUMIDITY,
        'soil_humidity': GrowBox.CURRENT_SOIL_HUMIDITY
    }
    return current_data
