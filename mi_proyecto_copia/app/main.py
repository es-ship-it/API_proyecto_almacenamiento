from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.api.api import api_router_v1
from app.core.config import settings

# --- Creación de la instancia de FastAPI ---
app = FastAPI(
    title=settings.APP_NAME,
    description="Aplicación para la gestión de eventos",
    version=settings.APP_VERSION,
)

# --- Configuración de Middleware CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Inclusión de Enrutadores de la API ---
app.include_router(api_router_v1, prefix="/api/v1")

# Redirección automática de la raíz a la documentación
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")