from datetime import datetime, timezone

from sqlalchemy.orm import Session, joinedload
from models.internacao_model import Internacao

import models.internacao_schemas as schemas

def get_internacoes(db:Session, skip:int=0, limit: int=100):
    return db.query(Internacao).options(joinedload(Internacao.tipo_alta)).offset(skip).limit(limit).all()

def get_internacao(db: Session, internacao_id: int):
    return db.query(Internacao).filter(Internacao.id == internacao_id).first()

def delete_internacao(db: Session, internacao: Internacao):
    db.delete(internacao)
    db.commit()
    return True

def update_internacao(db:Session, nova_internacao:schemas.Internacao, internacao_id: int):
    old_value = db.query(Internacao).filter(Internacao.id == internacao_id).first()
    if old_value is not None:
        update_data = nova_internacao.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(old_value, key, value)
        db.commit()
        db.refresh(old_value)
        return old_value
    else:
        return None


def update_internacao_alta(db:Session, alta:schemas.AltaInternacao, internacao_id: int):
    old_value = db.query(Internacao).filter(Internacao.id == internacao_id).first()
    if old_value is not None:
        old_value.data_alta = alta.data_alta
        old_value.obs_alta = alta.obs_alta
        old_value.tipo_alta_id = alta.tipo_alta_id
        db.commit()
        db.refresh(old_value)
        return old_value
    else:
        return None

def create_nova_internacao(db:Session, nova_internacao:schemas.Internacao):
    db_internacao = Internacao(
        data_internacao=nova_internacao.data_internacao,
        numero_prontuario=nova_internacao.numero_prontuario,
        setor_internacao=nova_internacao.setor_internacao,
        data_nascimento_paciente=nova_internacao.data_nascimento_paciente,
        nome_paciente=nova_internacao.nome_paciente,
        sexo_paciente=nova_internacao.sexo_paciente,
        grau_instrucao_paciente=nova_internacao.grau_instrucao_paciente,
        moradia_paciente=nova_internacao.moradia_paciente,
        familiares_atendidos=nova_internacao.familiares_atendidos,
        criado_por=nova_internacao.criado_por,
        criado_em=datetime.now(timezone.utc),
        data_alta=nova_internacao.data_alta,
        tipo_alta_id=nova_internacao.tipo_alta_id,
        obs_alta=nova_internacao.obs_alta
    )
    db.add(db_internacao)
    db.commit()
    db.refresh(db_internacao)
    return db_internacao
