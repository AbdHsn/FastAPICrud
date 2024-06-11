from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from settings.app_settings import Settings

DATABASE_URL = Settings.DATABASE_URL_ASYNC

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency for FastAPI to use in routes for getting a session
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session