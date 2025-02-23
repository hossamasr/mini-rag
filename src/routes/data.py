import os.path
from models import ResponseSignals
from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers.config import get_settings ,Settings
from controllers import DataController
from controllers import  ProjectControllers
import  aiofiles
data_router=APIRouter(
    prefix='/api/v1/data',
    tags=["api_v1","data"]
)

@data_router.post('/upload/{proj_id}')
async def upload_data(proj_id:str,file:UploadFile,
                      app_settings=Depends(get_settings)):
# validate the file
    is_valid,signal=DataController().validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":signal
            }
        )
    project_dir_path=ProjectControllers().get_proj_path(proj_id)
    file_path=DataController().generate_filenames(orig_name=file.filename,proj_id=proj_id)
    async with aiofiles.open(file_path, 'wb') as f:
        while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
            await f.write(chunk)

        return JSONResponse(

                content={
            "signal":ResponseSignals.FILE_UPLOADED_SUCCESSFULLY.value
        }

        )
