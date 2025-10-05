from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.mysql import get_session
from app.schemas.evento import CrearEvento, ActEvento, Evento
from app.service.evento import CrearEventoService, actualizarEventoService
import app.service.evento as service_evento

router = APIRouter()

@router.delete("/{idEvento}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_Evento(idEvento: int, session: AsyncSession = Depends(get_session)):
    evento = await service_evento.buscarEventoPorIDService(session, idEvento)
    await service_evento.eliminarEventoService(session, evento)
    return

@router.get("/{idEvento}", response_model=Evento, status_code=status.HTTP_200_OK)
async def obtener_Evento(idEvento: int, session: AsyncSession = Depends(get_session)):
    return await service_evento.buscarEventoPorIDService(session, idEvento)

@router.get("/", response_model=list[Evento], status_code=status.HTTP_200_OK)
async def listar_Eventos(session: AsyncSession = Depends(get_session)):
    return await service_evento.ListarEventosService(session)

@router.post("/", response_model=Evento, status_code=status.HTTP_201_CREATED)
async def crear_Evento(event: CrearEvento, session: AsyncSession = Depends(get_session)):
    try:
        return await service_evento.CrearEventoService(session, event)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{idEvento}", response_model=Evento, status_code=status.HTTP_200_OK)
async def actualizar_Evento(idEvento: int, updates: ActEvento, session: AsyncSession = Depends(get_session)):
    try:
        return await service_evento.actualizarEventoService(session, idEvento, updates)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))