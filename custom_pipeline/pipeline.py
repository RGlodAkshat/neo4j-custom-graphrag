import neo4j
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from neo4j import GraphDatabase
from neo4j_graphrag.experimental.pipeline.component import DataModel
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.experimental.components.text_splitters.fixed_size_splitter import FixedSizeSplitter
from neo4j_graphrag.experimental.components.types import Neo4jNode, Neo4jRelationship
from PyPDF2 import PdfReader
from neo4j_graphrag.experimental.components.types import (
        # LexicalGraphConfig,
        TextChunks
    )


from neo4j_graphrag.experimental.components.entity_relation_extractor import (
        EntityRelationExtractor,
        LLMEntityRelationExtractor,
        OnError,
    )
from neo4j_graphrag.experimental.components.schema import SchemaConfig
from neo4j_graphrag.experimental.components.types import (
        Neo4jGraph,
    )
from neo4j_graphrag.experimental.components.embedder import TextChunkEmbedder
from neo4j_graphrag.experimental.components.resolver import (
    # EntityResolver,
    SinglePropertyExactMatchResolver,
)

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

neo4j_driver = neo4j.GraphDatabase.driver(NEO4J_URI,
                auth=(NEO4J_USERNAME, NEO4J_PASSWORD))





async def split_documents(pdf_file_path):
    #block 1
    reader = PdfReader(pdf_file_path)  # Load the PDF
    text_per_page = [page.extract_text() for page in reader.pages]  # Extract text from each page
    print("Extracted text from PDF")


    #block 2
    text_splitter = FixedSizeSplitter(chunk_size=100, chunk_overlap=10)
    print("Splitting text into chunks")
    all_chunks = []
    for text in text_per_page:
        result = await (text_splitter.run(text=text))
        chunks = result.chunks
        all_chunks.extend(chunks)
        print(f"Extracted {len(all_chunks)} chunks from text")

    return all_chunks




async def main():

    # Extract text from pdf
    #block 1 taken from here
    
    # Split text into chunks

    
    from neo4j_graphrag.experimental.components.embedder import TextChunkEmbedder
    from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings
    #block 2 taken from here
    chunks = await split_documents("./pdfs/isha.pdf")

    #add embeddings to chunks
    print("Adding embeddings to chunks")
    text_chunks = TextChunks(chunks=chunks)
    embedder = OpenAIEmbeddings(model="text-embedding-3-large")
    chunk_embedder = TextChunkEmbedder(embedder)
    embedded_chunks = await chunk_embedder.run(text_chunks)
    for chunk in embedded_chunks.chunks:
        chunk.metadata['hushh_id'] = '10101'
        #print(chunk)
        #print(type(chunk))
    #print(type(embedded_chunks))


    

    # Extract entities and relations
    #Schema builder
    llm = OpenAILLM(
        model_name="gpt-4o-mini",
        model_params={
            "response_format": {"type": "json_object"},  # use json_object formatting for best results
            "temperature": 0  # turning temperature down for more deterministic results
        }
    )
    prompt_template = """
    You are an expert at reading medical reports and extracting information from them. 
    You have been asked to extract the entities (nodes) and specify their type from the following Input text. 
    Also extract the relationships between these nodes. the relationship direction goes from the start node to the end node.

    Return result as JSON using the following format:
    {{"nodes": [ {{"id": "0", "label": "the type of entity", "properties": {{"name": "name of entity" }} }}],
      "relationships": [{{"type": "TYPE_OF_RELATIONSHIP", "start_node_id": "0", "end_node_id": "1", "properties": {{"details": "Description of the relationship"}} }}] }}

    ...

    Use only fhe following nodes and relationships:
    {schema}

    Assign a unique ID (string) to each node, and reuse it to define relationships.
    Do respect the source and target node types for relationship and the relationship direction.

    Do not return any additional information other than the JSON in it.

    Examples:
    {examples}

    Input text:

    {text}
    """

    examples = """
    **Example 1:**

Input text: "John bought two Nike shoes for $150 using his credit card on March 5th, 2023."

Output: {
    "nodes": [
        {
            "id": "0",
            "label": "person",
            "properties": {
                "name": "John"
            }
        },
        {
            "id": "1",
            "label": "product",
            "properties": {
                "name": "Nike shoes"
            }
        },
        {
            "id": "2",
            "label": "quantity",
            "properties": {
                "value": "2"
            }
        },
        {
            "id": "3",
            "label": "price",
            "properties": {
                "value": "150"
            }
        },
        {
            "id": "4",
            "label": "payment_method",
            "properties": {
                "type": "credit card"
            }
        },
        {
            "id": "5",
            "label": "date",
            "properties": {
                "value": "March 5th, 2023"
            }
        },
        {
            "id": "6",
            "label": "brand",
            "properties": {
                "name": "Nike"
            }
        }
    ],
    "relationships": [
        {
            "type": "purchased",
            "start_node_id": "0",
            "end_node_id": "1",
            "properties": {}
        },
        {
            "type": "in_quantity",
            "start_node_id": "1",
            "end_node_id": "2",
            "properties": {}
        },
        {
            "type": "for_price",
            "start_node_id": "1",
            "end_node_id": "3",
            "properties": {}
        },
        {
            "type": "using_payment_method",
            "start_node_id": "1",
            "end_node_id": "4",
            "properties": {}
        },
        {
            "type": "on_date",
            "start_node_id": "1",
            "end_node_id": "5",
            "properties": {}
        },
        {
            "type": "from brand",
            "start_node_id": "1",
            "end_node_id": "6",
            "properties": {}
        }
    ]
}
"""
    basic_node_labels = ["person","email", "product", "size", "quantity", "date", "brand", "location", "product_category", "price", "currency", "payment_method"]
    node_labels = {label: {} for label in basic_node_labels}  # Create a dictionary

    rel_types = [
        "purchased",
        "having_category",  # Person → Test
        "from brand",  # Test → Biomarker
        "on_date",  # Test → Lab
        "in_size",  # Test → Method
        "for_price",
        "in_currency"  # Test → Unit
        "in_quantity",  # Test → Result
        "using_payment_method",  # Result → Reference Range
    ]
    rel_types = {rel: {} for rel in rel_types}  # Create a dictionary

    

    extractor = LLMEntityRelationExtractor(
        llm=llm,
        prompt_template=prompt_template,
    )

    schema = SchemaConfig(
        entities=node_labels,
        relations=rel_types,
        potential_schema=None
    )

    knowledge_graph = Neo4jGraph(nodes=[], relationships=[])
    
    for chunk in embedded_chunks.chunks:

        # Create Chunk node
        #print(f"Processing chunk {chunk.uid}")
        chunk_node = Neo4jNode(
            id=chunk.uid,
            label="10101_Chunk",
            properties={
                "text": chunk.text,
                "index": chunk.index,
                "embedding": chunk.metadata['embedding'],
                "hushh_id": chunk.metadata['hushh_id']
            }
        )
        knowledge_graph.nodes.append(chunk_node)  #verify step
                                #knowledge_graph.add_node(chunk_node)    #verify if add node exists

        graph: Neo4jGraph = await extractor.extract_for_chunk(schema, examples, chunk) #extract nodes and relationships from chunk
        nodes = graph.nodes
        relationships = graph.relationships

        for node in nodes:
            #print(f"Adding node {node.id} to knowledge graph")
            node.properties['hushh_id'] = chunk.metadata['hushh_id']  #keep adding hushh_id to each node
            node.label="__Entity__"  #add label to each node
            knowledge_graph.nodes.append(node)    #keep adding the nodes to knowledge graph

            chunk_relationship = Neo4jRelationship(   #keep linking the chunk node to the nodes
                start_node_id=chunk_node.id, 
                end_node_id=node.id,
                type="EXTRACTED_FROM",
                properties={}
            )
            knowledge_graph.relationships.append(chunk_relationship)  #keep adding chunk relationships to knowledge graph

        for relationship in relationships:
            #print(f"Adding relationship {relationship.type} to knowledge graph")
            knowledge_graph.relationships.append(relationship)  #add rest of the relationships
        print(knowledge_graph)


        # with open("isha.txt","a") as file:
        #     file.write(str(knowledge_graph) + "\n")


    # write the knowledge graph to Neo4j
    

    resolver = SinglePropertyExactMatchResolver(driver=neo4j_driver) #or "hushh_id"
    resolution_stats = await resolver.run()
    print(f"Entity Resolution Stats: {resolution_stats}")

    from neo4j_graphrag.experimental.components.types import (
        LexicalGraphConfig
    )
    from neo4j_graphrag.experimental.components.kg_writer import Neo4jWriter
    writer = Neo4jWriter(driver=neo4j_driver)
    print("Writing knowledge graph to Neo4j")
    result = await writer.run(graph=knowledge_graph)



    #lexical_graph_config=LexicalGraphConfig()


    # create index of chunk nodes

    INDEX_NAME="text_embeddings"  #unique name for each user

    from neo4j_graphrag.indexes import create_vector_index
    print(f"Creating index {INDEX_NAME}")
    create_vector_index(neo4j_driver, name=INDEX_NAME, label="Chunk",
                  embedding_property="embedding", dimensions=1536, similarity_fn="cosine")
    
    
if __name__ == "__main__":
    asyncio.run(main())


