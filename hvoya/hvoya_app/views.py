import json

from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import GrowBoxDateTime, GrowBoxHistoricalData
from .utils.settings_utils import get_settings_data, set_new_settings, get_settings_for_donut_chart
from .utils.statistic_utils import get_historical_data
from .utils.sensors_utils import update_sensors_data, give_sensors_cashed_data
from .utils.lighting_utils import get_lighting_data


@require_GET
def index(request: HttpRequest) -> HttpResponse:
    """
    Контроллер главной страницы с отображением состояния сенсоров.
    """
    context: dict = {
        'historical_data': get_historical_data(),
        'current_data': give_sensors_cashed_data(),
        'lighting_data': get_lighting_data(),
        'donut_chart_data': get_settings_for_donut_chart()
    }
    return render(request, 'hvoya_app/index.html', context)


@require_http_methods(['GET', 'POST'])
def settings(request: HttpRequest) -> HttpResponse:
    """
    Контроллер страницы с настройками гроубокса.
    """
    if request.method == 'GET':
        current_cached_settings: dict = get_settings_data()
        settings_for_donut_chart: dict = get_settings_for_donut_chart()
        context = {**current_cached_settings, **settings_for_donut_chart}
        return render(request, 'hvoya_app/settings.html', context)
    set_new_settings(request)
    context = {'message': 'Настройки успешно применены!'}
    return render(request, 'hvoya_app/notification.html', context)


@csrf_exempt
@require_POST
def send_data(request: HttpRequest) -> HttpResponse:
    """
    Контроллер приема показателей сенсоров и
    ответа текущими настройками гроубокса.
    """
    new_sensors_data: dict = json.loads(request.body)
    update_sensors_data(new_sensors_data)
    current_cached_settings: dict = get_settings_data()
    return JsonResponse(current_cached_settings)


@require_GET
def get_cached_sensors_data(request: HttpRequest) -> HttpResponse:
    """
    Контроллер отдающий текущие кешированные показатели сенсоров.
    """
    sensors_cashed_data = give_sensors_cashed_data()
    return JsonResponse(sensors_cashed_data)


@require_GET
def generate_test_data(request: HttpRequest) -> HttpResponse:
    """
    Контроллер заполнения БД историческими данными показаний с сенсоров.
    """
    GrowBoxDateTime.objects.all().delete()
    GrowBoxHistoricalData.objects.all().delete()

    from random import randint
    today: datetime = datetime.now()
    yesterday: datetime = today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    hours_offset: timedelta = timedelta(hours=2)
    fake_datetime: datetime = yesterday

    while True:

        if fake_datetime > today:
            break

        new_growbox_datetime: GrowBoxDateTime = GrowBoxDateTime(
            year=fake_datetime.year,
            month=fake_datetime.month,
            day=fake_datetime.day,
            hours=fake_datetime.hour
        )
        new_growbox_datetime.save()

        GrowBoxHistoricalData(
            air_temperature=randint(16, 30),
            air_humidity=randint(35, 85),
            soil_humidity=randint(25, 100),
            datetime=new_growbox_datetime
        ).save()

        fake_datetime += hours_offset

    return HttpResponse('Тестовые данные созданы')
