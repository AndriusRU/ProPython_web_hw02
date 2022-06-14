import requests
import bs4
import re
from data.data import HEADERS

class Article:

    def __init__(self, url):
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        text = response.text
        soup = bs4.BeautifulSoup(text, features='html.parser')
        self.desc = soup.find(class_="tm-article-presenter__content tm-article-presenter__content_narrow")
        self.link = url

    def get_title(self):
        result = self.desc.find("h1").find("span")
        if not result:
            result = ""
        else:
            result = result.text

        return result

    def get_date(self):
        return self.desc.find(class_="tm-article-snippet__datetime-published").find("time").attrs["title"]

    def get_user(self):
        result = self.desc.find(class_="tm-user-info__username")
        if not result:
            result = ""
        else:
            result = result.text

        return result

    def get_hubs(self):
        result = ""
        list_text = self.desc.find_all(class_="tm-hubs-list__link")
        for elem in list_text:
            result += elem.text

        temp_text = self.desc.find(class_="tm-hubs-list__link router-link-active")
        if temp_text:
            result += temp_text.text

        return result

    def get_tags(self):
        result = ""
        list_text = self.desc.find_all(class_="tm-tags-list__link")
        for elem in list_text:
            result = result + elem.text + " "

        return result.strip()

    def get_body(self):
        return self.desc.find(class_="tm-article-body").text


