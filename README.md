# Simple ELT Process

Simple custom Extract, Load, Transform (ELT) project that utilises Docker and PostgreSQL to demonstrate a simple ELT pipeline.

## Instructions of use
First, initialise Airflow container:

```
docker compose up init-airflow -d
```

Wait for 30 seconds (or until the airflow container has finished running) to initialise the rest of the containers:

```
docker compose up
```