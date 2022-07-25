FROM python:3.10-alpine3.15

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app

COPY ./frontend/ /app
COPY requirements.txt /app
COPY .env /app
RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev 

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]