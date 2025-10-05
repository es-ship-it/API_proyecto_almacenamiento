from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.mysql import Base

class Lugar(Base):
    __tablename__ = "lugar"

    idLugar = Column(Integer, primary_key=True, autoincrement=True)
    ubicacion = Column(String(70), nullable=True)
    capacidad = Column(Integer, nullable=True)
    nombreLugar = Column(String(100), nullable=False)
    
    eventos = relationship("Evento", secondary="lugar_evento", back_populates="lugares")
    
class LugarEvento(Base):
    __tablename__ = "lugar_evento"

    idlugar_evento = Column(Integer, primary_key=True, autoincrement=True)
    Lugar_idLugar = Column(Integer, ForeignKey("lugar.idLugar", ondelete="CASCADE"))
    Evento_idEvento = Column(Integer, ForeignKey("evento.idEvento", ondelete="CASCADE"))