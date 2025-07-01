from clients.neo4j_client import Neo4jClient
from neo4j_graphrag.experimental.components.resolver import SinglePropertyExactMatchResolver
from neo4j_graphrag.experimental.components.kg_writer import Neo4jWriter
from neo4j_graphrag.indexes import create_vector_index

class Neo4jService:
    def __init__(self, neo4j_client: Neo4jClient):
        self.driver = neo4j_client.get_driver()

    async def resolve_entities(self):
        resolver = SinglePropertyExactMatchResolver(driver=self.driver)
        return await resolver.run()

    async def write_knowledge_graph(self, knowledge_graph):
        writer = Neo4jWriter(driver=self.driver)
        return await writer.run(graph=knowledge_graph)

    def create_vector_index(self, name, label, embedding_property, dimensions, similarity_fn):
        create_vector_index(
            self.driver,
            name=name,
            label=label,
            embedding_property=embedding_property,
            dimensions=dimensions,
            similarity_fn=similarity_fn
        )
