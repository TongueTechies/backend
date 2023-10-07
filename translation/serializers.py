from rest_framework import serializers

from translation.models import SavedTranslation


class TextSerializer(serializers.Serializer):
    text = serializers.CharField()


class SavedTranslationSerializer(serializers.Serializer):
    newari_text = serializers.CharField()
    english_text = serializers.CharField()


class STModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedTranslation
        fields = ("english_text", "newari_text")
