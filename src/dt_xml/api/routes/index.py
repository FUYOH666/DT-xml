"""Эндпоинт индексации деклараций."""

import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException

from dt_xml.api.schemas.response import IndexResponse
from dt_xml.api.schemas.search import IndexRequest
from dt_xml.chunker.semantic_chunker import SemanticChunker
from dt_xml.embedding.multilingual_embedder import MultilingualEmbedder
from dt_xml.normalizer.field_normalizer import FieldNormalizer
from dt_xml.ocr.ocr_processor import OCRProcessor
from dt_xml.parser.xml_parser import XMLParser
from dt_xml.schema.schema_manager import SchemaManager
from dt_xml.storage.document_store import DocumentStore
from dt_xml.storage.metadata_store import MetadataStore
from dt_xml.storage.vector_store import VectorStore

router = APIRouter(prefix="/index", tags=["index"])

# Инициализация компонентов
schema_manager = SchemaManager()
parser = XMLParser(schema_manager=schema_manager)
normalizer = FieldNormalizer()
chunker = SemanticChunker()
embedder = MultilingualEmbedder()
ocr_processor = OCRProcessor(schema_manager=schema_manager)
vector_store = VectorStore()
metadata_store = MetadataStore()
document_store = DocumentStore()


@router.post("/", response_model=IndexResponse)
async def index_declaration(request: IndexRequest) -> IndexResponse:
    """Индексация декларации."""
    try:
        tenant_id = request.tenant_id or "default"

        # Определение источника данных
        if request.xml_content:
            # Парсинг XML
            parsed_data = parser.parse(request.xml_content, tenant_id=tenant_id)
            declaration_id = request.declaration_id or parsed_data.get("declaration_number", str(uuid.uuid4()))
        elif request.json_data:
            # Использование JSON данных
            parsed_data = request.json_data
            # Маппинг полей согласно схеме заказчика
            if schema_manager:
                schema_manager.load_tenant_schema(tenant_id)
                parsed_data = schema_manager.map_fields(parsed_data)
            declaration_id = request.declaration_id or parsed_data.get("declaration_number", str(uuid.uuid4()))
        elif request.ocr_text:
            # Обработка OCR текста
            parsed_data = ocr_processor.process(request.ocr_text, tenant_id=tenant_id)
            declaration_id = request.declaration_id or parsed_data.get("declaration_number", str(uuid.uuid4()))
        else:
            raise HTTPException(
                status_code=400,
                detail="Необходимо предоставить xml_content, json_data или ocr_text",
            )

        # Нормализация данных
        normalized_data = normalizer.normalize_all_fields(parsed_data)

        # Получение текста для чанкования
        text = normalized_data.get("full_text", "") or normalized_data.get("product_description", "")

        # Чанкование
        chunks = chunker.chunk_declaration(declaration_id, text, normalized_data)

        # Генерация эмбедингов
        chunk_texts = [chunk.content for chunk in chunks]
        embeddings = embedder.embed_batch(chunk_texts)

        # Сохранение в векторную БД
        vector_store.add_chunks(chunks, embeddings)

        # Сохранение метаданных
        metadata = parser.to_metadata(normalized_data)
        metadata_store.save_metadata(metadata, declaration_id)

        # Сохранение оригинального документа
        document_store.save_document(declaration_id, normalized_data, metadata.model_dump())

        return IndexResponse(
            declaration_id=declaration_id,
            chunks_count=len(chunks),
            indexed_at=datetime.utcnow(),
            status="success",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при индексации: {str(e)}")
