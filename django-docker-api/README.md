# Django Docker API

Este projeto é uma API Django dockerizada com PostgreSQL e pgAdmin.

## 🚀 Como executar

### Pré-requisitos
- Docker
- Docker Compose

### Execução
```bash
# 1. Copiar o arquivo de exemplo das variáveis de ambiente
cp .env.example .env

# 2. Editar o arquivo .env com suas configurações
# Especialmente o ZAPSIGN_API_TOKEN com sua chave da API ZapSign

# 3. Construir e iniciar os containers
docker-compose up --build -d

# 4. Executar migrações
docker-compose exec web python manage.py migrate

# 5. (Opcional) Criar superuser
docker-compose exec web python manage.py createsuperuser
```

## 📊 Serviços

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| Django API | http://localhost:8001 | - |
| pgAdmin | http://localhost:8080 | Email: admin@admin.com<br>Senha: admin |
| PostgreSQL | localhost:5432 | DB: django_db<br>User: django_user<br>Pass: django_password |

## 🔐 Variáveis de Ambiente

O projeto utiliza variáveis de ambiente para configurações sensíveis. Copie o arquivo `.env.example` para `.env` e configure:

### Variáveis Obrigatórias
- `ZAPSIGN_API_TOKEN`: Token de autenticação da API ZapSign
- `ZAPSIGN_API_BASE_URL`: URL base da API ZapSign (padrão: sandbox)

### Outras Variáveis
- `DB_*`: Configurações do banco de dados
- `SECRET_KEY`: Chave secreta do Django
- `DEBUG`: Modo de debug (1 para ativo, 0 para inativo)

## 🗄️ Configuração do pgAdmin

1. Acesse http://localhost:8080
2. Login com `admin@admin.com` / `admin`
3. Adicione um novo servidor:
   - **Name**: Django DB
   - **Host**: `db` (nome do container)
   - **Port**: `5432`
   - **Username**: `django_user`
   - **Password**: `django_password`

## 🔧 Comandos úteis

```bash
# Ver logs
docker-compose logs web
docker-compose logs db

# Parar containers
docker-compose down

# Reiniciar containers
docker-compose restart

# Executar comandos Django
docker-compose exec web python manage.py <comando>

# Acessar shell do container
docker-compose exec web bash

# Acessar shell do Django
docker-compose exec web python manage.py shell
```

## 📁 Estrutura do projeto

```
.
├── api/                    # App Django
├── core/                   # Configurações do Django
├── docker-compose.yml      # Configuração dos containers
├── Dockerfile              # Imagem do Django
├── requirements.txt        # Dependências Python
├── .env                    # Variáveis de ambiente
└── .dockerignore           # Arquivos ignorados pelo Docker
```

## 🔒 Variáveis de ambiente

As configurações estão no arquivo `.env`:

```env
# Database
DB_HOST=db
DB_PORT=5432
DB_NAME=django_db
DB_USER=django_user
DB_PASSWORD=django_password

# Django
SECRET_KEY=sua-chave-secreta
DEBUG=1

# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin
```

## 🐛 Troubleshooting

### Container não inicia
```bash
# Ver logs detalhados
docker-compose logs

# Reconstruir containers
docker-compose down
docker-compose up --build
```

### Problemas de conexão com banco
```bash
# Verificar se o banco está rodando
docker-compose ps

# Reiniciar apenas o banco
docker-compose restart db
```

### Resetar banco de dados
```bash
# CUIDADO: Isso apagará todos os dados
docker-compose down -v
docker-compose up --build -d
docker-compose exec web python manage.py migrate
```
