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



@login_required
def get_more_animal_information(request, id):
    animal_url = f"http://localhost:8000/pet/{id}"  # URL dla informacji o zwierzęciu
    response = requests.get(animal_url)

    if response.status_code == 200:
        data = response.json()

        animal_info = {
            'id': data['pet']['id'],
            'name': data['pet']['name'],
            'description': data['pet']['description']
        }

        habitat_info = {
            'temperature': {
                'min': data['pet_habitat']['information']['temperature']['min'],
                'max': data['pet_habitat']['information']['temperature']['max']
            },
            'humidity': {
                'min': data['pet_habitat']['information']['humidity']['min'],
                'max': data['pet_habitat']['information']['humidity']['max']
            }
        }

        return render(request, 'animals_more_info.html', {'animal_info': animal_info, 'habitat_info': habitat_info})

    else:
        error_message = "An error occurred while fetching data."
        return JsonResponse({'error_message': error_message})