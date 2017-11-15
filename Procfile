release: python manage.py migrate
web: gunicorn wsgi:application --log-file -
worker: celery -A project worker
