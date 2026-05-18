from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func
from data.connection import Base
from models.perfil_model import Perfil


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    senha_hash = Column(String(250), nullable=False)

    perfil_id = Column(Integer, ForeignKey("perfil.id"), nullable=False)

    criado_em = Column(DateTime(timezone=True), nullable=False, server_default=func.current_timestamp())
    inativado_em = Column(DateTime(timezone=True), nullable=True)

    perfil: Mapped[Optional["Perfil"]] = relationship()