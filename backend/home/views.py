from rest_framework.response import Response
from rest_framework.decorators import api_view
from logic import news_parser, sentiment_analyzer
from model import main
from pandas import DataFrame

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
def getGraphData(request, ticker, hours):
    response = dict()
    df1 = DataFrame()
    df2 = DataFrame()
    df1, df2 = main.generate_predictions(ticker, hours)
    end1 = df1['end'].tolist()
    end2 = df2['end'].tolist()
    close1 = df1['close'].tolist()
    close2 = df2['close'].tolist()

    end = []
    close = []
    for date in end1:
        end.append(date.strftime('%Y-%m-%d %X'))
    for date in end2:
        end.append(date.strftime('%Y-%m-%d %X'))
    for amount in close1:
        close.append(amount)
    for amount in close2:
        close.append(amount)

    response = dict()
    for i in range(len(end)):
        response[end[i]] = close[i]

    return Response(response)
