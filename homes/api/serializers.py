from rest_framework import serializers
from api.models import Property, Feature, Flag, Resolution

class PropertySerializer(serializers.ModelSerializer):
    submitter = serializers.PrimaryKeyRelatedField(read_only=True, 
            default=serializers.CurrentUserDefault())
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ('geocoded_address',)


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
