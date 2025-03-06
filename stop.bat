@echo off
echo Finalizando execução...
echo.

:: Para os serviços dos containers em background
docker-compose down

:: Mensagem de conclusão
echo.
echo Concluído!
