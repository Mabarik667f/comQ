from django.urls import path
from .views import *

urlpatterns = [
    path('group-chat-detail/<int:pk>/', GroupChatRetrieveView.as_view(), name="group-chat-detail"),
    path('chat-detail/<int:pk>/', ChatRetrieveView.as_view(), name='chat-detail'),

    path('group-settings/<int:pk>/', GroupSettingsRetrieveView.as_view(), name='group-settings'),

    path('create-group/', CreateGroupChatView.as_view(), name='create-group'),
    path('create-private/', CreatePrivateChatView.as_view(), name='create-private'),

]