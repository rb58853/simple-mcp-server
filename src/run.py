from .services.fast_api.api import create_app
from fastapi import FastAPI

app:FastAPI = create_app()
