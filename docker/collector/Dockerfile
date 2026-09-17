FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY collector ./collector
COPY database ./database

CMD ["python", "-u", "-m", "collector.main"]
