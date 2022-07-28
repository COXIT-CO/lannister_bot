FROM python:3.10-alpine3.15

ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY . ./
COPY requirements.txt .
RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY entrypoint.sh /app
RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8001"]
