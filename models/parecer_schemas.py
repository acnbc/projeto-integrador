from pydantic import BaseModel, ConfigDict, Field, field_serializer
from typing import Optional
from datetime import date, datetime, timezone

from models.usuario_schemas import UsuarioMinimoResponse


class InternacaoParecerResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    numero_prontuario: str
    setor_internacao: str
    nome_paciente: str


class Parecer(BaseModel):
    data_solicitacao_parecer: Optional[datetime] = None
    data_parecer: Optional[datetime] = None
    texto_parecer: Optional[str] = None
    numero_prontuario: Optional[str] = None
    internacao_id: int
    criado_por: int


class NovoParecer(BaseModel):
    numero_prontuario: Optional[str] = None
    data_solicitacao_parecer: Optional[datetime] = None
    data_parecer: Optional[datetime] = None
    texto_parecer: Optional[str] = None
    internacao_id: Optional[int] = None
    criado_por: Optional[int] = None


class ParecerFormulario(BaseModel):
    numero_prontuario: str
    internacao_id: Optional[int] = None
    nome_paciente: Optional[str] = None
    ocultar_nome_paciente: bool = False
    data_nascimento_paciente: Optional[date] = None
    sexo_paciente: Optional[str] = Field(default="F", pattern="^(F|M)$")
    data_internacao: date
    setor_internacao: str
    data_solicitacao_parecer: datetime
    data_parecer: Optional[datetime] = None
    data_alta: Optional[date] = None
    tipo_alta_id: Optional[int] = None
    observacoes_gerais: Optional[str] = None


class ParecerResponse(Parecer):
    model_config = ConfigDict(from_attributes=True)

    id: int
    criado_em: datetime
    usuario: Optional[UsuarioMinimoResponse] = None
    internacao: Optional[InternacaoParecerResumo] = None

    @field_serializer("criado_em", "data_solicitacao_parecer", "data_parecer")
    def serialize_datetimes(self, dt: datetime | None):
        if dt is None:
            return None
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()
