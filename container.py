from clients.openai_client import OpenAIClient
from clients.neo4j_client import Neo4jClient
from services.openai_service import OpenAIService
from services.neo4j_service import Neo4jService
from services.graphrag_service import GraphRAGService
import os

# Load environment variables or set directly
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-...")

# Create singletons
openai_client = OpenAIClient(api_key=OPENAI_API_KEY)
neo4j_client = Neo4jClient(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
openai_service = OpenAIService(openai_client)
neo4j_service = Neo4jService(neo4j_client)
graph_rag_service = GraphRAGService(openai_service, neo4j_service)
