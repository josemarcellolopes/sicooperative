#!/bin/bash

# Sobe os containers em background
docker-compose up -d

# Aguarda alguns segundos para garantir que o MySQL está pronto
echo "Aguardando o MySQL iniciar..."
sleep 60

# Executa o script SQL no banco de dados
mysql -h127.0.0.1 -uadmin -padmin < ./dags/sql/create_tables.sql

# Mensagem de conclusão
echo "Execução concluída!"
