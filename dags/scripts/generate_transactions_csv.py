import mysql.connector
import pandas as pd

from airflow.models import Variable
from mysql.connector import Error

username = 'admin'
password = 'admin'
host     = 'mysql_rdbms'
database = 'sicooperative'

filesystem = Variable.get("output")

csv_file = 'transacoes.csv'
csv_delimiter = ','

def conectar_bd():

    try:

        conexao = mysql.connector.connect(
            host = host,
            database = database,
            user = username,
            password = password
        )

        if conexao.is_connected():

            print("Conexão bem-sucedida ao banco de dados!")
            return conexao
        
    except Error as e:
        
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def executar_query(conexao):

    query = """
        SELECT
            a.nome_associado,
            a.sobrenome_associado,
            a.idade_associado,
            mo.vlr_transacao_movimento,
            mo.descricao_transacao_movimento,
            mo.data_transacao_movimento,
            ca.numero_cartao,
            ca.nome_impresso_cartao,
            co.data_criacao_conta AS data_criacao_cartao,
            co.tipo_conta,
            co.data_criacao_conta
        FROM 
            sicooperative.associado a 
            INNER JOIN sicooperative.conta co ON a.id_associado = co.id_associado
            INNER JOIN sicooperative.cartao ca ON co.id_conta = ca.id_conta
            INNER JOIN sicooperative.movimento mo ON ca.id_cartao = mo.id_cartao
    """

    try:

        cursor = conexao.cursor(dictionary=True)
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados
    
    except Error as e:

        print(f"Erro ao executar a consulta: {e}")
        return None
    
    finally:
        
        cursor.close()

def resultados_em_dataframe(resultados):

    if resultados:

        df = pd.DataFrame(resultados)
        return df
    
    else:
        
        print("Nenhum resultado para converter em DataFrame.")
        return None

def main():

    conexao = conectar_bd()

    if conexao:

        resultados = executar_query(conexao)
        df_resultados = resultados_em_dataframe(resultados)

        if df_resultados is not None:
            df_resultados.to_csv(f"{filesystem}/{csv_file}", sep = csv_delimiter, index = False)

        conexao.close()

        print("Conexão fechada.")

if __name__ == "__main__":
    main()
