from django.urls import path
from .consumers import ChartsConsumer

websocket_urlpatterns = [
    path('ws/charts/', ChartsConsumer.as_asgi())
]
