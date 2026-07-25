import pandas as pd
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    return text

def load_data(path):
    df = pd.read_csv(path)
    df['clean_text'] = df['text'].apply(clean_text)
    return df