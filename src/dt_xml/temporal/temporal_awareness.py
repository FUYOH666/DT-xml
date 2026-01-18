"""Временная осведомленность при поиске."""

import logging
from datetime import datetime
from typing import Any

from dt_xml.temporal.rule_versioning import RuleVersioning

logger = logging.getLogger(__name__)


class TemporalAwareness:
    """Учет временных изменений при поиске и ранжировании."""

    def __init__(self):
        """Инициализация временной осведомленности."""
        self.rule_versioning = RuleVersioning()

    def adjust_score_by_date(
        self,
        result: dict[str, Any],
        query_date: datetime | None = None,
    ) -> float:
        """Корректировка скора с учетом временных факторов.

        Args:
            result: Результат поиска.
            query_date: Дата запроса (если указана).

        Returns:
            Скорректированный скор.
        """
        base_score = result.get("score", 0.0)

        # Получение даты декларации из метаданных
        metadata = result.get("metadata", {})
        declaration_date = metadata.get("date_issued")

        if not declaration_date:
            return base_score

        # Преобразование строки в datetime, если нужно
        if isinstance(declaration_date, str):
            try:
                declaration_date = datetime.fromisoformat(declaration_date.replace("Z", "+00:00"))
            except Exception:
                return base_score

        # Если указана дата запроса, учитываем близость дат
        if query_date:
            date_diff = abs((query_date - declaration_date).days)

            # Бонус за близость дат (чем ближе, тем выше скор)
            if date_diff < 365:  # В пределах года
                temporal_bonus = 0.1 * (1 - date_diff / 365)
                base_score += temporal_bonus

        # Учет версии правил
        rule_version = self.rule_versioning.get_rule_version(declaration_date)
        if rule_version:
            metadata["rule_version"] = rule_version

        return base_score

    def add_temporal_context(self, result: dict[str, Any]) -> dict[str, Any]:
        """Добавление временного контекста к результату.

        Args:
            result: Результат поиска.

        Returns:
            Результат с добавленным временным контекстом.
        """
        metadata = result.get("metadata", {})
        declaration_date = metadata.get("date_issued")

        if declaration_date:
            if isinstance(declaration_date, str):
                try:
                    declaration_date = datetime.fromisoformat(declaration_date.replace("Z", "+00:00"))
                except Exception:
                    declaration_date = None

            if declaration_date:
                rule_version = self.rule_versioning.get_rule_version(declaration_date)
                metadata["rule_version"] = rule_version
                metadata["temporal_context"] = {
                    "declaration_date": declaration_date.isoformat(),
                    "rule_version": rule_version,
                    "years_ago": (datetime.now() - declaration_date).days / 365.0,
                }

        result["metadata"] = metadata
        return result
