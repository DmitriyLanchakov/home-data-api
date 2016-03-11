from rest_framework import serializers
from api.models import SimpleProperty, Property, Feature

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ('geocoded_address',)


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class SimplePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleProperty
        fields = '__all__'
