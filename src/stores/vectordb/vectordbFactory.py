from .vectordb_enums import VectordbEnum
from providers import QdrantDB
from controllers.BaseController import BaseController

class VectorDbProviderFactory:
    def __init__(self, config: dict):
        self.config = config
        self.base_cont=BaseController()
    def create(self, provider):
        if provider ==VectordbEnum.QDRANT.value:
            db_path=self.base_cont.get_db_path(self.config.VECTOR_DB_PATH)
            return QdrantDB(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD
            )
        return None
 