import pandas as pd
import joblib
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Create models folder
os.makedirs("models", exist_ok=True)

# Load dataset
df = pd.read_csv("datasets/phishing_emails.csv")

# Features
X = df["text"]

# Labels
y = df["label"]

# Vectorizer
vectorizer = CountVectorizer()

X_vectorized = vectorizer.fit_transform(X)

# Model
model = MultinomialNB()

# Train
model.fit(X_vectorized, y)

# Save model
joblib.dump(model, "models/phishing_model.pkl")

# Save vectorizer
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("Training Completed Successfully")


