from fastapi import FastAPI
from tags_agr.api.routes import routes

app = FastAPI(debug=True)

app.include_router(routes)
