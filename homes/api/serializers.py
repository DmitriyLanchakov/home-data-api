from rest_framework import serializers
from api.models import SimpleProperty


class SimplePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleProperty
        fields = '__all__'
