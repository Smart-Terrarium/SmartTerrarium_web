from django.db import models

class DeviceConfig(models.Model):
    device_type = models.CharField(max_length=100)
    purpose = models.CharField(max_length=100)
    MQTT_ID_NAME = models.CharField(max_length=100)
    MQTT_PORT = models.CharField(max_length=10)
    MQTT_SERVER_IP = models.CharField(max_length=100)
    TCP_SERVER_IP = models.CharField(max_length=100)
    TCP_PORT = models.CharField(max_length=10)
    BUTTON_ADC_PIN = models.CharField(max_length=10)
    PWM_PIN = models.CharField(max_length=10)
    WIFI_SSID = models.CharField(max_length=100)
    WIFI_PASSWORD = models.CharField(max_length=100)
    ESP_MAC_ADDRESS = models.CharField(max_length=17)
    LCD_WIDTH = models.CharField(max_length=10)
    LCD_HEIGHT = models.CharField(max_length=10)
    LCD_ROTATION = models.CharField(max_length=10)
    LCD_CLK_PIN = models.CharField(max_length=10)
    LCD_MOSI_PIN = models.CharField(max_length=10)
    LCD_MISO_PIN = models.CharField(max_length=10)
    LCD_CS_PIN = models.CharField(max_length=10)
    LCD_RST_PIN = models.CharField(max_length=10)
    LCD_DC_PIN = models.CharField(max_length=10)
    FONT_DIR = models.CharField(max_length=100)
    FONT_WIDTH = models.CharField(max_length=10)
    FONT_HEIGHT = models.CharField(max_length=10)

    class Meta:
        # Ustawienie managed na False zapobiega migracjom
        managed = False
