from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings.app_settings import settings
from routes.app_routes import app_router
from fastapi.openapi.utils import get_openapi
from core.middlewares.jwt_middleware import JWTMiddleware

def initialize_routes(app):
    app.include_router(app_router)

def main():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    initialize_routes(app)

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Specifies which origins are allowed (use ["*"] for all origins or be specific)
        allow_credentials=True,
        allow_methods=["*"],  # Specifies which methods can be used across the domain, use ["GET", "POST", etc.] to be specific
        allow_headers=["*"],  # Specifies which headers can be sent to the API
    )

        # Add JWT middleware
    #app.add_middleware(JWTMiddleware)


    return app

app = main()