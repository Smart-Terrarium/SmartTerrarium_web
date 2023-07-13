from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from requests import RequestException

from .models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import requests

API_URL = 'http://localhost:8000/'


@csrf_exempt
def register_user(request):
    if request.user.is_authenticated:  # Sprawdza, czy użytkownik jest zalogowany
        return redirect('charts')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            if email and password:
                response = requests.post(API_URL + 'register', json={'email': email, 'password': password})
                if response.status_code == 201:
                    user = User.objects.create_user(email, password)
                    return redirect('login')
                else:
                    message = 'Unable to create user.'
            else:
                message = 'Email and password are required.'
        else:
            message = ''
            return render(request, 'register.html', {'message': message})
        return render(request, 'register.html', {'message': message})


'''
def authenticate_user(email, password):
    response = requests.post(API_URL + 'login', json={'email': email, 'password': password})

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        return None

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        access_token = authenticate_user(email, password)

        if access_token:
            user = authenticate(request, token = access_token)
            if user is not None:
                login(request, user)
                return redirect('home')
        message = access_token
    else:
        message = 'cos sie nie udalo'
    #return render(request, 'login.html')
    return render(request, 'login.html', {'message': message})
'''



def home_view(request):
    access_token = request.session.get('access_token')

    context = {
        'access_token': access_token
    }

    bearer_token = request.session.get('access_token')
    headers = {
        'Authorization': 'Bearer ' + bearer_token,
    }

    try:
        devices_response = requests.get('http://localhost:8000/devices/', headers=headers)
        if devices_response.ok:
            response_json = devices_response.json()
            context['response_json'] = response_json
        else:
            context['error_message'] = 'Connection lost. Please log in again to see your devices.'
    except RequestException:
        context['error_message'] = 'Connection lost. Please log in again to see your devices.'

    return render(request, 'home.html', context)


def login_view(request):
    if request.user.is_authenticated:  # Sprawdza, czy użytkownik jest zalogowany
        return redirect('charts')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            # Uwierzytelnij użytkownika z użyciem customowego backendu uwierzytelnienia
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

        return render(request, 'login.html')


def forgot_password(request):
    if request.user.is_authenticated:
        return redirect('charts')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            if email:
                response = requests.post(API_URL + 'login/forgot-password', json={'email': email})
                if response.status_code == 200:
                    return redirect('login')
                else:
                    message = 'Unable to reset password, wrong email address'
            else:
                message = 'Set your email address'
        else:
            message = ''
            return render(request, 'forgot_password.html', {'message': message})
    return render(request, 'forgot_password.html', {'message': message})
