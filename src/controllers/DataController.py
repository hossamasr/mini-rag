import os.path

from .BaseController import BaseController
from fastapi import UploadFile
from .ProjectControllers import ProjectControllers
from models import ResponseSignals
import re


class DataController(BaseController):
    def __init__(self):
        super().__init__()  # wake up Father LOL xD
        self.size_scale = 1024*1024

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignals.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE*self.size_scale:
            return False, ResponseSignals.FILE_EXCEEDED_MAXIMUM_SIZE.value
        return True, ResponseSignals.FILE_UPLOADED_SUCCESSFULLY.value

    def generate_filenames(self, orig_name, proj_id: str):
        rand_filename = self.generate_random_strings()
        project_path = ProjectControllers().get_proj_path(project_id=proj_id)
        cleaned_name = self.clean_name(orig_name)
        new_file_path = os.path.join(
            project_path, rand_filename+'_'+cleaned_name)
        while os.path.exists(new_file_path):
            rand_filename = self.generate_random_strings()
            project_path = ProjectControllers().get_proj_path(project_id=proj_id)
            cleaned_name = self.clean_name(orig_name)
            new_file_path = os.path.join(
                project_path, rand_filename+'_'+cleaned_name)
        return new_file_path, rand_filename+'_'+cleaned_name

    def clean_name(self, orgname):
        clean_name = re.sub(r'[^\w.]', '', orgname.strip())
        cleaned_name = clean_name.replace(' ', '_')
        return cleaned_name
