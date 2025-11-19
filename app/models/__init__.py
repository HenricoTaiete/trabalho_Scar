# app/models/__init__.py
from app.models.user import User
from app.models.rfid_tag import RFIDTag

__all__ = ["User", "RFIDTag"]