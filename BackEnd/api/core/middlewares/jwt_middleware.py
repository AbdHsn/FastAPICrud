from fastapi import Depends, HTTPException, Request
from db.models.user_model import User
from db.repository.generic_repo import GenericRepository
from db.db_config import get_session
from jose import jwt, JWTError
from pydantic import ValidationError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware

# Secret key to encode and decode JWT
SECRET_KEY = "app-secret-key-for-jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 days

class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, public_paths=None):
        super().__init__(app)
        self.token_scheme = HTTPBearer()
        self.public_paths = public_paths or ["/docs", "/openapi.json", "/register", "/login"]

    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(path) for path in self.public_paths):
            return await call_next(request)
        
        credentials: HTTPAuthorizationCredentials = await self.token_scheme(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            token = credentials.credentials
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id: str = payload.get("sub")
                if user_id is None:
                    raise HTTPException(status_code=403, detail="Invalid token.")
                request.state.user = await self.get_user(user_id)
            except (JWTError, ValidationError):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
        else:
            request.state.user = None

        response = await call_next(request)
        return response

    async def get_user(self, user_id: int):
        async with get_session() as db:
            repo = GenericRepository(db, User)
            user = await repo.get_by_field(user_id=user_id)
            if user is None:
                raise HTTPException(status_code=403, detail="User not found.")
            return user