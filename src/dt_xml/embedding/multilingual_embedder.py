"""Многоязычный эмбеддер для генерации эмбедингов."""

import logging
from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer

from dt_xml.config.settings import get_settings
from dt_xml.embedding.models import EmbeddingModelConfig

logger = logging.getLogger(__name__)


class MultilingualEmbedder:
    """Многоязычный эмбеддер для генерации эмбедингов текстов."""

    def __init__(self, config: EmbeddingModelConfig | None = None):
        """Инициализация эмбеддера.

        Args:
            config: Конфигурация модели. Если None, используется конфигурация из настроек.
        """
        self.config = config or EmbeddingModelConfig()
        self.model: SentenceTransformer | None = None
        self._load_model()

    def _load_model(self) -> None:
        """Загрузка модели эмбедингов."""
        try:
            logger.info(f"Загрузка модели эмбедингов: {self.config.model_name}")
            self.model = SentenceTransformer(
                self.config.model_name,
                device=self.config.device,
            )
            logger.info("Модель эмбедингов загружена успешно")
        except Exception as e:
            logger.error(f"Ошибка при загрузке модели эмбедингов: {e}")
            raise

    def embed(self, texts: str | list[str]) -> np.ndarray | list[np.ndarray]:
        """Генерация эмбедингов для текста или списка текстов.

        Args:
            texts: Текст или список текстов для эмбединга.

        Returns:
            Массив эмбедингов или список массивов.
        """
        if self.model is None:
            raise RuntimeError("Модель не загружена")

        # Нормализация входных данных
        if isinstance(texts, str):
            texts = [texts]
            single_text = True
        else:
            single_text = False

        if not texts:
            return [] if not single_text else np.array([])

        try:
            # Генерация эмбедингов
            embeddings = self.model.encode(
                texts,
                batch_size=self.config.batch_size,
                show_progress_bar=False,
                normalize_embeddings=self.config.normalize_embeddings,
                max_length=self.config.max_length,
            )

            # Преобразование в numpy array
            if isinstance(embeddings, list):
                embeddings = np.array(embeddings)
            elif not isinstance(embeddings, np.ndarray):
                embeddings = np.array(embeddings)

            # Возврат одного эмбединга для одного текста
            if single_text:
                return embeddings[0] if len(embeddings) > 0 else np.array([])

            return embeddings

        except Exception as e:
            logger.error(f"Ошибка при генерации эмбедингов: {e}")
            raise

    def embed_batch(self, texts: list[str], batch_size: int | None = None) -> list[np.ndarray]:
        """Генерация эмбедингов для батча текстов.

        Args:
            texts: Список текстов для эмбединга.
            batch_size: Размер батча. Если None, используется из конфигурации.

        Returns:
            Список массивов эмбедингов.
        """
        if not texts:
            return []

        batch_size = batch_size or self.config.batch_size
        embeddings_list: list[np.ndarray] = []

        # Обработка батчами
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            batch_embeddings = self.embed(batch)

            if isinstance(batch_embeddings, np.ndarray):
                # Разделяем на отдельные эмбединги
                for j in range(len(batch)):
                    embeddings_list.append(batch_embeddings[j])
            else:
                embeddings_list.extend(batch_embeddings)

        return embeddings_list

    def get_embedding_dimension(self) -> int:
        """Получение размерности эмбедингов.

        Returns:
            Размерность эмбедингов.
        """
        if self.model is None:
            raise RuntimeError("Модель не загружена")

        # Получаем размерность из модели
        return self.model.get_sentence_embedding_dimension()

    def get_model_info(self) -> dict[str, Any]:
        """Получение информации о модели.

        Returns:
            Словарь с информацией о модели.
        """
        return {
            "model_name": self.config.model_name,
            "device": self.config.device,
            "embedding_dimension": self.get_embedding_dimension() if self.model else None,
            "max_length": self.config.max_length,
            "normalize_embeddings": self.config.normalize_embeddings,
        }
