"""Анализ сложности запроса."""

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


class QueryComplexityAnalyzer:
    """Анализатор сложности запроса."""

    def __init__(self):
        """Инициализация анализатора."""
        # Паттерны для определения сложных запросов
        self.complex_patterns = [
            re.compile(r"\b(и|and|или|or)\b", re.IGNORECASE),  # Логические операторы
            re.compile(r"\b(не|not|кроме|except)\b", re.IGNORECASE),  # Отрицания
            re.compile(r"\b(до|after|после|before|между|between)\b", re.IGNORECASE),  # Временные операторы
            re.compile(r"\d{4}", re.IGNORECASE),  # Годы
            re.compile(r"\b(более|менее|больше|меньше|>|<|>=|<=)\b", re.IGNORECASE),  # Сравнения
        ]

    def analyze(self, query: str) -> float:
        """Анализ сложности запроса.

        Args:
            query: Текст запроса.

        Returns:
            Оценка сложности от 0.0 (простой) до 1.0 (сложный).
        """
        if not query or not query.strip():
            return 0.0

        complexity_score = 0.0

        # Длина запроса
        query_length = len(query.split())
        if query_length > 10:
            complexity_score += 0.2
        elif query_length > 5:
            complexity_score += 0.1

        # Наличие сложных паттернов
        pattern_matches = sum(1 for pattern in self.complex_patterns if pattern.search(query))
        complexity_score += min(pattern_matches * 0.15, 0.6)

        # Наличие чисел и дат
        if re.search(r"\d", query):
            complexity_score += 0.1

        # Наличие специальных символов
        special_chars = len(re.findall(r"[^\w\s]", query))
        if special_chars > 3:
            complexity_score += 0.1

        return min(complexity_score, 1.0)
