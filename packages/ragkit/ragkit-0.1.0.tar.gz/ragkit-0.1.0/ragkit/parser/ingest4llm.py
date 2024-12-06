import os

from ingest4llm import Ingestor

from ragkit.document import Document

from ._base import BaseParser


class Ingest4LLM(BaseParser):
    def __init__(self, uri: str, description: str | None = None, base_url: str | None = None):
        super().__init__(uri, description)
        self.client = Ingestor(base_url or os.getenv("INGEST4LLM_BASE_URL"))

    async def parse(self) -> dict:
        ret = await self.client.ingest(self.uri)
        doc = Document.model_validate(ret.model_dump())
        doc.source = self.uri
        doc.description = self.description
        return doc
