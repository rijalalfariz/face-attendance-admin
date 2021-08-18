from rest_framework import serializers

from misweb import models


class TestSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)

class AbsensiSerializer(serializers.ModelSerializer):
    """Serializes a name field for testing our APIView"""

    class Meta:
        model = models.Absensi
        fields = ('id', 'employee', 'kamera', 'first_seen', 'last_seen')    
