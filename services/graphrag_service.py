from services.openai_service import OpenAIService
from services.neo4j_service import Neo4jService
from neo4j_graphrag.experimental.components.types import Neo4jGraph, Neo4jNode, Neo4jRelationship, TextChunks
from neo4j_graphrag.experimental.components.schema import SchemaConfig
from prompts.prompts import *
from neo4j_graphrag.experimental.components.types import TextChunks

class GraphRAGService:
    def __init__(self, openai_service: OpenAIService, neo4j_service: Neo4jService):
        self.openai_service = openai_service
        self.neo4j_service = neo4j_service

    async def process_pdf(self, pdf_path: str, hushh_id: str) -> None:
        # 1. Split PDF into chunks
        chunks = await self.openai_service.split_pdf(pdf_path)

        # 2. Embed the chunks
        embedded_chunks: TextChunks = await self.openai_service.embed_chunks(chunks)
        for chunk in embedded_chunks.chunks:
            chunk.metadata['hushh_id'] = hushh_id

        # 3. Build schema
        schema: SchemaConfig = SchemaConfig(
            entities=schema_entities,
            relations=schema_relations,
            potential_schema=None
        )

        # 4. Extract entities/relations and build knowledge graph
        knowledge_graph: Neo4jGraph = Neo4jGraph(nodes=[], relationships=[])
        for chunk in embedded_chunks.chunks:
            chunk_node = Neo4jNode(
                id=chunk.uid,
                label=f"{hushh_id}_Chunk",
                properties={
                    "text": chunk.text,
                    "index": chunk.index,
                    "embedding": chunk.metadata['embedding'],
                    "hushh_id": chunk.metadata['hushh_id']
                }
            )
            knowledge_graph.nodes.append(chunk_node)

            graph: Neo4jGraph = await self.openai_service.extract_entities_relations(
                TEMPLATE_PROMPT, INPUT_TEXT, schema, chunk
            )

            for node in graph.nodes:
                node.properties['hushh_id'] = chunk.metadata['hushh_id']
                node.label = "__Entity__"
                knowledge_graph.nodes.append(node)
                chunk_rel = Neo4jRelationship(
                    start_node_id=chunk_node.id,
                    end_node_id=node.id,
                    type="EXTRACTED_FROM",
                    properties={}
                )
                knowledge_graph.relationships.append(chunk_rel)

            for rel in graph.relationships:
                knowledge_graph.relationships.append(rel)

        # 5. Entity resolution
        await self.neo4j_service.resolve_entities()

        # 6. Write to Neo4j
        await self.neo4j_service.write_knowledge_graph(knowledge_graph)

        # 7. Create vector index
        self.neo4j_service.create_vector_index(
            name="text_embeddings",
            label="Chunk",
            embedding_property="embedding",
            dimensions=1536,
            similarity_fn="cosine"
        )