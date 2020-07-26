# Этот модуль предназначен для утилит получения данных из БД и классов находящихся в моделях


from datetime import datetime, timedelta
from typing import Dict

from django.http import HttpRequest
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.core.cache import cache

from hvoya_app.models import GrowBoxHistoricalData, CashedGrowBoxSettings, GrowBoxSettings


# БЛОК ОБРАБОТКИ СТАТИСТИЧЕСКИХ ДАННЫХ


def get_historical_data() -> Dict[str, list]:
    """
    Получает исторические данные за текуший и вчеращний день.
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


# БЛОК РАБОТЫ С НАСТРОЙКАМИ ГРОУБОКСА


def get_settings_data() -> Dict[str, int]:
    """
    Возвращает кеш настроек гроубокса в формате словаря.
    """
    minimal_soil_humidity = cache.get('minimal_soil_humidity')
    lamp_on_time = cache.get('lamp_on_time')
    lamp_off_time = cache.get('lamp_off_time')
    pump_run_time = cache.get('pump_run_time')
    data_sending_frequency = cache.get('data_sending_frequency')

    if not all([minimal_soil_humidity, lamp_on_time, lamp_off_time, pump_run_time, data_sending_frequency]):
        CashedGrowBoxSettings.set_cash(CashedGrowBoxSettings)
    return CashedGrowBoxSettings.get_cashed_settings_data(CashedGrowBoxSettings)


def set_new_settings(request: HttpRequest) -> None:
    """
    Устанавливает новые настройки полученные от пользователя.
    """
    settings: GrowBoxSettings = GrowBoxSettings.objects.all().first()

    if not settings:
        raise ObjectDoesNotExist

    minimal_soil_humidity = request.POST.get('minimal_soil_humidity')
    lamp_on_time = request.POST.get('lamp_on_time')
    lamp_off_time = request.POST.get('lamp_off_time')
    pump_run_time = request.POST.get('pump_run_time')
    data_sending_frequency = request.POST.get('data_sending_frequency')

    if not all([minimal_soil_humidity, lamp_on_time, lamp_off_time, pump_run_time, data_sending_frequency]):
        raise FieldError

    settings.minimal_soil_humidity = minimal_soil_humidity
    settings.lamp_on_time = lamp_on_time
    settings.lamp_off_time = lamp_off_time
    settings.pump_run_time = pump_run_time
    settings.data_sending_frequency = data_sending_frequency
    settings.save()


# БЛОК РАБОТЫ С ДАННЫМИ СЕНСОРОВ


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
        'soil_humidity': soil_humidity
    }
    return sensors_cashed_data
