from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

def run_script(script_name):
    subprocess.run(["python", script_name], check=True)

default_args = {
    'owner': 'SiCooperative',
    'description': 'Uma DAG para carregar arquivos CSV para o banco de dados',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
}

with DAG(
    dag_id="dag_etl_load_csv",
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    task_start = DummyOperator(task_id='task_start')

    task_associados = PythonOperator(
        task_id="load_associados",
        python_callable=run_script,
        op_args=["/opt/airflow/dags/scripts/load_csv_associados.py"],
    )
    
    task_contas = PythonOperator(
        task_id="load_contas",
        python_callable=run_script,
        op_args=["/opt/airflow/dags/scripts/load_csv_contas.py"],
    )
    
    task_cartoes = PythonOperator(
        task_id="load_cartoes",
        python_callable=run_script,
        op_args=["/opt/airflow/dags/scripts/load_csv_cartoes.py"],
    )
    
    task_movimentos = PythonOperator(
        task_id="load_movimentos",
        python_callable=run_script,
        op_args=["/opt/airflow/dags/scripts/load_csv_movimentos.py"],
    )

    task_end = DummyOperator(task_id='task_end')
    
    task_start >> task_associados >> task_contas >> task_cartoes >> task_movimentos >> task_end
