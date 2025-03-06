from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

# Definição dos argumentos padrão da DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 6),
    'retries': 0,
}

# Criando a DAG
with DAG(
    'dag_drop_tables',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    task_start = DummyOperator(task_id='task_start')

    task_create_tables = BashOperator(
        task_id='drop_tables',
        bash_command='mysql -hmysql_rdbms -uadmin -padmin sicooperative < /opt/airflow/dags/sql/drop_tables.sql',
        dag=dag
    )

    task_end = DummyOperator(task_id='task_end')

    task_start >> task_create_tables >> task_end
