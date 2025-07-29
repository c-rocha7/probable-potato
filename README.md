# ZapSign - Docker Full Stack

Este projeto conecta um frontend Angular com uma API Django, ambos rodando em containers Docker.

## Estrutura do Projeto

```
docker-zapsign/
├── docker-compose.yml          # Orquestração de todos os serviços
├── angular-docker-frontend/    # Frontend Angular
└── django-docker-api/         # API Django + PostgreSQL
```

## Serviços Disponíveis

- **Frontend Angular**: http://localhost:4200
- **API Django**: http://localhost:8001
- **PgAdmin**: http://localhost:8080
- **PostgreSQL**: localhost:5432

## Como Executar

### 1. Executar todo o projeto
```bash
# Na raiz do projeto
docker-compose up --build
```

### 2. Executar em background
```bash
docker-compose up -d --build
```

### 3. Parar todos os serviços
```bash
docker-compose down
```

### 4. Parar e remover volumes (limpar banco de dados)
```bash
docker-compose down -v
```

## Verificar Status dos Serviços

```bash
# Ver logs de todos os serviços
docker-compose logs

# Ver logs de um serviço específico
docker-compose logs angular-frontend
docker-compose logs django-api
docker-compose logs db
```

## Troubleshooting

### Se houver problemas de conexão:
1. Verifique se todos os containers estão na mesma rede
2. Use os nomes dos serviços ao invés de localhost para comunicação interna
3. Verifique as configurações de CORS no Django

### Reconstruir apenas um serviço:
```bash
docker-compose build django-api
docker-compose up django-api
```

## Configurações Importantes

### Comunicação Frontend ↔ Backend
- O Angular usa `http://django-api:8000/api` para chamadas internas (container-to-container)
- O Django permite CORS de `http://angular-frontend:4200`
- Ambos estão na rede `zapsign_network`

### Banco de Dados
- PostgreSQL rodando no container `db`
- Credenciais definidas no arquivo `.env` do Django
- PgAdmin disponível para administração visual

## Desenvolvimento

Para desenvolvimento local, você pode:
1. Executar apenas os serviços necessários
2. Usar volumes para hot-reload automático
3. Acessar logs individuais para debug

```bash
# Apenas backend + banco
docker-compose up db django-api

# Apenas frontend
docker-compose up angular-frontend
```
