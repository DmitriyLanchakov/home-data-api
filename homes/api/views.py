from django.shortcuts import render
from api.serializers import SimplePropertySerializer, PropertySerializer, FeatureSerializer
from api.models import SimpleProperty, Property, Feature
from rest_framework import viewsets

class SimplePropertyViewSet(viewsets.ModelViewSet):
    queryset = SimpleProperty.objects.all()
    serializer_class = SimplePropertySerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
