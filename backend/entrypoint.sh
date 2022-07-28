#!/bin/sh

echo "Make migrations"
python3 manage.py makemigrations

echo "Apply database migrations"
python3 manage.py migrate

echo "Run server"
python3 manage.py runserver 0.0.0.0:8001
