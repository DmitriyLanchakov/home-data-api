from django.shortcuts import render
from api.serializers import SimplePropertySerializer, PropertySerializer
from api.models import SimpleProperty, Property
from rest_framework import viewsets

class SimplePropertyViewSet(viewsets.ModelViewSet):
    queryset = SimpleProperty.objects.all()
    serializer_class = SimplePropertySerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
