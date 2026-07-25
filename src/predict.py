import pickle

# Load saved model and vectorizer
model = pickle.load(open("models/model.pkl", "rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))

# Test email
email = ["Congratulations! You won a free iPhone. Click here now"]

# Convert text → numbers
email_vector = vectorizer.transform(email)

# Predict
prediction = model.predict(email_vector)

# Output
if prediction[0] == 1:
    print("⚠️ Phishing Email Detected")
else:
    print("✅ Safe Email")