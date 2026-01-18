"""Health check эндпоинт."""

from fastapi import APIRouter

from dt_xml.api.schemas.response import HealthResponse
from dt_xml.config.settings import get_settings
from dt_xml.storage.metadata_store import MetadataStore
from dt_xml.storage.vector_store import VectorStore

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=HealthResponse)
@router.get("/healthz", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check эндпоинт."""
    settings = get_settings()
    status = "healthy"

    # Проверка векторной БД
    vector_db_info = {}
    try:
        vector_store = VectorStore()
        vector_db_info = vector_store.get_collection_info()
    except Exception as e:
        status = "degraded"
        vector_db_info = {"error": str(e)}

    # Проверка метаданных БД
    metadata_db_info = {}
    try:
        metadata_store = MetadataStore()
        # Простая проверка подключения
        metadata_db_info = {"status": "connected"}
    except Exception as e:
        status = "degraded"
        metadata_db_info = {"error": str(e)}

    # Информация о модели эмбедингов
    embedding_model_info = {}
    try:
        from dt_xml.embedding.multilingual_embedder import MultilingualEmbedder

        embedder = MultilingualEmbedder()
        embedding_model_info = embedder.get_model_info()
    except Exception as e:
        status = "degraded"
        embedding_model_info = {"error": str(e)}

    return HealthResponse(
        status=status,
        vector_db=vector_db_info,
        metadata_db=metadata_db_info,
        embedding_model=embedding_model_info,
    )
