from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
pages = APIRouter(tags=["Páginas"])


def _ctx(request: Request, page_title: str, active: str, **extra):
    return {"request": request, "page_title": page_title, "active": active, **extra}


@pages.get("/", response_class=HTMLResponse)
async def raiz():
    return RedirectResponse(url="/login", status_code=302)


@pages.get("/login", response_class=HTMLResponse)
async def pagina_login(request: Request):
    return templates.TemplateResponse(
        "login.html",
        _ctx(request, "Entrar", "login", hide_nav=True),
    )


@pages.get("/usuarios", response_class=HTMLResponse)
async def pagina_usuarios(request: Request):
    return templates.TemplateResponse(
        "usuarios.html",
        _ctx(request, "Usuários", "usuarios", perfil_requerido="coordenador"),
    )


@pages.get("/pareceres/novo", response_class=HTMLResponse)
async def pagina_parecer_novo(request: Request):
    return templates.TemplateResponse(
        "parecer_form.html",
        _ctx(request, "Novo parecer", "parecer-novo"),
    )


@pages.get("/pareceres", response_class=HTMLResponse)
async def pagina_pareceres(request: Request):
    return templates.TemplateResponse(
        "pareceres.html",
        _ctx(request, "Pareceres", "pareceres", perfil_requerido="coordenador"),
    )


@pages.get("/pacientes", response_class=HTMLResponse)
async def pagina_pacientes(request: Request):
    return templates.TemplateResponse(
        "pacientes.html",
        _ctx(request, "Pacientes", "pacientes", perfil_requerido="coordenador"),
    )


@pages.get("/dashboard", response_class=HTMLResponse)
async def pagina_dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        _ctx(request, "Dashboard", "dashboard", perfil_requerido="coordenador"),
    )


def use_pages(app_instance: FastAPI):
    app_instance.include_router(pages)
