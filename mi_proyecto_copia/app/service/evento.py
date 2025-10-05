from datetime import datetime
from typing import Sequence
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.evento import Evento
from app.models.lugar import LugarEvento, Lugar
from app.schemas.evento import CrearEvento, ActEvento
import app.crud.evento as eventoCrud
from fastapi import HTTPException, status

async def eliminarEventoService(session: AsyncSession, evento: Evento) -> None:
    await eventoCrud.eliminarEventoPorID(session, evento)

async def buscarEventoPorIDService(session: AsyncSession, id: int) -> Evento | None:
    evento = await eventoCrud.buscarPorID(session, id)

    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el evento con el id {id}",
        )
    return evento

async def ListarEventosService(session: AsyncSession) -> Sequence[Evento]:
    eventos = await eventoCrud.listarEventos(session)
    return eventos

async def CrearEventoService(session: AsyncSession, evento: CrearEvento):
    fecha_evento = evento.fechaEvento

    if fecha_evento < datetime.utcnow().date():
        raise ValueError("La fecha del evento no puede ser menor a la actual")
    
    lugar = await session.get(Lugar, evento.idLugar)
    if not lugar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un lugar con el id {evento.idLugar}"
        )
    
    nuevo_evento = Evento(
        nombre_Evento=evento.nombre_Evento,
        tipoEvento=evento.tipoEvento,
        descripcionEvento=evento.descripcionEvento,
        fechaEvento=evento.fechaEvento,
        horaInicioEvento=evento.horaInicioEvento,
        horaFinEvento=evento.horaFinEvento,
        estadoEvento=evento.estadoEvento,
        evento_OrganizadoPor=evento.evento_OrganizadoPor,
        tipoAvalEvento=evento.tipoAvalEvento
    )

   
    session.add(nuevo_evento)
    await session.commit()
    await session.refresh(nuevo_evento)

    if evento.idLugar:
        lugar = await session.get(Lugar, evento.idLugar)
        if not lugar:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe un lugar con el id {evento.idLugar}"
            )
        nueva_relacion = LugarEvento(
            Lugar_idLugar=evento.idLugar,
            Evento_idEvento=nuevo_evento.idEvento
        )
        session.add(nueva_relacion)
        await session.commit()
        await session.refresh(nuevo_evento)
    return nuevo_evento


async def actualizarEventoService(session: AsyncSession, event_id: int, updates: ActEvento) -> Evento:
    session_evento = await eventoCrud.buscarPorID(session, event_id)
    if not session_evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado"
        )

    nuevo_id_lugar = updates.idLugar

    evento_actualizado = await eventoCrud.ActualizarEvento(session, session_evento, updates)

    if nuevo_id_lugar:
        lugar = await session.get(Lugar, nuevo_id_lugar)
        if not lugar:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe un lugar con el id {nuevo_id_lugar}"
            )

        result = await session.execute(
            select(LugarEvento).where(LugarEvento.Evento_idEvento == event_id)
        )
        relacion_actual = result.scalars().first()

        if relacion_actual and relacion_actual.Lugar_idLugar != nuevo_id_lugar:
            relacion_actual.Lugar_idLugar = nuevo_id_lugar
            await session.commit()

        elif not relacion_actual:
            nueva_relacion = LugarEvento(
                Lugar_idLugar=nuevo_id_lugar,
                Evento_idEvento=event_id
            )
            session.add(nueva_relacion)
            await session.commit()

    await session.refresh(evento_actualizado)
    return evento_actualizado

