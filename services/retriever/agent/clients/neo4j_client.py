from neo4j import GraphDatabase, READ_ACCESS
from neo4j.time import DateTime, Date, Time, Duration
from config import settings


def convert_neo4j_types(value):
    if isinstance(value, DateTime):
        return value.isoformat()
    elif isinstance(value, Date):
        return value.isoformat()
    elif isinstance(value, Time):
        return value.isoformat()
    elif isinstance(value, Duration):
        return str(value)
    elif isinstance(value, dict):
        return {k: convert_neo4j_types(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [convert_neo4j_types(v) for v in value]
    return value


class Neo4jClient:
    def __init__(self):
        self._driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )

    def close(self):
        self._driver.close()

    def execute_read(self, cypher: str, params: dict | None = None) -> list[dict]:
        with self._driver.session(
            database=settings.neo4j_database, default_access_mode=READ_ACCESS
        ) as session:
            result = session.run(cypher, params or {})

            return [convert_neo4j_types(record.data()) for record in result]

    def get_schema(self) -> str:
        node_labels = self.execute_read("CALL db.labels()")
        rel_types = self.execute_read("CALL db.relationshipTypes()")
        properties = self.execute_read(
            "CALL db.schema.nodeTypeProperties() YIELD nodeLabels, propertyName, propertyTypes"
        )

        schema_lines = ["Node Labels:"]
        schema_lines.extend(f"  - {r['label']}" for r in node_labels)

        schema_lines.append("\nRelationship Types:")
        schema_lines.extend(f"  - {r['relationshipType']}" for r in rel_types)

        schema_lines.append("\nNode Properties:")
        for prop in properties:
            labels = ":".join(prop["nodeLabels"])
            schema_lines.append(
                f"  ({labels}).{prop['propertyName']}: {prop['propertyTypes']}"
            )

        return "\n".join(schema_lines)


neo4j_client = Neo4jClient()
