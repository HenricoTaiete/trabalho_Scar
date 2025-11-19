from fastapi import FastAPI
import time
import logging
from app.db.init_db import init_db

logger = logging.getLogger(__name__)
app = FastAPI(title="RFID API", version="1.0.0")

async def wait_for_mysql():
    from app.db.session import engine
    max_attempts = 45  
    for attempt in range(max_attempts):
        try:
            with engine.connect() as conn:
                logger.info("MySQL connected successfully")
                return True
        except Exception as e:
            if attempt < max_attempts - 1:
                wait_time = 3 
                logger.warning(f"MySQL not available (attempt {attempt + 1}/{max_attempts})")
                time.sleep(wait_time)
            else:
                logger.error(f"MySQL not available after {max_attempts} attempts")
                return False

@app.on_event("startup")
async def startup():
    try:
        mysql_ready = await wait_for_mysql()
        if mysql_ready:
            init_db()
            logger.info("Database initialized successfully")
        else:
            logger.error("Failed to connect to MySQL. Application may not work properly")
    except Exception as e:
        logger.error(f"Initialization error: {e}")

@app.get("/")
async def root():
    return {"message": "API working"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

try:
    from app.api.v1.auth import router as auth_router
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
    logger.info("Routes loaded successfully")
except Exception as e:
    logger.error(f"Error loading routes: {e}")