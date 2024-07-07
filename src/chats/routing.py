from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"sockets/chat/(?P<chat>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"sockets/hub/$", consumers.HubConsumer.as_asgi())
]