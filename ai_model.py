import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.naive_bayes import MultinomialNB


# LOAD DATASET

data = pd.read_csv('failure_dataset.csv')


# INPUT + OUTPUT

X = data['error_message']

y = data['cause']


# TEXT VECTORIZATION

vectorizer = CountVectorizer()

X_vectorized = vectorizer.fit_transform(X)


# TRAIN MODEL

model = MultinomialNB()

model.fit(X_vectorized, y)


# PREDICTION FUNCTION

def predict_failure(error_message):

    transformed = vectorizer.transform([error_message])

    prediction = model.predict(transformed)

    return prediction[0]