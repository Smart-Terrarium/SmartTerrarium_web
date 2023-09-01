from django.db import models


class DeviceConfig(models.Model):
    device_type = models.CharField(max_length=100)      # Type of the device
    purpose = models.CharField(max_length=100)          # Purpose or function of the device
    MQTT_ID_NAME = models.CharField(max_length=100)     # MQTT client ID or name
    MQTT_PORT = models.PositiveIntegerField()           # MQTT server port
    MQTT_SERVER_IP = models.CharField(max_length=100)   # MQTT server IP address
    TCP_SERVER_IP = models.CharField(max_length=100)    # TCP server IP address
    TCP_PORT = models.PositiveIntegerField()            # TCP server port
    BUTTON_ADC_PIN = models.PositiveIntegerField()      # ADC pin for the button
    PWM_PIN = models.PositiveIntegerField()             # PWM pin
    WIFI_SSID = models.CharField(max_length=100)        # WiFi SSID
    WIFI_PASSWORD = models.CharField(max_length=100)    # WiFi password
    ESP_MAC_ADDRESS = models.CharField(max_length=17)   # ESP device MAC address
    LCD_WIDTH = models.PositiveIntegerField()           # LCD screen width
    LCD_HEIGHT = models.PositiveIntegerField()          # LCD screen height
    LCD_ROTATION = models.PositiveIntegerField()        # LCD screen rotation
    LCD_CLK_PIN = models.PositiveIntegerField()         # LCD clock pin
    LCD_MOSI_PIN = models.PositiveIntegerField()        # LCD MOSI pin
    LCD_MISO_PIN = models.PositiveIntegerField()        # LCD MISO pin
    LCD_CS_PIN = models.PositiveIntegerField()          # LCD CS pin
    LCD_RST_PIN = models.PositiveIntegerField()         # LCD reset pin
    LCD_DC_PIN = models.PositiveIntegerField()          # LCD data/command pin
    FONT_DIR = models.CharField(max_length=100)         # Directory for fonts
    FONT_WIDTH = models.PositiveIntegerField()          # Font width
    FONT_HEIGHT = models.PositiveIntegerField()         # Font height
    WATER_PUMP_PIN = models.PositiveIntegerField()      # Pin for water pump
    PRESSURE_PLATE_PIN = models.PositiveIntegerField()  # Pin for pressure plate

    class Meta:
        # Setting managed to False prevents migrations,
        # in other words, the table won't be added to the local database.
        managed = False

