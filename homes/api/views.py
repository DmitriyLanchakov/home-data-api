from django.shortcuts import render
from api.serializers import SimplePropertySerializer
from api.models import SimpleProperty
from rest_framework import viewsets

class SimplePropertyViewSet(viewsets.ModelViewSet):
    queryset = SimpleProperty.objects.all()
    serializer_class = SimplePropertySerializer

