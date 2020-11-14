FROM python:3.9.0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /django_news
COPY . .

RUN apt-get update -y \
    && apt-get install -y gettext \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --upgrade pip \
	&& pip install -r requirements.txt \
	&& pip install uwsgi
