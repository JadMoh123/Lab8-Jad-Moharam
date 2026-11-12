# Lab 5 - Postman and APIs, served on port 5000
FROM python:3.12-alpine

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000
CMD ["python3", "app.py"]
