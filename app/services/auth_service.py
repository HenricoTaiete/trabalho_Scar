from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from typing import Optional, List

def create_user(db: Session, username: str, password: str) -> dict:
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise ValueError("User already exists")
    
    hashed_pw = hash_password(password)
    new_user = User(username=username, hashed_password=hashed_pw)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"id": new_user.id, "username": new_user.username}

def authenticate_user(db: Session, username: str, password: str) -> Optional[str]:
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, str(user.hashed_password)):
        return None
    
    return create_access_token(data={"sub": username, "user_id": user.id})

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()

def update_user_service(db: Session, user_id: int, user_update) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    
    if user_update.username:
        existing_user = db.query(User).filter(
            User.username == user_update.username,
            User.id != user_id
        ).first()
        if existing_user:
            raise ValueError("Username already in use")
        user.username = user_update.username
    
    if user_update.password:
        user.hashed_password = hash_password(user_update.password)
    
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}

def delete_user_service(db: Session, user_id: int) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    
    db.delete(user)
    db.commit()

def verify_user_token(token: str) -> Optional[dict]:
    from app.core.security import verify_token
    payload = verify_token(token)
    
    if payload:
        username = payload.get("sub")
        user_id = payload.get("user_id")
        if username and isinstance(username, str) and user_id:
            return {"id": user_id, "username": username}
    return None