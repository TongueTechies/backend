from rest_framework.views import APIView
from translation.models import SavedTranslation

from translation.serializers import (
    STModelSerializer,
    SavedTranslationSerializer,
    TextSerializer,
)
from .apps import (
    newari_transformer,
    newari_translator,
    english_translator,
    english_transformer,
)
from rest_framework.permissions import IsAuthenticated

from utils.responses import CustomResponse as cr


class TranslateNewariView(APIView):
    serializer_class = TextSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        translated_text = newari_translator.translate(
            newari_transformer, serializer.validated_data.get("text")
        )

        return cr.success(
            data={"translated_text": translated_text.strip()},
            message="Text translated successfully!",
        )


class TranslateEnglishView(APIView):
    serializer_class = TextSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        translated_text = english_translator.translate(
            english_transformer, serializer.validated_data.get("text")
        )

        return cr.success(
            data={"translated_text": translated_text.strip()},
            message="Text translated successfully!",
        )


class SavedTranslationView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SavedTranslationSerializer
    st_serializer_class = STModelSerializer

    def get(self, request):
        saved_translations = SavedTranslation.objects.filter(user=request.user).all()

        serializer = self.st_serializer_class(instance=saved_translations, many=True)

        return cr.success(
            data=serializer.data, message="Translations fetched successfully!"
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        newari_text = serializer.validated_data.get("newari_text")
        english_text = serializer.validated_data.get("english_text")

        SavedTranslation.objects.create(
            newari_text=newari_text, english_text=english_text, user=request.user
        )

        return cr.success(message="Translation saved successfully!")
