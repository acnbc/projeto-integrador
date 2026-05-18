from typing import Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func
from data.connection import Base
from models.usuario_model import Usuario


class Parecer(Base):
    __tablename__ = "parecer"

    id = Column(Integer, primary_key=True, index=True)
    data_solicitacao_parecer = Column(DateTime(timezone=True), nullable=True)
    data_parecer = Column(DateTime(timezone=True), nullable=True)
    texto_parecer = Column(Text, nullable=True)
    numero_prontuario = Column(String(50), nullable=False)

    internacao_id = Column(Integer, ForeignKey("internacao.id"), nullable=False)
    criado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    criado_em = Column(DateTime(timezone=True), nullable=False, server_default=func.current_timestamp())

    usuario: Mapped[Optional["Usuario"]] = relationship()
    internacao: Mapped[Optional["Internacao"]] = relationship(
        "Internacao", back_populates="pareceres"
    )
