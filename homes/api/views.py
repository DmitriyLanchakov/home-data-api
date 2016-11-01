from api.serializers import (PropertySerializer, FeatureSerializer,
                             FlagSerializer, ResolutionSerializer,
                             UserSerializer, AddressSerializer)
from api.filters import PropertyFilter
from api.models import (Property, Feature, Flag, Resolution, Profile, Address)
from api.permissions import SignUpPermission

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import viewsets, filters, mixins, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Allows a user to sign up by pushing data to this endpoint.
    
    This will also fail for an authenticated user.

    Data to push is username, password, first_name, last_name, email
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (SignUpPermission,)


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


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


@api_view(['GET'])
@permission_classes((AllowAny,))
def confirm_code(request, id, code):
    """Provides an endpoint to confirm a users account.

    Users cannot do anything but GET until accounts are confirmed.
    """
    profile = Profile.objects.filter(id=id, confirmation_code=code)

    if len(profile) == 0:
        return Response({"message":"Inocrrect User or Confirmation Code"},
                         status=status.HTTP_400_BAD_REQUEST)

    profile = profile[0]

    if profile.can_confirm():
        profile.confirmed = True
        profile.save()
        g = Group.objects.get(name='pushing')
        g.user_set.add(profile.user)
        return Response({"message":"OK"})
    else:
        return Response({"message":"Confirmation Code Expired or Account already Active"},
                         status=status.HTTP_400_BAD_REQUEST)

    
