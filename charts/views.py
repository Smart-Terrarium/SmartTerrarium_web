from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'charts.html', context={'text': 'Hello world'})

"""
Jest to kod Pythonowy, używany do pyChart.js z pliku charts/connection.py

label_array = []
data_array = []
dict_values = {}

def index(request):

    NewChart = MyBarGraph()


    NewChart.data.label = "My Favourite Numbers"      # can change data after creation


    ChartJSON = NewChart.get()

    return render(request=request,
                  template_name='charts.html',
                  context={"chartJSON": ChartJSON})


"""