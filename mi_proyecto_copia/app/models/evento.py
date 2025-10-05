from sqlalchemy import Column, Integer, String, Enum, Date, Time
from app.db.mysql import Base
import enum
from sqlalchemy.orm import relationship
#--- Definición de enums para Campos Específicos ---

class TipoEvento(str, enum.Enum):
    Ludico = "Ludico"
    Academico = "Academico"

class EstadoEvento(str, enum.Enum):
    Aprobado = "Aprobado"
    Revision = "Revision"
    Rechazado = "Rechazado"

class OrganizadoPor(str, enum.Enum):
    Estudiante = "Estudiante"
    Docente = "Docente"

class AvalTipo(str, enum.Enum):
    DirectorPrograma = "DirectorPrograma"
    DirectorDocencia = "DirectorDocencia"

#--- Definición del Modelo de Evento ---

class Evento(Base):
    __tablename__ = "evento"

    idEvento = Column(Integer, primary_key=True, index=True)
    nombre_Evento = Column(String, nullable=False)
    tipoEvento = Column(Enum(TipoEvento), nullable=False)
    descripcionEvento = Column(String, nullable=True)
    fechaEvento = Column(Date, nullable=False)
    horaInicioEvento = Column(Time, nullable=False)
    horaFinEvento = Column(Time, nullable=False)
    estadoEvento = Column(Enum(EstadoEvento), default=EstadoEvento.Revision, nullable=False)
    evento_OrganizadoPor = Column(Enum(OrganizadoPor), nullable=False)
    tipoAvalEvento = Column(Enum(AvalTipo), nullable=True)

    lugares = relationship("Lugar", secondary="lugar_evento", back_populates="eventos")