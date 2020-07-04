# Этот модуль предназначен для утилит получения данных из БД


from datetime import datetime

from hvoya_app.models import GrowBoxHistoricalData


def get_historical_data() -> dict:
    """

    :return:
    """
    historical_data: dict = {
        'air_temperature': [],
        'air_humidity': [],
        'soil_humidity': [],
        'yesterday_air_temperature': [],
        'yesterday_air_humidity': [],
        'yesterday_soil_humidity': []
    }
    current_datetime: datetime = datetime.now()
    historical_data_queryset = GrowBoxHistoricalData.objects.select_related().filter(
        datetime__year=current_datetime.year,
        datetime__month=current_datetime.month,
        datetime__day__gte=current_datetime.day - 1
    ).order_by('id')

    for data in historical_data_queryset:

        if data.datetime.day == current_datetime.day:
            historical_data['air_temperature'].append(data.air_temperature)
            historical_data['air_humidity'].append(data.air_humidity)
            historical_data['soil_humidity'].append(data.soil_humidity)
        else:
            historical_data['yesterday_air_temperature'].append(data.air_temperature)
            historical_data['yesterday_air_humidity'].append(data.air_humidity)
            historical_data['yesterday_soil_humidity'].append(data.soil_humidity)

    return historical_data