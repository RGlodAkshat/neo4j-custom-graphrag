TEMPLATE_PROMPT = """
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

INPUT_TEXT ="""
John bought two Nike shoes for $150 using his credit card on March 5th, 2023.

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

ENTITIES = ["person","email", "product", "size", "quantity", "date", "brand", "location", "product_category", "price", "currency", "payment_method"]
schema_entities = {label: {} for label in ENTITIES}  # Create a dictionary

RELATIONSHIPS = [
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
schema_relations = {rel: {} for rel in RELATIONSHIPS}