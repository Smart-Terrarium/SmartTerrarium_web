import requests
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required


# Create your views here.
from requests import RequestException


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
        devices_response = requests.get('http://localhost:8000/devices/', headers=headers)
        if devices_response.ok:
            response_json = devices_response.json()
            if isinstance(response_json, list) and len(response_json) > 0:
                device_id = response_json[0].get('id')
                context['device_id'] = device_id
            else:
                context['error_message'] = 'Invalid response format - missing or empty list of devices.'
        else:
            context['error_message'] = 'Connection lost. Please log in again to see your devices.'
    except RequestException:
        context['error_message'] = 'Connection lost. Please log in again to see your devices.'

    return render(request, 'charts.html', context)
