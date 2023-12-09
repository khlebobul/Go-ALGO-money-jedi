from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from logic import news_parser, sentiment_analyzer


def init_news():
    sentiment_analyzer.initialize()
    sentiment_analyzer.train()


init_news()


# Create your views here.

@api_view(['GET'])
def getNews(request, ticker="MOEX"):
    response = list()
    news, sources = news_parser.get_last_news_by_ticker(ticker)
    for i in range(len(news)):
        response.append([])
        response[-1].append(news[i])
        response[-1].append(sources[i])
        response[-1].append(sentiment_analyzer.sentimental_analyze(news[i]))
    return Response(response)

@api_view(['GET'])
def getGraphData(request, ticker="MOEX"):
    response = dict()
    return Response(response)
