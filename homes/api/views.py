from django.shortcuts import render
from api.serializers import PropertySerializer, FeatureSerializer
from api.models import Property, Feature

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PropertyViewSet(viewsets.ModelViewSet):
    """Allows the read and write of Property objects.

    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permissions_classes = (IsAuthenticatedOrReadOnly,)


class FeatureViewSet(viewsets.ModelViewSet):
    """Allows the read and write of Feature objects.

    """

    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permissions_classes = (IsAuthenticatedOrReadOnly,)
