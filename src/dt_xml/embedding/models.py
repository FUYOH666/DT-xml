"""Конфигурация моделей эмбедингов."""

from typing import Any

from dt_xml.config.settings import get_settings

settings = get_settings()


class EmbeddingModelConfig:
    """Конфигурация модели эмбедингов."""

    def __init__(self):
        """Инициализация конфигурации."""
        self.model_name = settings.embedding.model_name
        self.device = settings.embedding.device
        self.batch_size = settings.embedding.batch_size
        self.max_length = settings.embedding.max_length
        self.normalize_embeddings = settings.embedding.normalize_embeddings

    def to_dict(self) -> dict[str, Any]:
        """Преобразование в словарь.

        Returns:
            Словарь с конфигурацией.
        """
        return {
            "model_name": self.model_name,
            "device": self.device,
            "batch_size": self.batch_size,
            "max_length": self.max_length,
            "normalize_embeddings": self.normalize_embeddings,
        }
