FROM python:3.9.12-slim

RUN python -m pip install -U pip

WORKDIR /bot

COPY req.txt req.txt

RUN pip install -r req.txt

COPY . .

CMD [ "uvicorn", "main:app"]
