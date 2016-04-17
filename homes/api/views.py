from api.serializers import (PropertySerializer, FeatureSerializer,
                             FlagSerializer, ResolutionSerializer)
from api.filters import PropertyFilter
from api.models import (Property, Feature, Flag, Resolution)

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PropertyViewSet(viewsets.ModelViewSet):
    """Allows the read and write of Property objects.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permissions_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PropertyFilter


class FeatureViewSet(viewsets.ModelViewSet):
    """Allows the read and write of Feature objects.
    """
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permissions_classes = (IsAuthenticatedOrReadOnly,)


class FlagViewSet(viewsets.ModelViewSet):
    """Allows the read and write of new flag objects.
    """
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer
    permissions_classes = (IsAuthenticatedOrReadOnly,)


class ResolutionViewSet(viewsets.ModelViewSet):
    """Allows the read and write of resolution objects.
    """
    queryset = Resolution.objects.all()
    serializer_class = ResolutionSerializer
    permissions_classes = (IsAuthenticatedOrReadOnly,)


