from django.urls import path
from .views import *

urlpatterns = [
    path('chat-detail/<int:pk>/', ChatRetrieveView.as_view(), name='chat-detail'),
    path('group-chat-detail/<int:pk>/', GroupChatRetrieveView.as_view(), name="group-chat-detail"),
    path('group-settings/<int:pk>/', GroupSettingsRetrieveUpdateView.as_view(), name='group-settings'),
    path('group-settings-has-user/', GroupSettingsHasUserView.as_view(), name='group-settings-has-user'),

    path('create-group/', CreateGroupChatView.as_view(), name='create-group'),
    path('create-private/', CreatePrivateChatView.as_view(), name='create-private'),

]