FROM python:3.9-slim

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
EXPOSE 5000
ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "application:app"]
