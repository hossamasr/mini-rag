from .basedatamodel import BaseDataModel
from .db_schemas import Project
from .enums.database_Enum import DBeunm

class ProjectModel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client=db_client)
        self.collection=self.db_client[DBeunm.COLLECTION_PROJECT_NAME.value]

    async def create_project(self,project:Project):
        result=await self.collection.insert_one(project.model_dump(by_alias=True,exclude_unset=True))
        project.id= result.inserted_id
        return project

    async def getproject_createone(self,project_id:str):
        record=await self.collection.find_one({
            'project_id':project_id
        })
        if record is None:
            project=Project(project_id=project_id)
            project=await self.create_project(project=project)
            return project
        return Project(**record)


    async def get_all_projects(self,page=1,page_size=10):
        total_document=await self.collection.count_documents({})
        total_pages=total_document//page_size
        if total_pages %page_size >0:
            total_pages+=1

        cursor=self.collection.find().skip((page-1)*page_size).limit(page_size)
        projects=[]
        async for document in cursor:
            projects.append(Project(**document))

        return projects,total_pages
