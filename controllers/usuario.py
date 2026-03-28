from data.connection import get_db
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import data.usuarios_repository as repository
import models.usuario_schemas as schemas


usuario_api = APIRouter(prefix="/api/usuario", tags=["Usuario"])

@usuario_api.get("", summary="Lista todos os usuários", status_code=status.HTTP_200_OK, response_model=list[schemas.UsuarioResponse])
async def get_usuarios(skip: int = 0, limit: int = 100, db:Session=Depends(get_db)):
    return repository.get_usuarios(db, skip, limit)

@usuario_api.post("", summary="Cria um novo usuário", status_code=status.HTTP_201_CREATED, response_model=schemas.UsuarioResponse)
async def post_usuario(usuario:schemas.NovoUsuario, db:Session=Depends(get_db)):
    return repository.create_usuario(db, usuario)


@usuario_api.post("/{id}/inativar", summary="Inativa um usuário", status_code=status.HTTP_201_CREATED, response_model=schemas.UsuarioResponse)
async def post_usuario(id: int, db:Session=Depends(get_db)):
    return repository.inativa_usuario(db, id)


@usuario_api.get("/{id}", summary="Detalhes de um usuário", status_code=status.HTTP_200_OK, response_model=schemas.UsuarioResponse)
async def patch_usuario(id: int, db:Session=Depends(get_db)):
    parecer = repository.get_usuario(db, id)
    if parecer is None:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    return parecer

@usuario_api.put("/{id}", summary="Atualização de um usuário",status_code=status.HTTP_200_OK, response_model=schemas.UsuarioResponse)
async def put_usuario(id: int, update_usuario:schemas.UpdateUsuario, db:Session=Depends(get_db)):
    parecer = repository.get_usuario(db, id)
    if parecer is None:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")

    repository.update_usuario(db, update_usuario, id)
    return parecer

def use_usuario_api(app_instance:FastAPI):
    app_instance.include_router(usuario_api)