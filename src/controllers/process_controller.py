import os
from .BaseController import BaseController
from .ProjectControllers import ProjectControllers
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from models import ProcessEnum
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ProcessController(BaseController):
    def __init__(self, proj_id: str):
        super().__init__()
        self.proj_id = proj_id
        self.proj_path = ProjectControllers().get_proj_path(proj_id)

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str):
        file_path = os.path.join(self.proj_path, file_id)
        file_ext = self.get_file_extension(file_id)
        if not os.path.exists(file_path):
            return None
        if file_ext == ProcessEnum.TXT.value:
            return TextLoader(file_path, encoding='utf-8')
        if file_ext == ProcessEnum.PDF.value:
            return PyMuPDFLoader(file_path)

        return None

    def get_content(self, file_id: str):
        loader = self.get_file_loader(file_id=file_id)
        if loader:
            return loader.load()
        return None

    def process_file_content(self, file_content: list, file_id: str):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100,
                                                       chunk_overlap=20,
                                                       length_function=len,
                                                       is_separator_regex=False)
        file_content_text = [rec.page_content
                             for rec in file_content]
        file_metadata = [rec.metadata
                         for rec in file_content]
        chunks = text_splitter.create_documents(file_content_text, metadatas=file_metadata,

                                                )
        return chunks
