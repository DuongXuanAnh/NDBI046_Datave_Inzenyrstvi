# Second Assignment : Improving transformation process

Use Apache AirFlow to produce both data cubes from first assignment.

Use a single DAG with dag_id set to data-cubes.

All relevant files must be located under ./airflow/.

You can not utilize data files from your repository. All inputs must be downloaded.

You are save to use local file system as a data storage between tasks.

DAG must be scheduled to None (schedule=None).

Your DAG must produce files:

population.ttl

health_care.ttl

Files must be saved to a directory specified in DAG's configuration field output_path . 

See solution(s) at the end.

Your DAG should have reasonable design.

Do not use DockerOperators!

# System requirements

Docker (at least 4GB of memory)

Docker Compose v1.29.1 or newer

Python3 (>=3.10)

# Installation instructions
- Clone repository
- Then following this instructions:
  - https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
- On port 0.0.0.0:8080 login as "airflow" with password "airflow"

