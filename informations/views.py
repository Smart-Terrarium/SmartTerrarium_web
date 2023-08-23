from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
import requests
from core import settings
from informations.models import BasicAnimalInformation

URL = settings.API_URL

@login_required
def get_basic_animal_information(request):
    url = URL + "pets"  # Adres URL do żądania GET
    response = requests.get(url)

    if response.status_code == 200:
        animal_data = response.json()

        # Tworzenie instancji modelu BasicAnimalInformation dla sortowania
        animal_instances = [
            BasicAnimalInformation(id=animal['id'], name=animal['name'], description=animal['description'])
            for animal in animal_data
        ]

        sorted_animal_instances = sorted(animal_instances, key=lambda animal: animal.name)

        sorted_animal_data = [
            {
                'id': animal.id,
                'name': animal.name,
                'description': animal.description
            }
            for animal in sorted_animal_instances
        ]

        return render(request, 'pets.html', {'animal_data': sorted_animal_data})
    else:
        error_message = "An error occurred while fetching data."
        return render(request, 'pets.html', {'error_message': error_message})