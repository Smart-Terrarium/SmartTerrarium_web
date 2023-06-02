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
from user.views import register_user, login_view, home_view
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from sensors.views import create_sensor

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_user, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('base/', home_view, name='base'),
    path('logout/', auth_views.LogoutView.as_view()),
    path('sensorform/', create_sensor, name='sensor_form'),
    path('404/', TemplateView.as_view(template_name="errors_templates/404_error.html"), name='404'),
    path('', include('charts.urls'))
]
