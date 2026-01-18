"""BM25/keyword поиск."""

import logging
from typing import Any

from rank_bm25 import BM25Okapi

from dt_xml.config.settings import get_settings

logger = logging.getLogger(__name__)


class SparseSearch:
    """BM25 поиск по ключевым словам."""

    def __init__(self):
        """Инициализация BM25 поиска."""
        self.settings = get_settings()
        self.bm25: BM25Okapi | None = None
        self.documents: list[str] = []
        self.document_metadata: list[dict[str, Any]] = []

    def index_documents(self, documents: list[str], metadata: list[dict[str, Any]] | None = None) -> None:
        """Индексация документов для BM25 поиска.

        Args:
            documents: Список текстов документов.
            metadata: Список метаданных для каждого документа.
        """
        if len(documents) == 0:
            logger.warning("Пустой список документов для индексации")
            return

        self.documents = documents
        self.document_metadata = metadata or [{}] * len(documents)

        # Токенизация документов
        tokenized_docs = [doc.lower().split() for doc in documents]

        # Создание BM25 индекса
        self.bm25 = BM25Okapi(
            tokenized_docs,
            k1=self.settings.search.sparse.get("k1", 1.5),
            b=self.settings.search.sparse.get("b", 0.75),
        )

        logger.info(f"Индексировано {len(documents)} документов для BM25 поиска")

    def search(self, query: str, top_k: int = 10) -> list[dict[str, Any]]:
        """Поиск по запросу.

        Args:
            query: Текст запроса.
            top_k: Количество результатов.

        Returns:
            Список результатов с метаданными и скором.
        """
        if self.bm25 is None or len(self.documents) == 0:
            logger.warning("Индекс BM25 не создан или пуст")
            return []

        # Токенизация запроса
        tokenized_query = query.lower().split()

        # Поиск
        scores = self.bm25.get_scores(tokenized_query)

        # Сортировка по убыванию скора
        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )[:top_k]

        # Формирование результатов
        results = []
        for idx in top_indices:
            results.append(
                {
                    "document_id": idx,
                    "content": self.documents[idx],
                    "score": float(scores[idx]),
                    "metadata": self.document_metadata[idx],
                }
            )

        return results
