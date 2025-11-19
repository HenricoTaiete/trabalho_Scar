from app.db.session import engine
from app.db.base import Base
from app.models.user import User
from app.models.rfid_tag import RFIDTag
import logging

logger = logging.getLogger(__name__)

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise

if __name__ == "__main__":
    init_db()