from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import  LinearRegression
import pandas as pd
import googletrans

translator = googletrans.Translator()
data = None
model = None
tfidf_vectorizer = TfidfVectorizer(max_features=5000)


# Load data from disk
def initialize():
    global data
    data = pd.read_csv("data.tsv", sep='\t')


# Train model
def train():
    global model
    tfidf_vectorizer.fit(data['title'])
    model = LinearRegression()
    model.fit(tfidf_vectorizer.transform(data['title']), data['score'])


# Make prediction
def sentimental_analyze(text: str):
    new_text_tfidf = tfidf_vectorizer.transform([text])
    return model.predict(new_text_tfidf)[0]
