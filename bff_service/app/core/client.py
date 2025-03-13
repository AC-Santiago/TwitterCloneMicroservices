import httpx
from contextlib import asynccontextmanager
from app.core.config import get_settings

# Cliente HTTP asíncrono global
client: httpx.AsyncClient = None

TIMEOUT = get_settings().HTTP_TIMEOUT


async def get_client() -> httpx.AsyncClient:
    """
    Retorna el cliente HTTP global. Si no existe, crea uno nuevo.
    """
    global client
    if client is None:
        client = httpx.AsyncClient(timeout=TIMEOUT)
    return client


async def close_client():
    """
    Cierra el cliente HTTP global si existe.
    """
    global client
    if client is not None:
        await client.aclose()
        client = None


@asynccontextmanager
async def get_http_client():
    """
    Context manager para usar el cliente HTTP de forma segura.
    """
    try:
        _client = await get_client()
        yield _client
    finally:
        pass  # No cerramos el clien
