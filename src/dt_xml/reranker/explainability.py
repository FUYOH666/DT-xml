"""Объяснимость результатов поиска."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class Explainability:
    """Генерация объяснений релевантности результатов."""

    def __init__(self):
        """Инициализация модуля объяснимости."""
        pass

    def explain(
        self,
        query: str,
        result: dict[str, Any],
    ) -> dict[str, Any]:
        """Генерация объяснения релевантности результата.

        Args:
            query: Текст запроса.
            result: Результат поиска.

        Returns:
            Словарь с объяснением релевантности.
        """
        explanation: dict[str, Any] = {
            "relevance_score": result.get("score", 0.0),
            "matched_fields": [],
            "matched_terms": [],
            "reasons": [],
        }

        # Анализ совпадений по полям
        metadata = result.get("metadata", {})
        query_lower = query.lower()

        # Проверка совпадений в различных полях
        field_matches = {
            "manufacturer": metadata.get("manufacturer", ""),
            "importer": metadata.get("importer", ""),
            "product_code": metadata.get("product_code", ""),
            "country_origin": metadata.get("country_origin", ""),
            "content": result.get("content", ""),
        }

        for field, value in field_matches.items():
            if value and query_lower in str(value).lower():
                explanation["matched_fields"].append(field)
                explanation["reasons"].append(f"Совпадение в поле '{field}'")

        # Извлечение совпадающих терминов
        query_terms = query_lower.split()
        content_lower = str(result.get("content", "")).lower()

        matched_terms = [term for term in query_terms if term in content_lower]
        explanation["matched_terms"] = matched_terms

        if matched_terms:
            explanation["reasons"].append(f"Найдены совпадающие термины: {', '.join(matched_terms[:5])}")

        # Анализ скоров
        if "dense_score" in result:
            explanation["dense_score"] = result["dense_score"]
            explanation["reasons"].append("Высокий семантический скор")

        if "sparse_score" in result:
            explanation["sparse_score"] = result["sparse_score"]
            explanation["reasons"].append("Высокий скор по ключевым словам")

        if "rrf_score" in result:
            explanation["hybrid_score"] = result["rrf_score"]
            explanation["reasons"].append("Комбинированный скор (гибридный поиск)")

        return explanation
