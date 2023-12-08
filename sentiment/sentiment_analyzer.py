from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import  LinearRegression
from sklearn.metrics import mean_squared_error
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
    train, test = train_test_split(data, test_size=0.1, random_state=42)

    tfidf_vectorizer.fit(data['title'])

    model = LinearRegression()
    model.fit(tfidf_vectorizer.transform(train['title']), train['score'])

    print(mean_squared_error(test['score'], model.predict(tfidf_vectorizer.transform(test['title']))))


# Make prediction
def sentimental_analyze(text: str):
    new_text_tfidf = tfidf_vectorizer.transform([text])
    return model.predict(new_text_tfidf)[0]
