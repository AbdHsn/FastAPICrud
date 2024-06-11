from sqlalchemy.orm import Session
from schemas.user_type_schema import UserTypeCreate, UserTypeUpdate
from db.models.user_type_model import UserType

def get_user_types(db: Session):
    return db.query(UserType).all()

def get_user_type_by_id(user_type_id: int, db: Session):
    return db.query(UserType).filter(UserType.user_type_id == user_type_id).first()

def create_user_type(user_type: UserTypeCreate, db: Session,):
    db_user_type = UserType(name=user_type.name)
    db.add(db_user_type)
    db.commit()
    db.refresh(db_user_type)
    return db_user_type

def update_user_type(user_type_id: int, user_type: UserTypeUpdate, db: Session):
    db_user_type = db.query(UserType).filter(UserType.user_type_id == user_type_id).first()
    if db_user_type:
        db_user_type.name = user_type.name  # assuming UserTypeUpdate has the same structure as UserTypeCreate
        db.commit()
        db.refresh(db_user_type)
    return db_user_type

def delete_user_type(user_type_id: int, db: Session):
    db_user_type = db.query(UserType).filter(UserType.user_type_id == user_type_id).first()
    if db_user_type:
        db.delete(db_user_type)
        db.commit()
    return db_user_type