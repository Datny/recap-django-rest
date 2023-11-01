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
        django-user

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
      then pip3 install -r /tmp/requirements.dev.txt ; \
    fi
RUN apt update -y && \
    apt install -y postgresql postgresql-contrib
USER django-user