from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Alert
import requests
from django.conf import settings

@login_required
def get_not_served_alerts(request):
    # Get the access token from the user's session
    access_token = request.session.get('access_token')
    # Create a context dictionary with the access token
    context = {
        'access_token': access_token
    }
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }
    # Set parameters for the API request
    params = {
        'sort_by_priority': 'true',
        'only_not_served': 'true',
    }

    try:
        # Send a GET request to the API endpoint for not served alerts
        not_served_alerts = requests.get(settings.API_URL + 'devices/alerts', headers=headers, params=params)

        if not_served_alerts.ok:
            response_json = not_served_alerts.json()
            alerts = []
            # Iterate through each alert data in the response and create Alert objects
            for alert_data in response_json:
                alert_date = datetime.strptime(alert_data['date'], '%Y-%m-%dT%H:%M:%S')
                alert = Alert(
                    sensor_id=alert_data['sensor_id'],
                    device_id=alert_data['device_id'],
                    description=alert_data['description'],
                    served=alert_data['served'],
                    alert_id=alert_data['id'],
                    date=alert_date.strftime('%Y-%m-%d %H:%M:%S'),
                    priority=alert_data['priority']
                )
                alerts.append(alert)
            # Add the list of Alert objects to the context dictionary
            context['alerts'] = alerts

        else:
            # If the API response is not successful, display an error message
            context['error_message'] = 'Connection lost. Please log in again to see your alerts.'
    # Handle exceptions that might occur during the API request
    except requests.RequestException:
        context['error_message'] = 'Connection lost. Please log in again to see your alerts.'
    # Render the 'alerts.html' template with the populated context
    return render(request, 'alerts.html', context)


@login_required
def get_served_alerts(request):
    # Get the access token from the user's session
    access_token = request.session.get('access_token')
    # Create a context dictionary with the access token
    context = {
        'access_token': access_token
    }
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }
    # Set parameters for the API request
    params = {
        'sort_by_priority': 'true',
        'only_served': 'true',
    }

    try:
        # Send a GET request to the API endpoint for served alerts
        not_served_alerts = requests.get(settings.API_URL + 'devices/alerts', headers=headers, params=params)

        if not_served_alerts.ok:
            response_json = not_served_alerts.json()
            alerts = []
            # Iterate through each served alert data in the response and create Alert objects
            for alert_data in response_json:
                alert_date = datetime.strptime(alert_data['date'], '%Y-%m-%dT%H:%M:%S')
                alert = Alert(
                    sensor_id=alert_data['sensor_id'],
                    device_id=alert_data['device_id'],
                    description=alert_data['description'],
                    served=alert_data['served'],
                    alert_id=alert_data['id'],
                    date=alert_date.strftime('%Y-%m-%d %H:%M:%S'),
                    priority=alert_data['priority']
                )
                alerts.append(alert)
            # Add the list of Alert objects to the context dictionary
            context['alerts'] = alerts

        else:
            # If the API response is not successful, display an error message
            context['error_message'] = 'Connection lost. Please log in again to see your alerts.'
    # Handle exceptions that might occur during the API request
    except requests.RequestException:
        context['error_message'] = 'Connection lost. Please log in again to see your alerts.'
    # Render the 'alerts.html' template with the populated context
    return render(request, 'alerts.html', context)


@login_required
def delete_alert(request, alert_id):
    if request.method == 'POST':

        access_token = request.session.get('access_token')
        bearer_token = 'Bearer ' + access_token

        delete_url = settings.API_URL + f'devices/alerts/{alert_id}'
        headers = {'Authorization': bearer_token}

        try:
            # Send a DELETE request to the API endpoint for deleting the alert
            response = requests.delete(delete_url, headers=headers)
            # Check if the API response indicates a successful deletion
            if response.ok:
                return redirect('get_served_alerts')
            else:
                # If deletion fails, display an error message
                error_message = 'Failed to delete alert.'
                context = {'error_message': error_message}
                return render(request, 'alerts.html', context)
        # Handle exceptions that might occur during the API request
        except requests.RequestException:
            error_message = 'Connection lost. Please try again.'
            context = {'error_message': error_message}
            return render(request, 'alerts.html', context)

    else:
        # If the request method is not POST, render the 'alerts.html' template
        return render(request, 'alerts.html')


@login_required
def serve_alerts(request, alert_id):
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the access token from the user's session
        access_token = request.session.get('access_token')
        bearer_token = 'Bearer ' + access_token
        # Construct the URL for deleting the specific alert
        serve_alert_url = settings.API_URL + f'devices/alerts/{alert_id}'
        headers = {'Authorization': bearer_token}

        try:
            response = requests.put(serve_alert_url, headers=headers)
            if response.ok:
                return redirect('get_not_served_alerts')
            else:
                error_message = 'Failed to serve alert.'
                context = {'error_message': error_message}
                return render(request, 'alerts.html', context)

        except requests.RequestException:
            error_message = 'Connection lost. Please try again.'
            context = {'error_message': error_message}
            return render(request, 'alerts.html', context)

    else:
        return render(request, 'alerts.html')



