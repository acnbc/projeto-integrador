from datetime import date
from typing import Optional, List

from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, Mapped

from data.connection import Base
from models.parecer_model import Parecer
from models.tipo_alta_model import TipoAlta
from models.usuario_model import Usuario


class Internacao(Base):
    __tablename__ = "internacao"

    id = Column(Integer, primary_key=True, index=True)

    data_internacao = Column(Date, nullable=True)
    numero_prontuario = Column(String(50), nullable=False)
    setor_internacao = Column(String(100), nullable=False)

    data_nascimento_paciente:Mapped[Optional[date]] = Column(Date, nullable=True)
    nome_paciente = Column(String(250), nullable=False)
    sexo_paciente = Column(Enum('F', 'M'), default='F')
    grau_instrucao_paciente:Mapped[Optional[str]] = Column(String(50), nullable=True)
    moradia_paciente:Mapped[Optional[str]] = Column(String(250), nullable=True)

    familiares_atendidos:Mapped[Optional[int]] = Column(Integer, nullable=True)

    criado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    criado_em = Column(DateTime(timezone=True), nullable=False, server_default=func.current_timestamp())

    tipo_alta_id: Mapped[Optional[int]] = Column(Integer, ForeignKey("tipo_alta.id"), nullable=True)
    data_alta:Mapped[Optional[date]] = Column(Date, nullable=True)
    obs_alta:Mapped[Optional[str]] = Column(String(250), nullable=True)

    tipo_alta: Mapped[Optional["TipoAlta"]] = relationship()
    usuario: Mapped["Usuario"] = relationship()
    pareceres: Mapped[List["Parecer"]] = relationship()