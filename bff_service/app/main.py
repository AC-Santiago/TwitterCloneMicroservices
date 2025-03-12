from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.utils.http_error_handler import HTTPErrorHandler

import httpx
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación FastAPI
app = FastAPI(
    title="Twitter Clone BFF",
    description="Backend for Frontend service for Twitter Clone",
    version="1.0.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(HTTPErrorHandler)

# URLs de los microservicios
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8000")
TWEETS_SERVICE_URL = os.getenv("TWEETS_SERVICE_URL", "http://localhost:8001")
INTERACTIONS_SERVICE_URL = os.getenv(
    "INTERACTIONS_SERVICE_URL", "http://localhost:8002"
)

# Cliente HTTP asíncrono
client = httpx.AsyncClient(timeout=30.0)


@app.get("/")
async def read_root():
    return {"message": "Twitter Clone BFF Service"}


# Endpoints para autenticación
@app.post("/auth/register")
async def register(user_data: Dict[Any, Any]):
    try:
        response = await client.post(
            f"{AUTH_SERVICE_URL}/auth/register", json=user_data
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/login")
async def login(credentials: Dict[Any, Any]):
    try:
        response = await client.post(
            f"{AUTH_SERVICE_URL}/auth/login", json=credentials
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=str(e))


# # Endpoints para tweets
# @app.get("/tweets")
# async def get_tweets(token: str):
#     try:
#         response = await client.get(
#             f"{TWEETS_SERVICE_URL}/tweets",
#             headers={"Authorization": f"Bearer {token}"},
#         )
#         return response.json()
#     except httpx.HTTPError as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
# @app.post("/tweets")
# async def create_tweet(tweet_data: Dict[Any, Any], token: str):
#     try:
#         response = await client.post(
#             f"{TWEETS_SERVICE_URL}/tweets",
#             json=tweet_data,
#             headers={"Authorization": f"Bearer {token}"},
#         )
#         return response.json()
#     except httpx.HTTPError as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
# # Endpoints para interacciones
# @app.post("/interactions/like")
# async def like_tweet(interaction_data: Dict[Any, Any], token: str):
#     try:
#         response = await client.post(
#             f"{INTERACTIONS_SERVICE_URL}/like",
#             json=interaction_data,
#             headers={"Authorization": f"Bearer {token}"},
#         )
#         return response.json()
#     except httpx.HTTPError as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
# @app.post("/interactions/retweet")
# async def retweet(interaction_data: Dict[Any, Any], token: str):
#     try:
#         response = await client.post(
#             f"{INTERACTIONS_SERVICE_URL}/retweet",
#             json=interaction_data,
#             headers={"Authorization": f"Bearer {token}"},
#         )
#         return response.json()
#     except httpx.HTTPError as e:
#         raise HTTPException(status_code=500, detail=str(e))
#


@app.on_event("startup")
async def startup_event():
    global client
    client = httpx.AsyncClient(timeout=30.0)


@app.on_event("shutdown")
async def shutdown_event():
    await client.aclose()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
