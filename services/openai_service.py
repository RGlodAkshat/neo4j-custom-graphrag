from clients.openai_client import OpenAIClient
from neo4j_graphrag.experimental.components.text_splitters.fixed_size_splitter import FixedSizeSplitter
from neo4j_graphrag.experimental.components.entity_relation_extractor import LLMEntityRelationExtractor
from neo4j_graphrag.experimental.components.types import TextChunks

class OpenAIService:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client

    async def split_pdf(self, pdf_file_path):
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_file_path)
        text_per_page = [page.extract_text() for page in reader.pages]
        text_splitter = FixedSizeSplitter(chunk_size=100, chunk_overlap=10)
        all_chunks = []
        for text in text_per_page:
            result = await text_splitter.run(text=text)
            all_chunks.extend(result.chunks)
        return all_chunks

    async def embed_chunks(self, chunks):
        text_chunks = TextChunks(chunks=chunks)
        return await self.openai_client.embed_chunks(text_chunks)

    async def extract_entities_relations(self, prompt_template, examples, schema, chunk):
        extractor = LLMEntityRelationExtractor(
            llm=self.openai_client.get_llm(),
            prompt_template=prompt_template,
        )
        return await extractor.extract_for_chunk(schema, examples, chunk)
