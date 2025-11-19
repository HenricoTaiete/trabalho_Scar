from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter()
security = HTTPBearer()

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth"}

@router.post("/register", response_model=dict)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    from app.services.auth_service import create_user
    new_user = create_user(db, user.username, user.password)
    return {
        "message": "User created successfully",
        "username": new_user["username"],
        "id": new_user["id"]
    }

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    from app.services.auth_service import authenticate_user
    token = authenticate_user(db, user.username, user.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    from app.services.auth_service import verify_user_token, get_user_by_id
    token = credentials.credentials
    user_data = verify_user_token(token)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user = get_user_by_id(db, user_data["id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.get("/protected")
async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    from app.services.auth_service import verify_user_token
    token = credentials.credentials
    user = verify_user_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return {"message": f"Hello {user['username']}! This is a protected route."}

@router.get("/users", response_model=List[UserResponse])
async def get_all_users_route(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    from app.services.auth_service import verify_user_token, get_all_users
    token = credentials.credentials
    if not verify_user_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    users = get_all_users(db)
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    from app.services.auth_service import verify_user_token, get_user_by_id
    token = credentials.credentials
    if not verify_user_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/users/{user_id}", response_model=dict)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    from app.services.auth_service import verify_user_token, update_user_service
    token = credentials.credentials
    current_user = verify_user_token(token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    updated_user = update_user_service(db, user_id, user_update)
    return {
        "message": "User updated successfully",
        "username": updated_user["username"],
        "id": updated_user["id"]
    }

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    from app.services.auth_service import verify_user_token, delete_user_service
    token = credentials.credentials
    current_user = verify_user_token(token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    delete_user_service(db, user_id)
    return {"message": "User deleted successfully"}