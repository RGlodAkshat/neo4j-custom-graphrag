# openai_client.py
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings

class OpenAIClient:
    def __init__(self, api_key, embedding_model="text-embedding-3-large", llm_model="gpt-4o-mini"):
        self.embedding = OpenAIEmbeddings(model=embedding_model)
        self.llm = OpenAILLM(
            model_name=llm_model,
            model_params={
                "response_format": {"type": "json_object"},
                "temperature": 0
            }
        )

    async def embed_chunks(self, text_chunks):
        from neo4j_graphrag.experimental.components.embedder import TextChunkEmbedder
        chunk_embedder = TextChunkEmbedder(self.embedding)
        return await chunk_embedder.run(text_chunks)

    def get_llm(self):
        return self.llm
