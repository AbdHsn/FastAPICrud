from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.user_model import User
from db.repository.generic_repo import GenericRepository
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_config import get_session
from schemas.user_schema import Login, Register
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

# Secret key to encode and decode JWT
SECRET_KEY = "app-secret-key-for-jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

@router.post("/register", status_code=201)
async def register_endpoint(user_data: Register, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, User)
    
    # Check if user already exists by email or phone
    existing_user = await repo.get_by_field(or_conditions={'email': user_data.email, 'phone': user_data.phone})
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email or phone already exists")

    # Hash the password before saving
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User(
        email=user_data.email,
        phone=user_data.phone,
        password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        user_type_id=3  # Setting a default value for user_type_id
    )
    
    new_user = await repo.insert(new_user)
    
    # Create an access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.user_id, "email": new_user.email, "phone":new_user.phone, "user_type_id": new_user.user_type_id }, expires_delta=access_token_expires
    )
    
    return {
        "user": {
            "id": new_user.user_id,
            "email": new_user.email,
            "phone": new_user.phone,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "user_type_id": new_user.user_type_id
        },
        "token": {"access_token": access_token, "token_type": "bearer"}
    }

@router.post("/login", status_code=201)
async def login_endpoint(user_data: Login, db: AsyncSession = Depends(get_session)):
    repo = GenericRepository(db, User)
    user = await repo.get_by_field(or_conditions={'email': user_data.email_phone, 'phone': user_data.email_phone})
    
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=404, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_id, "email": user.email, "phone":user.phone, "user_type_id": user.user_type_id }, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt