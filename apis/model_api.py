from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
import re

app = FastAPI(
    title="AeroStream Sentiment Analysis API",
    version="1.0"
)

model = joblib.load("/app/models/svm_sentiment_model.pkl")
embedder = SentenceTransformer("cardiffnlp/twitter-roberta-base-sentiment")

class ReviewRequest(BaseModel):
    text: str

@app.get("/")
def health_check():
    return {"status": "API running"}

@app.post("/predict")
def predict_sentiment(request: ReviewRequest):

    if not isinstance(request.text, str):
        text = ''
    else:    
        text = re.sub(r'http+', '', request.text)
        text = re.sub(r'@+', '', text)
        text = re.sub(r'[^A-Za-z0-9]', ' ', text)
        text = text.lower().strip()


    embedding = embedder.encode([text])
    probs = model.predict_proba(embedding)[0]

    pred_idx = int(np.argmax(probs))
    sentiment = model.classes_[pred_idx]

    return {
        "text" : request.text,
        "sentiment": sentiment,
        "probabilities": {
            model.classes_[i]: float(probs[i])
            for i in range(len(probs))
        }
    }
