from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# The actual tasks defined here will run in a different context from the
# context of this script. Different tasks run on different workers at
# different points in time, which means that this script cannot be used to
# cross communicate between tasks. Note that for this purpose we have a more
# advanced feature called XComs.

def say_hello_world():
    print("Hello world!")


dag_args = {
    "email": ["petr.skoda@matfyz.cuni.cz"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    'retry_delay': timedelta(minutes=15)
}

with DAG(
    dag_id="my_first1",
    default_args=dag_args,
    start_date=datetime(2023, 3, 13),
    schedule_interval='0 9 * * *',
    catchup=False,
    tags=["NDBI046"],    
) as dag:

    task01 = PythonOperator(
        task_id="hello_world",
        python_callable=say_hello_world,
    )
    task01.doc_md = """This task prints a message."""

    task02 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 5",
    )

    task03 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    task01 >> [task02, task03]