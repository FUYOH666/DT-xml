"""Адаптивный реранкер."""

import logging
from typing import Any

from sentence_transformers import CrossEncoder

from dt_xml.config.settings import get_settings
from dt_xml.reranker.query_complexity import QueryComplexityAnalyzer

logger = logging.getLogger(__name__)


class AdaptiveReranker:
    """Адаптивный реранкер с выбором модели в зависимости от сложности запроса."""

    def __init__(self):
        """Инициализация адаптивного реранкера."""
        self.settings = get_settings()
        self.complexity_analyzer = QueryComplexityAnalyzer()
        self.simple_model: CrossEncoder | None = None
        self.complex_model: CrossEncoder | None = None
        self._load_models()

    def _load_models(self) -> None:
        """Загрузка моделей реранкера."""
        try:
            if self.settings.reranker.adaptive["enabled"]:
                simple_model_name = self.settings.reranker.adaptive["simple_model"]
                complex_model_name = self.settings.reranker.adaptive["complex_model"]

                logger.info(f"Загрузка простой модели реранкера: {simple_model_name}")
                self.simple_model = CrossEncoder(simple_model_name)

                logger.info(f"Загрузка сложной модели реранкера: {complex_model_name}")
                self.complex_model = CrossEncoder(complex_model_name)

                logger.info("Модели реранкера загружены")
            else:
                # Использование базовой модели
                logger.info(f"Загрузка базовой модели реранкера: {self.settings.reranker.model_name}")
                self.simple_model = CrossEncoder(self.settings.reranker.model_name)

        except Exception as e:
            logger.error(f"Ошибка при загрузке моделей реранкера: {e}")
            raise

    def rerank(
        self,
        query: str,
        documents: list[str],
        top_k: int | None = None,
    ) -> list[dict[str, Any]]:
        """Реранкинг документов по запросу.

        Args:
            query: Текст запроса.
            documents: Список текстов документов для реранкинга.
            top_k: Количество топ результатов. Если None, используется из настроек.

        Returns:
            Список реранкированных документов с скорами.
        """
        if not documents:
            return []

        top_k = top_k or self.settings.reranker.top_k

        # Определение сложности запроса
        complexity = self.complexity_analyzer.analyze(query)

        # Выбор модели
        model = self._select_model(complexity)

        try:
            # Подготовка пар (query, document)
            pairs = [[query, doc] for doc in documents]

            # Получение скоров от модели
            scores = model.predict(pairs)

            # Объединение документов и скоров
            results = [
                {
                    "document": doc,
                    "score": float(score),
                    "complexity": complexity,
                    "model_used": "simple" if model == self.simple_model else "complex",
                }
                for doc, score in zip(documents, scores)
            ]

            # Сортировка по убыванию скора
            results.sort(key=lambda x: x["score"], reverse=True)

            return results[:top_k]

        except Exception as e:
            logger.error(f"Ошибка при реранкинге: {e}")
            return []

    def _select_model(self, complexity: float) -> CrossEncoder:
        """Выбор модели в зависимости от сложности запроса.

        Args:
            complexity: Оценка сложности запроса (0.0 - 1.0).

        Returns:
            Выбранная модель реранкера.
        """
        threshold = self.settings.reranker.adaptive.get("complexity_threshold", 0.7)

        if complexity >= threshold and self.complex_model is not None:
            return self.complex_model
        else:
            if self.simple_model is None:
                raise RuntimeError("Простая модель реранкера не загружена")
            return self.simple_model
