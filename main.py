from fastapi import FastAPI
from api import incident_api, resolution_api

app = FastAPI()

app.include_router(incident_api.router)
app.include_router(resolution_api.router)