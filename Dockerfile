FROM python:3.8-buster

ENV DJANGO_SETTINGS_MODULE conf.settings.prod
VOLUME /data

WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 80
ENTRYPOINT ./run.sh
