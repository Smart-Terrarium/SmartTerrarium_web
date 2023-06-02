from django.shortcuts import render, redirect
from .forms import SensorForm
import requests
import json


def create_sensor(request):
    if request.method == 'POST':
        form = SensorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            bearer_token = request.session.get('access_token')
            headers = {
                'Authorization': 'Bearer ' + bearer_token,
            }

            response = requests.post('http://localhost:8000/device/sensor/', data=json.dumps(data), headers=headers)
            if response.ok:
                return redirect('home')  # Przekierowanie po udanym żądaniu
            else:
                return redirect('blad')  # Przekierowanie po błędnym żądaniu

    else:
        form = SensorForm()

    return render(request, 'new_sensor.html', {'form': form})
