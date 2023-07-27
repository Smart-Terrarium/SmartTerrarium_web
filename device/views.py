import json

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from requests import RequestException

API_URL = 'http://localhost:8000/'


# Create your views here.
def device_configuration(request):
    access_token = request.session.get('access_token')

    context = {
        'access_token': access_token
    }

    headers = {
        'Authorization': 'Bearer ' + access_token,
    }

    try:
        devices_response = requests.get(API_URL + 'devices', headers=headers)
        if devices_response.ok:
            device_info = devices_response.json()
            if isinstance(device_info, list) and len(device_info) > 0:
                device_id = device_info[0].get('id')
                context['device_id'] = device_id
                if device_id:
                    device_config_response = requests.get(API_URL + f'device/{device_id}/configuration', headers=headers)
                    if device_config_response.ok:
                        print(type(device_config_response))
                        device_config = json.loads(device_config_response.text)
                        context['device_config'] = json.dumps(device_config)
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