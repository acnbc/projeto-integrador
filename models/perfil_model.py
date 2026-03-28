from sqlalchemy import Column, Integer, String, DateTime
from data.connection import Base

class Perfil(Base):
    __tablename__ = "perfil"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255))
