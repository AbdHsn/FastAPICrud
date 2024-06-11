class Settings:
    PROJECT_NAME: str = "API"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./db/database/subzcars.db"
    DATABASE_URL_ASYNC: str = "sqlite+aiosqlite:///./db/database/subzcars.db"

settings = Settings()

