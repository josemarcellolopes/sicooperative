@echo off
REM Sobe os containers em background
docker-compose up -d

REM Aguarda alguns segundos para garantir que o MySQL está pronto
echo Aguardando o MySQL iniciar...
timeout /t 60 /nobreak >nul

REM Executa o script SQL no banco de dados
mysql -h127.0.0.1 -uadmin -padmin < .\dags\sql\create_tables.sql

REM Mensagem de conclusão
echo Execução concluída!
