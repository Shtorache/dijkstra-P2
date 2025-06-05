from rest_framework import serializers

class PointSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

class RouteSerializer(serializers.Serializer):
    path = serializers.ListField(
        child=serializers.ListField(child=serializers.FloatField())
    )