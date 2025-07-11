import os
from agents import Runner

from ai import agent

database_url = os.getenv("DB_CONNECTION_STRING")

columns = ["author"]


def main():
    result = Runner.run_sync(agent, "How many authors are do we have so far?")
    print(result.final_output)

if __name__ == "__main__":
    main()
