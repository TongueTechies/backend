from django.db import models


class TTS(models.Model):
    newari_text = models.CharField(max_length=200)
    speech_url = models.CharField(max_length=200)
