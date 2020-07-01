from django.db import models


class GrowBoxSettings(models.Model):
    minimal_soil_humidity = models.IntegerField('Минимальная влажность грунта в процентах')
    lamp_on_time = models.TimeField('Время включения лампы')
    lamp_off_time = models.TimeField('Время включения лампы')
    pump_run_time = models.IntegerField('Время работы помпы в секундах')
    data_sending_frequency = models.IntegerField('Таймер отправки данных с платы в секундах')


class GrowBoxDateTime(models.Model):
    date_time = models.DateTimeField('Дата и время контрольного снятия данных с сенсоров', auto_now_add=True)


class GrowBoxHistoricalData(models.Model):
    air_temperature = models.IntegerField('Температура воздуха')
    air_humidity = models.IntegerField('Влажность воздуха')
    soil_humidity = models.IntegerField('Влажность грунта')
    datetime = models.OneToOneField(GrowBoxDateTime, on_delete=models.CASCADE)


class GrowBox():
    CURRENT_AIR_TEMPERATURE: int = 0
    CURRENT_AIR_HUMIDITY: int = 0
    CURRENT_SOIL_HUMIDITY: int = 0

    def check_datetime(self):
        pass