from django.urls import path

from translation.views import TranslateNewariView

urlpatterns = [
    path("translate/newari/", TranslateNewariView.as_view()),
    # path("translate/english/", TranslateEnglishView.as_view()),
]
