FROM python:3.9.12-slim

RUN py -m pip install -U pip

WORKDIR /bot

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

CMD [ "uvicorn", "main:app"]
