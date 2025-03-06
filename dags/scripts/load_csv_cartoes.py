import pandas as pd

from sqlalchemy import create_engine, update, Table, MetaData

username = 'admin'
password = 'admin'
host     = 'mysql_rdbms'
database = 'sicooperative'

filesystem = '/opt/airflow/dags/data'

csv_file = 'cartoes.csv'
csv_delimiter = ','

table = 'cartao'
columns = ['id_cartao','numero_cartao','nome_impresso_cartao','id_conta']
pk = 'id_cartao'

connection_string = f'mysql+mysqlconnector://{username}:{password}@{host}/{database}'

engine = create_engine(connection_string)

df_csv = pd.read_csv(f'{filesystem}/{csv_file}', sep=csv_delimiter)

df_table = pd.read_sql_table(table, con=engine)

for col in df_table.columns:
    if col in df_csv.columns:
        target_dtype = df_table[col].dtype

        if pd.api.types.is_integer_dtype(target_dtype):
            df_csv[col] = pd.to_numeric(df_csv[col], errors='coerce').astype('Int64')

        elif pd.api.types.is_float_dtype(target_dtype):
            df_csv[col] = pd.to_numeric(df_csv[col], errors='coerce')

        elif pd.api.types.is_datetime64_any_dtype(target_dtype):
            df_csv[col] = pd.to_datetime(df_csv[col], errors='coerce')

        elif pd.api.types.is_bool_dtype(target_dtype):
            df_csv[col] = df_csv[col].astype(str).str.lower().map({'true': True, 'false': False, '1': True, '0': False})
            df_csv[col] = df_csv[col].astype('boolean')

        elif pd.api.types.is_object_dtype(target_dtype):
            df_csv[col] = df_csv[col].astype(str)

df_insert = df_csv.merge(df_table, on=pk, how='left', indicator=True)

df_insert = df_insert.drop(columns=[col for col in df_insert.columns if col.endswith('_y')])

df_insert = df_insert.rename(columns={col: col[:-2] for col in df_insert.columns if col.endswith('_x')})

df_insert = df_insert[df_insert['_merge'] == 'left_only']

df_insert.drop(columns='_merge', inplace=True)

df_insert.to_sql(table, con=engine, if_exists='append', index=False)

df_update = df_csv.merge(df_table, how='left', indicator=True)

df_update = df_update[df_update['_merge'] == 'left_only'].drop(columns=['_merge'])

metadata = MetaData()

associado = Table(table, metadata, autoload_with=engine)

statements = []

for index, row in df_update.iterrows():
    stmt = (
        update(associado)
        .where(associado.c.id_associado == row[pk])
        .values({col: row[col] for col in columns if col != pk})
    )
    statements.append(stmt)

    with engine.connect() as conn:
        conn.execute(stmt)
