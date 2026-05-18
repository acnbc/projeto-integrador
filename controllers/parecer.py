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
_autorizado = Depends(perfil_permitido(PerfilId.COORDENADOR, PerfilId.ALUNO))


@parecer_api.get("", summary="Lista todos os pareceres", status_code=status.HTTP_200_OK, response_model=list[schemas.ParecerResponse])
async def get_pareceres(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    return repository.get_pareceres(db, skip, limit)


@parecer_api.post(
    "/completo",
    summary="Registra parecer vinculado a uma internação (nova ou existente)",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ParecerResponse,
)
async def post_parecer_completo(
    formulario: schemas.ParecerFormulario,
    db: Session = Depends(get_db),
    usuario: Usuario = _autorizado,
):
    try:
        return repository.create_parecer_completo(
            db, formulario, usuario.id, usuario.nome
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@parecer_api.post("", summary="Cria um novo parecer", status_code=status.HTTP_201_CREATED, response_model=schemas.ParecerResponse)
async def post_parecer(
    novo_parecer: schemas.NovoParecer,
    db: Session = Depends(get_db),
    usuario: Usuario = _coordenador,
):
    dados = novo_parecer.model_dump()
    dados["criado_por"] = usuario.id
    return repository.create_novo_parecer(db, schemas.NovoParecer(**dados))


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
