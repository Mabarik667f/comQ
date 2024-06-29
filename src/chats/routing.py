from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<chat>\w+)/$", consumers.ChatConsumer.as_asgi()),
    path("ws/hub/", consumers.HubConsumer.as_asgi())
]