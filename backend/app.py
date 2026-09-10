from fastapi import FastAPI
from .routers import observations

app = FastAPI()

app.include_router(observations.router)