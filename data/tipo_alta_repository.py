from sqlalchemy.orm import Session
from models.tipo_alta_model import TipoAlta

import models.tipo_alta_schemas as schemas

def get_tipos_altas(db:Session, skip:int=0, limit: int=100):
    return db.query(TipoAlta).offset(skip).limit(limit).all()

def get_tipo_alta(db: Session, tipo_alta_id: int):
    return db.query(TipoAlta).filter(TipoAlta.id == tipo_alta_id).first()

def update_tipo_alta(db:Session, novo_tipo_alta:schemas.TipoAlta, tipo_id: int):
    old_value = db.query(TipoAlta).filter(TipoAlta.id == tipo_id).first()
    if old_value is not None:
        old_value.alta = novo_tipo_alta.alta if novo_tipo_alta.alta is not None else old_value.alta
        db.commit()
        db.refresh(old_value)
        return old_value
    else:
        return None

def create_tipo_alta(db:Session, novo_tipo_alta:schemas.TipoAlta):
    db_tipo_alta = TipoAlta(alta=novo_tipo_alta.alta)
    db.add(db_tipo_alta)
    db.commit()
    db.refresh(db_tipo_alta)
    return db_tipo_alta
