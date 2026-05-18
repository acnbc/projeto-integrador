from pydantic import BaseModel, Field, EmailStr, field_serializer
from typing import Optional
from datetime import datetime, timezone

from models.perfil_schemas import PerfilResponse
from enum import IntEnum


class PerfilId(IntEnum):
    COORDENADOR = 1
    ALUNO = 2

class Usuario(BaseModel):
    nome: str = Field(..., max_length=250)
    email: EmailStr
    senha: str = Field(..., max_length=250)
    perfil_id: int


class UpdateUsuario(BaseModel):
    nome: Optional[str] = Field(None, max_length=250)
    email: Optional[EmailStr] = None
    senha: Optional[str] = Field(None, max_length=250)
    perfil_id: Optional[int] = None

class NovoUsuario(BaseModel):
    nome: str = Field(None, max_length=250)
    email: EmailStr = Field(None, max_length=250)
    senha: str = Field(None, min_length=8)
    perfil_id: int = None


class Token(BaseModel):
	access_token: str
	token_type: str


class InativarUsuario(BaseModel):
    inativado_em: Optional[datetime] = None


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil_id: int
    criado_em: datetime
    inativado_em: Optional[datetime] = None
    perfil: Optional[PerfilResponse]

    @field_serializer("criado_em")
    def serialize_criado_em(self, dt: datetime | None):
        if dt is None:
            return None
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()

    @field_serializer("inativado_em")
    def serialize_inativado_em(self, dt: datetime | None):
        if dt is None:
            return None
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()


class UsuarioMinimoResponse(BaseModel):
    id: int
    nome: str
    perfil_id: int
    perfil: Optional[PerfilResponse]