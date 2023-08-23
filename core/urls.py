"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user.views import register_user, login_view, home_view, forgot_password, change_password
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from sensors.views import create_sensor, select_sensors, delete_sensor, edit_sensor, sync_sensors_with_db, create_dht_sensor
from alerts.views import get_not_served_alerts, get_served_alerts, delete_alert, serve_alerts
from device.views import device_configuration, edit_device_config
from informations.views import get_basic_animal_information


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_user, name='register'),
    path('forgot_password/', forgot_password,name="forgot_password"),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('', include('charts.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('base/', home_view, name='base'),
    path('sensorform/', create_sensor, name='sensor_form'),
    path('dth_sensor/', create_dht_sensor, name='dht_sensor'),
    path('alerts/served', get_served_alerts, name='get_served_alerts'),
    path('alerts/', get_not_served_alerts, name='get_not_served_alerts'),
    path('alerts/delete/<int:alert_id>/', delete_alert, name='delete_alert'),
    path('alerts/serve/<int:alert_id>/', serve_alerts, name='serve_alerts'),
    path('device/', device_configuration, name='device_config'),
    path('change_password/', change_password, name='change_password'),
    path('sensors/', select_sensors, name='sensors'),
    path('sensors/delete/<int:device_id>/<int:sensor_id>/', delete_sensor, name='delete_sensor'),
    path('sensors/edit/<int:device_id>/<int:sensor_id>/', edit_sensor, name='edit_sensor'),
    path('device/<int:device_id>/edit/', edit_device_config, name='edit_device_config'),
    path('sync_sensors/<int:device_id>/', sync_sensors_with_db, name='sync_sensors'),
    path('pets/', get_basic_animal_information, name='get_basic_animal_information'),
]

handler404 = TemplateView.as_view(template_name="errors_templates/404_error.html")