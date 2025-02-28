import os.path
from models import ResponseSignals
from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers.config import get_settings ,Settings
from controllers import DataController,ProcessController
from controllers import  ProjectControllers
from .schemas.data import ProcessRequest
import  aiofiles
import logging
logger=logging.getLogger('uvicorn.error')
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
    file_path,file_uniqueid=DataController().generate_filenames(orig_name=file.filename,proj_id=proj_id)
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
                await f.write(chunk)

    except Exception as e:
        logger.error(f"While Uploading File: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": "Error In Uploading Please Contact Support"
            }
        )

    return JSONResponse(

                    content={
                "signal":ResponseSignals.FILE_UPLOADED_SUCCESSFULLY.value
                    ,"fileid":file_uniqueid
        }
)


@data_router.post('/process/{proj_id}')
async def process_endpoint(proj_id:str,req:ProcessRequest):
    file_id=req.file_id
    process_controller=ProcessController(proj_id)
    file_content=process_controller.get_content(file_id)
    file_chunks=process_controller.process_file_content(file_content,file_id)
    if file_chunks is None or len(file_chunks)==0:
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "signal":ResponseSignals.PROCESSING_FAILED
        }
    return file_chunks
