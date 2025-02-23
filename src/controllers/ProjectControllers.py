from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignals
import  os
class ProjectControllers(BaseController):
    def __init__(self):
        super().__init__()
    def get_proj_path(self,project_id:str):
        proj_dir=os.path.join(self.file_dir,project_id)
        if not os.path.exists(proj_dir):
            os.makedirs(proj_dir)
        return proj_dir
