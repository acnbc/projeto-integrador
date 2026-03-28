from datetime import datetime, timezone

import bcrypt
from sqlalchemy.orm import Session
from models.usuario_model import Usuario

import models.usuario_schemas as schemas

def get_usuarios(db:Session, skip:int=0, limit: int=100):
    return db.query(Usuario).filter(Usuario.inativado_em.is_(None)).offset(skip).limit(limit).all()

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def inativa_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        return False
    usuario.inativado_em = datetime.now(timezone.utc)
    db.commit()
    db.refresh(usuario)
    return True

def update_usuario(db:Session, novo_usuario:schemas.UpdateUsuario, usuario_id: int):
    old_value = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if old_value is None:
        return None

    update_data = novo_usuario.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == 'senha':
            salt = bcrypt.gensalt()
            senha_bytes = value.encode('utf-8')
            hash_senha = bcrypt.hashpw(senha_bytes, salt)
            setattr(old_value, key, hash_senha.decode('utf-8'))
            continue
        setattr(old_value, key, value)
    db.commit()
    db.refresh(old_value)
    return old_value

def create_usuario(db:Session, nova_internacao:schemas.NovoUsuario):
    salt = bcrypt.gensalt()
    senha_bytes = nova_internacao.senha.encode('utf-8')
    hash_senha = bcrypt.hashpw(senha_bytes, salt)
    usuario = Usuario(
        nome=nova_internacao.nome,
        email = nova_internacao.email,
        senha = hash_senha.decode('utf-8'),
        perfil_id = nova_internacao.perfil_id,
        criado_em=datetime.now(timezone.utc)
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario
