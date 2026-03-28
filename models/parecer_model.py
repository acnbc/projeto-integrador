from typing import Optional

from sqlalchemy import Column, Integer, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func
from data.connection import Base
from models.usuario_schemas import Usuario


class Parecer(Base):
    __tablename__ = "parecer"

    id = Column(Integer, primary_key=True, index=True)
    data_solicitacao_parecer = Column(Date, nullable=True)
    data_parecer = Column(Date, nullable=True)
    texto_parecer = Column(Text, nullable=True)

    internacao_id = Column(Integer, ForeignKey("internacao.id"), nullable=False)
    criado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    criado_em = Column(DateTime(timezone=True), nullable=False, server_default=func.current_timestamp())

    usuario: Mapped[Optional["Usuario"]] = relationship()