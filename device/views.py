import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

API_URL = 'http://localhost:8000/'


@login_required
def device_configuration(request):
    access_token = request.session.get('access_token')
    context = {'access_token': access_token}
    headers = {'Authorization': 'Bearer ' + access_token}

    try:
        devices_response = requests.get(API_URL + 'devices', headers=headers)
        if devices_response.ok:
            device_info = devices_response.json()
            if isinstance(device_info, list) and len(device_info) > 0:
                device_id = device_info[0].get('id')
                context['device_id'] = device_id
                if device_id:
                    device_config_response = requests.get(API_URL + f'device/{device_id}/configuration',
                                                          headers=headers)
                    if device_config_response.ok:
                        device_config_data = device_config_response.json()
                        if 'payload' in device_config_data:
                            device_config_payload = device_config_data['payload']
                            # Przerobienie JSON-a na słownik dla ułatwienia obsługi
                            device_config_dict = {
                                'device_type': device_config_payload.get('type'),
                                'purpose': device_config_payload.get('purpose'),
                                'MQTT_ID_NAME': device_config_payload['MQTT']['MQTT_ID_NAME'],
                                'MQTT_PORT': device_config_payload['MQTT']['MQTT_PORT'],
                                'MQTT_SERVER_IP': device_config_payload['MQTT']['MQTT_SERVER_IP'],
                                'TCP_SERVER_IP': device_config_payload['TCP']['TCP_SERVER_IP'],
                                'TCP_PORT': device_config_payload['TCP']['TCP_PORT'],
                                'BUTTON_ADC_PIN': device_config_payload['BUTTONS']['BUTTON_ADC_PIN'],
                                'PWM_PIN': device_config_payload['PWM']['PWM_PIN'],
                                'WIFI_SSID': device_config_payload['WIFI']['WIFI_SSID'],
                                'WIFI_PASSWORD': device_config_payload['WIFI']['WIFI_PASSWORD'],
                                'ESP_MAC_ADDRESS': device_config_payload['WIFI']['ESP_MAC_ADDRESS'],
                                'LCD_WIDTH': device_config_payload['LCD']['LCD_WIDTH'],
                                'LCD_HEIGHT': device_config_payload['LCD']['LCD_HEIGHT'],
                                'LCD_ROTATION': device_config_payload['LCD']['LCD_ROTATION'],
                                'LCD_CLK_PIN': device_config_payload['LCD']['LCD_CLK_PIN'],
                                'LCD_MOSI_PIN': device_config_payload['LCD']['LCD_MOSI_PIN'],
                                'LCD_MISO_PIN': device_config_payload['LCD']['LCD_MISO_PIN'],
                                'LCD_CS_PIN': device_config_payload['LCD']['LCD_CS_PIN'],
                                'LCD_RST_PIN': device_config_payload['LCD']['LCD_RST_PIN'],
                                'LCD_DC_PIN': device_config_payload['LCD']['LCD_DC_PIN'],
                                'FONT_DIR': device_config_payload['LCD']['FONT_DIR'],
                                'FONT_WIDTH': device_config_payload['LCD']['FONT_WIDTH'],
                                'FONT_HEIGHT': device_config_payload['LCD']['FONT_HEIGHT'],
                            }
                            context['device_config'] = device_config_dict
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

        # Pobranie danych z formularza edycji konfiguracji urządzenia
        mqtt_id_name = request.POST.get('mqtt_id_name')
        mqtt_port = int(request.POST.get('mqtt_port'))
        mqtt_server_ip = request.POST.get('mqtt_server_ip')
        tcp_server_ip = request.POST.get('tcp_server_ip')
        tcp_port = int(request.POST.get('tcp_port'))
        button_adc_pin = int(request.POST.get('button_adc_pin'))
        pwm_pin = int(request.POST.get('pwm_pin'))
        wifi_ssid = request.POST.get('wifi_ssid')
        wifi_password = request.POST.get('wifi_password')
        esp_mac_address = request.POST.get('esp_mac_address')
        lcd_width = int(request.POST.get('lcd_width'))
        lcd_height = int(request.POST.get('lcd_height'))
        lcd_rotation = int(request.POST.get('lcd_rotation'))
        lcd_clk_pin = int(request.POST.get('lcd_clk_pin'))
        lcd_mosi_pin = int(request.POST.get('lcd_mosi_pin'))
        lcd_miso_pin = int(request.POST.get('lcd_miso_pin'))
        lcd_cs_pin = int(request.POST.get('lcd_cs_pin'))
        lcd_rst_pin = int(request.POST.get('lcd_rst_pin'))
        lcd_dc_pin = int(request.POST.get('lcd_dc_pin'))
        font_dir = request.POST.get('font_dir')
        font_width = int(request.POST.get('font_width'))
        font_height = int(request.POST.get('font_height'))

        # Utworzenie JSON z nowymi danymi konfiguracji urządzenia
        device_config_data = {
            "MQTT": {
                "MQTT_ID_NAME": mqtt_id_name,
                "MQTT_PORT": mqtt_port,
                "MQTT_SERVER_IP": mqtt_server_ip,
            },
            "TCP": {
                "TCP_SERVER_IP": tcp_server_ip,
                "TCP_PORT": tcp_port,
            },
            "BUTTONS": {
                "BUTTON_ADC_PIN": button_adc_pin,
            },
            "PWM": {
                "PWM_PIN": pwm_pin,
            },
            "WIFI": {
                "WIFI_SSID": wifi_ssid,
                "WIFI_PASSWORD": wifi_password,
                "ESP_MAC_ADDRESS": esp_mac_address,
            },
            "LCD": {
                "LCD_WIDTH": lcd_width,
                "LCD_HEIGHT": lcd_height,
                "LCD_ROTATION": lcd_rotation,
                "LCD_CLK_PIN": lcd_clk_pin,
                "LCD_MOSI_PIN": lcd_mosi_pin,
                "LCD_MISO_PIN": lcd_miso_pin,
                "LCD_CS_PIN": lcd_cs_pin,
                "LCD_RST_PIN": lcd_rst_pin,
                "LCD_DC_PIN": lcd_dc_pin,
                "FONT_DIR": font_dir,
                "FONT_WIDTH": font_width,
                "FONT_HEIGHT": font_height,
            },
        }

        # Utworzenie nagłówka z tokenem dostępu
        headers = {'Authorization': bearer_token}

        # Wysłanie żądania POST na adres edycji konfiguracji urządzenia
        edit_url = f'http://localhost:8000/device/{device_id}/configuration'
        try:
            response = requests.post(edit_url, json=device_config_data, headers=headers)
            if response.ok:
                error_message_device = 'Device configuration changed, reboot the device.'
                context = {'error_message': error_message_device}
                return render(request, 'home.html', context)
            else:
                error_message = 'Failed to edit device configuration.'
                context = {'error_message': error_message}
                return render(request, 'device.html', context)

        except requests.RequestException:
            error_message = 'Connection lost. Please try again.'
            context = {'error_message': error_message}
            return render(request, 'device.html', context)

    else:
        error_message = 'Connection lost. Please try again.'
        context = {'error_message': error_message}
        return render(request, 'device.html', context)
