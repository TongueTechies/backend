from django.urls import path

from translation.views import (
    SavedTranslationView,
    TranslateNewariView,
    TranslateEnglishView,
)

urlpatterns = [
    path("translate/newari/", TranslateNewariView.as_view()),
    path("translate/english/", TranslateEnglishView.as_view()),
    path("saved-translations/", SavedTranslationView.as_view()),
]
