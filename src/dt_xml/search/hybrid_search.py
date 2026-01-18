"""Гибридный поиск (sparse + dense)."""

import logging
from typing import Any

from dt_xml.config.settings import get_settings
from dt_xml.search.dense_search import DenseSearch
from dt_xml.search.sparse_search import SparseSearch

logger = logging.getLogger(__name__)


class HybridSearch:
    """Гибридный поиск, объединяющий sparse и dense результаты."""

    def __init__(self):
        """Инициализация гибридного поиска."""
        self.settings = get_settings()
        self.sparse_search = SparseSearch()
        self.dense_search = DenseSearch()
        self.alpha = self.settings.search.hybrid_alpha

    def search(
        self,
        query: str,
        top_k: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Гибридный поиск по запросу.

        Args:
            query: Текст запроса.
            top_k: Количество результатов.
            filters: Фильтры по метаданным.

        Returns:
            Список результатов с объединенными скорами.
        """
        # Dense поиск
        dense_results = self.dense_search.search(query, top_k=top_k * 2, filters=filters)

        # Sparse поиск (если есть индексированные документы)
        sparse_results = []
        if self.sparse_search.bm25 is not None:
            sparse_results = self.sparse_search.search(query, top_k=top_k * 2)

        # Объединение результатов через RRF (Reciprocal Rank Fusion)
        combined_results = self._rrf_fusion(dense_results, sparse_results, top_k)

        return combined_results

    def _rrf_fusion(
        self,
        dense_results: list[dict[str, Any]],
        sparse_results: list[dict[str, Any]],
        top_k: int,
        k: int = 60,
    ) -> list[dict[str, Any]]:
        """Объединение результатов через Reciprocal Rank Fusion.

        Args:
            dense_results: Результаты dense поиска.
            sparse_results: Результаты sparse поиска.
            top_k: Количество финальных результатов.
            k: Параметр RRF (обычно 60).

        Returns:
            Объединенный список результатов.
        """
        # Создание словаря для объединения
        combined_scores: dict[str, dict[str, Any]] = {}

        # Обработка dense результатов
        for rank, result in enumerate(dense_results, start=1):
            chunk_id = result.get("chunk_id") or result.get("document_id")
            if chunk_id:
                rrf_score = 1.0 / (k + rank)
                if chunk_id not in combined_scores:
                    combined_scores[chunk_id] = {
                        **result,
                        "dense_score": result.get("score", 0.0),
                        "sparse_score": 0.0,
                        "rrf_score": rrf_score * self.alpha,
                    }
                else:
                    combined_scores[chunk_id]["rrf_score"] += rrf_score * self.alpha
                    combined_scores[chunk_id]["dense_score"] = result.get("score", 0.0)

        # Обработка sparse результатов
        for rank, result in enumerate(sparse_results, start=1):
            chunk_id = result.get("chunk_id") or result.get("document_id")
            if chunk_id:
                rrf_score = 1.0 / (k + rank)
                if chunk_id not in combined_scores:
                    combined_scores[chunk_id] = {
                        **result,
                        "dense_score": 0.0,
                        "sparse_score": result.get("score", 0.0),
                        "rrf_score": rrf_score * (1 - self.alpha),
                    }
                else:
                    combined_scores[chunk_id]["rrf_score"] += rrf_score * (1 - self.alpha)
                    combined_scores[chunk_id]["sparse_score"] = result.get("score", 0.0)

        # Сортировка по RRF скору
        sorted_results = sorted(
            combined_scores.values(),
            key=lambda x: x["rrf_score"],
            reverse=True,
        )[:top_k]

        return sorted_results
