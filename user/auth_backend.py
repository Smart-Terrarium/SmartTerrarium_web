from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
import requests

'''Custom user auth backend'''

User = get_user_model()
API_URL = 'http://localhost:8000/'

class ExternalAPIBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        # Wysłanie zapytania do zewnętrznego API, aby zweryfikować użytkownika
        response = requests.post(API_URL + 'login', json={'email': email, 'password': password})

        # Sprawdzenie odpowiedzi i pobranie danych użytkownika, jeśli uwierzytelnienie się powiodło
        if response.status_code == 200:
            user_data = response.json()
            user, created = User.objects.get_or_create(email=email)

            # Aktualizacja danych użytkownika
            #user.first_name = user_data['first_name']
            #user.last_name = user_data['last_name']
            user.is_active = True
            user.save()

            # Pobranie tokena uwierzytelniającego z odpowiedzi API
            auth_token = user_data.get('access_token')

            # Zapisanie tokena uwierzytelniającego w sesji
            request.session['access_token'] = auth_token

            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
