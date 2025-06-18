import psycopg
from typing import List

from vectorstore import vectorize_documents
from constants import abu_dhabi_entities

def ingest_data(db_connection_url, table_name: str, columns: List[str]) -> None:

    # connect to database
    if db_connection_url.startswith("postgresql://"):
        with psycopg.connect(db_connection_url) as conn:
            with conn.cursor() as cursor:
                for column in columns:
                    cursor.execute(f'SELECT DISTINCT "{column}" FROM {table_name}') # assuming public schema
                    data = cursor.fetchall()
                    data = [row[0] for row in data if row[0] is not None]
                    vectorize_documents(column, data)
    else:
        raise ValueError("Unsupported database connection URL format. Only PostgreSQL is supported.")
