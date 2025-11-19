# app/services/auth_service.py
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from typing import Optional, cast

def create_user(db: Session, username: str, password: str) -> dict:
    """
    Cria um novo usuário com senha hasheada no banco
    """
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise ValueError("Usuário já existe")
    
    # Garantir que é string
    hashed_pw = str(hash_password(password))
    new_user = User(username=username, hashed_password=hashed_pw)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "id": new_user.id,
        "username": new_user.username
    }

def authenticate_user(db: Session, username: str, password: str) -> Optional[str]:
    """
    Autentica um usuário e retorna token JWT
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    
    # Converter explicitamente para string
    user_hashed_password = str(user.hashed_password)
    if verify_password(password, user_hashed_password):
        access_token = create_access_token(
            data={"sub": username, "user_id": user.id}
        )
        return access_token
    return None

def get_user_by_username(db: Session, username: str) -> Optional[dict]:
    """
    Busca usuário pelo username
    """
    user = db.query(User).filter(User.username == username).first()
    if user:
        return {
            "id": user.id,
            "username": user.username
        }
    return None

def verify_user_token(token: str) -> Optional[dict]:
    """
    Verifica se um token JWT é válido
    """
    from app.core.security import verify_token
    payload = verify_token(token)
    
    if payload:
        username = payload.get("sub")
        if username and isinstance(username, str):
            return {
                "id": payload.get("user_id"),
                "username": username
            }
    return None