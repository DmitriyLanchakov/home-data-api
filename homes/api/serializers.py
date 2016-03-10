from rest_framework import serializers
from api.models import SimpleProperty, Property

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ('geocoded_address',)


class SimplePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleProperty
        fields = '__all__'
