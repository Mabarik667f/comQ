from django.urls import path
from .views import *

urlpatterns = [
    path('chat-detail/<int:pk>', ChatRetrieveView.as_view(), name='chat-detail')
]