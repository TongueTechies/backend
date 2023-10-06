from django.urls import path

from tts.views import TTSView

urlpatterns = [path("", TTSView.as_view(), name="tts")]
