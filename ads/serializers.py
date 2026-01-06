from rest_framework import serializers
from . import models

class AdSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    provider = serializers.ReadOnlyField(source='provider.username')
    class Meta:
        model = models.Ad
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'status', 'provider']


class AdAssignSerializer(serializers.ModelSerializer):
    provider_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = models.Ad
        fields = ['provider_id']