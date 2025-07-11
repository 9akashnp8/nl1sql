import json
from agents import Agent, function_tool
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from entity_matcher import EntityMatcher

from vectorstore import query

core_agent_instructions = """
# Smart AI NL2SQL Assistant Instructions
You are an Smart AI NL2SQL Assistant, an expert in analyzing user questions about their tables and generating the most
accurate sql to retrieve data relevant to the user question.

## Objective
You primary role is understand the user's questions and generate the most relevant, accurate and optimal SQL that will
which when run will answer the users question.

### Inputs
You will be given the following inputs:
- User query: A natural language question about the data.
- Table schema: {config}

### Tools
- column_value_resolver: The table will have columns that contain various values/identifiers. Eg: "The New York Times".
The user might ask queries with incompleete or partial names (Eg: "New York Time"). You will use this tool to resolve the entity names to exact values in the database.

## Thought Process
Your task is to understand the user's question and perform the following:

### 1. Entity Name Resolution (If required):
- The table will have column with various values that we will have to apply filters with.
- The user query need not always specify the exact value, it could be partial/incomplete.
Eg: "what is number of articles by new york times" instead of "What is the number of articles by The New York Times".
We need to handle this by 1. extracting the right column to get the values from and 2. using the column_value_resolver to pass the column name and value as input to resolve the entity name to exact value in the database.
- The passing the column name to column_value_resolver, ensure the casing matches with the same specified in the table schema.
- Only perform entity resolution if the user query contains a specific entity name that needs to be resolved.

### 2. SQL Query Generation:
- Use the table schema, user query and resolved entity name details (if available) to generate optimized Postgres SQL query.
- The SQL query should be optimized and use the exact column expressions from the schema.
- Always recheck if the generated SQL query is valid and executable.

Return the final query.
"""

class AgentOutput(BaseModel):
    query: str = Field(
        description="The generated SQL query based on the user input and table schema."
    )


class ColumnResolverInput(TypedDict):
    table_name: str
    column_name: str
    value: str

@function_tool
def column_value_resolver(resolved_input: ColumnResolverInput):
    """
    Resolves the entity name to exact value in the database.
    
    Args:
        table_name (str): The name of the table where the column exists.
        column_name (str): The name of the column to resolve the value from.
        value (str): The partial or incomplete value to resolve.
    
    Returns:
        fuzzy_match (list): List of fuzzy matched values from the column along with score.
        semantic_match (list): List of semantically matched values from the column along with score.
    """
    matcher = EntityMatcher(
        table_name=resolved_input.get("table_name", "books"),
        column_name=resolved_input["column_name"]
    )
    fuzzy_match = matcher.fuzzy_match(resolved_input["value"])
    sematic_match = matcher.semantic_search(resolved_input["value"])

    return {
        "fuzzy_match": fuzzy_match,
        "semantic_match": sematic_match
    }
    
with open("table_config.json", "r") as f:
    config = json.load(f)


agent = Agent(
    name="NL2SQL Agent",
    instructions=core_agent_instructions.format(config=json.dumps(config)),
    output_type=AgentOutput,
    tools=[column_value_resolver]
)