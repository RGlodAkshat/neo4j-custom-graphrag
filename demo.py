# main.py
import os
import asyncio
from clients.openai_client import OpenAIClient
from clients.neo4j_client import Neo4jClient
from services.openai_service import OpenAIService
from services.neo4j_service import Neo4jService
from services.graphrag_service import GraphRAGService

# Environment variables
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize clients and services
openai_client = OpenAIClient(api_key=OPENAI_API_KEY)
neo4j_client = Neo4jClient(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
openai_service = OpenAIService(openai_client)
neo4j_service = Neo4jService(neo4j_client)
graph_rag_service = GraphRAGService(openai_service, neo4j_service)

# Define prompt, examples, schema_entities, schema_relations as in your pipeline

async def main():
    await graph_rag_service.process_pdf(
        pdf_path="./pdfs/isha.pdf",
        prompt_template=prompt_template,
        examples=examples,
        schema_entities=node_labels,
        schema_relations=rel_types,
        hushh_id="10101"
    )

if __name__ == "__main__":
    asyncio.run(main())
