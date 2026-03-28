from datetime import datetime, timezone

from sqlalchemy.orm import Session
from models.parecer_model import Parecer

import models.parecer_schemas as schemas

def update_parecer(db:Session, novo_parecer:schemas.NovoParecer, parecer_id: int):
    old_value = db.query(Parecer).filter(Parecer.id == parecer_id).first()
    if old_value is not None:
        update_data = novo_parecer.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(old_value, key, value)
        db.commit()
        db.refresh(old_value)
        return old_value
    else:
        return None

def create_novo_parecer(db:Session, novo_parecer:schemas.NovoParecer):
    db_parecer = Parecer(
        data_solicitacao_parecer=novo_parecer.data_solicitacao_parecer,
        data_parecer=novo_parecer.data_parecer,
        texto_parecer=novo_parecer.texto_parecer,
        internacao_id=novo_parecer.internacao_id,
        criado_por=novo_parecer.criado_por,
        criado_em=datetime.now(timezone.utc)
    )
    db.add(db_parecer)
    db.commit()
    db.refresh(db_parecer)
    return db_parecer

def get_pareceres(db:Session, skip:int=0, limit: int=100):
    return db.query(Parecer).offset(skip).limit(limit).all()

def get_parecer(db: Session, parecer_id: int):
    return db.query(Parecer).filter(Parecer.id == parecer_id).first()

def delete_parecer(db: Session, parecer: Parecer):
    db.delete(parecer)
    db.commit()
    return True
