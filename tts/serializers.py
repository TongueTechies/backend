from rest_framework import serializers


class TTSTextSerializer(serializers.Serializer):
    text = serializers.CharField()
