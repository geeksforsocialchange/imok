web: gunicorn imok.wsgi:application

release: python manage.py migrate --noinput && python manage.py compilemessages -v0
