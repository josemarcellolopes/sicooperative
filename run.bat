@echo off
echo Iniciando execução...
echo.

:: Sobe os containers em background
docker-compose up -d

:: Aguarda alguns segundos para garantir que o MySQL está pronto
echo.
echo Aguardando o MySQL iniciar...
timeout /T 60 /NOBREAK >nul

:: Executa o script SQL no banco de dados
mysql -h127.0.0.1 -uadmin -padmin < .\dags\sql\create_tables.sql 2> nul

:: Mensagem de conclusão
echo.
echo Execução concluída!
