FROM python:3.12.1


RUN apt-get update && apt-get install wget -y
RUN pip install pandas sqlalchemy psycopg2-binary pyarrow

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python", "ingest_data.py" ]

