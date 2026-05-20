from datetime import timedelta

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.orm import Session

from config.settings import settings
from controllers.auth import (
    create_access_token,
    get_current_user,
    perfil_permitido,
    verify_password,
)
from data.connection import get_db
from models.usuario_model import Usuario
import data.usuarios_repository as repository
import models.usuario_schemas as schemas

usuario_api = APIRouter(prefix="/api/usuario", tags=["Usuario"])

_coordenador = Depends(perfil_permitido(schemas.PerfilId.COORDENADOR))


@usuario_api.post("/token", response_model=schemas.Token)
async def login_para_token_acesso(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    usuario = (
        db.query(Usuario)
        .filter(func.lower(Usuario.email) == form_data.username.lower())
        .first()
    )
    if (
        not usuario
        or usuario.inativado_em is not None
        or not verify_password(form_data.password, usuario.senha_hash)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": str(usuario.id)},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@usuario_api.get("/me", response_model=schemas.UsuarioResponse)
async def me(usuario: Usuario = Depends(get_current_user)):
    return usuario


@usuario_api.get("", summary="Lista todos os usuários", status_code=status.HTTP_200_OK, response_model=list[schemas.UsuarioResponse])
async def get_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    return repository.get_usuarios(db, skip, limit)


@usuario_api.post("", summary="Cria um novo usuário", status_code=status.HTTP_201_CREATED, response_model=schemas.UsuarioResponse)
async def post_usuario(
    usuario: schemas.NovoUsuario,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    return repository.create_usuario(db, usuario)


@usuario_api.post("/{id}/inativar", summary="Inativa um usuário", status_code=status.HTTP_201_CREATED, response_model=schemas.UsuarioResponse)
async def post_inativar_usuario(
    id: int,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    usuario = repository.inativa_usuario(db, id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


@usuario_api.get("/{id}", summary="Detalhes de um usuário", status_code=status.HTTP_200_OK, response_model=schemas.UsuarioResponse)
async def get_usuario_por_id(
    id: int,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    usuario = repository.get_usuario(db, id)
    if usuario is None:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    return usuario


@usuario_api.put("/{id}", summary="Atualização de um usuário", status_code=status.HTTP_200_OK, response_model=schemas.UsuarioResponse)
async def put_usuario(
    id: int,
    update_usuario: schemas.UpdateUsuario,
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    usuario = repository.get_usuario(db, id)
    if usuario is None:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    repository.update_usuario(db, update_usuario, id)
    return repository.get_usuario(db, id)


def use_usuario_api(app_instance: FastAPI):
    app_instance.include_router(usuario_api)
