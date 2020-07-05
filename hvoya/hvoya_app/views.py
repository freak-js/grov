from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import GrowBoxDateTime, GrowBoxHistoricalData
from .utils.db_utils import get_historical_data
from .utils.token_auth import token_checker


@token_checker
def index(request: HttpRequest) -> HttpResponse:
    """

    :param request:
    :return: HttpResponse
    """
    historical_data = get_historical_data()
    return render(request, 'hvoya_app/index.html', {'historical_data': historical_data})


def change_settings(request: HttpRequest) -> HttpResponse:
     return render(request, 'hvoya_app/change_settings.html')


def create_new_flower(request: HttpRequest) -> HttpResponse:
    """

    :param request:
    :return: HttpResponse
    """
    return render(request, 'hvoya_app/create_new_flower.html')


# Контроллеры для заполнения БД тестовыми данными.


def generate_test_data(request: HttpRequest) -> HttpResponse:
    """
    Контроллер заполнения БД историческими данными показаний с сенсоров.
    :param request:
    :return:
    """
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
