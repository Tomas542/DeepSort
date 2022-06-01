FROM python:3.9

WORKDIR /WebApp

ENV FLASK_APP app.py

COPY  . .

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN pip install -r requirements.txt

EXPOSE 8080