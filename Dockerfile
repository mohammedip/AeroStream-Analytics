FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    bash \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# NLP models
RUN python -m spacy download en_core_web_sm

# Airflow base config
ENV AIRFLOW_HOME=/app/airflow
ENV PATH="$AIRFLOW_HOME/.local/bin:$PATH"
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor

EXPOSE 8888 8501 8080 8001 8002 8000

CMD ["bash"]
