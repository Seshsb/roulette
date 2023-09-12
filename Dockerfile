FROM python:3.11.4

RUN mkdir "/roulette"

WORKDIR /roulette

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x *.sh