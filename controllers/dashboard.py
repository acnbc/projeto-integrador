from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy import func
from sqlalchemy.orm import Session

from controllers.auth import perfil_permitido
from data.connection import get_db
from models.internacao_model import Internacao
from models.parecer_model import Parecer
from models.usuario_model import Usuario
from models.usuario_schemas import PerfilId

dashboard_api = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

_coordenador = Depends(perfil_permitido(PerfilId.COORDENADOR))


@dashboard_api.get("/stats")
async def obter_estatisticas(
    db: Session = Depends(get_db),
    _: Usuario = _coordenador,
):
    pareceres_completos = (
        db.query(Parecer)
        .filter(
            Parecer.data_solicitacao_parecer.isnot(None),
            Parecer.data_parecer.isnot(None),
        )
        .all()
    )

    if pareceres_completos:
        horas_totais = []
        for p in pareceres_completos:
            delta = p.data_parecer - p.data_solicitacao_parecer
            horas_totais.append(delta.total_seconds() / 3600)
        tempo_medio_dias = round(sum(horas_totais) / len(horas_totais) / 24, 1)
    else:
        tempo_medio_dias = 0

    contagens = (
        db.query(Internacao.setor_internacao, func.count(Parecer.id))
        .join(Parecer, Parecer.internacao_id == Internacao.id)
        .group_by(Internacao.setor_internacao)
        .all()
    )

    total = sum(c[1] for c in contagens) or 1
    distribuicao_setores = [
        {
            "setor": setor,
            "quantidade": qtd,
            "percentual": round(100 * qtd / total, 1),
        }
        for setor, qtd in contagens
    ]

    return {
        "tempo_medio_resposta_dias": tempo_medio_dias,
        "total_pareceres_com_resposta": len(pareceres_completos),
        "distribuicao_por_setor": distribuicao_setores,
    }


def use_dashboard_api(app_instance: FastAPI):
    app_instance.include_router(dashboard_api)
