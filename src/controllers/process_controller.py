import os
from .BaseController import BaseController
from .ProjectControllers import ProjectControllers
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from models import ProcessEnum
class ProcessController(BaseController):
    def __init__(self,proj_id:str):
        super().__init__()
        self.proj_id=proj_id
        self.proj_path=ProjectControllers().get_proj_path(proj_id)
    def get_file_extension(self,file_id:str):
        return os.path.splitext(file_id)[-1]
    def get_file_loader(self,file_id:str):
        file_path=os.path.join(self.proj_path,file_id)
        file_ext=self.get_file_extension(file_id)
        if file_ext==ProcessEnum.TXT.value:
            return TextLoader(file_path,encoding='utf-8')
        if file_ext==ProcessEnum.PDF.value:
            return PyMuPDFLoader(file_path)

        return None
    def get_content(self,file_id:str):
        loader=self.get_file_loader(file_id=file_id)
        return loader.load()

