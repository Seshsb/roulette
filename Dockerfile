FROM python:3.11.4

RUN mkdir "/roulette"

WORKDIR /roulette

COPY requirements.txt .

RUN pip install -requirements.txt

COPY . .

WORKDIR /src

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
