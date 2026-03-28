from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List
from datetime import date, datetime, timezone

from models.parecer_schemas import ParecerResponse
from models.tipo_alta_schemas import TipoAltaResponse
from models.usuario_schemas import UsuarioMinimoResponse


class InternacaoDelete(BaseModel):
    id: int


class Internacao(BaseModel):
    data_internacao: date = Field()
    numero_prontuario: str = Field(..., max_length=50)
    setor_internacao: str = Field(..., max_length=100)

    data_nascimento_paciente: Optional[date] = None
    nome_paciente: str = Field(..., max_length=250)
    sexo_paciente: str = Field(default='M', pattern="^(F|M)$")
    grau_instrucao_paciente: Optional[str] = Field(None, max_length=50)
    moradia_paciente: Optional[str] = Field(None, max_length=250)

    familiares_atendidos: Optional[int] = Field()
    criado_por:int = Field()

    data_alta: Optional[date] = Field(None)
    tipo_alta_id: Optional[int] = Field(None)
    obs_alta: Optional[str] = Field(None, max_length=250)


class AltaInternacao(BaseModel):
    data_alta: Optional[date] = None
    tipo_alta_id: Optional[int] = None
    obs_alta: Optional[str] = Field(None, max_length=250)


class NovaInternacao(BaseModel):
    data_internacao: Optional[date] = None
    numero_prontuario: str = Field(..., max_length=50)
    setor_internacao: str = Field(..., max_length=100)

    data_nascimento_paciente: Optional[date] = None
    nome_paciente: str = Field(..., max_length=250)
    sexo_paciente: Optional[str] = Field(default='F', pattern="^(F|M)$")
    grau_instrucao_paciente: Optional[str] = Field(None, max_length=50)
    moradia_paciente: Optional[str] = Field(None, max_length=250)

    familiares_atendidos: Optional[int] = None

class InternacaoResponse(Internacao):
    id: int
    criado_em: datetime
    usuario: Optional[UsuarioMinimoResponse]
    tipo_alta: Optional[TipoAltaResponse]
    pareceres: Optional[List[ParecerResponse]]

    @field_serializer("criado_em")
    def serialize_criado_em(self, dt: datetime | None):
        if dt is None:
            return None
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()