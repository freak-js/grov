# Этот модуль предназначен для работы с настройками гроубокса

from typing import Dict
import datetime

from django.http import HttpRequest
from django.core.cache import cache
from django.core.exceptions import FieldError

from hvoya import settings
from hvoya_app.models import GrowBoxSettings


def set_default_settings_and_cash_them() -> None:
    """
    Получает данные из GrowBoxSettings и кеширует их значения.
    Если настроек не найдено в базе, то они будут созданы с
    дефолтными значениями.
    """
    growbox_settings = GrowBoxSettings.objects.all().first()

    if not growbox_settings:
        growbox_settings = GrowBoxSettings(
            minimal_soil_humidity=settings.DEFAULT_MINIMAL_SOIL_HUMIDITY,
            lamp_on_time=settings.DEFAULT_LAMP_ON_TIME,
            lamp_off_time=settings.DEFAULT_LAMP_OFF_TIME,
            pump_run_time=settings.DEFAULT_PUMP_RUN_TIME,
            data_sending_frequency=settings.DEFAULT_DATA_SENDING_FREQUENCY
        )
        growbox_settings.save()
    else:
        cache.set('minimal_soil_humidity', growbox_settings.minimal_soil_humidity, timeout=None)
        cache.set('lamp_on_time', growbox_settings.lamp_on_time, timeout=None)
        cache.set('lamp_off_time', growbox_settings.lamp_off_time, timeout=None)
        cache.set('pump_run_time', growbox_settings.pump_run_time, timeout=None)
        cache.set('data_sending_frequency', growbox_settings.data_sending_frequency, timeout=None)


def get_settings_data() -> Dict[str, int]:
    """
    Возвращает кеш настроек гроубокса в формате словаря.
    Если настройки не найдены в Redis, то устанавливает
    значения по умолчанию из модуля settings и кеширует их.
    """
    cashed_settings_data_value = get_cashed_settings_data().values()

    if not all(cashed_settings_data_value):
        set_default_settings_and_cash_them()

    return get_cashed_settings_data()


def get_cashed_settings_data() -> Dict[str, int]:
    """
    Возвращает значения кешированных настроек из Redis в формате словаря.
    """
    cashed_settings_data = {
        'minimal_soil_humidity': cache.get('minimal_soil_humidity'),
        'lamp_on_time': cache.get('lamp_on_time'),
        'lamp_off_time': cache.get('lamp_off_time'),
        'pump_run_time': cache.get('pump_run_time'),
        'data_sending_frequency': cache.get('data_sending_frequency')
    }
    return cashed_settings_data


def get_settings_for_donut_chart() -> dict:
    """
    Делает запрос в базу и получает данные для
    формирования круговой диаграммы спелости.
    """
    growbox_settings: GrowBoxSettings = GrowBoxSettings.objects.all().first()
    date_format = '%Y-%m-%d'

    if not growbox_settings:
        set_default_settings_and_cash_them()

    planting_date = growbox_settings.planting_date
    days_before_harvest = growbox_settings.days_before_harvest

    planting_datetime = datetime.datetime.strptime(planting_date, date_format)
    harvest_datetime = planting_datetime + datetime.timedelta(days=days_before_harvest)
    now_datetime = datetime.datetime.now()

    remaining_days = 0 if now_datetime >= harvest_datetime else (harvest_datetime - now_datetime).days
    days_in_growth_stage = (now_datetime - planting_datetime).days

    data_for_donut_char = {
        'planting_date': planting_date,
        'days_before_harvest': days_before_harvest,
        'remaining_days': remaining_days,
        'days_in_growth_stage': days_in_growth_stage
    }
    return data_for_donut_char


def set_new_settings(request: HttpRequest) -> None:
    """
    Устанавливает новые настройки полученные от пользователя.
    """
    settings = GrowBoxSettings.objects.all().first()

    if not settings:
        set_default_settings_and_cash_them()

    minimal_soil_humidity = request.POST.get('minimal_soil_humidity')
    lamp_on_time = request.POST.get('lamp_on_time')
    lamp_off_time = request.POST.get('lamp_off_time')
    pump_run_time = request.POST.get('pump_run_time')
    data_sending_frequency = request.POST.get('data_sending_frequency')
    planting_date = request.POST.get('planting_date')
    days_before_harvest = request.POST.get('days_before_harvest')

    if not all([
        minimal_soil_humidity,
        lamp_on_time,
        lamp_off_time,
        pump_run_time,
        data_sending_frequency,
        planting_date,
        days_before_harvest
    ]):
        raise FieldError

    settings.minimal_soil_humidity = minimal_soil_humidity
    settings.lamp_on_time = lamp_on_time
    settings.lamp_off_time = lamp_off_time
    settings.pump_run_time = pump_run_time
    settings.data_sending_frequency = data_sending_frequency
    settings.planting_date = planting_date
    settings.days_before_harvest = days_before_harvest
    settings.save()

    cache.set('minimal_soil_humidity', minimal_soil_humidity, timeout=None)
    cache.set('lamp_on_time', lamp_on_time, timeout=None)
    cache.set('lamp_off_time', lamp_off_time, timeout=None)
    cache.set('pump_run_time', pump_run_time, timeout=None)
    cache.set('data_sending_frequency', data_sending_frequency, timeout=None)
