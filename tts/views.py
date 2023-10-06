from datetime import datetime

import scipy.io.wavfile as wavfile
from django.conf import settings
from django.core.cache import cache
from rest_framework.request import Request
from rest_framework.views import APIView

from utils.responses import CustomResponse as cr
from tts.serializers import TTSTextSerializer
from utils.preprocess import preprocess
from tts.models import TTS


class TTSView(APIView):
    serializer_class = TTSTextSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        tts = TTS.objects.filter(newari_text=serializer.data.get("text")).first()
        if tts is not None:
            return cr.success(
                data=tts.speech_url,
                message="Converted to speech succesfully!",
            )

        textmapper = cache.get("textmapper")
        hparams = cache.get("hparams")
        device = cache.get("device")
        synthtrain = cache.get("synthtrain")

        data = preprocess(
            serializer.data.get("text"), textmapper, hparams, device, synthtrain
        )

        filename = f"media/{datetime.now().timestamp()}_audio.wav"
        wavfile.write(filename, hparams.data.sampling_rate, data)

        created = TTS.objects.create(
            newari_text=serializer.data.get("text"),
            speech_url=f"/{filename}",
        )

        return cr.success(
            data=created.speech_url,
            message="Converted to speech succesfully!",
        )
