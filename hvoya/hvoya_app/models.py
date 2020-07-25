from django.db import models

from hvoya import settings


class GrowBoxSettings(models.Model):
    minimal_soil_humidity = models.IntegerField('Минимальная влажность грунта в процентах')
    lamp_on_time = models.IntegerField('Время включения лампы в часах')
    lamp_off_time = models.IntegerField('Время включения лампы в часах')
    pump_run_time = models.IntegerField('Время работы помпы в секундах')
    data_sending_frequency = models.IntegerField('Таймер отправки данных с платы в секундах')


class GrowBoxDateTime(models.Model):
    year = models.IntegerField('Год')
    month = models.IntegerField('Месяц')
    day = models.IntegerField('День')
    hours = models.IntegerField('Часы')
    minutes = models.IntegerField('Минуты')
    seconds = models.IntegerField('Секунды')


class GrowBoxHistoricalData(models.Model):
    air_temperature = models.IntegerField('Температура воздуха')
    air_humidity = models.IntegerField('Влажность воздуха')
    soil_humidity = models.IntegerField('Влажность грунта')
    datetime = models.OneToOneField(GrowBoxDateTime, on_delete=models.CASCADE)


class CashedGrowBoxSettings:
    minimal_soil_humidity: int = 0
    lamp_on_time: int = 0
    lamp_off_time: int = 0
    pump_run_time: int = 0
    data_sending_frequency: int = 0

    def set_cash(self) -> None:
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
            self.set_settings_from_database(self, growbox_settings)

    def set_settings_from_database(self, settings: GrowBoxSettings) -> None:
        """
        Кеширует настройки из объекта GrowBoxSettings.
        """
        self.minimal_soil_humidity = settings.minimal_soil_humidity
        self.lamp_on_time = settings.lamp_on_time
        self.lamp_off_time = settings.lamp_off_time
        self.pump_run_time = settings.pump_run_time
        self.data_sending_frequency = settings.data_sending_frequency

    def cache_is_installed(self) -> bool:
        """
        Проверяет есть ли закешированные настройки.
        """
        cash_list: list = [
            self.minimal_soil_humidity,
            self.lamp_on_time,
            self.lamp_off_time,
            self.pump_run_time,
            self.data_sending_frequency
        ]
        return all(cash_list)

    def get_cashed_settings_data(self) -> dict:
        """
        Возвращает значения настроек в формате словаря.
        """
        cashed_settings_data: dict = {
            'minimal_soil_humidity': self.minimal_soil_humidity,
            'lamp_on_time': self.lamp_on_time,
            'lamp_off_time': self.lamp_off_time,
            'pump_run_time': self.pump_run_time,
            'data_sending_frequency': self.data_sending_frequency
        }
        return cashed_settings_data
