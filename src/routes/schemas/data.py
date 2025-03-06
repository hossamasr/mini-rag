from pydantic import BaseModel
from typing import Optional
# schema of Data Validation ^_^
class ProcessRequest(BaseModel):
    file_id:str=None
    chunk_size:Optional[int]=100
    overlap:Optional[int]=20
    do_reset : Optional[int]=0
