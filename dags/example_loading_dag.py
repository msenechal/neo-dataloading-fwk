# dags/example_loading_dag.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta  # Make sure to import timedelta here
import my_loading_script

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 24),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'example_loading_dag',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(hours=1),
)

def run_my_script():
    my_loading_script.main()  # Call a function within your script

run_script_task = PythonOperator(
    task_id='run_my_script',
    python_callable=run_my_script,
    dag=dag,
)

