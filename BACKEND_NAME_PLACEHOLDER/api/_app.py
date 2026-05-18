from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ._routes import define_routes

_app: FastAPI | None = None


def build_app():
    global _app
    if not _app:
        _app = FastAPI()
        
        # CORS hinzufügen
        _app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        define_routes(_app)

    return _app