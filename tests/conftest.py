"""Fixtures compartilhadas: banco de testes e cliente HTTP."""
import os
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("ENV", "test")
os.environ.setdefault(
    "DATABASE_URL",
    "mysql+pymysql://admin:admin@127.0.0.1:3307/ufrj_test",
)
os.environ.setdefault("SECRET_KEY", "chave-secreta-de-teste-com-32-caracteres")
os.environ.setdefault("DATABASE_ECHO", "false")

from config.settings import settings  # noqa: E402
from controllers.auth import hash_password  # noqa: E402
from data.connection import Base, get_db  # noqa: E402
from main import app  # noqa: E402
from models.internacao_model import Internacao  # noqa: F401, E402
from models.parecer_model import Parecer  # noqa: F401, E402
from models.perfil_model import Perfil  # noqa: E402
from models.tipo_alta_model import TipoAlta  # noqa: F401, E402
from models.usuario_model import Usuario  # noqa: E402
from models.usuario_schemas import PerfilId  # noqa: E402

TEST_ADMIN_EMAIL = "coordenador@test.example"
TEST_ADMIN_PASSWORD = "senha12345"
TEST_ALUNO_EMAIL = "aluno@test.example"
TEST_ALUNO_PASSWORD = "senha12345"


@pytest.fixture(scope="session")
def engine():
    eng = create_engine(settings.database_url, pool_pre_ping=True)
    Base.metadata.drop_all(bind=eng)
    Base.metadata.create_all(bind=eng)
    yield eng
    Base.metadata.drop_all(bind=eng)


@pytest.fixture(scope="session")
def seed(engine):
    Session = sessionmaker(bind=engine)
    db = Session()
    try:
        if db.query(Perfil).count() == 0:
            db.add(Perfil(nome="coordenador"))
            db.add(Perfil(nome="aluno"))
            db.commit()

        if not db.query(Usuario).filter(Usuario.email == TEST_ADMIN_EMAIL).first():
            db.add(
                Usuario(
                    nome="Coordenador Teste",
                    email=TEST_ADMIN_EMAIL,
                    senha_hash=hash_password(TEST_ADMIN_PASSWORD),
                    perfil_id=PerfilId.COORDENADOR,
                    criado_em=datetime.now(timezone.utc),
                )
            )
        if not db.query(Usuario).filter(Usuario.email == TEST_ALUNO_EMAIL).first():
            db.add(
                Usuario(
                    nome="Aluno Teste",
                    email=TEST_ALUNO_EMAIL,
                    senha_hash=hash_password(TEST_ALUNO_PASSWORD),
                    perfil_id=PerfilId.ALUNO,
                    criado_em=datetime.now(timezone.utc),
                )
            )
        db.commit()
    finally:
        db.close()


@pytest.fixture
def db_session(engine, seed):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(engine, seed):
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def admin_headers(client):
    response = client.post(
        "/api/usuario/token",
        data={"username": TEST_ADMIN_EMAIL, "password": TEST_ADMIN_PASSWORD},
    )
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def aluno_headers(client):
    response = client.post(
        "/api/usuario/token",
        data={"username": TEST_ALUNO_EMAIL, "password": TEST_ALUNO_PASSWORD},
    )
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
