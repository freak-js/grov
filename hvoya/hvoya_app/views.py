# from typing import Union

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    """

    :param request:
    :return: HttpResponse
    """
    return render(request, 'hvoya_app/index.html', {})


def change_settings(request: HttpRequest) -> HttpResponse:
    """

    :param request:
    :return: HttpResponse
    """
    return render(request, 'hvoya_app/change_settings.html')


def create_new_flower(request: HttpRequest) -> HttpResponse:
    """

    :param request:
    :return: HttpResponse
    """
    return render(request, 'hvoya_app/create_new_flower.html')
