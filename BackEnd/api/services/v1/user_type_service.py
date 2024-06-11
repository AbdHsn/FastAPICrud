from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user_type_schema import UserTypeCreate, UserTypeUpdate
from fastapi import APIRouter
from db.session import get_db
from db.repository.user_type_repo import get_user_types, get_user_type_by_id, create_user_type, update_user_type, delete_user_type

router = APIRouter()

@router.get("/get-user-types")
def get_user_types_endpoint(db: Session = Depends(get_db)):
    user_types = get_user_types(db)
    return user_types

@router.get("/get-user-type-by-id")
def get_user_type_by_id_endpoint(id: int, db: Session = Depends(get_db)):
    user_type = get_user_type_by_id(id, db)
    if not user_type:
        raise HTTPException(status_code=404, detail="UserType not found")
    return user_type

@router.post("/create-user-type", status_code=201)
def create_user_type_endpoint(user_type: UserTypeCreate, db: Session = Depends(get_db)):
    return create_user_type(user_type=user_type, db=db)

@router.put("/update-user-type")
def update_user_type_endpoint(id: int, user_type: UserTypeUpdate, db: Session = Depends(get_db)):
    updated_user_type = update_user_type(id, user_type, db)
    if not updated_user_type:
        raise HTTPException(status_code=404, detail="UserType not found")
    return updated_user_type

@router.delete("/delete-user-type")
def delete_user_type_endpoint(id: int, db: Session = Depends(get_db)):
    deleted_user_type = delete_user_type(id, db)
    if not deleted_user_type:
        raise HTTPException(status_code=404, detail="UserType not found")
    return deleted_user_type