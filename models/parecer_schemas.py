from pydantic import BaseModel, field_serializer
from typing import Optional
from datetime import date, datetime, timezone

from models.usuario_schemas import UsuarioMinimoResponse


class Parecer(BaseModel):
    data_solicitacao_parecer: Optional[date] = None
    data_parecer: Optional[date] = None
    texto_parecer: Optional[str] = None
    internacao_id: int
    criado_por: int


class NovoParecer(BaseModel):
    data_solicitacao_parecer: date = None
    data_parecer: date = None
    texto_parecer: str = None
    internacao_id: int = None
    criado_por: int = None


class ParecerResponse(Parecer):
    id: int
    criado_em: datetime
    usuario: Optional[UsuarioMinimoResponse]

    @field_serializer("criado_em")
    def serialize_criado_em(self, dt: datetime | None):
        if dt is None:
            return None
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()