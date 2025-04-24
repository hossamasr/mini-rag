from abc import ABC, abstractmethod
from ast import List
from typing import Optional

from src.models.db_schemas.data_chuncks import RetrievedDocument


class VectorDBInterface(ABC):

    @abstractmethod
    def connect(self):

        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_collection_existed(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def list_all_collections(self):
        pass

    @abstractmethod
    def get_collection_info(self, collection_name):
        pass

    @abstractmethod
    def delete_connection(self, collection_name):
        pass

    @abstractmethod
    def create_collection(self, collection_name, embedding_size, do_reset: bool = False):
        pass

    @abstractmethod
    def insert_one(self, collection_name: str, text: str, vector: int, metadata: Optional[dict] = None, record_id: Optional[str] = None):
        pass

    @abstractmethod
    def insert_many(self, collection_name: str, text: list, vector: list, metadata: Optional[list] = None, record_id: Optional[list] = None, batch_size: int = 50):
        pass

    @abstractmethod
    def search_by_vector(self, collection_name: str, vector: list, limit: int) -> List[RetrievedDocument]:
        pass
