Write-Host "Finalizando execução..."
Write-Host ""

# Para os serviços dos containers em background
docker-compose down

# Mensagem de conclusão
Write-Host ""
Write-Host "Concluído!"
