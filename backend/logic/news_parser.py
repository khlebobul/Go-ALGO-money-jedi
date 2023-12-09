import requests
from bs4 import BeautifulSoup as bs


# Function that returns list of news titles by ticker
def get_last_news_by_ticker(ticker: str):
    URL_TEMPLATE = "https://www.tinkoff.ru/invest/stocks/" + ticker + "/news/"
    r = requests.get(URL_TEMPLATE, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"})
    r.encoding = "utf8"
    soup = bs(r.text, "html.parser")
    posts = soup.find_all("div")
    news = []
    sources = []
    for i in posts:
        if i.has_attr("data-qa-tag"):
            if i["data-qa-tag"] == "PulseReviewAndNewsBody":
                sources.append("https://www.tinkoff.ru"+i.find("a")["href"])
                for j in i.find("a").find_all("div"):
                    if j.has_attr("class"):
                        if "pulse-news-by-ticker" in j["class"][0]:
                            if j.has_attr("data-qa-file"):
                                if j["data-qa-file"] == "PulseReviewAndNewsBody":
                                    if len(j.text) != 0:
                                        news.append(j.text)
                                        break
    return news, sources
