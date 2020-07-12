# Этот модуль предназначен для утилит получения данных из БД и классов находящихся в моделях


from datetime import datetime, timedelta
from typing import Dict

from django.http import HttpRequest
from django.core.exceptions import ObjectDoesNotExist, FieldError

from hvoya_app.models import GrowBoxHistoricalData, GrowBox, CashedGrowBoxSettings, GrowBoxSettings


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


def get_current_data() -> Dict[str, int]:
    """
    Возвращает текущие данные показателей сенсоров из оперативной памяти.
    """
    current_data: dict = {
        'air_temperature': GrowBox.current_air_temperature,
        'air_humidity': GrowBox.current_air_humidity,
        'soil_humidity': GrowBox.current_soil_humidity
    }
    return current_data


def get_settings_data() -> Dict[str, int]:
    """
    Возвращает кеш настроек гроубокса в формате словаря.
    """
    if not CashedGrowBoxSettings.cache_is_installed(CashedGrowBoxSettings):
        CashedGrowBoxSettings.set_cash(CashedGrowBoxSettings)
    return CashedGrowBoxSettings.get_cashed_settings_data(CashedGrowBoxSettings)


def set_new_settings(request: HttpRequest) -> None:
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
