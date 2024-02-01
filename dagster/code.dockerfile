FROM python:3.7-slim
RUN pip install dagster dagster-postgres dagster-docker dagster-dbt
RUN pip install garminconnect minio

WORKDIR /opt/dagster/app

COPY ./orchestrator /opt/dagster/app/orchestrator

EXPOSE 4000

CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-f", "orchestrator/__init__.py"]
