"""Схемы запросов для API."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """Запрос на поиск."""

    query: str = Field(..., description="Текст запроса для поиска")
    tenant_id: str = Field(default="default", description="Идентификатор заказчика")
    top_k: int = Field(default=10, ge=1, le=100, description="Количество результатов")
    filters: dict[str, Any] = Field(
        default_factory=dict,
        description="Фильтры по метаданным (manufacturer, date_issued, product_code и т.д.)",
    )
    rerank: bool = Field(default=True, description="Применять ли реранкинг")
    explain: bool = Field(default=True, description="Включать ли объяснения релевантности")


class IndexRequest(BaseModel):
    """Запрос на индексацию декларации."""

    declaration_id: str | None = Field(None, description="Идентификатор декларации (опционально)")
    tenant_id: str = Field(default="default", description="Идентификатор заказчика")
    xml_content: str | None = Field(None, description="XML содержимое декларации")
    json_data: dict[str, Any] | None = Field(None, description="JSON данные декларации")
    ocr_text: str | None = Field(None, description="OCR текст (неструктурированный)")


class SchemaRegistrationRequest(BaseModel):
    """Запрос на регистрацию схемы заказчика."""

    tenant_id: str = Field(..., description="Идентификатор заказчика")
    tenant_name: str = Field(..., description="Название заказчика")
    schema: dict[str, Any] = Field(..., description="Конфигурация схемы")
    processing: dict[str, Any] = Field(default_factory=dict, description="Настройки обработки")
    search: dict[str, Any] = Field(default_factory=dict, description="Настройки поиска")


class FilterRequest(BaseModel):
    """Фильтры для поиска."""

    manufacturer: str | None = None
    importer: str | None = None
    exporter: str | None = None
    product_code: str | None = None
    country_origin: str | None = None
    date_issued_from: datetime | None = None
    date_issued_to: datetime | None = None
