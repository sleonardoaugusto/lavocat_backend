release: python ./backend/manage.py migrate
web: gunicorn backend.src.wsgi --log-file