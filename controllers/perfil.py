from data.connection import get_db
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import data.perfil_repository as repository
import models.perfil_schemas as schemas


perfil = APIRouter(prefix="/api/perfil", tags=["Perfil"])

@perfil.get("", summary="Lista todos os perfis", status_code=status.HTTP_200_OK, response_model=list[schemas.PerfilResponse])
async def get_tipos_alta(db:Session=Depends(get_db)):
    return repository.get_perfils(db)

def use_perfil(app_instance:FastAPI):
    app_instance.include_router(perfil)