import requests
from bs4 import BeautifulSoup as bs


# Function that returns list of news titles by ticker
def get_last_news_by_ticker(ticker: str):
    URL_TEMPLATE = "https://www.tinkoff.ru/invest/stocks/" + ticker + "/news/"
    r = requests.get(URL_TEMPLATE, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"})
    r.encoding = "utf8"
    soup = bs(r.text, "html.parser")
    divs = soup.find_all("div")
    news = []
    for i in divs:
        if i.has_attr("class"):
            if "pulse-news-by-ticker" in i["class"][0]:
                if i.has_attr("data-qa-file"):
                    if i["data-qa-file"] == "PulseReviewAndNewsBody":
                        if len(i.text) != 0:
                            news.append(i.text)
    return news
