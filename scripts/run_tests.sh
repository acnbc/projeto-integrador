#!/usr/bin/env bash
# Executa testes com MySQL do Docker (porta 3307 para evitar conflito com MySQL local).
set -euo pipefail
cd "$(dirname "$0")/.."

echo "Subindo MySQL (Docker)..."
docker compose up -d db

echo "Aguardando banco..."
export DATABASE_URL="${DATABASE_URL:-mysql+pymysql://admin:admin@127.0.0.1:3307/ufrj_test}"
for _ in $(seq 1 30); do
  if python scripts/wait_for_db.py 2>/dev/null; then
    break
  fi
  sleep 2
done

export ENV=test
export SECRET_KEY="${SECRET_KEY:-chave-secreta-de-teste-com-32-caracteres}"
export DATABASE_ECHO=false

if [[ -d venv ]]; then
  # shellcheck disable=SC1091
  source venv/bin/activate
fi

pip install -q -r requirements-dev.txt
pytest "$@"
