from fastapi import FastAPI
from pandas import to_datetime
from routes import data, base,nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager
from src.stores.llm import providers
from stores.llmProviderFactory import LLMProvideFactory
from stores.vectordb.vectordbFactory import VectorDbProviderFactory
app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (e.g., connecting to a database)
    print("Starting up...")
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    vectordb_factory=VectorDbProviderFactory(settings)
    llm_provider_fractory=LLMProvideFactory(settings)

    app.generation_client=llm_provider_fractory.create(provider=settings.GENERATION_BACKEND)
    if settings.GENERATION_MODEL_ID is not None:
        app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)
    else:
        raise ValueError("GENERATION_MODEL_ID must not be None")

    app.embedding_client=llm_provider_fractory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,embedding_size=settings.EMBEDDING_MODEL_SIZE)
    
    app.vectordb_client= vectordb_factory.create(
        provider=settings.VECTOR_DB_BACKEND
    )
    app.vectordb_client.connect()


    yield  # This marks the lifespan of the application

    # Shutdown logic (e.g., closing database connections)
    app.mongo_conn.close()
    app.vectordb_client.disconnect()


    print("Shutting down...")
    return


#deprecated

# @app.on_event('startup')
# async  def startdb_client():
#     settings=get_settings()
#     app.mongo_conn=AsyncIOMotorClient(settings.MONGODB_URL)
#     app.db_client=app.mongo_conn[settings.MONGODB_DATABASE]
# @app.on_event('shutdown')
# async  def shutdown_db():
#     app.mongo_conn.close()


# new way in another form

# async  def startdb_client():
#     settings=get_settings()
#     app.mongo_conn=AsyncIOMotorClient(settings.MONGODB_URL)
#     app.db_client=app.mongo_conn[settings.MONGODB_DATABASE]
# async  def shutdown_db():
#     app.mongo_conn.close()
#app.router.lifespan.on_startup.append(startup_db_client)
#app.router.lifespan.on_shutdown.append(shutdown_db_client)


app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)