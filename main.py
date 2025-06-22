import os
from entity_matcher import EntityMatcher

database_url = os.getenv("DB_CONNECTION_STRING")

columns = ["title"]


def main():
    matcher = EntityMatcher("books", "title")
    print(matcher.fuzzy_match("science fiction"))
    print(matcher.semantic_search("science fiction"))


if __name__ == "__main__":
    main()
