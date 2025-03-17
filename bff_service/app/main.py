from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.core.client import get_client, close_client
from app.core.config import SettingsDepends
from app.routers import auth, tweet, user
from app.utils.http_error_handler import HTTPErrorHandler


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


@app.get("/")
async def read_root(settings: SettingsDepends):
    return {
        "message": "Twitter Clone BFF Service",
        "services": {
            "auth": settings.AUTH_SERVICE_URL,
            "tweets": settings.TWEETS_SERVICE_URL,
            "interactions": settings.INTERACTIONS_SERVICE_URL,
        },
    }


app.include_router(auth.router, prefix="/service_auth")
app.include_router(user.router, prefix="/service_user")
app.include_router(tweet.router, prefix="/service_tweet")


@app.on_event("startup")
async def startup_event():
    await get_client()


@app.on_event("shutdown")
async def shutdown_event():
    await close_client()
