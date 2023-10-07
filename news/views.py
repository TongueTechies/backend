import requests
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from utils.responses import CustomResponse as cr

BASE_URL = "https://nepalbhasatimes.com"


class NewsView(APIView):
    def get(self, request: Request) -> Response:
        response = requests.get(BASE_URL)
        soup = BeautifulSoup(response.content, "html.parser")
        div_elements = soup.find_all("div", {"class": "post-detail12"})
        news_list = []

        for div_element in div_elements:
            a_element = div_element.find("a", {"itemprop": "url"})
            img_element = div_element.find("img")

            if a_element and img_element and "src" in img_element.attrs:
                article_title = a_element.get("title", "No title available")
                article_link = a_element["href"]
                thumbnail_url = img_element["src"]

                news_data = {
                    "title": article_title,
                    "link": article_link,
                    "thumbnail_url": thumbnail_url,
                }
                news_list.append(news_data)

        return cr.success(data=news_list, message="News fetched successfully!")
