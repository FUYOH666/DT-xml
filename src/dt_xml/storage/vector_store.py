"""Интерфейс к векторной базе данных."""

import logging
from typing import Any

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from dt_xml.config.models import DeclarationChunk
from dt_xml.config.settings import get_settings

logger = logging.getLogger(__name__)


class VectorStore:
    """Хранилище векторов для эмбедингов."""

    def __init__(self):
        """Инициализация хранилища векторов."""
        self.settings = get_settings()
        self.client: QdrantClient | None = None
        self.collection_name = self.settings.vector_db.collection_name
        self.vector_size = self.settings.vector_db.vector_size
        self._connect()

    def _connect(self) -> None:
        """Подключение к векторной базе данных."""
        try:
            self.client = QdrantClient(
                host=self.settings.vector_db.host,
                port=self.settings.vector_db.port,
                grpc_port=self.settings.vector_db.grpc_port,
            )
            logger.info("Подключение к Qdrant установлено")
            self._ensure_collection()
        except Exception as e:
            logger.error(f"Ошибка при подключении к Qdrant: {e}")
            raise

    def _ensure_collection(self) -> None:
        """Создание коллекции, если она не существует."""
        if self.client is None:
            raise RuntimeError("Клиент Qdrant не инициализирован")

        try:
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]

            if self.collection_name not in collection_names:
                logger.info(f"Создание коллекции {self.collection_name}")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE,
                    ),
                )
                logger.info(f"Коллекция {self.collection_name} создана")
            else:
                logger.info(f"Коллекция {self.collection_name} уже существует")
        except Exception as e:
            logger.error(f"Ошибка при создании коллекции: {e}")
            raise

    def add_chunks(
        self,
        chunks: list[DeclarationChunk],
        embeddings: list[np.ndarray],
    ) -> None:
        """Добавление чанков с эмбедингами в хранилище.

        Args:
            chunks: Список чанков деклараций.
            embeddings: Список эмбедингов для чанков.
        """
        if self.client is None:
            raise RuntimeError("Клиент Qdrant не инициализирован")

        if len(chunks) != len(embeddings):
            raise ValueError("Количество чанков и эмбедингов должно совпадать")

        try:
            points = []
            for chunk, embedding in zip(chunks, embeddings):
                # Преобразование numpy array в список
                if isinstance(embedding, np.ndarray):
                    embedding_list = embedding.tolist()
                else:
                    embedding_list = list(embedding)

                # Подготовка метаданных
                payload = {
                    "declaration_id": chunk.declaration_id,
                    "chunk_id": chunk.chunk_id,
                    "content": chunk.content,
                    "section": chunk.section,
                    "chunk_index": chunk.chunk_index,
                    **chunk.metadata,
                }

                point = PointStruct(
                    id=hash(chunk.chunk_id) % (2**63),  # Qdrant требует int64 ID
                    vector=embedding_list,
                    payload=payload,
                )
                points.append(point)

            # Вставка точек батчами
            batch_size = 100
            for i in range(0, len(points), batch_size):
                batch = points[i : i + batch_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch,
                )

            logger.info(f"Добавлено {len(chunks)} чанков в векторное хранилище")

        except Exception as e:
            logger.error(f"Ошибка при добавлении чанков: {e}")
            raise

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Поиск похожих векторов.

        Args:
            query_embedding: Эмбединг запроса.
            top_k: Количество результатов.
            filters: Фильтры по метаданным.

        Returns:
            Список результатов поиска с метаданными.
        """
        if self.client is None:
            raise RuntimeError("Клиент Qdrant не инициализирован")

        try:
            # Преобразование numpy array в список
            if isinstance(query_embedding, np.ndarray):
                query_vector = query_embedding.tolist()
            else:
                query_vector = list(query_embedding)

            # Построение фильтров для Qdrant
            qdrant_filter = None
            if filters:
                from qdrant_client.models import Filter, FieldCondition, MatchValue

                conditions = []
                for key, value in filters.items():
                    conditions.append(
                        FieldCondition(
                            key=f"payload.{key}",
                            match=MatchValue(value=value),
                        )
                    )

                if conditions:
                    qdrant_filter = Filter(must=conditions)

            # Поиск
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                query_filter=qdrant_filter,
            )

            # Преобразование результатов
            results = []
            for result in search_results:
                results.append(
                    {
                        "chunk_id": result.payload.get("chunk_id"),
                        "declaration_id": result.payload.get("declaration_id"),
                        "content": result.payload.get("content"),
                        "section": result.payload.get("section"),
                        "score": result.score,
                        "metadata": {k: v for k, v in result.payload.items() if k not in ["content"]},
                    }
                )

            return results

        except Exception as e:
            logger.error(f"Ошибка при поиске: {e}")
            raise

    def delete_by_declaration_id(self, declaration_id: str) -> None:
        """Удаление всех чанков декларации.

        Args:
            declaration_id: Идентификатор декларации.
        """
        if self.client is None:
            raise RuntimeError("Клиент Qdrant не инициализирован")

        try:
            from qdrant_client.models import Filter, FieldCondition, MatchValue

            # Поиск всех точек с данным declaration_id
            search_results = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="payload.declaration_id",
                            match=MatchValue(value=declaration_id),
                        )
                    ]
                ),
                limit=10000,
            )

            # Удаление найденных точек
            if search_results[0]:
                point_ids = [point.id for point in search_results[0]]
                if point_ids:
                    self.client.delete(
                        collection_name=self.collection_name,
                        points_selector=point_ids,
                    )
                    logger.info(f"Удалено {len(point_ids)} чанков для декларации {declaration_id}")

        except Exception as e:
            logger.error(f"Ошибка при удалении чанков: {e}")
            raise

    def get_collection_info(self) -> dict[str, Any]:
        """Получение информации о коллекции.

        Returns:
            Словарь с информацией о коллекции.
        """
        if self.client is None:
            raise RuntimeError("Клиент Qdrant не инициализирован")

        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                "name": collection_info.name,
                "vectors_count": collection_info.points_count,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance.name,
            }
        except Exception as e:
            logger.error(f"Ошибка при получении информации о коллекции: {e}")
            return {}
