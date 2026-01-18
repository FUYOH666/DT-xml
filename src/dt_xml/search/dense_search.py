"""Векторный поиск по эмбедингам."""

import logging
from typing import Any

import numpy as np

from dt_xml.embedding.multilingual_embedder import MultilingualEmbedder
from dt_xml.search.metadata_filter import MetadataFilter
from dt_xml.storage.vector_store import VectorStore

logger = logging.getLogger(__name__)


class DenseSearch:
    """Векторный поиск по эмбедингам."""

    def __init__(self, embedder: MultilingualEmbedder | None = None):
        """Инициализация векторного поиска.

        Args:
            embedder: Эмбеддер для генерации эмбедингов запросов.
        """
        self.vector_store = VectorStore()
        self.embedder = embedder or MultilingualEmbedder()
        self.metadata_filter = MetadataFilter()

    def search(
        self,
        query: str,
        top_k: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Векторный поиск по запросу.

        Args:
            query: Текст запроса.
            top_k: Количество результатов.
            filters: Фильтры по метаданным.

        Returns:
            Список результатов поиска.
        """
        try:
            # Генерация эмбединга запроса
            query_embedding = self.embedder.embed(query)

            if isinstance(query_embedding, list):
                query_embedding = np.array(query_embedding)

            # Поиск в векторной БД
            results = self.vector_store.search(
                query_embedding=query_embedding,
                top_k=top_k,
                filters=filters,
            )

            # Применение дополнительных фильтров, если нужно
            if filters:
                results = self.metadata_filter.filter_results(results, filters)

            return results

        except Exception as e:
            logger.error(f"Ошибка при векторном поиске: {e}")
            return []
