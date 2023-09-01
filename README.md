# SmartTerrarium Django Web App

## Launching the application

optional creation of a virtual environment
```bash
py -m venv venv
venv/Scripts/activate
```
download packages from requirements.txt file
```bash
pip install -r requirements.txt
```
run app server
```bash
python manage.py runserver PORT #for example 7000
```
## Change External API url / enabling debug mode
In the application's "core" folder, there is a "settings.py" file. There is an API_URL variable in it, changing it will result in changing it in every function, except for the "templates/charts.html" file.As for DEBUG mode, there is also a "DEBUG" variable in the settings file, which you just need to change to True.

```
├── core
│   ├── settings.py
│ 
├── templates
│   ├── charts.html
```
