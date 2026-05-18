from datetime import datetime, timezone

from sqlalchemy.orm import Session, joinedload

from models.internacao_model import Internacao
from models.parecer_model import Parecer

import models.parecer_schemas as schemas


SETORES_VALIDOS = {
    "CIRURGIA CARDÍACA",
    "CARDIOLOGIA",
    "CIRURGIA PLÁSTICA",
    "CIRURGIA GERA",
    "UI CIRÚRGICA",
    "CIRURGIA TORÁCICA",
    "CUCC (CENTRO UNIVERSITÁRIO DE CONTROLE DO CÂNCER)",
    "CIRURGIA VASCULAR",
    "CUIDADOS PALIATIVOS",
    "CLINICA DA DOR",
    "CLINICA MÉDICA",
    "CTI GERAL",
    "NAI (Núcleo de Atenção ao Idoso)",
    "DERMATOLOGIA",
    "NESA (Núcleo de Estudos de Saúde do Adolescente)",
    "DIP",
    "NEUROCIRURGIA",
    "ENDOCRINOLOGIA |",
    "OFTALMOLOGIA",
    "ORTOPEDIA",
    "GINECOLOGIA",
    "OTORRINOLARINGOLOGIA",
    "HEMATOLOGIA",
    "PEDIATRIA",
    "PSIQUIATRIA",
    "PNEUMOLOGIA",
    "UCI - Unidade Cardio Intensiva",
    "REUMATOLOGIA",
    "UROLOGIA",
}


def _nome_paciente_final(formulario: schemas.ParecerFormulario) -> str:
    if formulario.ocultar_nome_paciente:
        return "Paciente oculto"
    return (formulario.nome_paciente or "").strip() or "Não informado"


def _texto_parecer_final(formulario: schemas.ParecerFormulario, aluno_nome: str) -> str | None:
    texto = (formulario.observacoes_gerais or "").strip()
    if aluno_nome:
        prefixo = f"Parecer registrado por: {aluno_nome}.\n\n"
        return prefixo + texto if texto else prefixo.strip()
    return texto or None


def _sexo_paciente_final(formulario: schemas.ParecerFormulario) -> str:
    sexo = (formulario.sexo_paciente or "F").strip().upper()
    return sexo if sexo in ("F", "M") else "F"


def _atualizar_dados_paciente(internacao: Internacao, formulario: schemas.ParecerFormulario):
    internacao.numero_prontuario = formulario.numero_prontuario.strip()
    internacao.data_nascimento_paciente = formulario.data_nascimento_paciente
    internacao.nome_paciente = _nome_paciente_final(formulario)
    internacao.sexo_paciente = _sexo_paciente_final(formulario)


def _aplicar_dados_nova_internacao(internacao: Internacao, formulario: schemas.ParecerFormulario):
    _atualizar_dados_paciente(internacao, formulario)
    internacao.data_internacao = formulario.data_internacao
    internacao.setor_internacao = formulario.setor_internacao
    internacao.data_alta = formulario.data_alta
    internacao.tipo_alta_id = formulario.tipo_alta_id
    if formulario.observacoes_gerais:
        internacao.obs_alta = formulario.observacoes_gerais


def _atualizar_alta_se_informada(internacao: Internacao, formulario: schemas.ParecerFormulario):
    if formulario.data_alta is not None:
        internacao.data_alta = formulario.data_alta
    if formulario.tipo_alta_id is not None:
        internacao.tipo_alta_id = formulario.tipo_alta_id


def update_parecer(db: Session, novo_parecer: schemas.NovoParecer, parecer_id: int):
    old_value = db.query(Parecer).filter(Parecer.id == parecer_id).first()
    if old_value is not None:
        update_data = novo_parecer.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(old_value, key, value)
        db.commit()
        db.refresh(old_value)
        return old_value
    return None


def create_parecer_completo(
    db: Session,
    formulario: schemas.ParecerFormulario,
    aluno_id: int,
    aluno_nome: str,
):
    if formulario.setor_internacao not in SETORES_VALIDOS:
        raise ValueError("Setor de internação inválido")

    texto_parecer = _texto_parecer_final(formulario, aluno_nome)

    if formulario.internacao_id:
        internacao = db.query(Internacao).filter(Internacao.id == formulario.internacao_id).first()
        if internacao is None:
            raise ValueError("Internação não encontrada")
        if internacao.numero_prontuario.strip() != formulario.numero_prontuario.strip():
            raise ValueError("Internação não pertence a este prontuário")
        _atualizar_dados_paciente(internacao, formulario)
        _atualizar_alta_se_informada(internacao, formulario)
    else:
        internacao = Internacao(
            data_internacao=formulario.data_internacao,
            numero_prontuario=formulario.numero_prontuario.strip(),
            setor_internacao=formulario.setor_internacao,
            sexo_paciente=_sexo_paciente_final(formulario),
            criado_por=aluno_id,
            criado_em=datetime.now(timezone.utc),
        )
        _aplicar_dados_nova_internacao(internacao, formulario)
        db.add(internacao)
        db.flush()

    parecer = Parecer(
        data_solicitacao_parecer=formulario.data_solicitacao_parecer,
        data_parecer=formulario.data_parecer,
        texto_parecer=texto_parecer,
        numero_prontuario=formulario.numero_prontuario.strip(),
        internacao_id=internacao.id,
        criado_por=aluno_id,
        criado_em=datetime.now(timezone.utc),
    )
    db.add(parecer)
    db.commit()
    return get_parecer(db, parecer.id)


def create_novo_parecer(db: Session, novo_parecer: schemas.NovoParecer):
    internacao = (
        db.query(Internacao).filter(Internacao.id == novo_parecer.internacao_id).first()
    )
    prontuario = internacao.numero_prontuario if internacao else ""
    db_parecer = Parecer(
        data_solicitacao_parecer=novo_parecer.data_solicitacao_parecer,
        data_parecer=novo_parecer.data_parecer,
        texto_parecer=novo_parecer.texto_parecer,
        numero_prontuario=prontuario,
        internacao_id=novo_parecer.internacao_id,
        criado_por=novo_parecer.criado_por,
        criado_em=datetime.now(timezone.utc),
    )
    db.add(db_parecer)
    db.commit()
    db.refresh(db_parecer)
    return db_parecer


def get_pareceres(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Parecer)
        .options(joinedload(Parecer.usuario), joinedload(Parecer.internacao))
        .order_by(Parecer.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_parecer(db: Session, parecer_id: int):
    return (
        db.query(Parecer)
        .options(joinedload(Parecer.usuario), joinedload(Parecer.internacao))
        .filter(Parecer.id == parecer_id)
        .first()
    )


def delete_parecer(db: Session, parecer: Parecer):
    db.delete(parecer)
    db.commit()
    return True
