from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload, selectinload
from models.internacao_model import Internacao
from models.parecer_model import Parecer

import models.internacao_schemas as schemas

def get_internacoes(db:Session, skip:int=0, limit: int=100):
    return (
        db.query(Internacao)
        .options(
            joinedload(Internacao.tipo_alta),
            selectinload(Internacao.pareceres).joinedload(Parecer.usuario),
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_internacao(db: Session, internacao_id: int):
    return (
        db.query(Internacao)
        .options(
            joinedload(Internacao.tipo_alta),
            selectinload(Internacao.pareceres).joinedload(Parecer.usuario),
        )
        .filter(Internacao.id == internacao_id)
        .first()
    )


def get_internacoes_por_prontuario(db: Session, numero_prontuario: str):
    return (
        db.query(Internacao)
        .options(selectinload(Internacao.pareceres))
        .filter(Internacao.numero_prontuario == numero_prontuario.strip())
        .order_by(Internacao.data_internacao.desc(), Internacao.id.desc())
        .all()
    )


def _extrair_dados_demograficos(internacoes: list):
    nome = None
    nascimento = None
    sexo = None
    nome_oculto = False

    for row in internacoes:
        if row.nome_paciente == "Paciente oculto":
            nome_oculto = True
        elif row.nome_paciente and nome is None:
            nome = row.nome_paciente

    for row in internacoes:
        if row.data_nascimento_paciente and nascimento is None:
            nascimento = row.data_nascimento_paciente
        if row.sexo_paciente and sexo is None:
            sexo = row.sexo_paciente

    if nome is None and internacoes:
        nome = internacoes[0].nome_paciente
    if nascimento is None and internacoes:
        nascimento = internacoes[0].data_nascimento_paciente
    if sexo is None and internacoes:
        sexo = internacoes[0].sexo_paciente

    return nome, nascimento, sexo or "F", nome_oculto


def montar_paciente_por_prontuario(numero_prontuario: str, internacoes: list) -> schemas.PacientePorProntuario | None:
    if not internacoes:
        return None

    nome, nascimento, sexo, nome_oculto = _extrair_dados_demograficos(internacoes)

    return schemas.PacientePorProntuario(
        numero_prontuario=numero_prontuario,
        nome_paciente=nome,
        data_nascimento_paciente=nascimento,
        sexo_paciente=sexo,
        nome_oculto=nome_oculto,
        internacoes=[
            schemas.InternacaoResumo(
                id=i.id,
                data_internacao=i.data_internacao,
                setor_internacao=i.setor_internacao,
                data_alta=i.data_alta,
                tipo_alta_id=i.tipo_alta_id,
                total_pareceres=len(i.pareceres) if i.pareceres is not None else 0,
            )
            for i in internacoes
        ],
    )


def get_internacoes_por_nome(db: Session, nome_paciente: str):
    termo = nome_paciente.strip()
    if not termo or termo == "Paciente oculto":
        return []
    return (
        db.query(Internacao)
        .options(selectinload(Internacao.pareceres))
        .filter(func.lower(Internacao.nome_paciente) == termo.lower())
        .order_by(Internacao.data_internacao.desc(), Internacao.id.desc())
        .all()
    )


def buscar_paciente_por_nome(db: Session, nome_paciente: str) -> schemas.PacientePorProntuario | None:
    internacoes = get_internacoes_por_nome(db, nome_paciente)
    if not internacoes:
        return None

    prontuarios = {i.numero_prontuario.strip() for i in internacoes}
    if len(prontuarios) > 1:
        raise ValueError(
            "Existem vários pacientes com este nome. Informe o número do prontuário."
        )

    prontuario = prontuarios.pop()
    do_prontuario = [i for i in internacoes if i.numero_prontuario.strip() == prontuario]
    return montar_paciente_por_prontuario(prontuario, do_prontuario)


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
