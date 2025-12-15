FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# NLP models
RUN python -m spacy download en_core_web_sm

# Airflow config
ENV AIRFLOW_HOME=/app/airflow

EXPOSE 8888 8501 8080

CMD ["bash"]
