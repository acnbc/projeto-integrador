from controllers.tipo_alta import use_alta_api
from controllers.perfil import use_perfil
from controllers.internacao import use_internacao_api
from controllers.parecer import use_parecer_api
from controllers.usuario import use_usuario_api
from fastapi import FastAPI

app = FastAPI(title="Gestor de prontuários API", version="1.0.0")

use_internacao_api(app)
use_parecer_api(app)
use_alta_api(app)
use_perfil(app)
use_usuario_api(app)
