release: alembic upgrade head
web: gunicorn tags_agr.flask_app:app --bind 0.0.0.0:$PORT -w 1