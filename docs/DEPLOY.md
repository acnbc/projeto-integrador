# Deploy em nuvem

O projeto está preparado para execução em contêineres (Docker) e publicação em provedores de nuvem.

## Execução local com Docker (simulação de nuvem)

```bash
# Na raiz do projeto
export SECRET_KEY="sua-chave-secreta-com-pelo-menos-32-caracteres"
docker compose up --build
```

- API: http://localhost:8000  
- Documentação: http://localhost:8000/docs  
- Health check: http://localhost:8000/health  

Login inicial (criado automaticamente pelo seed):

- E-mail: `anacarolinacabral@protonmail.com`  
- Senha: `teste123`

## Render.com

1. Conecte o repositório Git no [Render](https://render.com).
2. Crie um **Web Service** usando o `Dockerfile` ou importe o `render.yaml`.
3. Crie um banco **MySQL** gerenciado (ou use PlanetScale, Railway, AWS RDS, etc.).
4. Defina a variável de ambiente `DATABASE_URL` com a URL do banco (formato `mysql+pymysql://...`).
5. Defina `SECRET_KEY` (Render pode gerar automaticamente via blueprint).
6. O health check usa `/health`.

## Railway / Fly.io / VPS

O mesmo `Dockerfile` funciona em qualquer plataforma que aceite contêineres:

1. Configure `DATABASE_URL` apontando para MySQL na nuvem.
2. Configure `SECRET_KEY` e `ENV=production`.
3. Exponha a porta `8000` (ou use `PORT` se o provedor injetar outra porta).

## Variáveis de ambiente

| Variável | Descrição |
|----------|-----------|
| `DATABASE_URL` | URL SQLAlchemy do MySQL |
| `SECRET_KEY` | Chave JWT (mín. 32 caracteres recomendado) |
| `ENV` | `dev` (lê `.env`) ou `production` / `test` |
| `DATABASE_ECHO` | `true` para log SQL (apenas debug) |
| `PORT` | Porta HTTP (padrão 8000 no Docker) |

Copie `.env.example` para `.env` no desenvolvimento local.

## Testes locais

```bash
./scripts/run_tests.sh
```

O MySQL do Docker usa a porta **3307** (evita conflito com MySQL instalado na máquina na 3306).

## Integração contínua

O pipeline em `.github/workflows/ci.yml` executa automaticamente em push e pull request:

1. Sobe MySQL como serviço.
2. Roda `pytest` com cobertura.
3. Valida o build da imagem Docker.
