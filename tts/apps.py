from django.apps import AppConfig
from django.core.cache import cache

from utils.preprocess import check


class TtsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tts"

    def ready(self) -> None:
        textmapper, hparams, device, synthtrain = check("tts/tts-model")
        cache.set("textmapper", textmapper, None)
        cache.set("hparams", hparams, None)
        cache.set("device", device, None)
        cache.set("synthtrain", synthtrain, None)
