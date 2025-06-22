import os
from entity_matcher import fuzzy_matcher, semantic_search

database_url = os.getenv("DB_CONNECTION_STRING")

columns = ["title"]


def main():
    print(fuzzy_matcher("books", "title", "science fiction"))
    print(semantic_search("title", "science fiction"))


if __name__ == "__main__":
    main()
