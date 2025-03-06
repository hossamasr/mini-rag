from .basedatamodel import BaseDataModel
from .db_schemas import Asset
from .enums.database_Enum import DBeunm
from bson import ObjectId

class AssetModel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client)
        self.collection=self.db_client[DBeunm.COLLECTION_ASSET_NAME.value]
    @classmethod
    async def create_instance(cls, db_client: object):
            instance = cls(db_client)
            await instance.init_collection()
            return instance
    async def init_collection(self):
        all_collection=await self.db_client.list_collection_names()
        if DBeunm.COLLECTION_ASSET_NAME.value not in all_collection:
            self.collection = self.db_client[DBeunm.COLLECTION_ASSET_NAME.value]
            indexes=Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]

                )


    async def create_asset(self, asset: Asset):
                    result = await self.collection.insert_one(asset.model_dump(by_alias=True, exclude_unset=True))
                    asset.id = result.inserted_id
                    return asset
    async def get_all_proj_assets(self,asset_project_id:str):
        return await self.collection.find({
            "asset_object_id":ObjectId(asset_project_id) if isinstance(asset_project_id,str) else asset_project_id

        }).to_list()
