# app/db/models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class User(Base):
    _tablename_ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)  # Isso define o tipo da coluna
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Quando você acessa user.hashed_password, retorna uma string