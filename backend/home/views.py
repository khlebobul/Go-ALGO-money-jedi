from rest_framework.response import Response
from rest_framework.decorators import api_view
from logic import news_parser, sentiment_analyzer
from model import main
from pandas import DataFrame
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


def init_news():
    sentiment_analyzer.initialize()
    sentiment_analyzer.train()


init_news()

# Init data base
cred = credentials.Certificate("goalgo-1170e-firebase-adminsdk-q2p4c-61dace46e1.json")
firebase_admin = firebase_admin.initialize_app(cred,
                                               {"databaseURL": "https://goalgo-1170e-default-rtdb.firebaseio.com/"})


# Create your views here.
@api_view(['Get'])
def getNews(request, ticker):
    ref = db.reference("news/")
    news, sources = news_parser.get_last_news_by_ticker(ticker)
    json_object = dict()
    json_object[ticker] = dict()
    json_object[ticker]["title"] = news
    json_object[ticker]["source"] = sources
    json_object[ticker]["sentiment"] = [json.dumps(sentiment_analyzer.sentimental_analyze(j)) for j in news]
    ref.update(json_object)
    return Response("Done")


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

    return Response(json.dumps(response))
