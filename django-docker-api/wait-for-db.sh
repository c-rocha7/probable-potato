#!/bin/sh

# wait-for-db.sh - Script para aguardar o PostgreSQL estar pronto

echo "🔍 Aguardando PostgreSQL estar disponível..."

# Aguardar até o banco estar disponível
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  echo "⏳ PostgreSQL não está pronto ainda - aguardando..."
  sleep 2
done

echo "✅ PostgreSQL está pronto!"

# Executar migrações e iniciar servidor
echo "🔄 Executando migrações..."
python manage.py makemigrations
python manage.py migrate

echo "🚀 Iniciando servidor Django..."
exec python manage.py runserver 0.0.0.0:8000
