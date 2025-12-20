from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime


def init_db_task_fn():
    import sys
    sys.path.insert(0, '/app')
    from tasks.postgress_db import init_db
    init_db()


def pipeline_task_fn():
    import sys
    sys.path.insert(0, '/app')
    from tasks.generate_tweets import fetch_tweets
    from tasks.predict_sentiment import predict_batch
    from tasks.postgress_db import store_predictions

    tweets = fetch_tweets(batch_size=20)
    predictions = predict_batch(tweets)
    store_predictions(predictions)


with DAG(
    dag_id="aerostream_streaming_pipeline",
    start_date=datetime(2025, 12, 19),
    schedule="*/1 * * * *",
    catchup=False,
) as dag:

    init_db_task = PythonOperator(
        task_id="init_postgres",
        python_callable=init_db_task_fn
    )

    run_pipeline = PythonOperator(
        task_id="fetch_predict_store",
        python_callable=pipeline_task_fn
    )

    init_db_task >> run_pipeline
