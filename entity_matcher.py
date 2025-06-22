import os
import psycopg
from typing import Tuple, List
from vectorstore import query


class EntityMatcher:

    def __init__(self, table_name: str, column_name: str):
        self.table_name = table_name
        self.column_name = column_name

    def fuzzy_match(self, value: str) -> List[Tuple[str, float]]:
        """check if fuzzy match exists in the table"""
        with psycopg.connect(os.getenv("DB_CONNECTION_STRING")) as conn:
            with conn.cursor() as cur:
                query = f"""
                    SELECT *
                    FROM (
                        SELECT {self.column_name}, similarity({self.column_name}, '{value}') AS score
                        FROM {self.table_name}
                    ) sub
                    ORDER BY score DESC
                    LIMIT 10;
                """
                cur.execute(query)
                exists = cur.fetchall()
                return [(row[0], row[1]) for row in exists] if exists else []

    def semantic_search(self, value: str) -> bool:
        """check if semantic search match exists in the table"""
        result = query(f"{self.column_name}", value, 10)
        return result
