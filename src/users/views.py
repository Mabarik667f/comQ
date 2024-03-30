from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics

from .models import CustomUser
from .serializers import UserSerializer


class UserListView(generics.ListAPIView):
    pass


class UserListOnChat(generics.ListAPIView):
    pass


class UserRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    pass


