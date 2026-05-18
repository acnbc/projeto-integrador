from fastapi import APIRouter, Depends, FastAPI, status
from sqlalchemy.orm import Session

from controllers.auth import perfil_permitido
from data.connection import get_db
from models.usuario_model import Usuario
from models.usuario_schemas import PerfilId
import data.perfil_repository as repository
import models.perfil_schemas as schemas

perfil = APIRouter(prefix="/api/perfil", tags=["Perfil"])

_coordenador = Depends(perfil_permitido(PerfilId.COORDENADOR))


@perfil.get("", summary="Lista todos os perfis", status_code=status.HTTP_200_OK, response_model=list[schemas.PerfilResponse])
async def get_perfis(
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    return repository.get_perfils(db)


def use_perfil(app_instance: FastAPI):
    app_instance.include_router(perfil)
