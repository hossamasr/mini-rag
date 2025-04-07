from .BaseController import BaseController
from ..models.db_schemas import Project, DataChunk
from ..stores.llm_enums import DocumentType

import json
class NLPController(BaseController):

    def __init__(self, vector_db_client, generation_client, embedding_client):
        super().__init__()
        self.vector_db_client = vector_db_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client

    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}".strip()

    def reset_vectordb_collection(self, project: Project):
        collection_name = self.create_collection_name(project.project_id)
        return self.vector_db_client.delete_collection(collection_name)

    def get_vector_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project.project_id)
        collection_info = self.vector_db_client.get_collection_info(
            collection_name)
        return json.load(
            json.dumps(collection_info,default=lambda x:x.__dict__)
        )

    def index_vectordb(self, project: Project, chunks: list[DataChunk], do_reset: bool = False):
        collection_name = self.create_collection_name(
            project.project_id)

        texts = [c.chunk_text for c in chunks]
        metadata = [c.chunk_metadata for c in chunks]

        vectors = [
            self.embedding_client.embed_text(
                text=text, document_type=DocumentType.DOCUMENT.value)
            for text in texts
        ]
        _ = self.vector_db_client.create_collection(
            collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset
        )
        _ = self.vector_db_client.insert_many(
            collection_name,
            texts=texts,
            metadata=metadata,
            vectors=vectors

        )
        return True
    def search_vector_db_collection(self,project:Project,text:str,limit :int=10):
            collection_name = self.create_collection_name(project.project_id)
            vector=self.embedding_client.embed_text(
                 text=text,document_type=DocumentType.QUERY.value
            )
            if not vector or len(vector)==0:
                return False
            results=self.vector_db_client.search_by_vector(
                 collection_name=collection_name,
                 vector=vector,
                 limit=limit
            )
            return json.load(
            json.dumps(results,default=lambda x:x.__dict__)
        )