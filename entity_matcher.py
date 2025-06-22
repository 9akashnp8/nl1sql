import os
import psycopg
from typing import List
from vectorstore import query


def fuzzy_matcher(table_name: str, column_name: str, value: str) -> List[str]:
    """check if fuzzy match exists in the table"""
    with psycopg.connect(os.getenv("DB_CONNECTION_STRING")) as conn:
        with conn.cursor() as cur:
            query = f"SELECT distinct {column_name} FROM {table_name} WHERE SIMILARITY({column_name}, '{value}') > 0.3 LIMIT 5"
            print(query)
            cur.execute(query)
            exists = cur.fetchall()
            return [row[0] for row in exists] if exists else []


def semantic_search(column_name: str, value: str) -> bool:
    """check if semantic search match exists in the table"""
    result = query(f"{column_name}", value, 5)
    return result
