from django.shortcuts import render
from rest_framework import generics
from .serializers import *


class ChatRetrieveView(generics.RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = 'pk'