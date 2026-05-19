"""Aguarda o MySQL ficar disponível (útil em Docker e CI)."""
import os
import sys
import time

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

MAX_ATTEMPTS = int(os.getenv("DB_WAIT_ATTEMPTS", "30"))
INTERVAL_SEC = float(os.getenv("DB_WAIT_INTERVAL", "2"))


def main() -> None:
    url = os.environ["DATABASE_URL"]
    print(f"Aguardando banco ({MAX_ATTEMPTS} tentativas)...")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            engine = create_engine(url, pool_pre_ping=True)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Banco disponível.")
            return
        except OperationalError as exc:
            print(f"Tentativa {attempt}/{MAX_ATTEMPTS}: {exc}")
            time.sleep(INTERVAL_SEC)
    print("Banco indisponível após todas as tentativas.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
