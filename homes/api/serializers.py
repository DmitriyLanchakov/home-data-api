from rest_framework import serializers
from api.models import Address, Property, Feature, Flag, Resolution
from django.contrib.auth import get_user_model
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    """Used for sign up of users.
    """
    password = serializers.CharField(
                style={'input_type': 'password'},
                write_only=True
                )
    
    email = serializers.EmailField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        write_only_fields = ('password')

    def create(self, validated_data):
        """Create a user and set the password correctly.
        """
        password = validated_data.pop('password')
        user = get_user_model()(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    submitter = serializers.PrimaryKeyRelatedField(read_only=True, 
            default=serializers.CurrentUserDefault())
    address_object = AddressSerializer(read_only=True)
    class Meta:
        model = Property
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class FlagSerializer(serializers.ModelSerializer):
    submitter = serializers.PrimaryKeyRelatedField(read_only=True, 
            default=serializers.CurrentUserDefault())
    class Meta:
        model = Flag
        fields = '__all__'


class ResolutionSerializer(serializers.ModelSerializer):
    resolver = serializers.PrimaryKeyRelatedField(read_only=True, 
            default=serializers.CurrentUserDefault())
    class Meta:
        model = Resolution
        fields = '__all__'
