FROM python:3.10
LABEL mainteiner="datny"


ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000


ARG DEV=false
RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
      then pip3 install -r /tmp/requirements.dev.txt ; \
    fi
RUN apt update -y && \
    apt install -y postgresql postgresql-contrib
RUN apt-get -y install python3-dev python3-setuptools

USER django-user