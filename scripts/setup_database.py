"""Cria banco, usuário, tabelas, perfis e admin inicial."""
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from config.settings import settings
from controllers.auth import hash_password
from data.connection import Base
from models.internacao_model import Internacao  # noqa: F401
from models.parecer_model import Parecer  # noqa: F401
from models.perfil_model import Perfil
from models.tipo_alta_model import TipoAlta  # noqa: F401
from models.usuario_model import Usuario
from models.usuario_schemas import PerfilId

ADMIN_EMAIL = "anacarolinacabral@protonmail.com"
ADMIN_PASSWORD = "teste123"
ADMIN_NOME = "admin"

MYSQL_BOOTSTRAP = """
CREATE DATABASE IF NOT EXISTS ufrj CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin';
CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON ufrj.* TO 'admin'@'localhost';
GRANT ALL PRIVILEGES ON ufrj.* TO 'admin'@'%';
FLUSH PRIVILEGES;
"""


def bootstrap_mysql_as_root() -> None:
    print("Configurando banco e usuário MySQL (mysql -u root)...")
    result = subprocess.run(
        ["mysql", "-u", "root", "-e", MYSQL_BOOTSTRAP],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr or result.stdout)
        raise SystemExit(
            "Falha ao conectar como root. Tente: mysql -u root -p < scripts/bootstrap.sql"
        )


def create_tables_and_seed() -> None:
    engine = create_engine(settings.database_url)
    print("Criando tabelas...")
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    db = Session()
    try:
        if db.query(Perfil).count() == 0:
            db.add(Perfil(nome="coordenador"))
            db.add(Perfil(nome="aluno"))
            db.commit()
            print("Perfis coordenador e aluno criados.")

        existing = (
            db.query(Usuario)
            .filter(Usuario.email == ADMIN_EMAIL.lower())
            .first()
        )
        if existing:
            print(f"Admin já existe (id={existing.id}, email={existing.email}).")
            return

        admin = Usuario(
            nome=ADMIN_NOME,
            email=ADMIN_EMAIL.lower(),
            senha_hash=hash_password(ADMIN_PASSWORD),
            perfil_id=PerfilId.COORDENADOR,
            criado_em=datetime.now(timezone.utc),
        )
        db.add(admin)
        db.commit()
        print(f"Admin criado com id={admin.id}")
        print(f"Login: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
    finally:
        db.close()


def main() -> None:
    bootstrap_mysql_as_root()
    create_tables_and_seed()
    print("Setup concluído.")


if __name__ == "__main__":
    main()
