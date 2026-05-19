"""Inicializa tabelas e seed em ambiente Docker/nuvem (sem acesso root ao MySQL)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(SCRIPTS))

from wait_for_db import main as wait_for_db
from setup_database import create_tables_and_seed


def main() -> None:
    wait_for_db()
    create_tables_and_seed()
    print("Setup Docker concluído.")


if __name__ == "__main__":
    main()
