from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import OperationalError

from controllers.dashboard import use_dashboard_api
from controllers.internacao import use_internacao_api
from controllers.pages import use_pages
from controllers.parecer import use_parecer_api
from controllers.perfil import use_perfil
from controllers.tipo_alta import use_alta_api
from controllers.usuario import use_usuario_api

app = FastAPI(title="Gestor de prontuários", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(OperationalError)
async def database_unavailable_handler(_request: Request, _exc: OperationalError):
    return JSONResponse(
        status_code=503,
        content={"detail": "Banco de dados indisponível. Verifique se o MySQL está em execução."},
    )


@app.get("/health", tags=["Sistema"])
async def health():
    return {"status": "ok"}

use_pages(app)
use_internacao_api(app)
use_parecer_api(app)
use_alta_api(app)
use_perfil(app)
use_usuario_api(app)
use_dashboard_api(app)
