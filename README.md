# Gestor de Prontuários

[![CI](https://github.com/acnbc/projeto-integrador/actions/workflows/ci.yml/badge.svg)](https://github.com/acnbc/projeto-integrador/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.12+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1)
![License](https://img.shields.io/badge/license-academic-lightgrey)

Sistema web para registro e gestão de pareceres clínicos vinculados a internações hospitalares, desenvolvido como **Projeto Integrador** da disciplina homônima do curso de **Ciência da Computação — UNIVESP**.

A aplicação permite que alunos registrem pareceres com dados do paciente e da internação, enquanto coordenadores acompanham listagens, pacientes, usuários e indicadores analíticos em um painel dedicado.

---

## Índice

- [Sobre o projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Stack tecnológica](#stack-tecnológica)
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Início rápido](#início-rápido)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Testes](#testes)
- [Integração contínua](#integração-contínua)
- [Deploy em nuvem](#deploy-em-nuvem)
- [Documentação da API](#documentação-da-api)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Relatório final](#relatório-final)
- [Licença](#licença)

---

## Sobre o projeto

O **Gestor de Prontuários** foi concebido para apoiar o fluxo de trabalho em contexto hospitalar simulado: um paciente pode ter várias internações, cada internação pode receber múltiplos pareceres, e cada parecer registra prontuário, datas de solicitação/resposta, setor e responsável pelo registro.

O sistema atende aos requisitos da matéria **Projeto Integrado (UNIVESP)**, contemplando framework web, banco de dados, JavaScript, nuvem, acessibilidade, controle de versão, integração contínua, testes automatizados e uso de API com análise de dados.

Documentação acadêmica detalhada: [docs/RELATORIO_FINAL.md](docs/RELATORIO_FINAL.md).

---

## Funcionalidades

| Perfil | Recursos |
|--------|----------|
| **Aluno** | Login, cadastro de pareceres (`/pareceres/novo`), busca de paciente por prontuário ou nome, preenchimento assistido de dados |
| **Coordenador** | Tudo do aluno + gestão de usuários, listagem de pareceres, visão de pacientes/internações, dashboard analítico |

Principais capacidades:

- Autenticação JWT com perfis (`coordenador` / `aluno`)
- API REST documentada (OpenAPI/Swagger)
- Interface web responsiva (menu mobile, tabelas adaptáveis)
- Dashboard com tempo médio de resposta e distribuição por setor
- Health check (`GET /health`) para monitoramento e deploy

---

## Stack tecnológica

| Camada | Tecnologia |
|--------|------------|
| Backend | [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/), [Pydantic](https://docs.pydantic.dev/) v2 |
| Banco de dados | MySQL 8 |
| Frontend | HTML (Jinja2), CSS e JavaScript vanilla |
| Autenticação | JWT (PyJWT), hash de senha (Argon2 via pwdlib) |
| Infraestrutura | Docker, Docker Compose, GitHub Actions |
| Testes | pytest, httpx (TestClient) |

---

## Arquitetura

```
┌─────────────┐     HTTP/JSON      ┌──────────────┐     SQLAlchemy     ┌────────┐
│  Browser    │ ◄────────────────► │   FastAPI    │ ◄────────────────► │ MySQL  │
│  (JS/CSS)   │                    │  controllers │                    │        │
└─────────────┘                    │  repositories│                    └────────┘
                                   │  models      │
                                   └──────────────┘
```

- **Controllers** — rotas HTTP, autorização e validação de entrada
- **Repositories** — regras de negócio e persistência
- **Models / Schemas** — entidades ORM e contratos Pydantic
- **Templates + Static** — camada de apresentação

---

## Pré-requisitos

- [Python](https://www.python.org/) 3.12+
- [MySQL](https://www.mysql.com/) 8+ **ou** [Docker](https://www.docker.com/) + Docker Compose
- [Git](https://git-scm.com/)

---

## Início rápido

### Opção 1 — Desenvolvimento local

```bash
git clone https://github.com/acnbc/projeto-integrador.git
cd projeto-integrador

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Ajuste DATABASE_URL e SECRET_KEY no .env

python scripts/setup_database.py
fastapi dev main.py
```

Acesse:

| Recurso | URL |
|---------|-----|
| Aplicação | http://localhost:8000 |
| Login | http://localhost:8000/login |
| API (Swagger) | http://localhost:8000/docs |
| Health check | http://localhost:8000/health |

Credenciais iniciais (criadas pelo seed em `scripts/setup_database.py`):

- **E-mail:** `anacarolinacabral@protonmail.com`
- **Senha:** `teste123`

### Opção 2 — Docker (recomendado para simular nuvem)

```bash
export SECRET_KEY="sua-chave-secreta-com-pelo-menos-32-caracteres"
docker compose up --build
```

O MySQL do Compose expõe a porta **3307** no host (evita conflito com instalações locais na 3306).

---

## Variáveis de ambiente

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `DATABASE_URL` | Sim | URL SQLAlchemy do MySQL (`mysql+pymysql://...`) |
| `SECRET_KEY` | Sim | Chave para assinatura JWT (mín. 32 caracteres em produção) |
| `ENV` | Não | `dev` (lê `.env`) ou `production` / `test` |
| `DATABASE_ECHO` | Não | `true` para log SQL (apenas debug) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Não | Expiração do token (padrão: 30) |

Exemplo completo em [.env.example](.env.example).

---

## Testes

```bash
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

O script sobe o MySQL via Docker (porta **3307**), aguarda o banco e executa a suíte `pytest` (13 testes: health, autenticação, páginas, dashboard, tipos de alta).

Execução manual:

```bash
docker compose up -d db
source venv/bin/activate
pip install -r requirements-dev.txt

export ENV=test
export DATABASE_URL=mysql+pymysql://admin:admin@127.0.0.1:3307/ufrj_test
export SECRET_KEY=chave-secreta-de-teste-com-32-caracteres

pytest
```

---

## Integração contínua

O pipeline [`.github/workflows/ci.yml`](.github/workflows/ci.yml) executa automaticamente em **push** e **pull request** para `main`, `master` e branches `feat/**`:

1. **test** — sobe MySQL, instala dependências, roda `pytest` com cobertura
2. **docker** — valida o build da imagem (`Dockerfile`)

Acompanhe em: [GitHub Actions](https://github.com/acnbc/projeto-integrador/actions).

---

## Deploy em nuvem

A aplicação está containerizada e pronta para publicação em provedores como Render, Railway ou VPS.

Guia completo: [docs/DEPLOY.md](docs/DEPLOY.md)  
Blueprint Render: [render.yaml](render.yaml)

---

## Documentação da API

Com a aplicação em execução, a documentação interativa está disponível em:

- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`

Principais prefixos:

| Prefixo | Descrição |
|---------|-----------|
| `/api/usuario` | Autenticação e gestão de usuários |
| `/api/internacao` | Internações e busca de pacientes |
| `/api/parecer` | Pareceres clínicos |
| `/api/tipo-alta` | Tipos de alta |
| `/api/dashboard` | Estatísticas analíticas |
| `/api/perfil` | Perfis de acesso |

---

## Estrutura do projeto

```
projeto-integrador/
├── config/           # Configurações (settings, env)
├── controllers/      # Rotas FastAPI (API + páginas)
├── data/             # Repositórios e scripts SQL
├── models/           # Modelos ORM e schemas Pydantic
├── templates/        # Páginas Jinja2
├── static/           # CSS e JavaScript
├── tests/            # Testes automatizados (pytest)
├── scripts/          # Setup de banco, testes, deploy
├── docs/             # Deploy e relatório final
├── .github/workflows/# CI (GitHub Actions)
├── Dockerfile
├── docker-compose.yml
└── main.py           # Ponto de entrada da aplicação
```

---

## Licença

Projeto acadêmico desenvolvido no âmbito da UNIVESP. Consulte a instituição quanto ao uso e redistribuição do código.
