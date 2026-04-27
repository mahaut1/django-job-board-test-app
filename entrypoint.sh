#!/bin/sh
set -e

echo "Upload des assets vers Azure..."
python initialize_azure.py

echo "Collectstatic..."
python manage.py collectstatic --noinput

echo "Migrations..."
python manage.py migrate --noinput

echo "Lancement Gunicorn..."
exec gunicorn job_board.wsgi:application --bind 0.0.0.0:8000 --workers 2