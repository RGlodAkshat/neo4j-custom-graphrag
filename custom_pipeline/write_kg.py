import os
import asyncio
import neo4j
from neo4j import GraphDatabase
from neo4j_graphrag.experimental.components.kg_writer import Neo4jWriter
from dotenv import load_dotenv



load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

neo4j_driver = neo4j.GraphDatabase.driver(NEO4J_URI,
                auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

from neo4j_graphrag.experimental.components.types import (
        Neo4jGraph,
        LexicalGraphConfig,
        Neo4jNode,
        Neo4jRelationship
    )

nodes=[Neo4jNode(id='0', label='Organization', properties={'name': 'Thyrocare'}, embedding_properties=None), Neo4jNode(id='1', label='Person', properties={'name': 'Selfisha Katoch'}, embedding_properties=None), Neo4jNode(id='2', label='Test', properties={'name': 'HbA1c'}, embedding_properties=None), Neo4jNode(id='3', label='Test', properties={'name': 'Hemogram'}, embedding_properties=None), Neo4jNode(id='4', label='Biomarker', properties={'name': 'HbA1c value'}, embedding_properties=None), Neo4jNode(id='5', label='Biomarker', properties={'name': 'Average Blood Glucose'}, embedding_properties=None), Neo4jNode(id='6', label='Person', properties={'name': 'Dr Neha Prabhakar'}, embedding_properties=None), Neo4jNode(id='7', label='Person', properties={'name': 'Dr Bhumika'}, embedding_properties=None)]
relationships=[Neo4jRelationship(start_node_id='2', end_node_id='0', type='PROVIDED_BY', properties={}, embedding_properties=None), Neo4jRelationship(start_node_id='1', end_node_id='2', type='UNDERWENT', properties={}, embedding_properties=None), Neo4jRelationship(start_node_id='1', end_node_id='3', type='UNDERWENT', properties={}, embedding_properties=None), Neo4jRelationship(start_node_id='2', end_node_id='4', type='HAS_RESULT', properties={}, embedding_properties=None), Neo4jRelationship(start_node_id='2', end_node_id='5', type='HAS_RESULT', properties={}, embedding_properties=None), Neo4jRelationship(start_node_id='6', end_node_id='2', type='AUTHORED', properties={}, embedding_properties=None), Neo4jRelationship(start_node_id='7', end_node_id='3', type='AUTHORED', properties={}, embedding_properties=None)]

graph=Neo4jGraph(nodes=nodes, relationships=relationships)

# Initialize Neo4jWriter
writer = Neo4jWriter(driver=neo4j_driver)


async def main():
    result = await writer.run(graph=graph, lexical_graph_config=LexicalGraphConfig())
    print(result.status)
    print(result.metadata)

asyncio.run(main())








