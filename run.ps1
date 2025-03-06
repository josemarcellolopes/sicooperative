Write-Host "Iniciando execução..."
Write-Host ""

# Sobe os containers em background
docker-compose up -d

# Aguarda alguns segundos para garantir que o MySQL está pronto
Write-Host ""
Write-Host "Aguardando o MySQL iniciar..."
Start-Sleep -Seconds 60

# Executa o script SQL no banco de dados
mysql -h127.0.0.1 -uadmin -padmin < .\dags\sql\create_tables.sql 2> $null

# Mensagem de conclusão
Write-Host ""
Write-Host "Execução concluída!"
