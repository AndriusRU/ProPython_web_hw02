import requests
import bs4
from article import Article
from data.data import HEADERS
from data.data import KEYWORDS


base_url = "https://habr.com"
url = base_url + "/ru/all/"


def search_words(article, preview):
    body = article.get_body()
    date = article.get_date()
    user = article.get_user()
    tags = article.get_tags()
    hubs = article.get_hubs()
    title = article.get_title()
    link = article.link
    for elem in KEYWORDS:
        if elem in date \
                or elem in user \
                or elem in title \
                or elem in body \
                or elem in tags \
                or elem in hubs \
                or elem in preview:
            print(f"{date} - {title} - {link}")
            break


if __name__ == '__main__':
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    text = response.text
    soup = bs4.BeautifulSoup(text, features='html.parser')

    articles = soup.find_all('article')

    for article in articles:
        preview_text = article.find(class_="tm-article-body tm-article-snippet__lead")
        if preview_text:
            preview_text = preview_text.text
        else:
            preview_text = ""

        link = base_url + article.find(class_="tm-article-snippet__title-link").attrs["href"]
        article = Article(link)

        search_words(article, preview_text)
