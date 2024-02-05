FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

RUN pip install django
COPY . .

EXPOSE 8000
