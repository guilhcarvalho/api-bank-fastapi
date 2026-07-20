# API BANCARIA FASTAPI

Uma API REST robusta e segura construída com as melhores práticas do ecossistema Python. Este projeto foi desenvolvido como um estudo prático para demonstrar a criação de uma API moderna e Assíncrona, com autenticação segura de usuários, ORM avançado e ambiente totalmente containerizado com o Docker.

## Tecnologias Utilizadas

• ***Python*** - Linguagem principal\
• ***Poetry*** - Gerenciador de packages\
• ***FastAPI*** - Framework web moderno e de alta performance\
• ***SQLAlchemy*** - ORM para mapeamento objeto-relacional\
• ***Alembic*** - Gerenciador de migrações do banco de dados\
• ***PostgreSQL*** - Banco de dados relacional (rodando em container Docker)\
• ***JWT (JSON Web Tokens)*** - Para autenticação e autorização stateless\
• ***Docker*** - Containerização do banco de dados e da aplicação\
• ***Uvicorn*** - Servidor ASGI para o FastAPI\
• ***Pytest*** e ***Coverage*** - Cobertura total dos testes\


## Funcionalidades
• CRUD completo para Accounts (Entidade responsável pelos usuários)\
• Funcionalidades de Create e Read para Transactions (Entidade responsável\ por retratar as transações do usuário)\
• Sistema de autenticação e autorização via JWT (Login, Registro e Proteção de Rotas)\
• Banco de dados PostgreSQL isolado em container Docker\
• Migrations com Alembic\
• Documentação interativa automática (Swagger UI / ReDoc) gerada pelo FastAPI\
• Variáveis de ambiente para configuração segura\


## Pré-requisitos
Antes de começar, você precisará ter as seguintes ferramentas instaladas na sua máquina:

• **Git**\
• **Python 3.14+**\
• **Poetry**\
• **Docker e Docker Compose**\


## Rodando o Projeto (Com Docker)
A maneira mais fácil de rodar este projeto é utilizando o Docker. O Dockerfile já está configurado para utilizar o Poetry e instalar as dependências de forma otimizada.

## Clone o repositório:
1. Rode o comando `git clone https://github.com/guilhcarvalho/api-bank-fastapi.git\`
2. Configure as variáveis de ambiente:
Crie um arquivo .env na raiz do projeto baseado no .env.example:
```bash title=".env"
DATABASE_URL="postgresql+psycopg://app_user:app_password@apibank_database:5432/app_db"
SECRET_KEY = '2d88cf9f62f9ff8fe8ddf74c6bff9a0d457e3662b8d56641ff2cc5982f8bec64'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Variáveis do banco de dados
POSTGRES_USER=app_user
POSTGRES_DB=app_db
POSTGRES_PASSWORD=app_password
```
3. Suba os containers:
```bash title="bash"
docker-compose up --build
```
4. Acesse as proximas vezes como:
```
docker-compose up
```
A API estará rodando em `http://localhost:8000`

## Documentação da API
Uma das grandes vantagens do FastAPI é a documentação interativa gerada automaticamente. Após rodar o projeto, acesse:

**Swagger UI**: http://localhost:8000/docs \
**ReDoc**: http://localhost:8000/redoc


## Autenticação
A API utiliza JWT para proteger as rotas. Para acessar rotas protegidas:
Após a criação de um usuário em `http://localhost:8000/accounts/` faça uma requisição POST para `http://localhost:8000/auth/` com suas credenciais, para gerar um token JWT com autorização.


## Estrutura do Projeto
```
├── migrations/
├── src/
│   ├── __init__.py
│   ├── main.py              # Configuração do FastAPI e rotas principais
│   ├── database.py          # Configuração do SQLAlchemy
│   ├── security.py          # Configurações de segurança
│   ├── settings.py          # Configurações de ambiente
│   ├── models/              # Modelos do banco de dados
│   ├── schemas/             # Modelos Pydantic (Validação)
│   ├── controllers/         # Rotas da API (Auth, Users, etc.)
├── compose.yml              # Orquestração dos containers
├── Dockerfile               # Receita para a imagem da API (com Poetry)
├── .dockerignore            
├── .gitignore
├── entrypoint.sh            # Arquivo build
├── README.md
├── alembic.ini
├── pyproject.toml           # Dependências e configurações do Poetry
├── poetry.lock              # Lock file para reprodutibilidade
└── tests/                   # Tests do app com Pytest
```