from django.db import models


class DeviceConfig(models.Model):
    device_type = models.CharField(max_length=100)
    purpose = models.CharField(max_length=100)
    MQTT_ID_NAME = models.CharField(max_length=100)
    MQTT_PORT = models.PositiveIntegerField()
    MQTT_SERVER_IP = models.CharField(max_length=100)
    TCP_SERVER_IP = models.CharField(max_length=100)
    TCP_PORT = models.PositiveIntegerField()
    BUTTON_ADC_PIN = models.PositiveIntegerField()
    PWM_PIN = models.PositiveIntegerField()
    WIFI_SSID = models.CharField(max_length=100)
    WIFI_PASSWORD = models.CharField(max_length=100)
    ESP_MAC_ADDRESS = models.CharField(max_length=17)
    LCD_WIDTH = models.PositiveIntegerField()
    LCD_HEIGHT = models.PositiveIntegerField()
    LCD_ROTATION = models.PositiveIntegerField()
    LCD_CLK_PIN = models.PositiveIntegerField()
    LCD_MOSI_PIN = models.PositiveIntegerField()
    LCD_MISO_PIN = models.PositiveIntegerField()
    LCD_CS_PIN = models.PositiveIntegerField()
    LCD_RST_PIN = models.PositiveIntegerField()
    LCD_DC_PIN = models.PositiveIntegerField()
    FONT_DIR = models.CharField(max_length=100)
    FONT_WIDTH = models.PositiveIntegerField()
    FONT_HEIGHT = models.PositiveIntegerField()
    WATER_PUMP_PIN = models.PositiveIntegerField()
    PRESSURE_PLATE_PIN = models.PositiveIntegerField()

    class Meta:
        # Ustawienie managed na False zapobiega migracjom,
        # innymi słowy nie doda się tabela do lokalnej bazy danych.
        managed = False
