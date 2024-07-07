"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from chats import routing
from users.middleware import JWTAuthMiddleWareStack


application = ProtocolTypeRouter({
    'websocket': JWTAuthMiddleWareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )}
)
