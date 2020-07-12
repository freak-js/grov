from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from .models import GrowBoxDateTime, GrowBoxHistoricalData
from .utils.db_utils import get_historical_data, get_current_data, get_settings_data, set_new_settings
from .utils.auth_utils import is_staff_checker


@require_GET
@is_staff_checker
def index(request: HttpRequest) -> HttpResponse:
    """
    Контроллер главной страницы с отображением состояния сенсоров.
    """
    historical_data: dict = get_historical_data()
    current_data: dict = get_current_data()
    context: dict = {
        'historical_data': historical_data,
        'current_data': current_data
    }
    return render(request, 'hvoya_app/index.html', context)


@require_http_methods(['GET', 'POST'])
@is_staff_checker
def settings(request: HttpRequest) -> HttpResponse:
    """
    Контроллер страницы с настройками гроубокса.
    """
    if request.method == 'GET':
        context = get_settings_data()
        return render(request, 'hvoya_app/settings.html', context)
    set_new_settings(request)
    return redirect('index')


@require_POST
def send_data(request: HttpRequest) -> HttpResponse:
    """
    Контроллер приема показателей сенсоров и
    ответа текущими настройками гроубокса.
    """
    pass


@require_GET
@is_staff_checker
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
            hours=fake_datetime.hour,
            minutes=fake_datetime.minute,
            seconds=fake_datetime.second
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
