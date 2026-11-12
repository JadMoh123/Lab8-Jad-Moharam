# get_users API, served on port 3000
FROM python:3.12-alpine

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 3000
CMD ["python3", "app.py"]
