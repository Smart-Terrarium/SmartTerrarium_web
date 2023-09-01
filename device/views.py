import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings

from device.models import DeviceConfig

API_URL = settings.API_URL


@login_required
def device_configuration(request):
    access_token = request.session.get('access_token')
    context = {}
    headers = {'Authorization': 'Bearer ' + access_token}

    try:
        # Send a GET request to fetch devices data from the API
        devices_response = requests.get(API_URL + 'devices', headers=headers)
        if devices_response.ok:
            device_info = devices_response.json()
            # Check if the response JSON is a list and not empty
            if isinstance(device_info, list) and len(device_info) > 0:
                device_id = device_info[0].get('id')
                context['device_id'] = device_id
                if device_id:
                    # Send a GET request to fetch device configuration for the specific device
                    device_config_response = requests.get(API_URL + f'device/{device_id}/configuration',
                                                          headers=headers)
                    # Check if the device configuration response is successful
                    if device_config_response.ok:
                        device_config_data = device_config_response.json()
                        # Check if 'payload' exists in the response data
                        if 'payload' in device_config_data:
                            device_config_payload = device_config_data['payload']['configuration']

                            try:
                                # Create a DeviceConfig object using the fetched data
                                device_config = DeviceConfig(
                                    device_type=device_config_payload.get('type'),
                                    purpose=device_config_payload.get('purpose'),
                                    MQTT_ID_NAME=device_config_payload['MQTT']['MQTT_ID_NAME'],
                                    MQTT_PORT=device_config_payload['MQTT']['MQTT_PORT'],
                                    MQTT_SERVER_IP=device_config_payload['MQTT']['MQTT_SERVER_IP'],
                                    TCP_SERVER_IP=device_config_payload['TCP']['TCP_SERVER_IP'],
                                    TCP_PORT=device_config_payload['TCP']['TCP_PORT'],
                                    BUTTON_ADC_PIN=device_config_payload['BUTTONS']['BUTTON_ADC_PIN'],
                                    PWM_PIN=device_config_payload['PWM']['PWM_PIN'],
                                    WIFI_SSID=device_config_payload['WIFI']['WIFI_SSID'],
                                    WIFI_PASSWORD=device_config_payload['WIFI']['WIFI_PASSWORD'],
                                    ESP_MAC_ADDRESS=device_config_payload['WIFI']['ESP_MAC_ADDRESS'],
                                    LCD_WIDTH=device_config_payload['LCD']['LCD_WIDTH'],
                                    LCD_HEIGHT=device_config_payload['LCD']['LCD_HEIGHT'],
                                    LCD_ROTATION=device_config_payload['LCD']['LCD_ROTATION'],
                                    LCD_CLK_PIN=device_config_payload['LCD']['LCD_CLK_PIN'],
                                    LCD_MOSI_PIN=device_config_payload['LCD']['LCD_MOSI_PIN'],
                                    LCD_MISO_PIN=device_config_payload['LCD']['LCD_MISO_PIN'],
                                    LCD_CS_PIN=device_config_payload['LCD']['LCD_CS_PIN'],
                                    LCD_RST_PIN=device_config_payload['LCD']['LCD_RST_PIN'],
                                    LCD_DC_PIN=device_config_payload['LCD']['LCD_DC_PIN'],
                                    FONT_DIR=device_config_payload['LCD']['FONT_DIR'],
                                    FONT_WIDTH=device_config_payload['LCD']['FONT_WIDTH'],
                                    FONT_HEIGHT=device_config_payload['LCD']['FONT_HEIGHT'],
                                    WATER_PUMP_PIN=device_config_payload['WATER_PUMP']['WATER_PUMP_PIN'],
                                    PRESSURE_PLATE_PIN=device_config_payload['PRESSURE_PLATE']['PRESSURE_PLATE_PIN'],
                                )
                                context['device_config'] = device_config
                            except Exception as e:
                                context['error_message'] = f'Error while creating DeviceConfig: {str(e)}'
                        else:
                            context['error_message'] = 'Incorrect response format - missing payload data.'
                    else:
                        context['error_message'] = 'The device configuration could not be retrieved. Try again.'
                else:
                    context['error_message'] = 'Device ID not found.'
            else:
                context['error_message'] = 'Incorrect response format - missing or empty list of devices.'
        else:
            context['error_message'] = 'Connection lost. Please log back in to see the devices.'
    except requests.exceptions.RequestException:
        context['error_message'] = 'Connection lost. Please log back in to see the devices.'

    return render(request, 'device.html', context)


@login_required
def edit_device_config(request, device_id):
    if request.method == 'POST':
        access_token = request.session.get('access_token')
        bearer_token = 'Bearer ' + access_token

        # Retrieve data from the device configuration edit form
        device_config_data = {
            "MQTT": {
                "MQTT_ID_NAME": request.POST.get('mqtt_id_name'),
                "MQTT_PORT": int(request.POST.get('mqtt_port')),
                "MQTT_SERVER_IP": request.POST.get('mqtt_server_ip'),
            },
            "TCP": {
                "TCP_SERVER_IP": request.POST.get('tcp_server_ip'),
                "TCP_PORT": int(request.POST.get('tcp_port')),
            },
            "BUTTONS": {
                "BUTTON_ADC_PIN": int(request.POST.get('button_adc_pin')),
            },
            "PWM": {
                "PWM_PIN": int(request.POST.get('pwm_pin')),
            },
            "WIFI": {
                "WIFI_SSID": request.POST.get('wifi_ssid'),
                "WIFI_PASSWORD": request.POST.get('wifi_password'),
                "ESP_MAC_ADDRESS": request.POST.get('esp_mac_address'),
            },
            "LCD": {
                "LCD_WIDTH": int(request.POST.get('lcd_width')),
                "LCD_HEIGHT": int(request.POST.get('lcd_height')),
                "LCD_ROTATION": int(request.POST.get('lcd_rotation')),
                "LCD_CLK_PIN": int(request.POST.get('lcd_clk_pin')),
                "LCD_MOSI_PIN": int(request.POST.get('lcd_mosi_pin')),
                "LCD_MISO_PIN": int(request.POST.get('lcd_miso_pin')),
                "LCD_CS_PIN": int(request.POST.get('lcd_cs_pin')),
                "LCD_RST_PIN": int(request.POST.get('lcd_rst_pin')),
                "LCD_DC_PIN": int(request.POST.get('lcd_dc_pin')),
                "FONT_DIR": request.POST.get('font_dir'),
                "FONT_WIDTH": int(request.POST.get('font_width')),
                "FONT_HEIGHT": int(request.POST.get('font_height')),
            },
            "PRESSURE_PLATE": {
                "PRESSURE_PLATE_PIN": int(request.POST.get('pressure_plate_pin')),
            },
            "WATER_PUMP": {
                "WATER_PUMP_PIN": int(request.POST.get('water_pump_pin')),
            },
        }
        # Create headers with the bearer token
        headers = {'Authorization': bearer_token}

        # Construct the URL for editing the device configuration
        edit_url = f'{settings.API_URL}device/{device_id}/configuration'
        try:
            # Send a POST request to edit the device configuration
            response = requests.post(edit_url, json=device_config_data, headers=headers)
            # Check if the API response indicates successful edit
            if response.ok:
                success_message_device = 'Device configuration changed, reboot the device.'
                context = {'success_message_device': success_message_device}
                return render(request, 'device.html', context)
            else:
                error_message = 'Failed to edit device configuration.'
                context = {'error_message': error_message}
                return render(request, 'device.html', context)
        # Handle exceptions that might occur during the API request
        except requests.RequestException:
            error_message = 'Connection lost. Please try again.'
            context = {'error_message': error_message}
            return render(request, 'device.html', context)

    else:
        error_message = 'Connection lost. Please try again.'
        context = {'error_message': error_message}
        return render(request, 'device.html', context)
