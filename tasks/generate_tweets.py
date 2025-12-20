import requests

GENERATOR_API_URL = "http://aerostream_api2:8002/batch"

def fetch_tweets(batch_size: int = 10) -> list[dict]:

    response = requests.get(
        GENERATOR_API_URL,
        params={"batch_size": batch_size},
        timeout=10
    )
    response.raise_for_status()
    return response.json()
