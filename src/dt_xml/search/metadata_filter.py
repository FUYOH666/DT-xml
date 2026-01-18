"""Фильтрация результатов по метаданным."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class MetadataFilter:
    """Фильтрация результатов поиска по метаданным."""

    def filter_results(
        self,
        results: list[dict[str, Any]],
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Фильтрация результатов по метаданным.

        Args:
            results: Список результатов поиска.
            filters: Словарь фильтров.

        Returns:
            Отфильтрованный список результатов.
        """
        filtered_results = []

        for result in results:
            if self._matches_filters(result, filters):
                filtered_results.append(result)

        return filtered_results

    def _matches_filters(self, result: dict[str, Any], filters: dict[str, Any]) -> bool:
        """Проверка соответствия результата фильтрам.

        Args:
            result: Результат поиска.
            filters: Словарь фильтров.

        Returns:
            True если результат соответствует фильтрам.
        """
        metadata = result.get("metadata", {})

        for key, value in filters.items():
            if key not in metadata:
                continue

            result_value = metadata[key]

            # Поддержка различных типов фильтров
            if isinstance(value, dict):
                # Диапазоны и операторы
                if "gte" in value and result_value < value["gte"]:
                    return False
                if "lte" in value and result_value > value["lte"]:
                    return False
                if "gt" in value and result_value <= value["gt"]:
                    return False
                if "lt" in value and result_value >= value["lt"]:
                    return False
                if "eq" in value and result_value != value["eq"]:
                    return False
            elif isinstance(value, list):
                # Список допустимых значений
                if result_value not in value:
                    return False
            else:
                # Точное совпадение
                if result_value != value:
                    return False

        return True
