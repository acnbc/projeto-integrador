from sqlalchemy.orm import Session
from models.perfil_model import Perfil

def get_perfis(db:Session, skip:int=0, limit: int=100):
    return db.query(Perfil).offset(skip).limit(limit).all()
