from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.http_error_handler import HTTPErrorHandler
from app.routers import tweet

app = FastAPI(
    title="Tweet Service",
    description="Servicio de tweets para Twitter Clone",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(HTTPErrorHandler)

app.include_router(tweet.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth-service"}
