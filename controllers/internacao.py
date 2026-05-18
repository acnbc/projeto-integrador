from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from controllers.auth import perfil_permitido
from data.connection import get_db
from models.usuario_model import Usuario
from models.usuario_schemas import PerfilId
import data.internacao_repository as repository
import data.tipo_alta_repository as tipo_alta_repository
import models.internacao_schemas as schemas

internacao_api = APIRouter(prefix="/api/internacao", tags=["Internação"])

_coordenador = Depends(perfil_permitido(PerfilId.COORDENADOR))


@internacao_api.get("", summary="Lista todas as internações", status_code=status.HTTP_200_OK, response_model=list[schemas.InternacaoResponse])
async def listar_internacoes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    return repository.get_internacoes(db, skip, limit)


@internacao_api.post("", summary="Cria uma nova internação", status_code=status.HTTP_201_CREATED, response_model=schemas.InternacaoResponse)
async def post_internacao(
    internacao: schemas.Internacao,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    return repository.create_nova_internacao(db, internacao)


@internacao_api.get("/{id}", summary="Detalhes de uma internacao", status_code=status.HTTP_200_OK, response_model=schemas.InternacaoResponse)
async def get_internacao(
    id: int,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    internacao = repository.get_internacao(db, id)
    if internacao is None:
        raise HTTPException(status_code=400, detail="Internação não encontrado")
    return internacao


@internacao_api.put("/{id}/alta", summary="Atualiza a alta de uma internacao", status_code=status.HTTP_200_OK, response_model=schemas.InternacaoResponse)
async def put_internacao_alta(
    id: int,
    alta_internacao: schemas.AltaInternacao,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    internacao = repository.get_internacao(db, id)
    if internacao is None:
        raise HTTPException(status_code=400, detail="Internação não encontrada")
    tipo_alta = tipo_alta_repository.get_tipo_alta(db, alta_internacao.tipo_alta_id)
    if tipo_alta is None:
        raise HTTPException(status_code=400, detail="Tipo de alta não encontrada")
    repository.update_internacao_alta(db, alta_internacao, id)
    return repository.get_internacao(db, id)


@internacao_api.put("/{id}", summary="Atualização de uma internacao", status_code=status.HTTP_200_OK, response_model=schemas.InternacaoResponse)
async def put_internacao(
    id: int,
    update_internacao: schemas.Internacao,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    internacao = repository.get_internacao(db, id)
    if internacao is None:
        raise HTTPException(status_code=400, detail="Internação não encontrada")
    repository.update_internacao(db, update_internacao, id)
    return repository.get_internacao(db, id)


@internacao_api.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove uma internação")
async def delete_internacao(
    id: int,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    internacao = repository.get_internacao(db, id)
    if internacao is None:
        raise HTTPException(status_code=400, detail="Internação não encontrada")
    repository.delete_internacao(db, internacao)


def use_internacao_api(app_instance: FastAPI):
    app_instance.include_router(internacao_api)
