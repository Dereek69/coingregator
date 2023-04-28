FROM python:3.7

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY app.py .
COPY redis_manager.py .

CMD ["uvicorn", "app:frontend", "--host", "0.0.0.0", "--port", "55555"]
