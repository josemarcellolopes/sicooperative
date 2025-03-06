# %%
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# %%
# Initialize Spark session
spark = SparkSession.builder \
    .appName("GenerateTransactionsCSV") \
    .config("spark.jars", "mysql-connector-java.jar") \
    .getOrCreate()

    # %%
    # Database connection parameters
username = 'admin'
password = 'admin'
host = 'localhost'
database = 'sicooperative'
jdbc_url = f"jdbc:mysql://{host}/{database}"

connection_properties = {
    "user": username,
    "password": password,
    "driver": "com.mysql.jdbc.Driver"
}

# %%
# Output path
filesystem = '../dags/data/output'
csv_file = 'transacoes.csv'
csv_delimiter = ','

# %%
def conectar_bd():
    """
    Test database connection and return True if successful
    """
    try:
        # Test connection by attempting to read a small amount of data
        test_df = spark.read.jdbc(
            url=jdbc_url,
            table="(SELECT 1) AS test",
            properties=connection_properties
        )
        print("Conexão bem-sucedida ao banco de dados!")
        return True
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return False

# %%
def executar_query():
    """
    Execute query and return results as a Spark DataFrame
    """
    try:
        # SQL query
        query = """
            SELECT
                a.nome_associado,
                a.sobrenome_associado,
                a.idade_associado,
                mo.vlr_transacao_movimento,
                mo.descricao_transacao_movimento,
                mo.data_movimento,
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
        
        # Execute the query using JDBC
        df = spark.read.jdbc(
            url=jdbc_url,
            table=f"({query}) AS query_result",
            properties=connection_properties
        )
        
        return df
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        return None

# %%
def main():
    # Check database connection
    if conectar_bd():
        # Get results as Spark DataFrame
        df_resultados = executar_query()
        
        if df_resultados is not None:
            # Write to CSV
            df_resultados.write \
                .option("header", "true") \
                .option("delimiter", csv_delimiter) \
                .mode("overwrite") \
                .csv(f"{filesystem}")
            
            # Rename the file (Spark creates a directory with part files)
            # This is a simplification - in production you might want to:
            # 1. Use coalesce(1) to ensure single file output
            # 2. Use a shell command to rename the file
            print(f"Dados escritos para {filesystem}")
        
        print("Processamento concluído.")

# %%
if __name__ == "__main__":
    main()
    # Stop the Spark session
    spark.stop()
