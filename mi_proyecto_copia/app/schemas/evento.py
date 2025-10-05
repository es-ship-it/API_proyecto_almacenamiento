from typing import List, Optional
from pydantic import BaseModel
from datetime import date, time, datetime
from app.models.evento import TipoEvento, EstadoEvento, OrganizadoPor, AvalTipo
    
class BaseEvento(BaseModel):
    nombre_Evento: str
    tipoEvento: TipoEvento
    descripcionEvento: str | None = None
    fechaEvento: date
    horaInicioEvento: time
    horaFinEvento: time
    estadoEvento: EstadoEvento = EstadoEvento.Revision
    tipoAvalEvento: AvalTipo | None = None

class CrearEvento(BaseEvento):
    evento_OrganizadoPor: OrganizadoPor
    idLugar: Optional[int] = None

class ActEvento(BaseModel):
    nombre_Evento: Optional [str] | None = None
    tipoEvento: Optional [TipoEvento] | None = None
    descripcionEvento: Optional [str] | None = None
    fechaEvento: Optional [date] | None = None
    horaInicioEvento: Optional [time] | None = None
    horaFinEvento: Optional [time] | None = None
    estadoEvento: Optional [EstadoEvento] | None = None
    tipoAvalEvento: Optional [AvalTipo] | None = None
    idLugar: Optional [int] | None = None

class Evento(BaseEvento):
    idEvento: int
    evento_OrganizadoPor: OrganizadoPor
    idLugares: Optional[List[int]] = []  
    
    class Config:
        orm_mode = True