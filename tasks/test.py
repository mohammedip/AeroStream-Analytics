import sys
import time

# Make sure Python sees /app
sys.path.insert(0, "/app")

from tasks.postgress_db import init_db, store_predictions
from tasks.generate_tweets import fetch_tweets
from tasks.predict_sentiment import predict_batch


def run_pipeline(batch_size=20):
    tweets = fetch_tweets(batch_size=batch_size)
    predictions = predict_batch(tweets)
    store_predictions(predictions)


if __name__ == "__main__":
    print("🔧 Initializing database...")
    init_db()

    print("🚀 Running pipeline 100 times...\n")

    for i in range(1, 101):
        print(f"▶️ Run {i}/100")
        try:
            run_pipeline(batch_size=20)
        except Exception as e:
            print(f"❌ Error on run {i}: {e}")

        # optional: avoid hammering APIs
        time.sleep(0.5)

    print("\n✅ Done! 100 runs completed.")
