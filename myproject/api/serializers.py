from rest_framework import serializers

class PredictionSerializer(serializers.Serializer):
    product = serializers.CharField()
    quantity = serializers.FloatField()
    price = serializers.FloatField()
    month = serializers.CharField()
    city = serializers.CharField()
    hour = serializers.IntegerField()
