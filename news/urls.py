from django.urls import path

from news.views import NewsView


urlpatterns = [path("", NewsView.as_view(), name="news")]
