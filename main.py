import os
from data_ingestion import ingest_data
from vectorstore import query

database_url = os.getenv("DB_CONNECTION_STRING")

columns = ["ADGEENGLISHNAME"]


def main():
    # data = []
    # ingest_data(database_url, "vw_tamm_al_ain_case_status", columns)
    query_text = "Google"
    results = query("EName", query_text, 0.2, 1)
    print(results)


if __name__ == "__main__":
    main()
