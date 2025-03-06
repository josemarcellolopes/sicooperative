from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator  # No Airflow 2.0+, DummyOperator foi substituído por EmptyOperator

# Definição dos argumentos padrão da DAG
default_args = {
    'owner': 'SiCooperative',
    'description': 'Uma DAG de teste usando DummyOperator',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 3),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
}

# Criando a DAG
with DAG(
    'dag_test',
    default_args=default_args,
    description='Uma DAG de teste usando DummyOperator',
    schedule_interval=None,
    catchup=False,
) as dag:
    
    dummy_task = EmptyOperator(
        task_id='dummy_task',
    )

    dummy_task
