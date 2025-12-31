from openai import OpenAI
from config import settings
from ..clients.neo4j_client import neo4j_client

class DBQueryAgent:

    SYSTEM_PROMPT = """You are an expert Neo4j Cypher query generator.

Given a database schema and a natural language question, generate a valid READ-ONLY Cypher query.

Rules:
1. ONLY generate READ queries (MATCH, OPTIONAL MATCH, WITH, RETURN, etc.)
2. NEVER generate write operations (CREATE, DELETE, MERGE, SET, REMOVE, etc.)
3. Use proper Cypher syntax and best practices
4. Return ONLY the Cypher query, no explanations
5. Use parameterized queries where appropriate (use $param_name syntax)

Database Schema:
{schema}
"""

    def __init__(self, schema: str):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.schema = schema
        self._system_prompt = self.SYSTEM_PROMPT.format(schema=schema)

    def generate_cypher(self, question: str) -> str:
        """Generate Cypher query from natural language."""
        response = self.client.chat.completions.create(
            model=settings.query_builder_model,
            messages=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": f"Question: {question}"},
            ],
            temperature=0,
        )

        cypher = response.choices[0].message.content.strip()

        # Strip markdown fences
        if cypher.startswith("```"):
            cypher = cypher.split("\n", 1)[1] if "\n" in cypher else cypher[3:]
        if cypher.endswith("```"):
            cypher = cypher[:-3]

        return cypher.strip()

    def execute_query(self, cypher: str) -> list[dict]:
        """Execute Cypher query against Neo4j."""
        return neo4j_client.execute_read(cypher)
