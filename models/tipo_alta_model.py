from sqlalchemy import Column, Integer, String, DateTime
from data.connection import Base

class TipoAlta(Base):
    __tablename__ = "tipo_alta"
    id = Column(Integer, primary_key=True, index=True)
    alta = Column(String(255))
