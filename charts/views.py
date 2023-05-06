from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'charts.html', context={'text': 'Hello world'})