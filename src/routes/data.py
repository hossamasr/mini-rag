from fastapi import FastAPI,APIRouter,Depends,UploadFile
from helpers.config import get_settings ,Settings
from controllers import DataController
data_router=APIRouter(
    prefix='/api/v1/data',
    tags=["api_v1","data"]
)

@data_router.post('/upload/{proj_id}')
async def upload_data(proj_id:str,file:UploadFile,
                      app_settings=Depends(get_settings)):
# validate the file
    is_valid,signal=DataController().validate_uploaded_file(file=file)
    return {
        "signal":signal,

    }
