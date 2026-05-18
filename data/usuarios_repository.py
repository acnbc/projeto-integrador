from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import func

from fastapi import HTTPException

from models.usuario_model import Usuario

import models.usuario_schemas as schemas
from controllers.auth import hash_password

def get_usuarios(db:Session, skip:int=0, limit: int=100):
    return db.query(Usuario).filter(Usuario.inativado_em.is_(None)).offset(skip).limit(limit).all()

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def inativa_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        return None
    usuario.inativado_em = datetime.now(timezone.utc)
    db.commit()
    db.refresh(usuario)
    return usuario

def update_usuario(db:Session, novo_usuario:schemas.UpdateUsuario, usuario_id: int):
    old_value = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if old_value is None:
        return None

    update_data = novo_usuario.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == 'senha':
            setattr(old_value, 'senha_hash', hash_password(value))
            continue
        if key == 'email':
            setattr(old_value, 'email', value.lower())
            continue
        setattr(old_value, key, value)
    db.commit()
    db.refresh(old_value)
    return old_value

def create_usuario(db:Session, novo_usuario:schemas.NovoUsuario):
    existing_user = db.query(Usuario).filter(
        func.lower(Usuario.email) == novo_usuario.email.lower()
    ).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email já cadastrado")
    usuario = Usuario(
        nome=novo_usuario.nome,
        email=novo_usuario.email.lower(),
        senha_hash=hash_password(novo_usuario.senha),
        perfil_id=novo_usuario.perfil_id,
        criado_em=datetime.now(timezone.utc)
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario
