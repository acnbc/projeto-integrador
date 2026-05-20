from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from controllers.auth import perfil_permitido
from data.connection import get_db
from models.usuario_model import Usuario
from models.usuario_schemas import PerfilId
import data.tipo_alta_repository as repository
import models.tipo_alta_schemas as schemas

alta_api = APIRouter(prefix="/api/tipo-alta", tags=["Tipos de Alta"])

_coordenador = Depends(perfil_permitido(PerfilId.COORDENADOR))
_leitura = Depends(perfil_permitido(PerfilId.COORDENADOR, PerfilId.ALUNO))


@alta_api.get("", summary="Lista todos os tipos de altas", status_code=status.HTTP_200_OK, response_model=list[schemas.TipoAltaResponse])
async def get_tipos_alta(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = _leitura,
):
    return repository.get_tipos_altas(db, skip, limit)


@alta_api.post("", summary="Cria um novo tipo de alta", status_code=status.HTTP_201_CREATED, response_model=schemas.TipoAltaResponse)
async def post_tipo_alta(
    tipo_alta: schemas.TipoAlta,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    return repository.create_tipo_alta(db, tipo_alta)


@alta_api.get("/{id}", summary="Detalhes de um tipo de alta", status_code=status.HTTP_200_OK, response_model=schemas.TipoAltaResponse)
async def get_tipo_alta(
    id: int,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    tipo_alta = repository.get_tipo_alta(db, id)
    if tipo_alta is None:
        raise HTTPException(status_code=400, detail="Tipo de alta não encontrado")
    return tipo_alta


@alta_api.put("/{id}", summary="Atualização de um tipo de alta", status_code=status.HTTP_200_OK, response_model=schemas.TipoAltaResponse)
async def put_tipo_alta(
    id: int,
    update_tipo_alta: schemas.TipoAlta,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    tipo_alta = repository.get_tipo_alta(db, id)
    if tipo_alta is None:
        raise HTTPException(status_code=400, detail="Tipo de alta não encontrado")
    repository.update_tipo_alta(db, update_tipo_alta, id)
    return repository.get_tipo_alta(db, id)


def use_alta_api(app_instance: FastAPI):
    app_instance.include_router(alta_api)
