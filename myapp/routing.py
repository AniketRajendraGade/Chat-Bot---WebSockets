# myapp/routing.py
from myapp.consumers import ChatConsumer
from django.urls import re_path



websocket_urlpatterns = [
    re_path(r"ws/chatbot", ChatConsumer.as_asgi()),
]
