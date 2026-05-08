from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier

# Training data
errors = [
    "division by zero",
    "list index out of range",
    "file not found",
    "connection timeout",
    "null pointer exception",
    "database connection failed",
    "memory overflow",
    "syntax error"
]

# Labels
labels = [
    "Math Error",
    "List Error",
    "File Error",
    "Network Error",
    "Null Reference Error",
    "Database Error",
    "Memory Error",
    "Code Syntax Error"
]

# AI Suggestions
solutions = {

    "Math Error":
    "Validate denominator before performing division.",

    "List Error":
    "Check list size before accessing elements.",

    "File Error":
    "Verify file path and existence before reading.",

    "Network Error":
    "Check network connectivity and timeout settings.",

    "Null Reference Error":
    "Initialize objects before usage.",

    "Database Error":
    "Verify database server status and credentials.",

    "Memory Error":
    "Optimize memory allocation and close unused resources.",

    "Code Syntax Error":
    "Review syntax and code formatting carefully."
}

# Convert text into vectors
vectorizer = CountVectorizer()

X = vectorizer.fit_transform(errors)

# Train model
model = DecisionTreeClassifier()

model.fit(X, labels)

# Prediction function
def predict_error(error_text):

    transformed = vectorizer.transform([error_text])

    prediction = model.predict(transformed)[0]

    solution = solutions[prediction]

    return prediction, solution