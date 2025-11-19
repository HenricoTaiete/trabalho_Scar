# app/main.py
from fastapi import FastAPI
from app.api.v1 import auth

app = FastAPI(
    title="RFID API",
    description="API para sistema RFID",
    version="1.0.0"
)

# Incluir rotas
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])

@app.get("/")
async def root():
    return {"message": "RFID API está funcionando!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}