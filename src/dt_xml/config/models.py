"""Модели конфигурации для различных компонентов системы."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DeclarationType(str, Enum):
    """Типы таможенных деклараций."""

    IMPORT = "import"
    EXPORT = "export"
    TRANSIT = "transit"


class DeclarationStatus(str, Enum):
    """Статусы декларации."""

    REGISTERED = "registered"
    RELEASED = "released"
    REJECTED = "rejected"
    CORRECTED = "corrected"


class DeclarationMetadata(BaseModel):
    """Метаданные декларации."""

    declaration_number: str
    date_issued: datetime
    declaration_type: DeclarationType
    status: DeclarationStatus
    manufacturer: str | None = None
    importer: str | None = None
    exporter: str | None = None
    product_code: str | None = None  # ТН ВЭД код
    country_origin: str | None = None
    customs_value: float | None = None
    currency: str | None = None
    quantity: float | None = None
    unit_of_measure: str | None = None
    language: str = "ru"
    version: str = "1.0"
    source: str | None = None
    processed_at: datetime | None = None

    class Config:
        """Конфигурация модели."""

        json_encoders = {datetime: lambda v: v.isoformat()}


class DeclarationChunk(BaseModel):
    """Чанк декларации."""

    chunk_id: str
    declaration_id: str
    content: str
    section: str | None = None
    chunk_index: int
    metadata: dict[str, Any] = Field(default_factory=dict)
    embedding: list[float] | None = None


class SearchQuery(BaseModel):
    """Запрос поиска."""

    query: str
    top_k: int = 10
    filters: dict[str, Any] = Field(default_factory=dict)
    rerank: bool = True
    explain: bool = True


class SearchResult(BaseModel):
    """Результат поиска."""

    declaration_id: str
    score: float
    chunk_id: str | None = None
    content: str
    metadata: DeclarationMetadata
    explanation: dict[str, Any] | None = None
    matched_fields: list[str] = Field(default_factory=list)


class SearchResponse(BaseModel):
    """Ответ на запрос поиска."""

    results: list[SearchResult]
    total: int
    query_time_ms: float
    query: str
