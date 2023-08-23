import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
from requests import RequestException

from sensors.models import Sensor


@login_required
def index(request):
    access_token = request.session.get('access_token')
    context = {
        'access_token': access_token,
        'text': 'Error - connection to server failed'
    }

    headers = {
        'Authorization': 'Bearer ' + access_token,
    }

    try:
        devices_response = requests.get(settings.API_URL + 'devices/', headers=headers)
        if devices_response.ok:
            response_json = devices_response.json()
            if isinstance(response_json, list) and len(response_json) > 0:
                device_id = response_json[0].get('id')
                context['device_id'] = device_id
                if device_id:
                    sensor_response = requests.get(settings.API_URL + 'device/' + str(device_id) + '/sensor',
                                                   headers=headers)
                    if sensor_response.ok:
                        sensor_response_json = sensor_response.json()
                        context['sensors_data'] = sensor_response_json  # Przekazanie całości JSON do szablonu
                    else:
                        context['error_message'] = 'Failed to fetch sensor data'
            else:
                context['error_message'] = 'Invalid response format - missing or empty list of devices.'
        else:
            context['error_message'] = 'Connection lost. Please log in again to see your devices.'
    except RequestException:
        context['error_message'] = 'Connection lost. Please log in again to see your devices.'

    return render(request, 'charts.html', context)


