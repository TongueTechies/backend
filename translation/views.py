from rest_framework.views import APIView

from translation.serializers import TextSerializer
from .apps import (
    newari_transformer,
    newari_translator,
    english_translator,
    english_transformer
)

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
