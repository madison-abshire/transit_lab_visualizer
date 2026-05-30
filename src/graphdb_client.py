from SPARQLWrapper import SPARQLWrapper, JSON
import os

GRAPHDB_HOST = os.getenv("GRAPHDB_HOST", "http://localhost:7200")
GRAPHDB_REPO = os.getenv("GRAPHDB_REPO", "transit-project")

class GraphDBClient:
    def __init__(self):
        endpoint = f"{GRAPHDB_HOST}/repositories/{GRAPHDB_REPO}"
        self._sparql = SPARQLWrapper(endpoint)
        self._sparql.setReturnFormat(JSON)


    def query(self, query: str) -> list[dict[str, str]]:
        """Run a SELECT query; returns a list of row dicts."""
        self._sparql.setQuery(query)
        results = self._sparql.query().convert()
        return [
            {k: v["value"] for k, v in row.items()}
            for row in results["results"]["bindings"]
        ]

