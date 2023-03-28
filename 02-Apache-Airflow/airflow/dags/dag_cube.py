import requests
from datetime import datetime, timedelta

from airflow import DAG

from airflow.operators.python import PythonOperator

from operators.careProviders import care_providers_main
from operators.population import population_main


def consumer_operator(consumer, **context):
    output_path = context['dag_run'].conf.get("output_path", None)
    if output_path:
        consumer(output_path)
    else:
        consumer()

def download_file(url: str, verify_ssl: bool = True) -> str:
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True, verify=verify_ssl) as response:
        response.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename


default_args = {
    "email": ["david.anh@email.cz"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    'retry_delay': timedelta(minutes=15)
}

dag = DAG(
    dag_id="data-cubes",
    default_args=default_args,
    start_date=datetime(2023, 3, 28),
    schedule_interval=None,
    tags=["NDBI046"],
)


task1 = PythonOperator(
    task_id="download-care-providers",
    python_callable=download_file,
    op_kwargs={"url": "https://opendata.mzcr.cz/data/nrpzs/narodni-registr-poskytovatelu-zdravotnich-sluzeb.csv"},
    dag=dag,
)

task2 = PythonOperator(
    task_id="process-care-providers",
    python_callable=consumer_operator,
    op_kwargs={"consumer": care_providers_main},
    provide_context=True,
    dag=dag,
)

task3 = PythonOperator(
    task_id="download-population-2021",
    python_callable=download_file,
    op_kwargs={"url": "https://www.czso.cz/documents/10180/184344914/130141-22data2021.csv"},
    dag=dag,
)

task4 = PythonOperator(
    task_id="download-county-codelist",
    python_callable=download_file,
    op_kwargs={
        "url": "https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/02/číselník-okresů-vazba-101-nadřízený.csv",
        "verify_ssl": False
    },
    dag=dag,
)

task5 = PythonOperator(
    task_id="process-population-2021",
    python_callable=consumer_operator,
    op_kwargs={"consumer": population_main},
    provide_context=True,
    dag=dag,
)


task1 >> task2
[task1, task3, task4] >> task5