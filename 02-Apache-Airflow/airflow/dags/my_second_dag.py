from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task

from my_operator import consumer

@task
def consumer_operator(arguments, **kwargs):
    # We just wrap the function here, to keep the code AirFlow free.
    consumer(arguments, **kwargs)

@task
def producer():
    return {"content": "Here we go..."}

@task
def configurable(**kwargs):
    # We can access the configuration in this way.
    output = kwargs['dag_run'].conf.get("output_path", "N/A")
    print(f"Output path: '{output}'")

dag_args = {
    "email": ["petr.skoda@matfyz.cuni.cz"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    'retry_delay': timedelta(minutes=15)
}

with DAG(
    dag_id="my_second2",
    default_args=dag_args,
    start_date=datetime(2023, 3, 13),
    schedule=None,
    catchup=False,
    tags=["NDBI046"],
) as dag:

    input_data = producer()

    # Accessing values on input_data is reading directly from XCom
    result = consumer_operator(input_data)

    configurable()