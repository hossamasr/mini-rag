from qdrant_client.models import PointStruct
from ..vectordb_interface import VectorDBInterface
from ..vectordb_enums import DistanceMethodEnum
import logging
from typing import Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, Batch


class QdrantDB(VectorDBInterface):

    def __init__(self, db_path, distance_method):
        self.db_path = db_path
        self.client = None
        if distance_method == DistanceMethodEnum.COSINE.value:
            self.distance_method = Distance.COSINE
        elif distance_method == DistanceMethodEnum.DOT.value:
            self.distance_method = Distance.DOT
        else:
            raise ValueError(f"Invalid distance method: {distance_method}")

        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        self.client = None

    def is_collection_existed(self, collection_name: str):

        return self.client.collection_exists(collection_name=collection_name)

    def list_all_collections(self):
        return self.client.get_collections()

    def get_collection_info(self, collection_name):
        return self.client.get_collection(collection_name)

    def delete_connection(self, collection_name):
        if self.is_collection_existed(collection_name):
            self.client.delete_collection(collection_name)

    def create_collection(self, collection_name, embedding_size, do_reset: bool = False):
        if do_reset:
            _ = self.delete_connection(collection_name)
        if not self.is_collection_existed(collection_name):
            _ = self.client.create_collection(
                collection_name="test_collection",
                vectors_config=VectorParams(size=embedding_size, distance=self.distance_method),)
            return True
        return False

    def insert_one(self, collection_name: str, text: str, vector: int, metadata: Optional[dict] = None, record_id: Optional[str] = None):
        if not self.is_collection_existed(collection_name):
            self.logger.error(f"No Collection with Name {collection_name}")
            return False
        try:
            operation_info = self.client.upsert(
                collection_name=collection_name,
                points=[
                    PointStruct(
                        id="",
                        payload={
                            "text": text,
                            "metadata": metadata
                        },
                        vector=[vector],
                    )
                ]

            )
        except Exception as e:
            self.logger.error(f"Error While inserting batch: {e}")
            return False

        return operation_info

    def insert_many(self, collection_name: str, text: list, vector: list, metadata: Optional[list] = None, record_id: Optional[list] = None, batch_size: int = 50):
        if not metadata:
            metadata = [None]*len(text)
        if not record_id:
            record_id = [None]*len(text)
        for i in range(0, len(text), batch_size):
            batch_end = i+batch_size
            batch_texts = text[i:batch_end]
            batch_vector = vector[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            batch_records = Batch(
                ids=[],
                payloads=[
                    {
                        "text": batch_texts[x],
                        "metadata": batch_metadata[x]
                    }
                    for x in range(len(batch_texts))
                ],

                vectors=[batch_vector[x]for x in range(len(batch_texts))]
            )
        try:
            self.client.upsert(
                collection_name=collection_name,
                points=batch_records
            )
        except Exception as e:
            self.logger.error(f"Error While Inserting Batch {e}")
            return False

    def search_by_vector(self, collection_name: str, vector: list, limit: int = 5):
        return self.client.query_points(
            collection_name=collection_name,
            query=vector, limit=limit
        )
