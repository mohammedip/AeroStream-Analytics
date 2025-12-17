from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer

app = FastAPI(
    title="AeroStream Sentiment Analysis API",
    version="1.0"
)

model = joblib.load("rf_model.pkl")
embedder = SentenceTransformer("paraphrase-MiniLM-L6-v2")

class ReviewRequest(BaseModel):
    text: str

@app.get("/")
def health_check():
    return {"status": "API running"}

@app.post("/predict")
def predict_sentiment(request: ReviewRequest):
    embedding = embedder.encode([request.text])
    probs = model.predict_proba(embedding)[0]

    pred_idx = int(np.argmax(probs))
    sentiment = model.classes_[pred_idx]

    return {
        "sentiment": sentiment,
        "probabilities": {
            model.classes_[i]: float(probs[i])
            for i in range(len(probs))
        }
    }
