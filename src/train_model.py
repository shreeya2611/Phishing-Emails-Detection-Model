import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Sample dataset (you can change later)
data = {
    "email": [
        "Win money now!!!",
        "Your account is secure",
        "Click this link to claim prize",
        "Meeting scheduled tomorrow",
        "Urgent: update your bank details",
        "Project discussion at 10am"
    ],
    "label": [0, 1, 0, 1, 0, 1]   # 0 = phishing, 1 = safe
}

df = pd.DataFrame(data)

# Split data
X = df["email"]
y = df["label"]

# Convert text to numbers
vectorizer = CountVectorizer()
X_vector = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression()
model.fit(X_vector, y)

# Save files
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ model.pkl and vectorizer.pkl created!")