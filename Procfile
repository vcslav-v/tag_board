release: alembic upgrade head
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker tags_agr.main:app