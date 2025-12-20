import requests

PREDICT_API_URL = "http://aerostream_api:8001/predict"

def predict_tweet(tweet: dict) -> dict:

    payload = {"text": tweet["text"]}

    response = requests.post(
        PREDICT_API_URL,
        json=payload,
        timeout=10
    )
    response.raise_for_status()

    prediction = response.json()

    return {
        **tweet,
        "predicted_sentiment": prediction["sentiment"],
        "sentiment_probabilities": prediction["probabilities"]
    }


def predict_batch(tweets: list[dict]) -> list[dict]:
    return [predict_tweet(tweet) for tweet in tweets]
