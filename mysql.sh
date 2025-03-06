#!/bin/bash

# Definição do comando base
MYSQL_CMD="mysql -h 127.0.0.1 -P 3306 -uroot -padmin"

# Verifica se há argumentos
if [ "$#" -gt 0 ]; then
    # Se houver argumentos, adiciona ao comando
    $MYSQL_CMD "$@"
else
    # Se não houver argumentos, executa o comando básico
    $MYSQL_CMD
fi