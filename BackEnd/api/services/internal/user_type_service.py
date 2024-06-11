from fastapi import APIRouter, Depends, HTTPException
from db.db_config import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.user_type_model import UserType
from schemas.user_type_schema import UserTypeCreate
from db.repository.generic_repo import GenericRepository

router = APIRouter()


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/user-types/user_type_by_id")
async def read_user_type_by_id(id: int, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db)
    user_type = await repo.get_by_id(user_type_id = id)
    if user_type is None:
        raise HTTPException(status_code=404, detail="UserType not found")
    return user_type
