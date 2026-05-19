# Gestor de Prontuários

Sistema web para registro e gestão de pareceres clínicos vinculados a internações hospitalares (FastAPI + MySQL + JavaScript).

## Requisitos

- Python 3.12+
- MySQL 8+ (local ou Docker)
- Git

## Desenvolvimento local

1. Clone o repositório e crie o ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copie as variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```

3. Configure o banco e o usuário admin:
   ```bash
   python scripts/setup_database.py
   ```

4. Execute a API:
   ```bash
   fastapi dev main.py
   ```

5. Acesse http://localhost:8000/docs

## Docker (nuvem / contêineres)

```bash
export SECRET_KEY="sua-chave-secreta-com-pelo-menos-32-caracteres"
docker compose up --build
```

Detalhes de deploy em nuvem: [docs/DEPLOY.md](docs/DEPLOY.md)

## Testes

Com Docker (recomendado — MySQL na porta **3307** para não conflitar com MySQL local):

```bash
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

Ou manualmente:

```bash
docker compose up -d db
export ENV=test
export DATABASE_URL=mysql+pymysql://admin:admin@127.0.0.1:3307/ufrj_test
export SECRET_KEY=chave-secreta-de-teste-com-32-caracteres
pip install -r requirements-dev.txt
pytest
```

## Integração contínua

O workflow GitHub Actions (`.github/workflows/ci.yml`) executa testes e build Docker em cada push/PR.