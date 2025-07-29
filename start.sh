#!/bin/bash

# Script de inicialização do projeto ZapSign
echo "🚀 Iniciando ZapSign - Full Stack Docker"
echo ""

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Inicie o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está disponível
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não encontrado. Instale o Docker Compose primeiro."
    exit 1
fi

echo "✅ Docker está disponível"
echo ""

# Parar containers existentes se houver
echo "🛑 Parando containers existentes..."
docker-compose down

echo ""
echo "🔨 Construindo e iniciando todos os serviços..."
echo "   - PostgreSQL Database"
echo "   - PgAdmin"
echo "   - Django API"
echo "   - Angular Frontend"
echo ""

# Construir e iniciar todos os serviços
docker-compose up --build -d

echo ""
echo "⏳ Aguardando serviços iniciarem..."
sleep 10

# Verificar status dos containers
echo ""
echo "📊 Status dos serviços:"
docker-compose ps

echo ""
echo "🎉 Projeto inicializado com sucesso!"
echo ""
echo "🌐 Serviços disponíveis:"
echo "   • Frontend Angular:  http://localhost:4200"
echo "   • API Django:        http://localhost:8001"
echo "   • PgAdmin:           http://localhost:8080"
echo "   • Database:          localhost:5432"
echo ""
echo "📋 Comandos úteis:"
echo "   • Ver logs: docker-compose logs"
echo "   • Parar: docker-compose down"
echo "   • Reconstruir: docker-compose up --build"
echo ""
echo "🔍 Para ver logs em tempo real: docker-compose logs -f"
