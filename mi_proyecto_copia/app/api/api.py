from fastapi import APIRouter
from app.api.v1.routes import evento

api_router_v1 = APIRouter()
api_router_v1.include_router(evento.router, prefix="/eventos", tags=["Eventos"])