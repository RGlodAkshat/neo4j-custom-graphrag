# Neo4j Custom GraphRAG

This project demonstrates how to build a small knowledge graph pipeline using the `neo4j-graphrag` framework together with OpenAI models. It provides both a command line example and a minimal FastAPI service that reads a PDF, extracts entities/relations and writes the results into Neo4j.

## Features

- Split PDF documents into text chunks and generate embeddings with OpenAI.
- Use an LLM to extract entities and relationships according to a custom prompt.
- Store the resulting graph in Neo4j and create a vector index for similarity search.
- Expose the pipeline through a FastAPI endpoint.

## Getting Started

1. **Install requirements**
   ```bash
   pip install -r custom_pipeline/requirements.txt
   ```

2. **Set environment variables**
   - `NEO4J_URI` – Neo4j connection string (e.g. `bolt://localhost:7687`)
   - `NEO4J_USERNAME` – Neo4j username
   - `NEO4J_PASSWORD` – Neo4j password
   - `OPENAI_API_KEY` – OpenAI API key

3. **Run the API server**
   ```bash
   uvicorn main:app --reload
   ```
   The service exposes `GET /user_route` which expects `file_path` (path to a PDF) and `hushh_id`.

4. **CLI Example**
   The `custom_pipeline/pipeline.py` script shows the same process without FastAPI. Adapt the file paths and run it with Python to load a PDF and write a graph.

## Repository Layout

- `clients/` – Thin wrappers around Neo4j and OpenAI utilities.
- `services/` – Higher level services that perform splitting, embedding, extraction and Neo4j interactions.
- `routes/` – FastAPI route definition.
- `prompts/` – Prompt template and schema examples used for the LLM extractor.
- `custom_pipeline/` – Stand‑alone pipeline and requirements file.
- `container.py` – Wires together the services used by the API.
- `demo.py` – Example script showing how to invoke the pipeline programmatically.

## License

This repository is provided for demonstration purposes and does not include any specific license terms.
