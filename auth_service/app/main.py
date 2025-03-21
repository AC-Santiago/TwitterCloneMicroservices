from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, user
from app.utils.http_error_handler import HTTPErrorHandler

app = FastAPI(
    title="Auth Service",
    description="Servicio de autenticación para Twitter Clone",
    version="1.0.0",
)


# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # URL del BFF en desarrollo
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(HTTPErrorHandler)

app.include_router(auth.router, prefix="/service_auth", tags=["Authentication"])
app.include_router(user.router, prefix="/service_auth/users", tags=["Users"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth-service"}
