from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from controllers.auth import perfil_permitido
from data.connection import get_db
from models.usuario_model import Usuario
from models.usuario_schemas import PerfilId
import data.parecer_repository as repository
import models.parecer_schemas as schemas

parecer_api = APIRouter(prefix="/api/parecer", tags=["Parecer"])

_coordenador = Depends(perfil_permitido(PerfilId.COORDENADOR))
_aluno = Depends(perfil_permitido(PerfilId.ALUNO))


@parecer_api.get("", summary="Lista todos os pareceres", status_code=status.HTTP_200_OK, response_model=list[schemas.ParecerResponse])
async def get_pareceres(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    return repository.get_pareceres(db, skip, limit)


@parecer_api.post("", summary="Cria um novo parecer", status_code=status.HTTP_201_CREATED, response_model=schemas.ParecerResponse)
async def post_parecer(
    internacao: schemas.NovoParecer,
    db: Session = Depends(get_db),
    _: Usuario = _aluno,
):
    return repository.create_novo_parecer(db, internacao)


@parecer_api.get("/{id}", summary="Detalhes de um parecer", status_code=status.HTTP_200_OK, response_model=schemas.ParecerResponse)
async def get_parecer(
    id: int,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    parecer = repository.get_parecer(db, id)
    if parecer is None:
        raise HTTPException(status_code=400, detail="Parecer não encontrado")
    return parecer


@parecer_api.put("/{id}", summary="Atualização de um parecer", status_code=status.HTTP_200_OK, response_model=schemas.ParecerResponse)
async def put_parecer(
    id: int,
    update_parecer: schemas.NovoParecer,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    parecer = repository.get_parecer(db, id)
    if parecer is None:
        raise HTTPException(status_code=400, detail="Parecer não encontrado")
    repository.update_parecer(db, update_parecer, id)
    return repository.get_parecer(db, id)


@parecer_api.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove um parecer")
async def delete_parecer(
    id: int,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    parecer = repository.get_parecer(db, id)
    if parecer is None:
        raise HTTPException(status_code=400, detail="Parecer não encontrado")
    repository.delete_parecer(db, parecer)


def use_parecer_api(app_instance: FastAPI):
    app_instance.include_router(parecer_api)
