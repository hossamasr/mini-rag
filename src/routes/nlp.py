import os.path
from unittest import result
from fastapi import APIRouter, Depends, UploadFile, status, Request
from httpx import request
from openai import project
from models.enums.ResponseEnums import ResponseSignals
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import NLPController
from models.projectmodel import ProjectModel
from src.controllers import NlpController
from .schemas.nlp import PushReq, SearchRequest
from models.chunkModel import ChunkModel
from models.db_schemas import DataChunk, Asset
from models.Asset_Model import AssetModel
from models.enums.asset_enum import AssetType

import logging
logger = logging.getLogger('uvicorn.error')
nlp_router = APIRouter(
    prefix='/api/v1/nlp',
    tags=["api_v1", "nlp"]
)


@nlp_router.post("/index/push/{project_id}")
async def index_project(request: Request, project_id: str, push_request: PushReq):

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.getproject_createone(project_id=project_id)

    chunk_model = await ChunkModel.create_instance(
        db_client=request.app.db_client
    )

    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={
                "signal": "Project Not Found"
            }
        )
    nlp_controller = NLPController(
        vector_db_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        templeate_parser=request.app.tempelate_parser

    )
    has_records = True
    page_no = 1
    while has_records:
        page_chunks = chunk_model.get_project_chunks(project.id, page_no=1)
        if len(page_chunks):
            page_no += 1
        if not page_chunks or len(page_chunks) == 0:
            has_records = False
            break
        is_inserted = nlp_controller.index_vectordb(
            project, page_chunks, do_reset=push_request.do_reset)
        if not is_inserted:
            return "error nlp controller"
    return "success"


@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(request: Request, project_id: str):
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.getproject_createone(project_id=project_id)
    nlp_controller = NLPController(
        vector_db_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        templeate_parser=request.app.tempelate_parser
    )
    collection_info = nlp_controller.get_vector_collection_info(project)
    return JSONResponse(
        content={
            "collection_info": collection_info

        }
    )


@nlp_router.get("/index/search/{project_id}")
async def search_index(request: Request, project_id: str, search_request: SearchRequest):
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.getproject_createone(project_id=project_id)
    nlp_controller = NLPController(
        vector_db_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        templeate_parser=request.app.templeate_parser
    )
    results = nlp_controller.search_vector_db_collection(
        project, search_request.text, search_request.limit
    )
    return JSONResponse(
        content={
            "results": [result.dict() for result in results]
        }
    )


@nlp_router.get("/index/answer/{project_id}")
async def answer_rag(request: Request, project_id: str, search_request: SearchRequest):
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.getproject_createone(project_id=project_id)
    nlp_controller = NLPController(
        vector_db_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        templeate_parser=request.app.templeate_parser
    )
    answer, full_prompt, chat_history = nlp_controller.answer_rag_question(
        project, search_request.text, search_request.limit
    )
    return JSONResponse(
        content={
            "signal": "success",
            "answer": answer,
            "full_prompt": full_prompt,
            "chat_history": chat_history
        }
    )
