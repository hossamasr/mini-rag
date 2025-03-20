import os.path

from fastapi import APIRouter, Depends, UploadFile, status, Request
from models.enums.ResponseEnums import ResponseSignals
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProcessController
from controllers import ProjectControllers
from models.projectmodel import ProjectModel
from .schemas.data import ProcessRequest
from models.chunkModel import ChunkModel
from models.db_schemas import DataChunk, Asset
from models.Asset_Model import AssetModel
from models.enums.asset_enum import AssetType

import aiofiles
import logging
logger = logging.getLogger('uvicorn.error')
data_router = APIRouter(
    prefix='/api/v1/data',
    tags=["api_v1", "data"]
)


@data_router.post('/upload/{proj_id}')
async def upload_data(request: Request, proj_id: str, file: UploadFile,
                      app_settings=Depends(get_settings)):

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.getproject_createone(proj_id)

# validate the file
    is_valid, signal = DataController().validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": signal
            }
        )
    project_dir_path = ProjectControllers().get_proj_path(proj_id)
    file_path, file_uniqueid = DataController().generate_filenames(
        orig_name=file.filename, proj_id=proj_id)
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
    # store assets into db
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
    asset_resource = Asset(asset_object_id=project.id,
                           asset_type=AssetType.FILE.value,
                           asset_name=file_uniqueid,
                           asset_size=os.path.getsize(file_path)
                           )
    asset_record = await asset_model.create_asset(asset_resource)
    return JSONResponse(

        content={
            "signal": ResponseSignals.FILE_UPLOADED_SUCCESSFULLY.value, "fileid": str(asset_record.id)
        }
    )


@data_router.post('/process/{proj_id}')
async def process_endpoint(request: Request, proj_id: str, req: ProcessRequest):
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.getproject_createone(proj_id)
    # file_id=req.file_id
    do_reset = req.do_reset
    process_controller = ProcessController(proj_id)
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
    project_files_ids = {}
    if req.file_id:
        asset_record = await asset_model.get_asset_record(project.id, req.file_id)
        project_files_ids = [req.file_id]
        if asset_record is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={
                                    "signal": "Asset Not Found"

                                })
        project_files_ids = {
            asset_record.id: asset_record.asset_name
        }

    else:
        # store assets into db
        project_files = await asset_model.get_all_proj_assets(project.id, AssetType.FILE.value)

        project_files_ids = {
            record.id: record.asset_name for record in project_files

        }
        if len(project_files_ids) == 0:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": "No files"
                })
    no_records = 0
    no_files = 0
    chunk_model = await ChunkModel.create_instance(
        db_client=request.app.db_client
    )
    if do_reset == 1:
        await chunk_model.delete_chunk_byprojid(project.id)
    for asset_id, file_id in project_files_ids.items():
        file_content = process_controller.get_content(file_id)
        if file_content is None:
            logger.error(f"error while processing {file_id}")
            continue
        file_chunks = process_controller.process_file_content(
            file_content, file_id)
        if file_chunks is None or len(file_chunks) == 0:
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "signal": ResponseSignals.PROCESSING_FAILED
            }
        chunk_model = await ChunkModel.create_instance(
            db_client=request.app.db_client
        )

        file_chunks_records = [
            DataChunk(

                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=i+1,
                chunk_project_id=project.id,
                chunk_asset_id=asset_id
            )
            for i, chunk in enumerate(file_chunks)
        ]
        no_records += await chunk_model.insert_many_chunks(file_chunks_records)
        no_files += 1
        return JSONResponse(content={
            "signal": ResponseSignals.PROCESSING_SUCESS.value,
            "inserted_chunks": no_records,
            "no_files": no_files
        })
