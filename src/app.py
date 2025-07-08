from dotenv import load_dotenv

load_dotenv()

from .services.fast_api.api import FastAPP, FastAPI

app: FastAPI = FastAPP().create_app()
