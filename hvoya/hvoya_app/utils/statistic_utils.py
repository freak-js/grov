# Этот модуль предназначен для работы со статистическими данными

from typing import Dict
from datetime import datetime, timedelta

from hvoya_app.models import GrowBoxHistoricalData


def get_historical_data() -> Dict[str, list]:
    """
    Получает исторические данные за текуший и вчеращний день.
    Если не найдено данных за сегоднящний день, то они будут
    сгенерированы с нулевыми значениями вплоть до текущего часа
    фиксации реальных данных.
    """
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    historical_data = GrowBoxHistoricalData.objects.select_related().filter(
        datetime__year__gte=yesterday.year,
        datetime__month__gte=yesterday.month,
        datetime__day__gte=yesterday.day
    ).order_by('id')

    today_data = fill_blank([data for data in historical_data if data.datetime.day == today.day])
    yesterday_data = fill_blank([data for data in historical_data if data.datetime.day != today.day], yesterday=True)
    return {**today_data, **yesterday_data}


def fill_blank(historical_data: list, yesterday: bool = False) -> dict:
    """
    Получает список с объектами исторических данных.
    Итерируется по каждому объекту и проверяет есть
    ли промежутки без данных от сенсоров, если есть,
    то заполняет их нулевыми значениями.
    """
    current_hour = datetime.now().hour
    measurement_checkpoints = [hour for hour in range(0, current_hour - 1, 2)]

    if not historical_data:

        ed = [0 for _ in measurement_checkpoints]

        if yesterday:
            return {'yesterday_air_temperature': ed, 'yesterday_air_humidity': ed, 'yesterday_soil_humidity': ed}
        return {'air_temperature': ed, 'air_humidity': ed, 'soil_humidity': ed}

    if yesterday:
        result = {'yesterday_air_temperature': [], 'yesterday_air_humidity': [], 'yesterday_soil_humidity': []}
    else:
        result = {'air_temperature': [], 'air_humidity': [], 'soil_humidity': []}
    historical_data_hours = [data.datetime.hours for data in historical_data]

    for hour in measurement_checkpoints:

        if hour in historical_data_hours:
            data = historical_data.pop(0)
            result['yesterday_air_temperature' if yesterday else 'air_temperature'].append(data.air_temperature)
            result['yesterday_air_humidity' if yesterday else 'air_humidity'].append(data.air_humidity)
            result['yesterday_soil_humidity' if yesterday else 'soil_humidity'].append(data.soil_humidity)
            continue

        result['yesterday_air_temperature' if yesterday else 'air_temperature'].append(0)
        result['yesterday_air_humidity' if yesterday else 'air_humidity'].append(0)
        result['yesterday_soil_humidity' if yesterday else 'soil_humidity'].append(0)

    return result
