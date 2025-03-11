import os

from fastapi import FastAPI, HTTPException, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from routers import auth, user
from utils.http_error_handler import HTTPErrorHandler
from database.connection import create_db_and_tables

app = FastAPI(
    title="Auth Service",
    description="Servicio de autenticación para Twitter Clone",
    version="1.0.0",
)


API_KEY = os.getenv("AUTH_SERVICE_API_KEY", "your-secret-api-key")
api_key_header = APIKeyHeader(name="X-API-Key")


async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate API Key",
        )
    return api_key


# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # URL del BFF en desarrollo
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(HTTPErrorHandler)

app.middleware("http")(verify_api_key)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/api/users", tags=["Users"])


@app.on_event("startup")
async def startup_event():
    create_db_and_tables()


@app.get("/health")
async def health_check(api_key: str = Security(api_key_header)):
    await verify_api_key(api_key)
    return {"status": "healthy", "service": "auth-service"}
