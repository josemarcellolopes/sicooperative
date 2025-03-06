from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Initialize Spark session
spark = SparkSession.builder \
    .appName("LoadAssociadosCSV") \
    .config("spark.jars", "mysql-connector-java.jar") \
    .getOrCreate()

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

# File paths and configurations
filesystem = '../dags/data'
csv_file = 'associados.csv'
csv_delimiter = ','

# Table information
table = 'associado'
columns = ['id_associado', 'nome_associado', 'sobrenome_associado', 'idade_associado', 'email_associado']
pk = 'id_associado'

# Function to infer schema from database
def get_table_schema(table_name):
    """Get schema from database table"""
    sample_df = spark.read.jdbc(
        url=jdbc_url,
        table=table_name,
        properties=connection_properties,
        numPartitions=1,
        lowerBound=1,
        upperBound=2,
        partitionColumn=pk
    ).limit(1)
    
    return sample_df.schema

# Read the existing table from the database
df_table = spark.read.jdbc(
    url=jdbc_url,
    table=table,
    properties=connection_properties
)

# Read the CSV file
df_csv = spark.read.csv(
    f"{filesystem}/{csv_file}",
    header=True,
    sep=csv_delimiter,
    inferSchema=True
)

# Function to match data types with the database schema
def match_data_types(csv_df, table_schema):
    """Match CSV data types with database schema"""
    
    for field in table_schema.fields:
        field_name = field.name
        if field_name in csv_df.columns:
            field_type = field.dataType
            
            if isinstance(field_type, IntegerType) or isinstance(field_type, LongType):
                csv_df = csv_df.withColumn(field_name, col(field_name).cast(field_type))
            elif isinstance(field_type, FloatType) or isinstance(field_type, DoubleType):
                csv_df = csv_df.withColumn(field_name, col(field_name).cast(field_type))
            elif isinstance(field_type, TimestampType) or isinstance(field_type, DateType):
                csv_df = csv_df.withColumn(field_name, col(field_name).cast(field_type))
            elif isinstance(field_type, BooleanType):
                csv_df = csv_df.withColumn(field_name, 
                    when(lower(col(field_name)) == "true", lit(True))
                    .when(lower(col(field_name)) == "false", lit(False))
                    .when(col(field_name) == "1", lit(True))
                    .when(col(field_name) == "0", lit(False))
                    .otherwise(lit(None)).cast(BooleanType())
                )
            elif isinstance(field_type, StringType):
                csv_df = csv_df.withColumn(field_name, col(field_name).cast(StringType()))
    
    return csv_df

# Apply schema matching
df_csv_typed = match_data_types(df_csv, df_table.schema)

# Identify records to insert (left anti join)
df_insert = df_csv_typed.join(
    df_table,
    on=pk,
    how="left_anti"
)

# Write new records to the database
if df_insert.count() > 0:
    df_insert.write.jdbc(
        url=jdbc_url,
        table=table,
        mode="append",
        properties=connection_properties
    )
    print(f"Inserted {df_insert.count()} new records into {table}")

# For updates, we'll use individual updates to match the original code's approach
# This approach is less efficient than bulk updates but matches the original logic
df_update = df_csv_typed.join(
    df_table,
    on=[pk],
    how="inner"
)

# If there are records to update
if df_update.count() > 0:
    # Collect to driver for processing (like the original code's approach)
    # Note: In production, this could be optimized to avoid collecting to driver
    update_rows = df_update.collect()
    
    # For each row that needs updating
    for row in update_rows:
        # Create update SQL
        set_clauses = []
        for col_name in columns:
            if col_name != pk:
                set_clauses.append(f"{col_name} = '{row[col_name]}'")
        
        if set_clauses:
            update_sql = f"UPDATE {table} SET {', '.join(set_clauses)} WHERE {pk} = {row[pk]}"
            
            # Execute the update using JDBC
            spark.sql(f"""
            SET spark.sql.legacy.timeParserPolicy=LEGACY;
            SELECT 1
            """)  # Dummy query to initialize the session
            
            # Create a temporary connection to execute the update
            # Note: In production, this would be better handled with a proper connection pool
            spark._jsparkSession.sql(update_sql)
    
    print(f"Updated {len(update_rows)} records in {table}")

print("Processing completed")
spark.stop()
