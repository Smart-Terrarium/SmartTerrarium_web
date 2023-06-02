from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
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
                    return JsonResponse({'success': True, 'message': 'User created successfully.'})
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
