import sqlite3
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

# DATABASE

conn = sqlite3.connect("failures.db")

query = """

SELECT

    error_message,
    predicted_cause

FROM failures

"""

df = pd.read_sql_query(query, conn)

conn.close()

# TRAIN DATA

X = df["error_message"]

y = df["predicted_cause"]

# TEXT VECTORIZATION

vectorizer = CountVectorizer()

X_vectorized = vectorizer.fit_transform(X)

# MODEL

model = RandomForestClassifier()

model.fit(X_vectorized, y)

# PREDICTION FUNCTION

def predict_failure(error_message):

    transformed = vectorizer.transform(

        [error_message]

    )

    prediction = model.predict(

        transformed

    )

    return prediction[0]