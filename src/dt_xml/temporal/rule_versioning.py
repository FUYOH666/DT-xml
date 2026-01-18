"""Версионирование правил ЕАЭС."""

import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class RuleVersioning:
    """Управление версиями правил ЕАЭС."""

    def __init__(self):
        """Инициализация версионирования правил."""
        # Примеры версий правил (в реальной реализации загружаются из БД или конфига)
        self.rule_versions: list[dict[str, Any]] = [
            {
                "version": "2020-01-01",
                "description": "Базовая версия правил ЕАЭС 2020",
                "effective_from": datetime(2020, 1, 1),
            },
            {
                "version": "2021-07-01",
                "description": "Обновление правил ЕАЭС 2021",
                "effective_from": datetime(2021, 7, 1),
            },
            {
                "version": "2023-01-01",
                "description": "Обновление правил ЕАЭС 2023",
                "effective_from": datetime(2023, 1, 1),
            },
        ]

    def get_rule_version(self, date: datetime) -> str:
        """Получение версии правил для указанной даты.

        Args:
            date: Дата для определения версии правил.

        Returns:
            Версия правил.
        """
        # Поиск актуальной версии правил на указанную дату
        for rule_version in sorted(
            self.rule_versions,
            key=lambda x: x["effective_from"],
            reverse=True,
        ):
            if date >= rule_version["effective_from"]:
                return rule_version["version"]

        # Возврат самой ранней версии, если дата раньше всех
        return self.rule_versions[0]["version"] if self.rule_versions else "unknown"

    def get_rule_info(self, version: str) -> dict[str, Any] | None:
        """Получение информации о версии правил.

        Args:
            version: Версия правил.

        Returns:
            Информация о версии правил или None.
        """
        for rule_version in self.rule_versions:
            if rule_version["version"] == version:
                return rule_version

        return None
