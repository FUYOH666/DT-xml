"""Настройки приложения с использованием pydantic-settings."""

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict, YamlConfigSettingsSource


class DatabaseSettings(BaseSettings):
    """Настройки базы данных PostgreSQL."""

    host: str = "localhost"
    port: int = 5432
    database: str = "dt_xml"
    user: str = "dt_xml_user"
    password: str = Field(default="", validation_alias="POSTGRES_PASSWORD")
    pool_size: int = 10
    max_overflow: int = 20

    @property
    def url(self) -> str:
        """URL подключения к базе данных."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class VectorDBSettings(BaseSettings):
    """Настройки векторной базы данных."""

    type: str = "qdrant"
    host: str = "localhost"
    port: int = 6333
    grpc_port: int = 6334
    collection_name: str = "declarations"
    vector_size: int = 1024


class EmbeddingSettings(BaseSettings):
    """Настройки модели эмбедингов."""

    model_name: str = "BAAI/bge-m3"
    device: str = "cpu"
    batch_size: int = 32
    max_length: int = 8192
    normalize_embeddings: bool = True


class RerankerSettings(BaseSettings):
    """Настройки реранкера."""

    model_name: str = "BAAI/bge-reranker-v2-m3"
    device: str = "cpu"
    batch_size: int = 16
    top_k: int = 100
    adaptive: dict[str, Any] = Field(
        default_factory=lambda: {
            "enabled": True,
            "complexity_threshold": 0.7,
            "simple_model": "BAAI/bge-reranker-base",
            "complex_model": "BAAI/bge-reranker-v2-m3",
        }
    )


class SearchSettings(BaseSettings):
    """Настройки поиска."""

    top_k: int = 50
    rerank_top_k: int = 10
    hybrid_alpha: float = 0.5
    sparse: dict[str, Any] = Field(
        default_factory=lambda: {"enabled": True, "k1": 1.5, "b": 0.75}
    )
    dense: dict[str, Any] = Field(
        default_factory=lambda: {"enabled": True, "similarity_threshold": 0.0}
    )
    metadata_filters: dict[str, Any] = Field(
        default_factory=lambda: {
            "enabled": True,
            "fields": [
                "declaration_number",
                "date_issued",
                "manufacturer",
                "importer",
                "product_code",
                "country_origin",
            ],
        }
    )


class ChunkingSettings(BaseSettings):
    """Настройки чанкования."""

    strategy: str = "semantic"
    chunk_size: int = 512
    chunk_overlap: int = 50
    min_chunk_size: int = 100
    preserve_structure: bool = True


class NormalizationSettings(BaseSettings):
    """Настройки нормализации."""

    language_detection: bool = True
    field_normalization: bool = True
    code_normalization: bool = True
    temporal_normalization: bool = True


class TemporalSettings(BaseSettings):
    """Настройки временной осведомленности."""

    enabled: bool = True
    rule_versioning: bool = True
    date_awareness: bool = True


class ExplainabilitySettings(BaseSettings):
    """Настройки объяснимости."""

    enabled: bool = True
    show_scores: bool = True
    show_matched_fields: bool = True
    show_temporal_context: bool = True


class APISettings(BaseSettings):
    """Настройки API."""

    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    workers: int = 1
    cors_enabled: bool = True
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])


class LoggingSettings(BaseSettings):
    """Настройки логирования."""

    level: str = "INFO"
    format: str = "json"
    file: str | None = None


class Settings(BaseSettings):
    """Основные настройки приложения."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
        yaml_file="config/config.yaml",
    )

    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    vector_db: VectorDBSettings = Field(default_factory=VectorDBSettings)
    embedding: EmbeddingSettings = Field(default_factory=EmbeddingSettings)
    reranker: RerankerSettings = Field(default_factory=RerankerSettings)
    search: SearchSettings = Field(default_factory=SearchSettings)
    chunking: ChunkingSettings = Field(default_factory=ChunkingSettings)
    normalization: NormalizationSettings = Field(default_factory=NormalizationSettings)
    temporal: TemporalSettings = Field(default_factory=TemporalSettings)
    explainability: ExplainabilitySettings = Field(default_factory=ExplainabilitySettings)
    api: APISettings = Field(default_factory=APISettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    environment: str = "local"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: Any,
        env_settings: Any,
        dotenv_settings: Any,
        file_secret_settings: Any,
    ) -> tuple[Any, ...]:
        """Кастомизация источников настроек."""
        config_file = Path("config/config.yaml")
        if config_file.exists():
            return (
                init_settings,
                YamlConfigSettingsSource(settings_cls, yaml_file=config_file),
                env_settings,
                dotenv_settings,
                file_secret_settings,
            )
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


@lru_cache()
def get_settings() -> Settings:
    """Получить настройки приложения (singleton)."""
    return Settings()
