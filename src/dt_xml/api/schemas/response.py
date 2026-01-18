"""Схемы ответов API."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class SearchResultResponse(BaseModel):
    """Результат поиска."""

    declaration_id: str
    chunk_id: str | None = None
    content: str
    score: float
    metadata: dict[str, Any] = Field(default_factory=dict)
    explanation: dict[str, Any] | None = None
    matched_fields: list[str] = Field(default_factory=list)


class SearchResponse(BaseModel):
    """Ответ на запрос поиска."""

    results: list[SearchResultResponse]
    total: int
    query_time_ms: float
    query: str


class IndexResponse(BaseModel):
    """Ответ на запрос индексации."""

    declaration_id: str
    chunks_count: int
    indexed_at: datetime
    status: str = "success"


class HealthResponse(BaseModel):
    """Ответ health check."""

    status: str
    vector_db: dict[str, Any] = Field(default_factory=dict)
    metadata_db: dict[str, Any] = Field(default_factory=dict)
    embedding_model: dict[str, Any] = Field(default_factory=dict)
