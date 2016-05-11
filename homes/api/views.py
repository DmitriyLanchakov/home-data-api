from api.serializers import (PropertySerializer, FeatureSerializer,
                             FlagSerializer, ResolutionSerializer,
                             UserSerializer)
from api.filters import PropertyFilter
from api.models import (Property, Feature, Flag, Resolution)
from django.contrib.auth import get_user_model
from api.permissions import SignUpPermission

from rest_framework import viewsets, filters, mixins

class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Allows a user to sign up by pushing data to this endpoint.
    
    This will also fail for an authenticated user.

    Data to push is username, password, first_name, last_name, email
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (SignUpPermission,)

class PropertyViewSet(viewsets.ModelViewSet):
    """Allows the read and write of Property objects.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PropertyFilter


class FeatureViewSet(viewsets.ModelViewSet):
    """Allows the read and write of Feature objects.
    """
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FlagViewSet(viewsets.ModelViewSet):
    """Allows the read and write of new flag objects.
    """
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer


class ResolutionViewSet(viewsets.ModelViewSet):
    """Allows the read and write of resolution objects.
    """
    queryset = Resolution.objects.all()
    serializer_class = ResolutionSerializer


