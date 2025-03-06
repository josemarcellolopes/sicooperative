from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

def run_script(script_name):
    subprocess.run(["python", script_name], check=True)

default_args = {
    'owner': 'SiCooperative',
    'description': 'Uma DAG para gerar arquivo CSV das transações financeiras',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
}

with DAG(
    dag_id="dag_generate_transactions_csv",
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    task_start = DummyOperator(task_id='task_start')

    task_generate_transactions_csv = PythonOperator(
        task_id="generate_transactions_csv",
        python_callable=run_script,
        op_args=["/opt/airflow/dags/scripts/generate_transactions_csv.py"],
    )

    task_end = DummyOperator(task_id='task_end')
    
    task_start >> task_generate_transactions_csv >> task_end
