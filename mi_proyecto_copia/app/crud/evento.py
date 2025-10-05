from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.evento import Evento
from app.schemas.evento import CrearEvento, ActEvento

async def eliminarEventoPorID(session: AsyncSession, evento: Evento) -> None:
    await session.delete(evento)
    await session.commit()

async def crear_evento(session: AsyncSession, event: CrearEvento) -> Evento:
    session_evento = Evento(**event.dict())
    session.add(session_evento)
    await session.commit()
    await session.refresh(session_evento)
    return session_evento

async def buscarPorID(session: AsyncSession, id: int) -> Evento | None:
    stmt = (select(Evento).where(Evento.idEvento == id))

    result = await session.execute(stmt)
    evento = result.scalar_one_or_none()
    return evento

async def listarEventos(session: AsyncSession) -> Sequence[Evento]:
    stmt = (select(Evento).order_by(Evento.idEvento))

    result = await session.execute(stmt)
    eventos = result.scalars().unique().all()
    return eventos

async def ActualizarEvento(session: AsyncSession, session_evento: Evento, updates: ActEvento) -> Evento:
    update_data = updates.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(session_evento, key, value)
    
    await session.commit()
    await session.refresh(session_evento)
    return session_evento