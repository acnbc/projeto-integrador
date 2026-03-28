from data.connection import get_db
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import data.tipo_alta_repository as repository
import models.tipo_alta_schemas as schemas


alta_api = APIRouter(prefix="/api/tipo-alta", tags=["Tipos de Alta"])

@alta_api.get("", summary="Lista todos os tipos de altas", status_code=status.HTTP_200_OK, response_model=list[schemas.TipoAltaResponse])
async def get_tipos_alta(skip: int = 0, limit: int = 100, db:Session=Depends(get_db)):
    return repository.get_tipos_altas(db, skip, limit)


'''
 -  We use response from TodoRead schema so it'll show all 4 properties of the record.
 -  Incoming request uses Todo schema. According to the schema two parameters are mandatory
    it'll act as a validation as well
'''
@alta_api.post("", summary="Cria um novo tipo de alta", status_code=status.HTTP_201_CREATED, response_model=schemas.TipoAltaResponse)
async def post_tipo_alta(tipo_alta:schemas.TipoAlta, db:Session=Depends(get_db)):
    return repository.create_tipo_alta(db, tipo_alta)


'''
 -  To get todo detail we only need one parameter to fetch a todo based on its id
 -  Throw http exception if record is not found
'''
@alta_api.get("/{id}", summary="Detalhes de um tipo de alta", status_code=status.HTTP_200_OK, response_model=schemas.TipoAltaResponse)
async def get_tipo_alta(id: int, db:Session=Depends(get_db)):
    tipo_alta = repository.get_tipo_alta(db, id)
    if tipo_alta is None:
        raise HTTPException(status_code=400, detail="Tipo de alta não encontrado")
    return tipo_alta


'''
 -  Put request means all update according to the REST best practice. On this case 
    the required parameters are identical with post so we use the same schema for 
    incoming request with post which is Todo
'''
@alta_api.put("/{id}", summary="Atualização de um tipo de alta",status_code=status.HTTP_200_OK, response_model=schemas.TipoAltaResponse)
async def put_tipo_alta(id: int, update_tipo_alta:schemas.TipoAlta, db:Session=Depends(get_db)):
    tipo_alta = repository.get_tipo_alta(db, id)
    if tipo_alta is None:
        raise HTTPException(status_code=400, detail="Todo is not found")

    repository.update_tipo_alta(db, update_tipo_alta, id)
    return tipo_alta

def use_alta_api(app_instance:FastAPI):
    app_instance.include_router(alta_api)